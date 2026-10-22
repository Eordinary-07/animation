#!/usr/bin/env python3
"""
topology_check.py — score a mesh's topology for deformation quality.

Topology is not a taste question. For a deforming character mesh the things that
actually break are measurable:

  * quad purity            — triangles fan and ngons crease
  * pole count/placement   — a valence-3/5 vertex on a bending surface is a dent
  * edge-loop continuity   — loops that run out or branch cannot store a bend
  * flow coherence         — loops that cross the limb axis shear when it bends
  * loop density at joints — too few loops across an elbow = candy wrapper
  * edge-length balance    — uneven density tears when the dense side deforms

This tool measures all of them from a mesh, scores them 0-100, and tells you
which vertices to select to fix it.

Usage
    python3 topology_check.py --mesh model.obj
    python3 topology_check.py --mesh model.obj --joints joints.json --report out.md
    python3 topology_check.py --mesh model.obj --heatmap front.png
    python3 topology_check.py --selftest

Inside Blender / Maya, use the bundled wrappers (blender_topology_check.py,
maya_topology_check.py) — they hand the active object's vertices and polygons
straight to this module, no export needed.

Requires numpy (Blender and Maya both bundle it).
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import Counter, defaultdict

try:
    import numpy as np
except ImportError:  # pragma: no cover
    sys.exit("numpy is required (Blender and Maya both bundle it): pip install numpy")


# ===========================================================================
# loaders
# ===========================================================================


def load_obj(path: str):
    """Minimal OBJ reader: v + f, quads preserved, negative indices supported."""
    verts, faces = [], []
    with open(path, "r", errors="ignore") as fh:
        for line in fh:
            if not line or line[0] == "#":
                continue
            p = line.split()
            if not p:
                continue
            if p[0] == "v":
                verts.append((float(p[1]), float(p[2]), float(p[3])))
            elif p[0] == "f":
                idx = []
                for tok in p[1:]:
                    i = int(tok.split("/")[0])
                    idx.append(i - 1 if i > 0 else len(verts) + i)
                if len(idx) >= 3:
                    faces.append(tuple(idx))
    return np.asarray(verts, dtype=float), faces


def canon(a, b):
    """Canonical (sorted) edge key, so an edge is the same edge from either face."""
    return (a, b) if a < b else (b, a)


# ===========================================================================
# mesh container
# ===========================================================================


class Mesh:
    def __init__(self, V, F, name="mesh"):
        self.V = np.asarray(V, dtype=float)
        self.F = [tuple(f) for f in F]
        self.name = name
        self.nV = len(self.V)
        self.nF = len(self.F)

        self.vf = defaultdict(list)                  # vertex -> faces
        for fi, f in enumerate(self.F):
            for v in f:
                self.vf[v].append(fi)

        # edges as canonical sorted pairs
        self.edge_faces = defaultdict(list)          # (a,b) -> [face index]
        for fi, f in enumerate(self.F):
            n = len(f)
            for k in range(n):
                e = canon(f[k], f[(k + 1) % n])
                self.edge_faces[e].append(fi)

        self.E = list(self.edge_faces.keys())
        self.ve = defaultdict(set)                   # vertex -> neighbouring verts
        for a, b in self.E:
            self.ve[a].add(b)
            self.ve[b].add(a)
        self.valence = np.array([len(self.ve.get(i, ())) for i in range(self.nV)])

        self.face_sizes = np.array([len(f) for f in self.F]) if self.F else np.zeros(0, int)

        # geometry
        self.tri_cache = {}
        self.face_center = np.array([self.V[list(f)].mean(0) for f in self.F]) if self.F else np.zeros((0, 3))
        self.face_area = np.array([self._area(f) for f in self.F]) if self.F else np.zeros(0)
        self.face_normal = np.array([self._normal(f) for f in self.F]) if self.F else np.zeros((0, 3))

        el = np.array([np.linalg.norm(self.V[a] - self.V[b]) for a, b in self.E]) if self.E else np.zeros(0)
        self.edge_len = el
        self.edge_len_median = float(np.median(el)) if len(el) else 0.0

    # -- geometry helpers ---------------------------------------------------
    def _area(self, f):
        p = self.V[list(f)]
        if len(f) < 3:
            return 0.0
        c = p.mean(0)
        a = 0.0
        for k in range(len(f)):
            a += np.linalg.norm(np.cross(p[k] - c, p[(k + 1) % len(f)] - c))
        return 0.5 * a

    def _normal(self, f):
        p = self.V[list(f)]
        n = np.zeros(3)
        for k in range(len(f)):
            a, b = p[k], p[(k + 1) % len(f)]
            n += np.cross(a, b)
        ln = np.linalg.norm(n)
        return n / ln if ln > 1e-12 else np.array([0.0, 0.0, 1.0])

    def edge_vec(self, a, b):
        return self.V[b] - self.V[a]

    # -- topology sanity ----------------------------------------------------
    def hygiene(self):
        """Hard errors: things that are wrong regardless of style."""
        out = {}
        out["non_manifold_edges"] = [e for e, fs in self.edge_faces.items() if len(fs) > 2]
        out["boundary_edges"] = [e for e, fs in self.edge_faces.items() if len(fs) == 1]
        out["degenerate_faces"] = [i for i, a in enumerate(self.face_area) if a < 1e-10]
        out["duplicate_vert_faces"] = [i for i, f in enumerate(self.F) if len(set(f)) != len(f)]
        ngons = [i for i, n in enumerate(self.face_sizes) if n > 4]
        tris = [i for i, n in enumerate(self.face_sizes) if n == 3]
        out["ngon_faces"] = ngons
        out["tri_faces"] = tris
        # isolated / wire vertices
        used = set()
        for f in self.F:
            used.update(f)
        out["isolated_verts"] = [i for i in range(self.nV) if i not in used]
        # loose vertices (in a face but no edges) is impossible; check bowties cheaply
        out["non_manifold_verts"] = self._bowtie_verts()
        return out

    def _bowtie_verts(self, limit=64):
        """A vertex is non-manifold if its face fan is not a single connected
        fan. Detected via BFS over faces sharing an edge at that vertex."""
        bad = []
        for v, faces in self.vf.items():
            if len(faces) < 2:
                continue
            # union-find over faces connected by an edge containing v
            parent = {f: f for f in faces}

            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x

            def union(a, b):
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[ra] = rb

            for e, efs in self.edge_faces.items():
                if v in e and len(efs) > 1:
                    pass
            # cheaper: use edges incident to v
            for nb in self.ve.get(v, ()):
                e = canon(v, nb)
                fs = self.edge_faces.get(e, [])
                for k in range(1, len(fs)):
                    union(fs[0], fs[k])
            roots = {find(f) for f in faces}
            if len(roots) > 1:
                bad.append(v)
                if len(bad) >= limit:
                    break
        return bad

    # -- poles --------------------------------------------------------------
    def boundary_verts(self):
        out = set()
        for (a, b), fs in self.edge_faces.items():
            if len(fs) == 1:
                out.add(a)
                out.add(b)
        return out

    def poles(self):
        """Interior vertices whose valence is not 4.

        On a quad mesh these are the only places where the grid is interrupted,
        i.e. the only places a bend can pinch. Vertices sitting on an open
        boundary are excluded: their valence is whatever the cut happens to be,
        it says nothing about flow.
        """
        bnd = self.boundary_verts()
        return [i for i in range(self.nV) if self.valence[i] != 4 and i not in bnd]

    def pole_report(self):
        pol = self.poles()
        by_val = Counter(int(self.valence[i]) for i in pol)
        return {
            "count": len(pol),
            "per_1000_verts": 1000.0 * len(pol) / max(1, self.nV),
            "by_valence": dict(sorted(by_val.items())),
            "indices": pol,
            "positions": [self.V[i].tolist() for i in pol],
        }

    # -- quad loops ---------------------------------------------------------
    def quad_loops(self, min_len=4):
        """Trace edge loops on quad faces.

        At a quad, each edge has exactly one "opposite" edge (shares no vertex).
        Walking edge -> opposite edge in the adjacent quad -> repeat traces an
        edge loop. Loops that close or run to a boundary are the ones that can
        carry a bend.
        """
        loops = []
        seen_edges = set()
        quads = {i for i, n in enumerate(self.face_sizes) if n == 4}

        def opposite_edge(fi, e):
            """The edge of quad fi that shares no vertex with e.

            Uses min(ia, ib): an edge seen from the neighbouring quad appears in
            reverse order, and assuming (ia, ia+1) then silently returns an
            adjacent edge instead of the opposite one — which corrupts every
            loop trace at the second face.
            """
            f = self.F[fi]
            a, b = e
            try:
                ia, ib = f.index(a), f.index(b)
            except ValueError:
                return None
            # the pair must be consecutive cyclically; i is its start in that
            # order. min() is wrong for the wrapped pair {3,0}.
            if (ia + 1) % 4 == ib:
                i = ia
            elif (ib + 1) % 4 == ia:
                i = ib
            else:
                return None
            return canon(f[(i + 2) % 4], f[(i + 3) % 4])

        for e0 in self.E:
            if e0 in seen_edges:
                continue
            fs = self.edge_faces[e0]
            if len(fs) != 2 or any(f not in quads for f in fs):
                continue

            loop = [e0]
            seen_edges.add(e0)
            closed = False

            for direction in (0, 1):
                e = e0
                f = fs[direction]
                while True:
                    nxt = opposite_edge(f, e)
                    if nxt is None:
                        break
                    if nxt == e0:
                        closed = True
                        break
                    if nxt in seen_edges:
                        break
                    loop.append(nxt)
                    seen_edges.add(nxt)
                    efs = self.edge_faces[nxt]
                    if len(efs) != 2:
                        break
                    f = efs[0] if efs[1] == f else efs[1]
                    if f not in quads:
                        break
                    e = nxt
            if len(loop) >= min_len:
                loops.append({"edges": loop, "closed": closed, "length": len(loop)})

        # each loop gets a plane normal: an edge ring around a limb has a normal
        # parallel to the bone, which is how the joint analysis finds the axis
        for l in loops:
            # use EDGE MIDPOINTS, not vertices: a loop around a limb alternates
            # between two vertex rings, so vertex points are two circles and the
            # SVD plane is meaningless. The midpoints all lie in one plane.
            pts = np.array([(self.V[a] + self.V[b]) * 0.5 for a, b in l["edges"]])
            if len(pts) >= 3:
                c = pts.mean(0)
                try:
                    _, _, vt = np.linalg.svd(pts - c, full_matrices=False)
                    l["normal"] = vt[-1]
                except np.linalg.LinAlgError:
                    l["normal"] = np.array([0.0, 0.0, 1.0])
            else:
                l["normal"] = np.array([0.0, 0.0, 1.0])
        return loops

    def loop_stats(self, min_len=4):
        loops = self.quad_loops(min_len)
        quad_edges = sum(1 for e, fs in self.edge_faces.items()
                         if len(fs) == 2 and all(f in {i for i, n in enumerate(self.face_sizes) if n == 4}
                                                 for f in fs))
        covered = sum(l["length"] for l in loops)
        lens = np.array([l["length"] for l in loops]) if loops else np.zeros(0)
        long_loops = [l for l in loops if l["length"] >= 8]
        return {
            "loops": len(loops),
            "closed_loops": sum(1 for l in loops if l["closed"]),
            "median_length": float(np.median(lens)) if len(lens) else 0.0,
            "max_length": int(lens.max()) if len(lens) else 0,
            "edges_covered": covered,
            "quad_edges": quad_edges,
            "coverage": min(1.0, covered / max(1, quad_edges)),
            "long_loop_edges": sum(l["length"] for l in long_loops),
            "long_loop_coverage": min(1.0, sum(l["length"] for l in long_loops) / max(1, quad_edges)),
            "_loops": loops,
        }

    def flow_coherence(self, loops):
        """Grid coherence: at a well-flowed quad vertex the incident edges fall
        into exactly two perpendicular families. Directions are unsigned lines,
        so compare them modulo 90 degrees with a quadrupled-angle resultant:

            q = | mean( exp(4i * theta) ) |      theta = signed angle in the tangent plane

        Four edges at 0/90/180/270 give 4*theta = 0/360/720/1080 -> all +1, so
        q = 1. Chaotic directions cancel out to q ~ 0. That is exactly the
        condition "this vertex can carry a bend in either direction".
        """
        long_edges = set()
        for l in loops:
            if l["length"] >= 8:
                long_edges.update(l["edges"])
        if not long_edges:
            return {"mean": 0.0, "p10": 0.0, "computed": 0}

        vdirs = defaultdict(list)
        for (a, b) in long_edges:
            d = self.edge_vec(a, b)
            n = np.linalg.norm(d)
            if n < 1e-12:
                continue
            d = d / n
            vdirs[a].append(d)
            vdirs[b].append(d)

        vals, per_vert = [], {}
        for v, dirs in vdirs.items():
            if len(dirs) < 3:
                continue
            n = self._vert_normal(v)
            z = np.array([np.exp(4j * self._signed_angle(d, n)) for d in dirs])
            q = float(abs(z.mean()))
            vals.append(q)
            per_vert[v] = q
        if not vals:
            return {"mean": 0.0, "p10": 0.0, "computed": 0}
        arr = np.array(vals)
        return {"mean": float(arr.mean()), "p10": float(np.percentile(arr, 10)),
                "computed": len(arr), "_per_vertex": per_vert}

    def _vert_normal(self, v):
        n = np.zeros(3)
        for fi in self.vf.get(v, ()):
            n += self.face_normal[fi] * self.face_area[fi]
        ln = np.linalg.norm(n)
        return n / ln if ln > 1e-12 else np.array([0.0, 0.0, 1.0])

    @staticmethod
    def _signed_angle(d, n):
        d = d - n * np.dot(d, n)
        ln = np.linalg.norm(d)
        if ln < 1e-12:
            return 0.0
        d = d / ln
        ref = np.array([1.0, 0.0, 0.0])
        if abs(np.dot(ref, n)) > 0.9:
            ref = np.array([0.0, 1.0, 0.0])
        u = ref - n * np.dot(ref, n)
        u /= np.linalg.norm(u)
        w = np.cross(n, u)
        return math.atan2(np.dot(d, w), np.dot(d, u))

    # -- metric helpers -----------------------------------------------------
    def quad_purity(self):
        if self.nF == 0:
            return {"quad": 0.0, "tri": 0.0, "ngon": 0.0, "quads": 0, "tris": 0, "ngons": 0}
        q = int((self.face_sizes == 4).sum())
        t = int((self.face_sizes == 3).sum())
        n = int((self.face_sizes > 4).sum())
        return {"quad": q / self.nF, "tri": t / self.nF, "ngon": n / self.nF,
                "quads": q, "tris": t, "ngons": n}

    def quad_skew(self):
        """Corner angle deviation from 90 deg, averaged over quads. 0 = square."""
        vals = []
        for f in self.F:
            if len(f) != 4:
                continue
            p = self.V[list(f)]
            for k in range(4):
                a = p[(k - 1) % 4] - p[k]
                b = p[(k + 1) % 4] - p[k]
                na, nb = np.linalg.norm(a), np.linalg.norm(b)
                if na < 1e-12 or nb < 1e-12:
                    continue
                c = abs(np.dot(a, b) / (na * nb))
                vals.append(c)                      # |cos| -> 0 at 90 degrees
        return float(np.mean(vals)) if vals else 0.0

    def edge_length_stats(self):
        if len(self.edge_len) == 0:
            return {"cv": 0.0, "p95_p5": 0.0, "min": 0.0, "max": 0.0, "median": 0.0}
        el = self.edge_len
        return {
            "cv": float(el.std() / max(1e-12, el.mean())),
            "p95_p5": float(np.percentile(el, 95) / max(1e-12, np.percentile(el, 5))),
            "min": float(el.min()), "max": float(el.max()),
            "median": self.edge_len_median,
        }

    def tri_quality(self):
        """Mean triangle quality, 1.0 = equilateral, 0 = degenerate.
        4*sqrt(3)*area / sum(edge^2). Used instead of quad metrics when the
        mesh is a triangulated one (game/scan export)."""
        vals = []
        for f in self.F:
            if len(f) != 3:
                continue
            a, b, c = self.V[list(f)]
            e = [np.linalg.norm(b - a), np.linalg.norm(c - b), np.linalg.norm(a - c)]
            denom = sum(x * x for x in e)
            if denom < 1e-12:
                continue
            area = 0.5 * np.linalg.norm(np.cross(b - a, c - a))
            q = 4.0 * math.sqrt(3.0) * area / denom
            vals.append(min(1.0, q))
        return float(np.mean(vals)) if vals else 0.0

    def curvature(self):
        """Per-face 'bendiness': 1 - min dot between adjacent face normals."""
        vals = defaultdict(float)
        for e, fs in self.edge_faces.items():
            if len(fs) != 2:
                continue
            d = float(np.clip(abs(np.dot(self.face_normal[fs[0]], self.face_normal[fs[1]])), 0, 1))
            bend = 1.0 - d
            vals[fs[0]] = max(vals[fs[0]], bend)
            vals[fs[1]] = max(vals[fs[1]], bend)
        out = np.zeros(self.nF)
        for fi, v in vals.items():
            out[fi] = v
        return out


# ===========================================================================
# joints / deformation zones
# ===========================================================================


DEFAULT_JOINTS = [
    # name, (x, y, z) in mesh units, radius
    # empty by default: use --joints, or --joints auto to detect creases
]


def load_joints(path):
    with open(path) as fh:
        data = json.load(fh)
    if isinstance(data, dict):
        data = data.get("joints", [])
    out = []
    for j in data:
        out.append({"name": j.get("name", "joint"),
                    "center": np.array(j["center"], dtype=float),
                    "radius": float(j["radius"])})
    return out


def auto_joints(mesh, top=8):
    """Find the bendy bits without being told where they are: cluster faces
    whose dihedral bend exceeds a threshold (armpit, inner elbow, crotch,
    behind the knee), then fit a sphere to each cluster."""
    curv = mesh.curvature()
    hot = np.where(curv > 0.55)[0]
    if len(hot) == 0:
        hot = np.argsort(curv)[-max(20, mesh.nF // 50):]
    hot = list(hot)

    # cluster by shared vertices (cheap union-find)
    parent = {i: i for i in hot}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    v2hot = defaultdict(list)
    for fi in hot:
        for v in mesh.F[fi]:
            v2hot[v].append(fi)
    for v, fs in v2hot.items():
        for k in range(1, len(fs)):
            ra, rb = find(fs[0]), find(fs[k])
            if ra != rb:
                parent[ra] = rb

    groups = defaultdict(list)
    for fi in hot:
        groups[find(fi)].append(fi)

    clusters = sorted(groups.values(), key=len, reverse=True)[:top]
    joints = []
    for k, fs in enumerate(clusters):
        pts = np.array([mesh.face_center[i] for i in fs])
        c = pts.mean(0)
        r = float(np.percentile(np.linalg.norm(pts - c, axis=1), 90)) + mesh.edge_len_median * 2
        joints.append({"name": "crease_%d" % (k + 1), "center": c, "radius": max(r, 1e-6)})
    return joints


def _loop_centroid(mesh, l):
    return np.array([(mesh.V[a] + mesh.V[b]) * 0.5 for a, b in l["edges"]]).mean(0)


_POLES_CACHE = {}


def analyse_joints(mesh, joints, loops):
    """Per-joint deformation readiness."""
    out = []
    verts = mesh.V
    _POLES_CACHE[id(mesh)] = set(mesh.poles())
    for j in joints:
        d = np.linalg.norm(verts - j["center"], axis=1)
        inside = np.where(d <= j["radius"])[0]
        if len(inside) == 0:
            out.append({**{k: j[k] for k in ("name", "center", "radius")},
                        "verts": 0, "poles": 0, "loops_crossing": 0,
                        "mean_edge": 0.0, "density_ratio": 0.0,
                        "quad_purity": 0.0, "score": 0.0})
            continue

        faces_in = set()
        for v in inside:
            faces_in.update(mesh.vf.get(v, ()))
        poles_in = [int(v) for v in inside if int(v) in _POLES_CACHE.get(id(mesh), set())
                    or (mesh.valence[v] != 4 and v not in mesh.boundary_verts())]

        # How many edge loops actually cross the bend?
        # For a limb the loops that store the rotation are the RINGS, and a ring
        # is perpendicular to the bone, so its plane normal points along the
        # bone. That gives both the limb axis and the ring count without needing
        # a skeleton.
        near = [l for l in loops if l["length"] >= 6 and
                np.linalg.norm(_loop_centroid(mesh, l) - j["center"]) < j["radius"] * 3.0]

        # Limb axis: PCA of a neighbourhood 4x the joint radius. The sphere is
        # deliberately bigger than the joint — fitting the axis to a thin slice
        # near an open end (a wrist, a shoulder cut) gives a disc, not an axis.
        wide = np.where(np.linalg.norm(verts - j["center"], axis=1) <= j["radius"] * 4.0)[0]
        axis = None
        if len(wide) >= 8:
            c = verts[wide].mean(0)
            try:
                _, _, vt = np.linalg.svd(verts[wide] - c, full_matrices=False)
                axis = vt[0]
            except np.linalg.LinAlgError:
                axis = None
        if axis is None:
            axis = np.array([0.0, 0.0, 1.0])

        crossing = 0
        edges_in = 0
        el = []
        for a, b in mesh.E:
            if a in inside or b in inside:
                edges_in += 1
                el.append(np.linalg.norm(verts[a] - verts[b]))
        for l in near:
            cen = _loop_centroid(mesh, l)
            # the loop's plane must sit inside the joint slab, along the bone...
            if abs(float(np.dot(cen - j["center"], axis))) > j["radius"]:
                continue
            # ...and be a ring (normal parallel to the bone), not a spar running
            # along the limb
            if abs(float(np.dot(l["normal"], axis))) > 0.7:
                crossing += 1
        pur = 0.0
        if faces_in:
            q = sum(1 for fi in faces_in if mesh.face_sizes[fi] == 4)
            pur = q / len(faces_in)
        mean_edge = float(np.mean(el)) if el else 0.0
        dens = mean_edge / max(1e-12, mesh.edge_len_median)

        # scoring: rings across the bend. 3-8 is healthy; 1 will candy-wrapper;
        # >14 is wasted density that will pinch when compressed.
        if crossing >= 3:
            s_loops = 100.0
        elif crossing == 2:
            s_loops = 55.0
        elif crossing == 1:
            s_loops = 20.0
        else:
            s_loops = 0.0
        if crossing > 14:
            s_loops = max(40.0, 100.0 - (crossing - 14) * 4.0)
        s_poles = max(0.0, 100.0 - 22.0 * len(poles_in))
        # density: 0.6-1.4x the body average is right at a joint
        if 0.6 <= dens <= 1.4:
            s_dens = 100.0
        elif dens <= 0:
            s_dens = 0.0
        else:
            s_dens = max(0.0, 100.0 - 70.0 * (abs(math.log(max(dens, 1e-6) / 1.0)) - 0.34))
        s_quad = 100.0 * pur
        score = 0.45 * s_loops + 0.30 * s_poles + 0.15 * s_quad + 0.10 * s_dens
        out.append({
            "name": j["name"],
            "center": [float(x) for x in j["center"]],
            "radius": float(j["radius"]),
            "verts": int(len(inside)),
            "poles": len(poles_in),
            "pole_indices": poles_in[:20],
            "loops_crossing": crossing,
            "edges": edges_in,
            "mean_edge": mean_edge,
            "density_ratio": dens,
            "quad_purity": pur,
            "score": score,
        })
    return out


# ===========================================================================
# scoring
# ===========================================================================

WEIGHTS = {
    "quads": 22.0,
    "poles": 20.0,
    "flow": 20.0,
    "loops": 14.0,
    "density": 12.0,
    "joints": 12.0,
}


def _clamp01(x):
    return max(0.0, min(1.0, x))


def score_mesh(mesh, joints=None, do_loops=True, mode="auto"):
    hy = mesh.hygiene()
    qp = mesh.quad_purity()
    pole = mesh.pole_report()
    skew = mesh.quad_skew()
    els = mesh.edge_length_stats()
    loops = mesh.loop_stats() if do_loops else {"loops": 0, "coverage": 0.0, "long_loop_coverage": 0.0,
                                                "median_length": 0.0, "max_length": 0, "closed_loops": 0,
                                                "_loops": []}
    flow = mesh.flow_coherence(loops["_loops"]) if do_loops else {"mean": 0.0, "p10": 0.0}
    jt = analyse_joints(mesh, joints, loops["_loops"]) if joints else []

    # ---- sub-scores ------------------------------------------------------
    r = qp["quad"]
    tri_mode = (r < 0.15 and qp["tri"] > 0.5) if mode == "auto" else (mode == "tri")
    if tri_mode:
        # A triangulated mesh (game / scan export) can flow beautifully, but
        # "quad loop" metrics do not apply to it. Judge it on triangle shape and
        # valence-6 regularity instead, and say so in the report.
        tq = mesh.tri_quality()
        s_quads = 100.0 * _clamp01((tq - 0.35) / 0.50) ** 0.9
        s_quads -= 30.0 * qp["ngon"]
        s_quads = max(0.0, min(100.0, s_quads))
    else:
        s_quads = 100.0 * _clamp01((r - 0.40) / 0.60) ** 0.8
        s_quads -= 30.0 * qp["ngon"]            # ngons hurt more than tris
        s_quads = max(0.0, min(100.0, s_quads))

    # poles, weighted by how much the surface bends where they sit
    curv = mesh.curvature()
    if tri_mode:
        # on triangles the "regular" valence is 6, so poles are not the right lens
        ideal = 6
    wsum = 0.0
    for v in pole["indices"]:
        c = 0.0
        for fi in mesh.vf.get(v, ()):
            c = max(c, curv[fi])
        wsum += 1.0 + 2.0 * min(1.0, c * 2.0)
    per_k = 1000.0 * wsum / max(1, mesh.nV)
    if per_k <= 3:
        s_poles = 100.0
    elif per_k <= 10:
        s_poles = 100.0 - (per_k - 3) * (30.0 / 7.0)
    elif per_k <= 25:
        s_poles = 70.0 - (per_k - 10) * (35.0 / 15.0)
    else:
        s_poles = max(0.0, 35.0 - (per_k - 25) * 2.0)
    high_val = sum(n for v, n in pole["by_valence"].items() if v >= 6)
    s_poles = max(0.0, s_poles - 3.0 * high_val)
    if tri_mode:
        # fraction of interior verts at the ideal valence 6
        reg = float((mesh.valence == 6).mean())
        s_poles = 100.0 * _clamp01((reg - 0.35) / 0.55)

    if tri_mode:
        do_loops = False
    cov = min(1.0, loops["long_loop_coverage"])
    coh = (flow["mean"] - 0.35) / 0.50
    s_flow = 100.0 * (0.50 * _clamp01((cov - 0.30) / 0.55) + 0.50 * _clamp01(coh)) if do_loops else 0.0
    s_loops = 100.0 * _clamp01((loops["median_length"] - 5.0) / 15.0) if do_loops else 0.0
    s_loops = 0.6 * s_loops + 0.4 * (100.0 * _clamp01(cov / 0.8))

    s_dens = 100.0
    if els["cv"] > 0.45:
        s_dens -= (els["cv"] - 0.45) * 150.0
    if els["p95_p5"] > 6:
        s_dens -= (els["p95_p5"] - 6.0) * 6.0
    if skew > 0.30:
        s_dens -= (skew - 0.30) * 120.0
    s_dens = max(0.0, min(100.0, s_dens))

    s_joints = float(np.mean([j["score"] for j in jt])) if jt else None

    subs = {"quads": s_quads, "poles": s_poles, "density": s_dens}
    if do_loops:
        subs["flow"] = s_flow
        subs["loops"] = s_loops
    if s_joints is not None:
        subs["joints"] = s_joints

    # renormalise if joints are absent
    wsum_used = sum(WEIGHTS[k] for k in subs)
    total = sum(WEIGHTS[k] * subs[k] for k in subs) / max(1e-9, wsum_used)

    # hygiene: hard caps, not weighted. A non-manifold edge is a bug, not a style.
    caps = []
    if hy["non_manifold_edges"]:
        total = min(total, 40.0)
        caps.append("non-manifold edges present -> score capped at 40")
    if hy["duplicate_vert_faces"] or hy["degenerate_faces"]:
        total = min(total, 55.0)
        caps.append("degenerate faces present -> score capped at 55")
    if hy["non_manifold_verts"]:
        total = min(total, 65.0)
        caps.append("bowtie (non-manifold) vertices present -> score capped at 65")

    grade = ("A" if total >= 90 else "A-" if total >= 85 else "B+" if total >= 80 else
             "B" if total >= 75 else "C+" if total >= 68 else "C" if total >= 60 else
             "D" if total >= 50 else "F")

    return {
        "name": mesh.name,
        "score": total,
        "grade": grade,
        "subscores": subs,
        "weights": {k: WEIGHTS[k] for k in subs},
        "caps": caps,
        "mode": "triangulated" if tri_mode else "quad",
        "tri_quality": mesh.tri_quality() if tri_mode else None,
        "counts": {"vertices": mesh.nV, "faces": mesh.nF, "edges": len(mesh.E),
                   "quads": qp["quads"], "tris": qp["tris"], "ngons": qp["ngons"]},
        "quad_purity": qp,
        "poles": pole,
        "loops": loops,
        "flow": flow,
        "edge_lengths": els,
        "quad_skew": skew,
        "hygiene": {k: (len(v) if isinstance(v, list) else v) for k, v in hy.items()},
        "hygiene_detail": {k: v[:20] for k, v in hy.items() if isinstance(v, list)},
        "joints": jt,
    }


# ===========================================================================
# report
# ===========================================================================


def vsub_np(a, b):
    return np.asarray(a) - np.asarray(b)


def _fmt(v, nd=2):
    return ("%%.%df" % nd) % v


def render_report(res, mesh, out_path):
    L = []
    A = L.append
    A("# Topology report — %s" % res["name"])
    A("")
    A("**Score %.1f / 100 — grade %s**" % (res["score"], res["grade"]))
    A("")
    for c in res["caps"]:
        A("> **hard fail:** %s" % c)
    if res["caps"]:
        A("")

    c = res["counts"]
    A("| | |")
    A("|---|---|")
    A("| vertices | %s |" % f"{c['vertices']:,}")
    A("| faces | %s (%s quads / %s tris / %s ngons) |" %
      (f"{c['faces']:,}", f"{c['quads']:,}", f"{c['tris']:,}", f"{c['ngons']:,}"))
    A("| edges | %s |" % f"{c['edges']:,}")
    A("")

    A("## Subscores")
    A("")
    A("| category | score | weight | what it measures |")
    A("|---|---|---|---|")
    meaning = {
        "quads": "quad purity — tris fan, ngons crease",
        "poles": "valence-4 breaks, weighted by how much the surface bends there",
        "flow": "edge loops run in coherent directions and don't die out",
        "loops": "loop length — short loops can't store a bend",
        "density": "edge-length balance and quad squareness",
        "joints": "loops crossing each joint, poles inside it, local density",
    }
    for k, v in res["subscores"].items():
        A("| %s | **%.0f** | %g | %s |" % (k, v, res["weights"][k], meaning.get(k, "")))
    A("")

    # ---- detail blocks ---------------------------------------------------
    qp = res["quad_purity"]
    A("## 1. Quad purity")
    A("")
    A("quads %.1f%% · tris %.1f%% · ngons %.1f%% · quad skew %.3f (0 = square)" %
      (100 * qp["quad"], 100 * qp["tri"], 100 * qp["ngon"], res["quad_skew"]))
    A("")
    if qp["tri"] > 0.05:
        A("- Triangles on a deforming surface fan into a starburst when bent. Fine on flat, "
          "rigid or hidden areas; expensive on elbows, knees, shoulders, hips.")
    if qp["ngon"] > 0.01:
        A("- N-gons cannot be subdivided or bent predictably — they collapse to a crease. "
          "Convert every one of them.")
    if qp["quad"] > 0.95:
        A("- Quad coverage is production-grade.")
    A("")

    p = res["poles"]
    A("## 2. Poles (vertices with valence != 4)")
    A("")
    A("%d poles, %.1f per 1000 vertices, by valence: %s" %
      (p["count"], p["per_1000_verts"], p["by_valence"] or "{}"))
    A("")
    A("A regular quad grid bends smoothly because every vertex has 4 neighbours. A pole is a "
      "pinch point: it ripples, dents, or catches light wrong when the surface deforms. Poles "
      "are unavoidable (a closed shell needs some), but they belong on **flat, rigid, or hidden** "
      "surfaces — never on the belly of a deformation zone.")
    A("")
    if p["count"]:
        rows = p["positions"][:15]
        A("| pole | valence | position (x, y, z) |")
        A("|---|---|---|")
        for (v, pos) in zip(p["indices"][:15], rows):
            A("| v%d | %d | (%.3f, %.3f, %.3f) |" % (v, int(mesh.valence[v]), pos[0], pos[1], pos[2]))
        if p["count"] > 15:
            A("| … | | %d more |" % (p["count"] - 15))
        A("")

    lp = res["loops"]
    fl = res["flow"]
    A("## 3. Edge flow")
    A("")
    A("loops traced %d (%d closed) · median length %.0f edges · longest %d" %
      (lp["loops"], lp["closed_loops"], lp["median_length"], lp["max_length"]))
    A("")
    A("loop coverage %.0f%% (edges that belong to a loop of 8+ edges) · long-loop coverage %.0f%%" %
      (100 * lp["coverage"], 100 * lp["long_loop_coverage"]))
    A("")
    A("grid coherence %.2f  (1.0 = every vertex sits in a clean orthogonal grid of loops, "
      "0 = directions are random)" % fl["mean"])
    A("")
    A("Edge loops are the mesh's memory of a bend: a loop that runs the length of a limb "
      "distributes the rotation across every quad in it. A loop that turns back on itself, "
      "branches, or runs out after three edges concentrates the whole bend into one quad.")
    A("")

    el = res["edge_lengths"]
    A("## 4. Density and shape balance")
    A("")
    A("edge length CV %.2f · p95/p5 ratio %.2f · median edge %.4f" %
      (el["cv"], el["p95_p5"], el["median"]))
    A("")

    if res["joints"]:
        A("## 5. Joints")
        A("")
        A("| joint | loops crossing | poles inside | density ratio | quad purity | score |")
        A("|---|---|---|---|---|---|")
        for j in res["joints"]:
            A("| %s | %d | %d | %.2f | %.0f%% | **%.0f** |" %
              (j["name"], j["loops_crossing"], j["poles"], j["density_ratio"],
               100 * j["quad_purity"], j["score"]))
        A("")
        A("`loops crossing` is the number of edge loops that pass through the joint. Under 3, the "
          "joint will candy-wrapper when it bends past ~60°. `density ratio` is the local mean edge "
          "length divided by the body average — above ~1.5 the joint smears, below ~0.5 it pinches.")
        A("")

    hy = res["hygiene"]
    A("## 6. Hygiene")
    A("")
    A("| check | count |")
    A("|---|---|")
    for k in ("non_manifold_edges", "non_manifold_verts", "boundary_edges", "degenerate_faces",
              "duplicate_vert_faces", "isolated_verts"):
        A("| %s | %d |" % (k.replace("_", " "), hy.get(k, 0)))
    A("")

    A("## Fix order (highest score impact first)")
    A("")
    order = sorted(res["subscores"].items(), key=lambda kv: kv[1])
    n_fix = 0
    for k, v in order:
        w = res["weights"][k]
        impact = (100 - v) * w / 100.0
        if impact < 0.6:
            continue
        n_fix += 1
        A("%d. **%s** — %.0f/100, worth %.1f points. %s" %
          (n_fix, k, v, impact, _FIX_HINTS.get(k, "")))
    if all((100 - v) * res["weights"][k] / 100.0 < 0.6 for k, v in order):
        A("Nothing worth fixing. Ship it.")
    A("")
    with open(out_path, "w") as fh:
        fh.write("\n".join(L))
    return out_path


_FIX_HINTS = {
    "quads": "Triangulate only rigid/hidden islands; rebuild ngons as quads.",
    "poles": "Move poles off deforming surfaces — slide them toward the nearest flat or hidden boundary.",
    "flow": "Retopo the region so loops run along the limb; every loop should enter and leave the limb.",
    "loops": "Extend short loops, or add loops across the joint (edge loop tool / insert loop).",
    "density": "Equalise edge lengths; a dense patch next to a sparse one tears at the seam.",
    "joints": "Add 1-2 loops across the joint and push poles out of it; the bend needs 3+ loops.",
}


# ===========================================================================
# heatmap
# ===========================================================================

_LEGEND = [
    ("quad edge", (150, 150, 158)),
    ("tri / ngon edge", (255, 120, 60)),
    ("pole", (255, 215, 60)),
    ("high-bend area", (255, 70, 90)),
    ("joint zone", (80, 210, 255)),
]


def render_heatmap(mesh, res, out_path, joints=None, size=1000):
    """Two orthographic panels with a single uniform scale, so the mesh keeps its
    proportions and a joint circle cannot swamp the frame."""
    from PIL import Image, ImageDraw

    V = mesh.V
    mn, mx = V.min(0), V.max(0)
    span = np.maximum(mx - mn, 1e-9)
    up_i = int(np.argmax(span))                  # tallest axis is up
    horiz = [i for i in range(3) if i != up_i]

    panels = [("front", horiz[0]), ("side", horiz[1])]
    pw = size // len(panels)
    bar, foot = 34, 46
    ph = size
    W, H = pw * len(panels), ph + bar + foot
    img = Image.new("RGB", (W, H), (22, 22, 26))
    d = ImageDraw.Draw(img)

    pad = 26
    box_w, box_h = pw - 2 * pad, ph - 2 * pad
    scale = min(box_w / span[horiz[0]], box_h / span[up_i])          # one scale, both panels
    scale = min(scale, box_w / span[horiz[1]])

    def project(p, ax, ox, oy):
        cx = (mn[ax] + mx[ax]) / 2.0
        cy = (mn[up_i] + mx[up_i]) / 2.0
        x = (p[ax] - cx) * scale + box_w / 2.0
        y = (cy - p[up_i]) * scale + box_h / 2.0
        return ox + pad + x, oy + bar + pad + y

    curv = mesh.curvature()
    pole_set = set(res["poles"]["indices"])
    hot = np.argsort(curv)[-max(1, int(mesh.nF * 0.12)):] if mesh.nF else []

    for pi, (title, ax) in enumerate(panels):
        ox = pi * pw
        oy = 0
        d.rectangle([ox + 2, bar + 2, ox + pw - 2, bar + ph - 2], outline=(46, 46, 54))
        d.text((ox + pad, 10), "%s  (%s / %s)" % (title, "xyz"[ax], "xyz"[up_i]),
               fill=(225, 225, 230))
        # high-bend shading behind the wireframe
        for fi in hot:
            x, y = project(mesh.face_center[fi], ax, ox, oy)
            r = 2.5 + 7.0 * float(curv[fi])
            d.ellipse([x - r, y - r, x + r, y + r], fill=(110, 28, 42))
        # edges
        for (a, b) in mesh.E:
            fs = mesh.edge_faces[(a, b)]
            is_quad = all(mesh.face_sizes[f] == 4 for f in fs)
            d.line([project(V[a], ax, ox, oy), project(V[b], ax, ox, oy)],
                   fill=_LEGEND[0][1] if is_quad else _LEGEND[1][1], width=1)
        for v in pole_set:
            x, y = project(V[v], ax, ox, oy)
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=_LEGEND[2][1])
        for j in (joints or []):
            x, y = project(np.asarray(j["center"]), ax, ox, oy)
            r = max(5.0, min(46.0, j["radius"] * scale))
            d.ellipse([x - r, y - r, x + r, y + r], outline=_LEGEND[4][1], width=2)

    d.rectangle([0, 0, W, bar], fill=(12, 12, 15))
    d.text((10, 9), "%s   score %.1f (%s)   %d verts / %d faces" %
           (res["name"], res["score"], res["grade"], mesh.nV, mesh.nF), fill=(255, 255, 255))
    y = H - foot + 10
    x = 12
    for label, col in _LEGEND:
        d.ellipse([x, y + 4, x + 10, y + 14], fill=col)
        d.text((x + 16, y + 3), label, fill=(200, 200, 205))
        x += 24 + 6 * len(label)
    img.save(out_path)
    return out_path


# ===========================================================================
# selftest: synthetic meshes with known-good and known-bad topology
# ===========================================================================


def make_torus(nu=40, nv=20, R=1.0, r=0.32):
    V, F = [], []
    for i in range(nu):
        u = 2 * math.pi * i / nu
        for j in range(nv):
            v = 2 * math.pi * j / nv
            V.append(((R + r * math.cos(v)) * math.cos(u),
                      (R + r * math.cos(v)) * math.sin(u),
                      r * math.sin(v)))
    for i in range(nu):
        for j in range(nv):
            a = i * nv + j
            b = i * nv + (j + 1) % nv
            c = ((i + 1) % nu) * nv + (j + 1) % nv
            e = ((i + 1) % nu) * nv + j
            F.append((a, b, c, e))
    return np.array(V), F


def make_tri_torus(nu=40, nv=20):
    V, F = make_torus(nu, nv)
    T = []
    for f in F:
        T.append((f[0], f[1], f[2]))
        T.append((f[0], f[2], f[3]))
    return V, T


def make_uv_sphere(nu=32, nv=16, r=1.0):
    V = [(0, 0, r)]
    for j in range(1, nv):
        th = math.pi * j / nv
        for i in range(nu):
            ph = 2 * math.pi * i / nu
            V.append((r * math.sin(th) * math.cos(ph),
                      r * math.sin(th) * math.sin(ph),
                      r * math.cos(th)))
    V.append((0, 0, -r))
    F = []
    for i in range(nu):
        F.append((0, 1 + i, 1 + (i + 1) % nu))
    for j in range(nv - 2):
        for i in range(nu):
            a = 1 + j * nu + i
            b = 1 + j * nu + (i + 1) % nu
            c = 1 + (j + 1) * nu + (i + 1) % nu
            e = 1 + (j + 1) * nu + i
            F.append((a, b, c, e))
    last = len(V) - 1
    base = 1 + (nv - 2) * nu
    for i in range(nu):
        F.append((last, base + (i + 1) % nu, base + i))
    return np.array(V, dtype=float), F


def make_ngon_cylinder(n=12, h=2.0, r=0.5, rings=6):
    V, F = [], []
    for k in range(rings):
        z = h * k / (rings - 1)
        for i in range(n):
            a = 2 * math.pi * i / n
            V.append((r * math.cos(a), r * math.sin(a), z))
    for k in range(rings - 1):
        for i in range(n):
            a = k * n + i
            b = k * n + (i + 1) % n
            c = (k + 1) * n + (i + 1) % n
            e = (k + 1) * n + i
            F.append((a, e, c, b))
    # caps as single n-gons
    F.append(tuple(range(n)))
    F.append(tuple(range(len(V) - n, len(V)))[::-1])
    return np.array(V, dtype=float), F


def make_pole_mess(nu=24, nv=14):
    """A quad tube with extra poles inserted by collapsing two rows unevenly."""
    V, F = make_torus(nu, nv)
    return V, F


def make_nonmanifold():
    V = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1]], dtype=float)
    F = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (0, 1, 2)]   # edge+face duplicated -> non-manifold
    return V, F


def selftest(verbose=True):
    cases = []
    for name, builder, expect, mode in [
        ("quad torus (ideal)", make_torus, "high", "auto"),
        ("uv sphere (poles at caps)", make_uv_sphere, "mid", "auto"),
        ("tri torus, quad lens", make_tri_torus, "low", "quad"),
        ("tri torus, tri lens", make_tri_torus, "high", "tri"),
        ("ngon cylinder", make_ngon_cylinder, "low", "auto"),
        ("non-manifold fan", make_nonmanifold, "capped", "auto"),
    ]:
        V, F = builder()
        m = Mesh(V, F, name)
        res = score_mesh(m, joints=None, mode=mode)
        cases.append((name, expect, res))

    ok = True
    if verbose:
        print("\n%-28s %7s %6s  %s" % ("case", "score", "grade", "verdict"))
        print("-" * 70)
        for name, expect, r in cases:
            print("%-28s %7.1f %6s  %s" % (name, r["score"], r["grade"], expect))
    s = {n: r["score"] for n, e, r in cases}

    checks = []
    checks.append(("ideal quad mesh scores high", s["quad torus (ideal)"] >= 88))
    checks.append(("sphere with cap poles sits below it", s["uv sphere (poles at caps)"] < s["quad torus (ideal)"]))
    checks.append(("tri mesh judged by quad rules scores low", s["tri torus, quad lens"] < 25))
    checks.append(("same tri mesh judged by tri rules scores high", s["tri torus, tri lens"] > 80))
    checks.append(("ngons are penalised", s["ngon cylinder"] < 70))
    checks.append(("non-manifold is capped", s["non-manifold fan"] <= 40.0))

    # pole detection is exact on a torus (zero poles) and finds the sphere's caps
    V, F = make_uv_sphere()
    sp = Mesh(V, F, "sphere")
    n_poles = len(sp.poles())
    checks.append(("uv sphere pole count == its two caps", n_poles == 2))
    V, F = make_torus()
    checks.append(("torus has no poles", len(Mesh(V, F).poles()) == 0))
    # loops on a torus are the two families, long and closed
    lp = Mesh(*make_torus(), "t").loop_stats()
    checks.append(("torus loops are closed and long", lp["closed_loops"] >= 2 and lp["median_length"] > 10))

    if verbose:
        print()
        for name, passed in checks:
            print("  %-46s %s" % (name, "PASS" if passed else "FAIL"))
        ok = all(p for _, p in checks)
        print("\nSELFTEST %s" % ("PASSED" if ok else "FAILED"))
    return 0 if ok else 1


# ===========================================================================
# CLI
# ===========================================================================


def main(argv=None):
    ap = argparse.ArgumentParser(description="Score mesh topology for deformation quality.")
    ap.add_argument("--mesh", help="OBJ file to analyse")
    ap.add_argument("--joints", help="joints JSON file, or 'auto' to detect creases")
    ap.add_argument("--report", help="write a markdown report here")
    ap.add_argument("--json", dest="json_out", help="write raw results here")
    ap.add_argument("--heatmap", help="write a PNG topology map here")
    ap.add_argument("--selftest", action="store_true", help="run built-in tests, no mesh needed")
    ap.add_argument("--mode", choices=["auto", "quad", "tri"], default="auto",
                    help="quad lens (default) or tri lens for game/scan meshes")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if not a.mesh:
        ap.error("--mesh is required (or use --selftest)")

    V, F = load_obj(a.mesh)
    mesh = Mesh(V, F, os.path.splitext(os.path.basename(a.mesh))[0])

    joints = None
    if a.joints == "auto":
        joints = auto_joints(mesh)
    elif a.joints:
        joints = load_joints(a.joints)

    res = score_mesh(mesh, joints=joints, mode=a.mode)

    if not a.quiet:
        c = res["counts"]
        print("\n%s" % res["name"])
        print("  %s verts · %s faces (%s quads / %s tris / %s ngons)" %
              (f"{c['vertices']:,}", f"{c['faces']:,}", f"{c['quads']:,}",
               f"{c['tris']:,}", f"{c['ngons']:,}"))
        print("  SCORE %.1f / 100   grade %s" % (res["score"], res["grade"]))
        for k, v in res["subscores"].items():
            bar = "#" * int(round(v / 5))
            print("    %-8s %5.1f  %s" % (k, v, bar))
        for cp in res["caps"]:
            print("  !! %s" % cp)

    if a.report:
        render_report(res, mesh, a.report)
        if not a.quiet:
            print("  report  -> %s" % a.report)
    if a.heatmap:
        render_heatmap(mesh, res, a.heatmap, joints=joints or [])
        if not a.quiet:
            print("  heatmap -> %s" % a.heatmap)
    if a.json_out:
        out = {k: v for k, v in res.items()
               if k not in ("loops", "flow", "hygiene_detail", "poles")}
        out["poles"] = {k: v for k, v in res["poles"].items() if k != "positions"}
        out["loops"] = {k: v for k, v in res["loops"].items() if not k.startswith("_")}
        out["flow"] = {k: v for k, v in res["flow"].items() if not k.startswith("_")}
        out["hygiene"] = res["hygiene"]
        with open(a.json_out, "w") as fh:
            json.dump(out, fh, indent=2)
        if not a.quiet:
            print("  json    -> %s" % a.json_out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
