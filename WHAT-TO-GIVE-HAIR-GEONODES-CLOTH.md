# 🎯 HAIR GROOMING · GEOMETRY NODES · CLOTH — What to Give Me for Studio Level

> Answering: *"I want these at expert level too — what can I give you so you can
> build it at studio level?"*
> Verified 2026-10-22 · Blender 5.2 LTS baseline.

---

## 1. Why there's no book — and what "studio level" actually needs

These three have **no canonical textbook** (unlike lighting, animation, rigging).
I checked: the only area with real books is the **art/observation half of cloth**.
So expert level has to be assembled from **three layers**:

| Layer | What it is | Where it comes from |
|---|---|---|
| **L1 — Physics & model** | what the solver actually does, why settings behave as they do | Peer-reviewed papers + **Blender source code** |
| **L2 — Tool craft** | every parameter, node and click in Blender 5.2 | **Blender 5.2 LTS manual** + release notes + dev blog |
| **L3 — Production workflow** | the *order* a studio works in, QC gates, "this is how we knew it was right" | **Only you can supply this** 👈 |

**L1 and L2 I can build myself. L3 — the studio part — is what you must give me.**

---

## 2. ✅ WHAT I CAN PULL MYSELF (verified today — no upload needed)

**Blender 5.2 LTS Manual** (docs.blender.org — confirmed live, "latest" = 5.2):
* **Cloth** — `physics/cloth/` → Introduction (workflow, springs), Settings
  (Physical Properties, Cache, Shape, Collisions, Property Weights, Field
  Weights), Examples (sculpting with sim, smoothing, **cloth on armature**,
  animated vertex groups, dynamic paint, soft bodies, wind).
* **Hair Nodes** — `modeling/geometry_nodes/hair/`:
  *Deformation:* Blend, Displace, **Frizz**, **Noise**, Roll, Rotate, Shrinkwrap,
  Smooth, Straighten, Trim · *Generation:* Duplicate, **Generate**, Interpolate ·
  *Guides:* **Braid**, **Clump**, Create Guide Index Map, **Curl** · *Read:*
  Attachment Info, Curve Info/Root/Segment/Tip · *Utility:* **Attach Hair Curves
  to Surface**, Redistribute Curve Points, Restore Curve Segment Length ·
  *Write:* Set Hair Curve Profile.
* **Geometry Nodes** core node set + *Hair Curves* object type + Curves Sculpt brushes.

**Blender source code** (github.com/blender/blender, tag `blender-v5.2-release` —
verified reachable): `source/blender/blenkernel/intern/cloth.cc` exists, so I can
read the **actual defaults and math** (structural/shear/bending springs, damping,
solver steps) — the difference between "turn this up" and *knowing what it does*.

**Release notes + dev blog:** developer.blender.org 5.0/5.1/5.2 notes (already used
for v17–v19) and code.blender.org (e.g. *"The Future of Hair Grooming"*, Jul 2022)
for the developers' own design rationale.

**Peer-reviewed sources (verified URLs — free PDFs):**
* **Cloth:** Bridson, Fedkiw & Anderson, *Robust Treatment of Collisions, Contact
  and Friction for Cloth Animation*, SIGGRAPH 2002 — the collision/friction model
  modern solvers use.
