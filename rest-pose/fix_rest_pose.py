#!/usr/bin/env python3
"""
fix_rest_pose.py — audit and repair a character's rest pose in Maya or Blender.

Your rest pose is supposed to be a T-pose. What is in the viewport is not one.
This tool tells you *exactly* how far off it is, then puts it back.

    # Maya: run inside the script editor, or  mayapy fix_rest_pose.py --audit
    # Blender:  blender -b file.blend --python fix_rest_pose.py -- --audit
    # Pure math check, no DCC needed:
    python3 fix_rest_pose.py --selftest

Modes
    --audit              print measured deviations, change nothing (default)
    --zero               zero every pose rotation in the chains -> back to the
                         skeleton's own rest pose. This is the correct fix when
                         the skeleton was authored in T and a pose was applied.
    --tpose              aim the arms to horizontal, legs vertical, feet forward
                         and flat, spine/neck/head upright. Use when the
                         skeleton's rest is NOT a T-pose.
    --apose DEG          same, but arms down DEG degrees from horizontal (45).
    --apply              actually write the changes (without it, dry run)
    --bake-rest          after fixing, save the current pose as the bind pose
                         (Maya: dagPose -bindPose / Blender: apply as rest pose)
    --roll JOINT DEG     extra twist about the limb axis, repeatable, e.g.
                         --roll upperarm_L 15 --roll hand_R -10
    --up {y,z}           world up axis (Maya default y, Blender default z)

Notes
    * Joints are found by name pattern, covering the usual suspects:
      Mixamo, Maya HumanIK, Advanced Skeleton, Rigify, SOMA/Kimodo, generic.
      Use --map to override:  --map upperarm_L:upperArm_l
    * Twist about a limb's own axis is not observable from bone directions, so
      palm/knee/foot roll is left as-is unless you pass --roll. Eyeball it.
    * Always --audit first. Always keep a backup of the file.
"""

from __future__ import annotations

import argparse
import math
import re
import sys

# ---------------------------------------------------------------------------
# tiny 3x3 / vec3 maths (no numpy: Maya and Blender both have it, but keeping
# this dependency-free means --selftest runs anywhere)
# ---------------------------------------------------------------------------


def vsub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def vadd(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vmul(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def vdot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vcross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def vlen(a):
    return math.sqrt(vdot(a, a))


def vnorm(a):
    n = vlen(a)
    return (a[0] / n, a[1] / n, a[2] / n) if n > 1e-12 else (0.0, 0.0, 0.0)


def mmul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3))
                 for i in range(3))


def mT(a):
    return tuple(tuple(a[j][i] for j in range(3)) for i in range(3))


def mvec(m, v):
    return tuple(sum(m[i][k] * v[k] for k in range(3)) for i in range(3))


def m_from_axis_angle(axis, ang):
    x, y, z = vnorm(axis)
    c, s = math.cos(ang), math.sin(ang)
    C = 1.0 - c
    return ((c + x * x * C, x * y * C - z * s, x * z * C + y * s),
            (y * x * C + z * s, c + y * y * C, y * z * C - x * s),
            (z * x * C - y * s, z * y * C + x * s, c + z * z * C))


def rotation_between(a, b):
    """Shortest-arc rotation matrix taking unit vector a onto unit vector b."""
    a, b = vnorm(a), vnorm(b)
    d = max(-1.0, min(1.0, vdot(a, b)))
    if d > 1.0 - 1e-9:
        return ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    if d < -1.0 + 1e-9:                                   # 180 degrees
        axis = vcross(a, (1.0, 0.0, 0.0))
        if vlen(axis) < 1e-6:
            axis = vcross(a, (0.0, 1.0, 0.0))
        return m_from_axis_angle(axis, math.pi)
    axis = vcross(a, b)
    return m_from_axis_angle(axis, math.acos(d))


def angle_between(a, b):
    a, b = vnorm(a), vnorm(b)
    return math.degrees(math.acos(max(-1.0, min(1.0, vdot(a, b)))))


