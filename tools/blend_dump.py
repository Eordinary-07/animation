"""
blend_dump.py — run inside Blender headless:
    blender -b file.blend --python tools/blend_dump.py -- out.json

Extracts the STUDIO-RELEVANT data from a production .blend file:
  scenes (fps/resolution/engine), objects, collections, modifiers,
  Geometry Nodes trees (nodes + links + default values), vertex groups,
  shape keys, multires/dyntopo state, material summary, mesh statistics,
  and (for small enough meshes) fold/curvature metrics.

Output: one JSON file. Read-only: never modifies the .blend.
"""
import bpy
import json
import sys
import os
import math
from collections import defaultdict


def out_path():
    argv = sys.argv
    if "--" in argv:
        tail = argv[argv.index("--") + 1:]
        if tail:
            return tail[0]
    return os.path.splitext(bpy.data.filepath)[0] + "_dump.json"


def ser(v, depth=0):
    """Serialize Blender RNA values into plain JSON types."""
    if depth > 6:
        return str(v)
    if v is None:
        return None
    if isinstance(v, (bool, int, float, str)):
        return v
    if hasattr(v, "to_tuple"):
        try:
            return list(v.to_tuple())
        except Exception:
            pass
    if hasattr(v, "__iter__") and not hasattr(v, "bl_rna"):
        try:
            return [ser(x, depth + 1) for x in v][:32]
        except Exception:
            return str(v)
    if hasattr(v, "bl_rna"):
        d = {}
        for p in v.bl_rna.properties:
            pid = p.identifier
            if pid in ("rna_type", "bl_rna", "id_data"):
                continue
            if p.is_readonly and pid not in ("type", "name", "bl_idname"):
                continue
            try:
                d[pid] = ser(getattr(v, pid), depth + 1)
            except Exception:
                d[pid] = None
        return d
    return str(v)


def node_socket_value(sock):
    """Default value of a socket (the thing that carries the real settings)."""
    try:
        if hasattr(sock, "default_value"):
            dv = sock.default_value
            if hasattr(dv, "to_tuple"):
                return list(dv.to_tuple())
            if isinstance(dv, (int, float, bool, str)):
                return dv
            return str(dv)
    except Exception:
        pass
    return None


def dump_node_tree(ng, depth=0):
    if ng is None:
        return None
    data = {
        "name": ng.name,
        "type": ng.bl_idname if hasattr(ng, "bl_idname") else ng.type,
        "nodes": [],
        "links": [],
        "interface": [],
    }
    try:
        for item in ng.interface.items_tree:
            data["interface"].append({
                "name": item.name,
                "in_out": getattr(item, "in_out", None),
                "socket_type": getattr(item, "socket_type", None),
            })
    except Exception:
        pass
    try:
        for n in ng.nodes:
            nd = {
                "name": n.name,
                "type": getattr(n, "type", None),
                "bl_idname": getattr(n, "bl_idname", None),
                "label": getattr(n, "label", ""),
                "location": [round(n.location.x, 1), round(n.location.y, 1)],
                "parent": n.parent.name if getattr(n, "parent", None) else None,
                "mute": getattr(n, "mute", None),
            }
            props = {}
            skip = ("rna_type", "bl_rna", "id_data", "name", "label",
                    "location", "width", "height", "type", "bl_idname",
                    "inputs", "outputs", "internal_links", "parent",
                    "select", "color", "use_custom_color", "mute",
                    "hide", "dimensions", "show_options", "show_preview",
                    "show_texture", "bl_description", "bl_icon",
                    "bl_static_type", "bl_width_default", "bl_width_min",
                    "bl_width_max", "bl_height_default", "bl_height_min",
                    "bl_height_max")
            for p in n.bl_rna.properties:
                pid = p.identifier
                if pid in skip:
                    continue
                try:
                    val = getattr(n, pid)
                except Exception:
                    continue
                if hasattr(val, "bl_rna") or (hasattr(val, "__iter__")
                                              and not isinstance(val, str)):
                    continue
                if isinstance(val, (int, float, bool, str)) or val is None:
                    props[pid] = val
            nd["props"] = props
            nd["inputs"] = []
            for s in n.inputs:
                nd["inputs"].append({
                    "name": s.name,
                    "identifier": getattr(s, "identifier", ""),
                    "type": s.type,
                    "default_value": node_socket_value(s),
                })
            if n.type == "GROUP" and getattr(n, "node_tree", None):
                if depth < 3:
                    nd["group_tree"] = dump_node_tree(n.node_tree, depth + 1)
            data["nodes"].append(nd)
    except Exception as e:
        data["nodes_error"] = str(e)
    try:
        for l in ng.links:
            data["links"].append([
                l.from_node.name, getattr(l.from_socket, "name", ""),
                l.to_node.name, getattr(l.to_socket, "name", ""),
            ])
    except Exception as e:
        data["links_error"] = str(e)
    return data


