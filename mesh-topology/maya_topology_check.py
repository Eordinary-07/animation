# Run in Maya's script editor (Python), with the mesh selected.
#
#   import sys; sys.path.append("/path/to/mesh-topology")
#   import maya_topology_check as m
#   m.main()
#
# Or from a shell:  mayapy maya_topology_check.py
#
# The score, the report and the pole selection all land in the script editor and
# in OUT_DIR.

import os
import sys

import maya.cmds as cmds

HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
JOINTS_PATH = ""            # "" or a JSON path, or "auto"
OUT_DIR = HERE
EVALUATE_DEFORMED = False    # True = measure the skinned/posed mesh instead of rest

if HERE not in sys.path:
    sys.path.append(HERE)

import topology_check as tc          # noqa: E402


def gather(obj, deformed=False):
    """Verts in world space + polygons as (V, F) on a plain (non-shape) copy."""
    tmp = cmds.polyCopy(obj, name=obj + "_topoCheck#")[0]
    try:
        if not deformed:
            # rest shape: strip history so the skin cluster does not move the copy
            cmds.delete(tmp, constructionHistory=True)
        cmds.polyTriangulate(tmp, constructionHistory=False) if False else None
        n = cmds.polyEvaluate(tmp, vertex=True)
        V = []
        for i in range(n):
            p = cmds.xform("%s.vtx[%d]" % (tmp, i), q=True, ws=True, translation=True)
            V.append(tuple(p))
        counts = [cmds.polyEvaluate("%s.f[%d]" % (tmp, i), vertex=True)
                  for i in range(cmds.polyEvaluate(tmp, face=True))]
        F, k = [], 0
        for c in counts:
            F.append(tuple(range(k, k + c)))
            k += c
        return V, F
    finally:
        cmds.delete(tmp)


def main():
    sel = cmds.ls(selection=True, long=True)
    if not sel:
        cmds.error("select a mesh first")
    obj = sel[0]
    V, F = gather(obj, EVALUATE_DEFORMED)
    mesh = tc.Mesh(V, F, obj.split("|")[-1])

    joints = None
    if JOINTS_PATH == "auto":
        joints = tc.auto_joints(mesh)
    elif JOINTS_PATH:
        joints = tc.load_joints(JOINTS_PATH)

    res = tc.score_mesh(mesh, joints=joints)

    print("\n=== %s ===" % mesh.name)
    print("SCORE %.1f / 100   grade %s" % (res["score"], res["grade"]))
    for k, v in res["subscores"].items():
        print("  %-8s %5.1f" % (k, v))
    for c in res["caps"]:
        print("  !! %s" % c)

    report = os.path.join(OUT_DIR, "topology_%s.md" % mesh.name.replace(" ", "_"))
    tc.render_report(res, mesh, report)
    print("report -> %s" % report)

    if res["poles"]["indices"]:
        cmds.select(cl=True)
        for v in res["poles"]["indices"]:
            cmds.select("%s.vtx[%d]" % (obj, v), add=True)
        print("%d pole vertices selected" % len(res["poles"]["indices"]))


if __name__ == "__main__":
    main()