def fmt_m(v):
    return "(%.3f, %.3f, %.3f)" % v


# ---------------------------------------------------------------------------
# joint-name resolution
# ---------------------------------------------------------------------------

CHAIN_PATTERNS = {
    # side-less token: matched against a lowercased joint name
    "clavicle": [r"clavicle", r"shoulder", r"collar", r"c_shoulder"],
    "upperarm": [r"upper[_.]?arm", r"uparm", r"upperarm", r"(?<![a-z])arm(?![a-z])"],
    "lowerarm": [r"lower[_.]?arm", r"fore[_.]?arm", r"loarm", r"elbow"],
    "hand": [r"(?<![a-z])hand(?![a-z])", r"wrist"],
    "thigh": [r"thigh", r"upper[_.]?leg", r"upleg", r"(?<![a-z])leg(?![a-z])"],
    "calf": [r"calf", r"shin", r"lower[_.]?leg", r"lowleg", r"knee"],
    "foot": [r"(?<![a-z])foot(?![a-z])", r"ankle"],
    "toe": [r"toe"],
    "neck": [r"neck"],
    "head": [r"(?<![a-z])head(?![a-z])"],
    "pelvis": [r"hips?(?![a-z])", r"pelvis", r"(?<![a-z])root(?![a-z])"],
}

# names that must never be picked for a chain, because they contain a token
# that looks right but means something else
CHAIN_REJECT = {
    "upperarm": [r"lower", r"fore", r"hand", r"wrist", r"twist", r"roll"],
    "lowerarm": [r"hand", r"wrist", r"twist"],
    "hand": [r"thumb", r"index", r"middle", r"ring", r"pinky", r"finger", r"twist"],
    "thigh": [r"lower", r"calf", r"shin", r"twist", r"foot"],
    "calf": [r"foot", r"thigh", r"twist"],
    "foot": [r"toe", r"ball", r"tip", r"end"],
    "head": [r"top", r"end", r"nub", r"jaw", r"eye"],
    "neck": [r"twist"],
}

SIDE_PATTERNS = {
    "L": [r"left"],
    "R": [r"right"],
}

SIDE_PREFIX = {"l_": "L", "lf_": "L", "left": "L", "r_": "R", "rt_": "R", "right": "R"}


def side_of(name: str):
    """L/R from a joint name, without getting fooled by substring traps
    (the 'lf_' inside 'ca-lf-_R' is the classic one)."""
    low = name.lower()
    tokens = [t for t in re.split(r"[^a-z]+", low) if t]
    if "l" in tokens:
        return "L"
    if "r" in tokens:
        return "R"
    for side, pats in SIDE_PATTERNS.items():
        for p in pats:
            if re.search(p, low):
                return side
    for pre, side in SIDE_PREFIX.items():
        if low.startswith(pre):
            return side
    return None


def resolve(joints, chain: str, side: str | None):
    """First joint whose name matches the chain pattern (and side, if given)."""
    rejects = CHAIN_REJECT.get(chain, [])
    cands = []
    for j in joints:
        low = j.lower()
        if side and side_of(j) != side:
            continue
        if any(re.search(p, low) for p in rejects):
            continue
        if any(re.search(p, low) for p in CHAIN_PATTERNS[chain]):
            cands.append(j)
    # prefer the shortest name: kills "upperarm_twist_01" style extras
    cands.sort(key=lambda n: (len(n), n))
    return cands[0] if cands else None


# ---------------------------------------------------------------------------
# rig adapters
# ---------------------------------------------------------------------------


class Rig:
    """Minimal interface the fixer needs. Subclass per DCC."""

    up_axis = (0.0, 1.0, 0.0)

    def joints(self):
        raise NotImplementedError

    def world_pos(self, name):
        raise NotImplementedError

    def world_rot(self, name):
        raise NotImplementedError

    def set_world_rot(self, name, mat):
        raise NotImplementedError

    def parent_of(self, name):
        raise NotImplementedError

    def local_rot(self, name):
        raise NotImplementedError

    def set_local_rot(self, name, mat):
        raise NotImplementedError

    def refresh(self):
        pass

    def bake_rest(self):
        raise NotImplementedError