def mesh_stats(me):
    s = {
        "vertices": len(me.vertices),
        "edges": len(me.edges),
        "polygons": len(me.polygons),
        "loops": len(me.loops),
        "uv_layers": [uv.name for uv in me.uv_layers],
        "color_attributes": [c.name for c in me.color_attributes],
        "attributes": [],
    }
    try:
        for a in me.attributes:
            s["attributes"].append({"name": a.name,
                                    "domain": a.domain,
                                    "data_type": a.data_type})
    except Exception:
        pass
    if me.polygons:
        tris = sum(1 for p in me.polygons if len(p.vertices) == 3)
        quads = sum(1 for p in me.polygons if len(p.vertices) == 4)
        ngons = len(me.polygons) - tris - quads
        s.update({
            "tris": tris,
            "quads": quads,
            "ngons": ngons,
            "quad_percent": round(100.0 * quads / len(me.polygons), 1),
        })
    return s


def fold_metrics(me, max_verts=400000):
    """
    Quantitative fold/drapery data from a SCULPTED mesh.
    fold amplitude = distance from a Laplacian-smoothed version of the mesh
    (the "body under the cloth"), reported absolute and as % of bbox diagonal.
    """
    n = len(me.vertices)
    if n == 0 or n > max_verts:
        return {"skipped": True, "reason": "mesh too large or empty",
                "vertices": n}
    try:
        verts = [v.co.copy() for v in me.vertices]
        adj = defaultdict(set)
        for e in me.edges:
            adj[e.vertices[0]].add(e.vertices[1])
            adj[e.vertices[1]].add(e.vertices[0])
        def smooth(iterations, factor):
            cur = [(v[0], v[1], v[2]) for v in verts]
            for _ in range(iterations):
                nxt = []
                for i, (x, y, z) in enumerate(cur):
                    nb = adj.get(i)
                    if not nb:
                        nxt.append((x, y, z))
                        continue
                    sx = sy = sz = 0.0
                    for j in nb:
                        sx += cur[j][0]
                        sy += cur[j][1]
                        sz += cur[j][2]
                    k = len(nb)
                    nxt.append(((1 - factor) * x + factor * sx / k,
                                (1 - factor) * y + factor * sy / k,
                                (1 - factor) * z + factor * sz / k))
                cur = nxt
            return cur

        def devs_from(base):
            out = []
            for i, (x, y, z) in enumerate(verts):
                cx, cy, cz = base[i]
                out.append(math.sqrt((x - cx) ** 2 + (y - cy) ** 2 +
                                     (z - cz) ** 2))
            out.sort()
            return out

        devs = devs_from(smooth(3, 0.5))            # fine surface detail
        devs_form = devs_from(smooth(30, 1.0))      # folds / form deviation
        xs = [v[0] for v in verts]
        ys = [v[1] for v in verts]
        zs = [v[2] for v in verts]
        dims = [max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)]
        diag = math.sqrt(sum(d * d for d in dims)) or 1.0

        def pct(p):
            return devs[min(len(devs) - 1, int(p * len(devs)))]

        return {
            "skipped": False,
            "vertices": n,
            "bbox_diagonal": round(diag, 5),
            "fold_amplitude": {
                "median": round(pct(0.50), 6),
                "p75": round(pct(0.75), 6),
                "p95": round(pct(0.95), 6),
                "max": round(devs[-1], 6),
                "p95_percent_of_diagonal": round(100.0 * pct(0.95) / diag, 3),
                "max_percent_of_diagonal": round(100.0 * devs[-1] / diag, 3),
            },
            "fold_depth_form": {
                "median": round(devs_form[len(devs_form) // 2], 6),
                "p95": round(devs_form[int(0.95 * len(devs_form))], 6),
                "max": round(devs_form[-1], 6),
                "median_percent_of_diagonal": round(
                    100.0 * devs_form[len(devs_form) // 2] / diag, 3),
                "p95_percent_of_diagonal": round(
                    100.0 * devs_form[int(0.95 * len(devs_form))] / diag, 3),
                "max_percent_of_diagonal": round(
                    100.0 * devs_form[-1] / diag, 3),
            },
        }
    except Exception as e:
        return {"skipped": True, "reason": str(e), "vertices": n}


def dump_object(ob, do_fold=True):
    d = {
        "name": ob.name,
        "type": ob.type,
        "parent": ob.parent.name if ob.parent else None,
        "dimensions": [round(x, 5) for x in ob.dimensions],
        "location": [round(x, 5) for x in ob.location],
        "modifiers": [],
        "vertex_groups": [],
        "shape_keys": None,
        "materials": [],
    }
    try:
        d["materials"] = [m.name for m in (getattr(ob, "materials", None) or [])
                          if m]
    except Exception:
        pass
    for m in getattr(ob, "modifiers", []) or []:
        try:
            md = {"name": m.name, "type": m.type, "props": ser(m)}
        except Exception as e:
            d["modifiers"].append({"name": getattr(m, "name", "?"), "error": str(e)})
            continue
        if m.type == "NODES" and getattr(m, "node_group", None):
            md["node_group"] = m.node_group.name
            md["node_tree"] = dump_node_tree(m.node_group)
        if m.type in ("MULTIRES", "SUBSURF", "CLOTH", "PARTICLE_SYSTEM",
                      "SOLIDIFY", "SHRINKWRAP", "CORRECTIVE_SMOOTH"):
            md["key_settings"] = {
                "levels": getattr(m, "levels", None),
                "render_levels": getattr(m, "render_levels", None),
                "sculpt_levels": getattr(m, "sculpt_levels", None),
                "total_levels": getattr(m, "total_levels", None),
                "quality": getattr(m, "quality", None),
                "subdivision_type": getattr(m, "subdivision_type", None),
            }
        d["modifiers"].append(md)
    try:
        d["vertex_groups"] = [{"name": g.name, "index": g.index}
                              for g in ob.vertex_groups]
    except Exception:
        pass
    try:
        if ob.data and hasattr(ob.data, "shape_keys") and ob.data.shape_keys:
            d["shape_keys"] = [k.name for k in ob.data.shape_keys.key_blocks]
    except Exception:
        pass
    if ob.type == "MESH" and ob.data:
        d["mesh"] = mesh_stats(ob.data)
        if do_fold:
            d["fold_metrics"] = fold_metrics(ob.data)
    if ob.type == "CURVES" and ob.data:
        try:
            d["curves"] = {
                "curve_count": len(ob.data.curves),
                "point_count": len(ob.data.points),
                "attributes": [a.name for a in ob.data.attributes],
            }
        except Exception as e:
            d["curves"] = {"error": str(e)}
    return d


def main():
    out = {
        "file": os.path.basename(bpy.data.filepath),
        "blender_version": ".".join(str(x) for x in bpy.app.version),
        "scenes": [],
        "objects": [],
        "collections": [],
        "node_groups": [],
        "meshes_count": len(bpy.data.meshes),
        "materials": [m.name for m in bpy.data.materials],
        "images": [i.name for i in bpy.data.images][:40],
    }
    for sc in bpy.data.scenes:
        out["scenes"].append({
            "name": sc.name,
            "fps": sc.render.fps,
            "fps_base": sc.render.fps_base,
            "frame_start": sc.frame_start,
            "frame_end": sc.frame_end,
            "resolution": [sc.render.resolution_x, sc.render.resolution_y],
            "engine": sc.render.engine,
            "view_transform": getattr(sc.view_settings, "view_transform", None),
        })
    for c in bpy.data.collections:
        out["collections"].append({
            "name": c.name,
            "children": [ch.name for ch in c.children],
            "objects": [o.name for o in c.objects],
        })
    for ng in bpy.data.node_groups:
        out["node_groups"].append(dump_node_tree(ng))
    for ob in bpy.data.objects:
        try:
            out["objects"].append(dump_object(ob))
        except Exception as e:
            out["objects"].append({"name": ob.name, "error": str(e)})
    with open(out_path(), "w") as f:
        json.dump(out, f, indent=1, default=str)
    print("WROTE", out_path())


main()
