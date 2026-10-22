# Run this inside Blender: Scripting workspace -> Open -> Run Script, with the
# mesh object selected. Uses the active object directly, no export needed.
#
#   blender --background file.blend --python blender_topology_check.py
#
# Optional: set JOINTS_PATH below to a JSON file, or leave it empty to detect
# the bendy regions automatically.

import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(bpy.data.filepath)) if bpy.data.filepath else os.getcwd()
JOINTS_PATH = ""          # e.g. os.path.join(HERE, "joints.json"), or "auto"
OUT_DIR = HERE

# find topology_check.py next to this file or in the blend folder
for cand in (os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else HERE,
             HERE, os.getcwd()):
    if os.path.exists(os.path.join(cand, "topology_check.py")):
        sys.path.insert(0, cand)
        break

import topology_check as tc          # noqa: E402


def active_mesh():
    obj = bpy.context.object
    if obj is None or obj.type != "MESH":
        meshes = [o for o in bpy.context.selected_objects if o.type == "MESH"]
        if not meshes:
            raise RuntimeError("select a mesh object first")
        obj = meshes[0]
    return obj


def gather(obj, apply_modifiers=True):
    """World-space vertices + polygons as (V, F). Optionally evaluates
    modifiers so subdivision / mirror show up in the analysis."""
    deps = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(deps) if apply_modifiers else obj
    me = ev.to_mesh()
    M = obj.matrix_world
    V = [tuple(M @ v.co) for v in me.vertices]
    F = [tuple(p.vertices) for p in me.polygons]
    ev.to_mesh_clear()
    return V, F


def select_verts(obj, indices, name="TOPOLOGY_PROBLEMS"):
    """Create a vertex group so you can see the problem areas in the viewport."""
    for vg in list(obj.vertex_groups):
        if vg.name == name:
            obj.vertex_groups.remove(vg)
    vg = obj.vertex_groups.new(name=name)
    vg.add(list(indices), 1.0, "REPLACE")
    return vg


def main():
    obj = active_mesh()
    V, F = gather(obj)
    mesh = tc.Mesh(V, F, obj.name)

    joints = None
    if JOINTS_PATH == "auto":
        joints = tc.auto_joints(mesh)
    elif JOINTS_PATH:
        joints = tc.load_joints(JOINTS_PATH)

    res = tc.score_mesh(mesh, joints=joints)

    print("\n=== %s ===" % obj.name)
    print("SCORE %.1f / 100   grade %s" % (res["score"], res["grade"]))
    for k, v in res["subscores"].items():
        print("  %-8s %5.1f" % (k, v))
    for c in res["caps"]:
        print("  !! %s" % c)

    # select the problem vertices so they are visible in the viewport
    bad = set(res["poles"]["indices"])
    report = os.path.join(OUT_DIR, "topology_%s.md" % obj.name.replace(" ", "_"))
    tc.render_report(res, mesh, report)
    print("report ->", report)
    if bad:
        select_verts(obj, sorted(bad))
        print("%d pole vertices put in vertex group TOPOLOGY_PROBLEMS" % len(bad))


if __name__ == "__main__":
    main()