class MayaRig(Rig):
    def __init__(self):
        import maya.cmds as cmds
        self.cmds = cmds
        sel = cmds.ls(selection=True, type="joint")
        if not sel:
            raise RuntimeError("select the armature's root joint (or any joint) first")
        root = sel[0]
        while True:
            p = cmds.listRelatives(root, parent=True, type="joint") or []
            if not p:
                break
            root = p[0]
        self._joints = cmds.listRelatives(root, allDescendents=True, type="joint") or []
        self._joints = [root] + self._joints
        self.up_axis = (0.0, 1.0, 0.0)

    def joints(self):
        return self._joints

    def world_pos(self, name):
        return tuple(self.cmds.xform(name, q=True, ws=True, translation=True))

    def world_rot(self, name):
        m = self.cmds.xform(name, q=True, ws=True, matrix=True)
        # Maya matrix flag returns row-major 16 floats
        return ((m[0], m[1], m[2]), (m[4], m[5], m[6]), (m[8], m[9], m[10]))

    def set_world_rot(self, name, mat):
        e = self._to_euler(mat)
        self.cmds.xform(name, ws=True, rotation=e)

    def parent_of(self, name):
        p = self.cmds.listRelatives(name, parent=True, type="joint") or []
        return p[0] if p else None

    def local_rot(self, name):
        m = self.cmds.xform(name, q=True, matrix=True)
        return ((m[0], m[1], m[2]), (m[4], m[5], m[6]), (m[8], m[9], m[10]))

    def set_local_rot(self, name, mat):
        self.cmds.xform(name, rotation=self._to_euler(mat))

    @staticmethod
    def _to_euler(m):
        # XYZ order euler from a rotation matrix
        sy = math.sqrt(m[0][0] ** 2 + m[1][0] ** 2)
        if sy > 1e-6:
            x = math.atan2(m[2][1], m[2][2])
            y = math.atan2(-m[2][0], sy)
            z = math.atan2(m[1][0], m[0][0])
        else:
            x = math.atan2(-m[1][2], m[1][1])
            y = math.atan2(-m[2][0], sy)
            z = 0.0
        return (math.degrees(x), math.degrees(y), math.degrees(z))

    def bake_rest(self):
        self.cmds.dagPose(self._joints[0], save=True, bindPose=True)


class BlenderRig(Rig):
    def __init__(self):
        import bpy
        obj = bpy.context.object
        if obj is None or obj.type != "ARMATURE":
            arms = [o for o in bpy.context.selected_objects if o.type == "ARMATURE"]
            if not arms:
                raise RuntimeError("select the armature object first")
            obj = arms[0]
        self.bpy = bpy
        self.obj = obj
        self._bones = [b.name for b in obj.pose.bones]
        self.up_axis = (0.0, 0.0, 1.0)

    def joints(self):
        return self._bones

    def _pb(self, name):
        return self.obj.pose.bones[name]

    def world_pos(self, name):
        m = self.obj.matrix_world @ self._pb(name).head
        return (m.x, m.y, m.z)

    def world_rot(self, name):
        m = self.obj.matrix_world @ self._pb(name).matrix
        return tuple(tuple(m[i][j] for j in range(3)) for i in range(3))

    def set_world_rot(self, name, mat):
        from mathutils import Matrix
        rest = self.obj.matrix_world
        # keep translation, replace rotation, convert back to armature space
        cur = self.obj.matrix_world @ self._pb(name).matrix
        t = cur.translation
        world = Matrix((mat[0], mat[1], mat[2])).to_4x4()
        for i in range(3):
            world[i][3] = t[i]
        self._pb(name).matrix = rest.inverted() @ world
        self.bpy.context.view_layer.update()

    def parent_of(self, name):
        p = self._pb(name).parent
        return p.name if p else None

    def local_rot(self, name):
        m = self._pb(name).rotation_quaternion.to_matrix()
        return tuple(tuple(m[i][j] for j in range(3)) for i in range(3))

    def set_local_rot(self, name, mat):
        from mathutils import Matrix
        self._pb(name).rotation_mode = "QUATERNION"
        self._pb(name).rotation_quaternion = Matrix((mat[0], mat[1], mat[2])).to_quaternion()
        self.bpy.context.view_layer.update()

    def refresh(self):
        self.bpy.context.view_layer.update()

    def bake_rest(self):
        bpy, obj = self.bpy, self.obj
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode="POSE")
        bpy.ops.pose.select_all(action="SELECT")
        bpy.ops.pose.armature_apply(selected=True)   # pose -> rest
        bpy.ops.object.mode_set(mode="OBJECT")


