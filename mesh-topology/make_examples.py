#!/usr/bin/env python3
"""
make_examples.py — build the demo meshes the topology checker is tested against.

    python3 make_examples.py          # writes examples/*.obj and examples/*.json

The arm is deliberately the simplest possible deforming shape: a tapered tube
with a shoulder, an elbow and a wrist. Two versions differ only in edge-loop
density, which is exactly the variable that decides whether an elbow bends or
pinches.
"""

import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "examples")


def arm_mesh(rings, segs=16, length=1.40):
    """Tapered arm tube along +Z: shoulder at z=0, elbow at z=0.72, wrist at 1.4."""
    V = []
    for k in range(rings):
        t = k / (rings - 1)
        z = t * length
        # radius profile: deltoid -> elbow -> forearm -> wrist
        if t < 0.45:
            r = 0.078 - 0.018 * (t / 0.45)
        elif t < 0.55:
            r = 0.060 + 0.002 * math.sin((t - 0.45) / 0.10 * math.pi)
        else:
            r = 0.058 - 0.024 * ((t - 0.55) / 0.45)
        for i in range(segs):
            a = 2 * math.pi * i / segs
            V.append((r * math.cos(a), r * math.sin(a), z))

    F = []
    for k in range(rings - 1):
        for i in range(segs):
            a = k * segs + i
            b = k * segs + (i + 1) % segs
            c = (k + 1) * segs + (i + 1) % segs
            d = (k + 1) * segs + i
            F.append((a, b, c, d))
    return np.array(V, dtype=float), F


def write_obj(path, V, F, name="mesh"):
    with open(path, "w") as fh:
        fh.write("# %s\n" % name)
        for v in V:
            fh.write("v %.6f %.6f %.6f\n" % (v[0], v[1], v[2]))
        for f in F:
            fh.write("f %s\n" % " ".join(str(i + 1) for i in f))


JOINTS = {
    "joints": [
        {"name": "shoulder", "center": [0.0, 0.0, 0.02], "radius": 0.13},
        {"name": "elbow", "center": [0.0, 0.0, 0.72], "radius": 0.13},
        {"name": "wrist", "center": [0.0, 0.0, 1.36], "radius": 0.10},
    ]
}


def main():
    os.makedirs(OUT, exist_ok=True)

    # 1. dense loops across every joint -> the elbow has ~12 loops
    V, F = arm_mesh(rings=40)
    write_obj(os.path.join(OUT, "arm_good.obj"), V, F, "arm, 40 rings")
    # 2. too few loops -> a single loop across the elbow: candy wrapper
    V, F = arm_mesh(rings=9)
    write_obj(os.path.join(OUT, "arm_coarse.obj"), V, F, "arm, 9 rings")
    # 3. same as good, but capped with n-gons (a classic beginner mistake)
    V, F = arm_mesh(rings=40)
    F.append(tuple(range(16)))                                     # bottom n-gon
    F.append(tuple(range(len(V) - 16, len(V)))[::-1])              # top n-gon
    write_obj(os.path.join(OUT, "arm_ngon_caps.obj"), V, F, "arm with n-gon caps")
    # 4. triangulated export of the good arm, for the tri lens
    V, F = arm_mesh(rings=40)
    T = []
    for f in F:
        T.append((f[0], f[1], f[2]))
        T.append((f[0], f[2], f[3]))
    write_obj(os.path.join(OUT, "arm_triangulated.obj"), V, T, "arm, triangulated")

    with open(os.path.join(OUT, "joints_arm.json"), "w") as fh:
        json.dump(JOINTS, fh, indent=2)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