* **Cloth:** Baraff & Witkin, *Large Steps in Cloth Simulation*, SIGGRAPH 1998 —
  implicit integration (why cloth doesn't explode at big timesteps).
* **Cloth:** Tsiknis & Bridson, *Better Cloth Through Bulletproof Time Integration
  and Physics-Aware Subdivision*, SCA 2006.
* **SIGGRAPH ’99 Course Notes, Physically Based Modeling** (incl. Kass/Baraff cloth).
* *Hair-sim papers will be verified before citing (discrete elastic rods /
  mass-spring hair) — nothing gets written into the skill from memory.*

---

## 3. 👉 WHAT YOU SHOULD GIVE ME (ranked by value)

### 🥇 A. Course material you already own — **the single biggest win**
These teach the *production order of operations* no manual contains. Any of:
Blender Studio training (studio.blender.org/training — e.g. the grooming sections
of their character courses), CGBoost *Master 3D Characters*, CG Cookie, Udemy
*Blender 5 Hair & Fur: Complete Workflow* (Artem Academy), FXPHD.

**Best form, worst to best:** video file → **PDF handouts/notes** → **screenshots
of the finished node trees** → pasted transcript/timestamps.
*(I can't watch video, so PDF/notes/screenshots are the usable forms.)*

### 🥇 B. A settings dump from a REAL file — the most precise thing you can give
Run this in Blender (Text editor → Run Script) on any file whose hair/cloth/geo-nodes
you like. It writes **every modifier, node, link and setting** to a JSON file:

```python
import bpy, json, os
def ser(v):
    if isinstance(v,(int,float,str,bool)) or v is None: return v
    if hasattr(v,'bl_rna'):
        return {p.identifier: ser(getattr(v,p.identifier)) for p in v.bl_rna.properties
                if not p.is_readonly and p.identifier not in ('rna_type','bl_rna')}
    if hasattr(v,'__len__'):
        try: return [ser(x) for x in v][:16]
        except Exception: return str(v)
    return str(v)
data={}
for ob in bpy.data.objects:
    o={'type':ob.type,'modifiers':[]}
    for m in ob.modifiers:
        d={'name':m.name,'type':m.type,'props':ser(m)}
        if m.type=='NODES' and m.node_group:
            d['node_group']=m.node_group.name
            d['nodes']=[{'name':n.name,'id':n.bl_idname,'props':ser(n)} for n in m.node_group.nodes]
            d['links']=[[l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name] for l in m.node_group.links]
        o['modifiers'].append(d)
    data[ob.name]=o
p=os.path.join(os.path.expanduser('~'),'Desktop','blender-dump.json')
open(p,'w').write(json.dumps(data,indent=1,default=str))
print('WROTE',p)
```

👉 Upload `blender-dump.json` (it's tiny) — I turn it into a verified
parameter table with real production values, then Blender-manual-verify each one.

### 🥈 C. Real-world reference for the ACTUAL hair & fabric
Photos — better, **short video clips** — of: braided hair moving (for Ava), and the
real fabric you're simulating (athletic/lycra, cotton, denim…). This is the
observation discipline the skill already uses for texturing (Demers, Gurney): you
cannot groom or drape convincingly what you haven't watched.

### 🥈 D. Your own .blend + renders for iteration
Upload to the GitHub release (your existing ingestion route). Keep **under 100 MB**
(disable bake caches / packed textures first). I diagnose your real file and the
fixes become tolerance rules in the skill.

### 🥉 E. Target look: 2–3 reference frames of the studio result you want
The skill's lookdev/gate system needs a target to measure against.

### 🥉 F. The one verified ART book for cloth
**Dynamic Wrinkles and Drapery — Burne Hogarth** (Watson-Guptill, 144 pp,
ISBN 9780823015870). Teaches the fold *logic*: direct-thrust wrinkles, bend
wrinkles, crossing wrinkles, compression wrinkles, fragmentation wrinkles,
kinetic forces. Sim gets you motion; **this gets you folds that read as fabric**.
*(I could not verify the often-recommended "Fabric Folding" by Timo Wuerz —
dropping it rather than inventing a source. For hair's art side I found no
verified book; real reference (C) covers it better.)*

---

## 4. ⚡ MINIMUM PATH

| You give | Result |
|---|---|
| **Nothing** | I build v20 from manual + source + papers → **technically correct**, complete parameter craft, NOT yet studio workflow |
| **B + C** | **Studio-usable** — verified real values + observation-based art |
| **A + B + C + D** | **Studio level** — expert workflow, QC gates, tolerances, Lessons Ledger |

---

## 5. 🔧 HOW IT LANDS IN THE SKILL

* **ref 31 — Hair Grooming** — curves object & scalp, density/length/clump/frizz/
  **braid** stack, guides→children, sculpt brushes, hair shaders, dynamics,
  Ava-specific braid recipe.
* **ref 32 — Geometry Nodes** — fields/attributes, procedural systems, reusable
  node groups, performance, the Blender 5.0 Geometry-Attribute-constraint bridge
  to rigs.
* **ref 33 — Cloth & Fabric** — solver model, springs/stiffness/damping,
  collision & pinning, **fold logic** per Hogarth, sim-on-armature workflow,
  baking, cache management.

Every entry follows the existing skill law:
**rule → Blender 5.2 click-path → exact parameter values → failure symptom → fix →
pass/fail tolerance**, wired into the gates/Lessons Ledger and routed through
**Tool Intelligence (ref 26)** so future tools are handled automatically.