# ---------------------------------------------------------------------------
# audit
# ---------------------------------------------------------------------------


def pick(rig, chain, side=None):
    return resolve(rig.joints(), chain, side)


def audit(rig):
    print("\n=== REST POSE AUDIT ===")
    up = rig.up_axis
    found = {}
    for chain in ("clavicle", "upperarm", "lowerarm", "hand", "thigh", "calf", "foot", "toe",
                  "neck", "head", "pelvis"):
        for side in (None, "L", "R"):
            n = pick(rig, chain, side) if side or chain in ("neck", "head", "pelvis") else None
            if n:
                found[(chain, side)] = n

    print("\n-- bones found --")
    for (chain, side), n in sorted(found.items(), key=lambda kv: (kv[0][0], str(kv[0][1]))):
        print("   %-9s %-2s -> %s" % (chain, side or "", n))

    problems = []

    # 1. symmetry: mirror each left joint across the body's sagittal plane
    pelvis = found.get(("pelvis", None))
    if pelvis:
        p = rig.world_pos(pelvis)
        print("\n-- pelvis --\n   %s at %s" % (pelvis, fmt_m(p)))

    print("\n-- left/right symmetry --")
    axis_i = up.index(max(up))
    for chain in ("clavicle", "upperarm", "lowerarm", "hand", "thigh", "calf", "foot", "toe"):
        lj, rj = found.get((chain, "L")), found.get((chain, "R"))
        if not lj or not rj:
            continue
        pl, pr = rig.world_pos(lj), rig.world_pos(rj)
        mid = [(pl[i] + pr[i]) * 0.5 for i in range(3)]
        dl = vsub(pl, mid)
        dr = vsub(pr, mid)
        # a mirrored pair has dl == -dr
        err = vlen(vadd(dl, dr))          # how far from a perfect mirror the pair is
        print("   %-9s mirror error %6.2f cm   (L%s R%s)" %
              (chain, err * 100.0, fmt_m(dl), fmt_m(dr)))
        if err > 0.005:
            problems.append("%s pair is %.1f mm off a perfect mirror" % (chain, err * 1000))

    # 1b. direction mismatch: mirror each left limb direction and compare it to
    # the right one. This is the check that catches "both arms are down, but by
    # different amounts" — a positional mirror test cannot see that.
    sl, sr = found.get(("clavicle", "L")), found.get(("clavicle", "R"))
    side_vec = vnorm(vsub(rig.world_pos(sl), rig.world_pos(sr))) if (sl and sr) else (1.0, 0.0, 0.0)
    side_i = max(range(3), key=lambda i: abs(side_vec[i]))
    print("\n-- left/right direction mismatch --")
    for a_chain, b_chain in (("upperarm", "lowerarm"), ("lowerarm", "hand"),
                             ("thigh", "calf"), ("calf", "foot"), ("foot", "toe")):
        al, bl = found.get((a_chain, "L")), found.get((b_chain, "L"))
        ar, br = found.get((a_chain, "R")), found.get((b_chain, "R"))
        if not (al and bl and ar and br):
            continue
        dl = vnorm(vsub(rig.world_pos(bl), rig.world_pos(al)))
        dr = vnorm(vsub(rig.world_pos(br), rig.world_pos(ar)))
        dm = list(dl)
        dm[side_i] = -dm[side_i]
        err = angle_between(tuple(dm), dr)
        print("   %-9s direction mismatch %5.1f deg" % (a_chain, err))
        if err > 3.0:
            problems.append("%s points %.0f deg differently left vs right" % (a_chain, err))

    # 2. arm elevation: T-pose wants ~0 deg below horizontal
    print("\n-- arm elevation (0 = horizontal, 90 = hanging down) --")
    for side in ("L", "R"):
        ua, la, hd = found.get(("upperarm", side)), found.get(("lowerarm", side)), found.get(("hand", side))
        if not (ua and la):
            continue
        p_ua, p_la = rig.world_pos(ua), rig.world_pos(la)
        d = vsub(p_la, p_ua)
        horiz = vlen((d[0], 0.0, d[2])) if axis_i == 1 else vlen((d[0], d[1], 0.0))
        elev = math.degrees(math.atan2(-d[axis_i], horiz))
        elbow = ""
        if hd:
            e = angle_between(vsub(p_la, p_ua), vsub(rig.world_pos(hd), p_la))
            elbow = "   elbow bend %.1f deg (0 = straight)" % e
        print("   %s: %.1f deg below horizontal%s" % (side, elev, elbow))
        if abs(elev) > 8:
            problems.append("%s arm is %.0f deg off horizontal" % (side, elev))

    # 3. legs vertical
    print("\n-- leg verticality --")
    for side in ("L", "R"):
        th, ca = found.get(("thigh", side)), found.get(("calf", side))
        if not (th and ca):
            continue
        d = vsub(rig.world_pos(ca), rig.world_pos(th))
        tilt = math.degrees(math.atan2(math.sqrt(d[0] ** 2 + d[2] ** 2), abs(d[1])))
        print("   %s thigh: %.1f deg off vertical" % (side, tilt))
        if tilt > 8:
            problems.append("%s thigh is %.0f deg off vertical" % (side, tilt))

    # 4. feet forward and flat
    print("\n-- feet --")
    for side in ("L", "R"):
        ft, to = found.get(("foot", side)), found.get(("toe", side))
        if not (ft and to):
            continue
        d = vnorm(vsub(rig.world_pos(to), rig.world_pos(ft)))
        yaw = math.degrees(math.atan2(d[0], d[2]))
        roll = math.degrees(math.asin(max(-1, min(1, d[axis_i]))))
        print("   %s foot: yaw %+.1f deg (0 = straight ahead), pitch %+.1f deg" % (side, yaw, roll))
        if abs(yaw) > 12:
            problems.append("%s foot is turned %.0f deg" % (side, yaw))

    # 5. spine stack: is the head over the pelvis?
    neck, head = found.get(("neck", None)), found.get(("head", None))
    if pelvis and neck:
        px, pz = rig.world_pos(pelvis)[0], rig.world_pos(pelvis)[2]
        nx, nz = rig.world_pos(neck)[0], rig.world_pos(neck)[2]
        drift = math.hypot(nx - px, nz - pz)
        print("\n-- spine --\n   neck is %.1f cm %s of the pelvis in plan view" %
              (drift * 100, "off" if drift > 0.01 else "over"))
        if drift > 0.02:
            problems.append("neck sits %.0f mm off the pelvis axis (lean or weight shift)" % (drift * 1000))

    # 6. hip level
    if found.get(("thigh", "L")) and found.get(("thigh", "R")):
        hl = rig.world_pos(found[("thigh", "L")])[axis_i]
        hr = rig.world_pos(found[("thigh", "R")])[axis_i]
        print("   hip height difference L-R: %.2f cm" % ((hl - hr) * 100))
        if abs(hl - hr) > 0.005:
            problems.append("hips are %.0f mm out of level" % (abs(hl - hr) * 1000))

    print("\n=== VERDICT ===")
    if not problems:
        print("   pose is symmetric and axis-aligned. If it still looks wrong,")
        print("   the mesh (not the skeleton) is the thing to look at.")
    else:
        for p in problems:
            print("   ! " + p)
        print("\n   %d issue(s). Run with --zero (skeleton authored in T) or" % len(problems))
        print("   --tpose (skeleton rest is not a T-pose) to fix.")
    return problems


# ---------------------------------------------------------------------------
# fix
# ---------------------------------------------------------------------------


def aim(rig, joint, child, desired_dir, roll_deg=0.0, dry=True):
    """Rotate `joint` so that (child - joint) points along desired_dir."""
    p = rig.world_pos(joint)
    c = rig.world_pos(child)
    cur = vsub(c, p)
    if vlen(cur) < 1e-6:
        return
    q = rotation_between(cur, desired_dir)
    if abs(roll_deg) > 1e-9:
        # twist about the axis the limb ends up on, applied after the aim
        q = mmul(m_from_axis_angle(vnorm(desired_dir), math.radians(roll_deg)), q)
    new = mmul(q, rig.world_rot(joint))
    if not dry:
        rig.set_world_rot(joint, new)
        rig.refresh()
    return new


def fix(rig, mode, apose_deg, rolls, dry=True):
    up = rig.up_axis
    joints = rig.joints()

    found = {}
    for chain in ("clavicle", "upperarm", "lowerarm", "hand", "thigh", "calf", "foot", "toe",
                  "neck", "head", "pelvis"):
        for side in ("L", "R"):
            n = pick(rig, chain, side)
            if n:
                found[(chain, side)] = n

    if mode == "zero":
        I = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
        for n in joints:
            if dry:
                continue
            rig.set_local_rot(n, I)
        print("zeroed %d joint rotation(s)%s" % (len(joints), "" if not dry else "  [dry run]"))
        return

    # side axis: right -> left across the shoulders. Never derived from the feet:
    # the feet are one of the things we are about to fix.
    sl, sr = found.get(("clavicle", "L")), found.get(("clavicle", "R"))
    if not (sl and sr):
        sl, sr = found.get(("upperarm", "L")), found.get(("upperarm", "R"))
    if sl and sr:
        side_vec = vnorm(vsub(rig.world_pos(sl), rig.world_pos(sr)))
    else:
        raise RuntimeError("could not find a left/right shoulder pair — pass --map")

    # facing = left x up  (Y-up: (1,0,0)x(0,1,0) = +Z;  Z-up: (1,0,0)x(0,0,1) = -Y)
    fwd = vnorm(vcross(side_vec, up))
    if vlen(fwd) < 0.5:
        fwd = (0.0, 0.0, 1.0)

    print("facing %s   side axis %s   up %s" % (fmt_m(fwd), fmt_m(side_vec), fmt_m(up)))

    down = vmul(up, -1.0)
    arm_dir = {}
    for side, sgn in (("L", 1.0), ("R", -1.0)):
        lateral = vmul(side_vec, sgn)
        if mode == "tpose":
            arm_dir[side] = lateral
        else:
            a = math.radians(apose_deg)
            arm_dir[side] = vadd(vmul(lateral, math.cos(a)), vmul(down, math.sin(a)))

    def roll_of(j):
        return rolls.get(j, 0.0)

    # --- arms: clavicle, upper arm, forearm, hand (parent -> child order) ---
    for side in ("L", "R"):
        cl = found.get(("clavicle", side))
        ua = found.get(("upperarm", side))
        la = found.get(("lowerarm", side))
        hd = found.get(("hand", side))
        if cl and ua:
            aim(rig, cl, ua, arm_dir[side], roll_of(cl), dry)
        if ua and la:
            aim(rig, ua, la, arm_dir[side], roll_of(ua), dry)
        if la and hd:
            aim(rig, la, hd, arm_dir[side], roll_of(la), dry)

    # --- spine, neck, head upright ---
    for chain, side in (("neck", None), ("head", None)):
        n = found.get((chain, side))
        if not n:
            continue
        kids = [j for j in joints if rig.parent_of(j) == n]
        if kids:
            aim(rig, n, kids[0], up, roll_of(n), dry)

    # --- legs: thigh and calf straight down, foot forward and flat ---
    for side in ("L", "R"):
        th = found.get(("thigh", side))
        ca = found.get(("calf", side))
        ft = found.get(("foot", side))
        to = found.get(("toe", side))
        if th and ca:
            aim(rig, th, ca, down, roll_of(th), dry)
        if ca and ft:
            aim(rig, ca, ft, down, roll_of(ca), dry)
        if ft and to:
            aim(rig, ft, to, fwd, roll_of(ft), dry)

    print("%s applied%s" % (mode, "" if not dry else "  [dry run — pass --apply to write]"))


# ---------------------------------------------------------------------------
# selftest: build a fake rig in a bad pose, fix it, measure
# ---------------------------------------------------------------------------


class FakeRig(Rig):
    """A test double with real forward kinematics, so rotation actually moves
    children the way it does in a DCC."""

    def __init__(self):
        self.off = {}     # local translation, expressed in the parent's frame
        self.loc = {}     # local rotation
        self.par = {}
        self.order = []
        self.up_axis = (0.0, 1.0, 0.0)

    def add(self, name, parent, offset, local_rot=None):
        self.off[name] = offset
        self.par[name] = parent
        I = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
        self.loc[name] = local_rot or I
        self.order.append(name)

    # --- FK ---------------------------------------------------------------
    def _world_rot(self, n):
        p = self.par.get(n)
        R = self.loc[n]
        return mmul(self._world_rot(p), R) if p else R

    def _world_pos(self, n):
        p = self.par.get(n)
        if not p:
            return self.off[n]
        return vadd(self._world_pos(p), mvec(self._world_rot(p), self.off[n]))

    # --- Rig interface ----------------------------------------------------
    def joints(self):
        return list(self.order)

    def world_pos(self, n):
        return self._world_pos(n)

    def world_rot(self, n):
        return self._world_rot(n)

    def set_world_rot(self, n, m):
        p = self.par.get(n)
        self.loc[n] = mmul(mT(self._world_rot(p)), m) if p else m

    def parent_of(self, n):
        return self.par.get(n)

    def local_rot(self, n):
        return self.loc[n]

    def set_local_rot(self, n, m):
        self.loc[n] = m

    def bake_rest(self):
        pass


def _rot(axis, deg):
    return m_from_axis_angle(axis, math.radians(deg))


def _build_bad_rig():
    """A humanoid authored in T, then posed into a relaxed asymmetric idle:
    arms rotated 80/74 degrees down, legs splayed, feet turned out."""
    r = FakeRig()
    I = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    r.add("hips", None, (0.0, 0.95, 0.0))
    r.add("spine", "hips", (0.0, 0.20, 0.0))
    r.add("neck", "spine", (0.0, 0.30, 0.0))
    r.add("head", "neck", (0.0, 0.15, 0.0))
    r.add("head_end", "head", (0.0, 0.18, 0.0))
    for side, s in (("L", 1.0), ("R", -1.0)):
        down = 80.0 if side == "L" else 74.0          # the asymmetry
        arm_rot = _rot((0.0, 0.0, 1.0), -down * s)    # +X/+Y frame; mirrors per side
        r.add(f"clavicle_{side}", "spine", (s * 0.04, 0.27, 0.0))
        r.add(f"upperarm_{side}", f"clavicle_{side}", (s * 0.14, 0.0, 0.0), arm_rot)
        r.add(f"lowerarm_{side}", f"upperarm_{side}", (s * 0.27, 0.0, 0.0), I)
        r.add(f"hand_{side}", f"lowerarm_{side}", (s * 0.09, 0.0, 0.0), I)
        r.add(f"thigh_{side}", "hips", (s * 0.09, -0.03, 0.0), _rot((0.0, 0.0, 1.0), -s * 8.0))
        r.add(f"calf_{side}", f"thigh_{side}", (s * 0.05, -0.42, 0.0), I)
        r.add(f"foot_{side}", f"calf_{side}", (s * 0.02, -0.40, 0.0), I)
        r.add(f"toe_{side}", f"foot_{side}", (s * 0.04, 0.0, 0.16), I)
    return r


def selftest():
    print("=== SELFTEST (pure math, no DCC) ===")
    rig = _build_bad_rig()
    print("\nbefore:")
    props = audit(rig)
    print("\n-- fixing --")
    fix(rig, "tpose", 45.0, {}, dry=False)
    print("\nafter:")
    props2 = audit(rig)

    # numeric assertions
    ok = True
    for name, want in [("upperarm_L", (1.0, 0.0, 0.0)), ("upperarm_R", (-1.0, 0.0, 0.0))]:
        side = name[-1]
        child = f"lowerarm_{side}"
        d = vnorm(vsub(rig.world_pos(child), rig.world_pos(name)))
        err = angle_between(d, want)
        print("   %s now points %s, %.2f deg off horizontal" % (name, fmt_m(d), err))
        ok &= err < 0.5
    for side, s in (("L", 1.0), ("R", -1.0)):
        d = vnorm(vsub(rig.world_pos(f"calf_{side}"), rig.world_pos(f"thigh_{side}")))
        err = angle_between(d, (0.0, -1.0, 0.0))
        print("   thigh_%s now %.2f deg off vertical" % (side, err))
        ok &= err < 0.5
        d = vnorm(vsub(rig.world_pos(f"toe_{side}"), rig.world_pos(f"foot_{side}")))
        yaw = math.degrees(math.atan2(d[0], d[2]))
        print("   foot_%s toe yaw %+.2f deg" % (side, yaw))
        ok &= abs(yaw) < 0.5
    print("\nSELFTEST %s" % ("PASSED" if ok and len(props2) == 0 else "FAILED"))
    return 0 if (ok and len(props2) == 0) else 1


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------


def main(argv):
    ap = argparse.ArgumentParser(description="Audit and repair a character rest pose.")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--audit", action="store_true", help="report only (default)")
    g.add_argument("--zero", action="store_true", help="zero pose rotations -> skeleton rest")
    g.add_argument("--tpose", action="store_true", help="aim into a T-pose")
    g.add_argument("--apose", type=float, metavar="DEG", help="aim into an A-pose, DEG below horizontal")
    ap.add_argument("--apply", action="store_true", help="write the changes")
    ap.add_argument("--bake-rest", action="store_true", help="save the result as the bind pose")
    ap.add_argument("--roll", nargs=2, action="append", metavar=("JOINT", "DEG"), default=[])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--backend", choices=["auto", "maya", "blender"], default="auto")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    rig = None
    if args.backend in ("auto", "maya"):
        try:
            rig = MayaRig()
            print("backend: Maya")
        except Exception as e:
            if args.backend == "maya":
                print("Maya backend unavailable: %s" % e)
                return 2
    if rig is None and args.backend in ("auto", "blender"):
        try:
            rig = BlenderRig()
            print("backend: Blender")
        except Exception as e:
            print("No DCC found (%s). Run inside Maya or Blender, or use --selftest." % e)
            return 2

    rolls = {}
    for j, d in args.roll:
        rolls[j] = float(d)

    if args.audit or not (args.zero or args.tpose or args.apose is not None):
        audit(rig)
        if not (args.zero or args.tpose or args.apose is not None):
            return 0
        print()

    if args.zero:
        fix(rig, "zero", 0.0, rolls, dry=not args.apply)
    elif args.tpose:
        fix(rig, "tpose", 0.0, rolls, dry=not args.apply)
    else:
        fix(rig, "apose", args.apose, rolls, dry=not args.apply)

    if args.apply and not args.zero:
        audit(rig)

    if args.bake_rest:
        if not args.apply:
            print("\n--bake-rest ignored without --apply (nothing was changed)")
        else:
            rig.bake_rest()
            print("bind pose saved")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
