#!/usr/bin/env python3
"""Build the 3D model of the arm viewer (landing and kinematics pages) from PAROL6's URDFs in robot_descriptions.

    python tools/build_model.py [--descriptions PATH]

Reads urdf/parol6_description/ in a clone of Source-Robotics/robot_descriptions (--descriptions, else
$ROBOT_DESCRIPTIONS_DIR, else ../../projects/robot_descriptions), the models the kinematics sheets come from: the
arm from parol6_flange.urdf and the tool of each variant in TOOLS. It first checks that the arm (every link up to
wrist_2_link and the six movable joints) is the same in all the variants. Writes docs/assets/models/parol6/:

- one GLB per moving link of the arm, in the link's own frame (links on fixed joints folded into their moving
  parent);
- tool_<id>.glb per tool: everything wrist_3_link carries (flange, gripper body, the fingers at FINGER_M, the
  review sheets' "jaws open"), in wrist_3_link's frame;
- viewer.json: the arm links, the kinematic chain of the movable joints (each joint's parent and child link,
  origin, axis and limits), the tools (id, label, file) and the default one, the colour swatches, the default
  joint angles and the camera.

Inside a GLB the visuals are merged per material. The printed parts, the URDF's structure colour (parol6_structure,
STRUCTURE_RGBA), become one node <part>__body, which the viewer recolours; every other material (motors, jaws,
camera lens, the aluminium pneumatic body) one node <part>__<material> in the model's own colour. Each GLB is
decimated for the web as one mesh (MAX_FACES) and meshopt-compressed with gltfpack (Node.js) when it is there. docs/javascripts/arm-viewer.js reads them. Needs trimesh (with fast-simplification) and numpy.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "models" / "parol6"
URDF_DIR = Path("urdf") / "parol6_description"
ARM_URDF = "parol6_flange.urdf"   # the arm is built from this one; every variant must carry the same arm
TOOL_LINK = "wrist_3_link"        # everything this link carries is the tool
TOOLS = [                         # id (robot_descriptions' profile name), label, URDF
    ("flange", "Flange only", "parol6_flange.urdf"),
    ("pneumatic", "Pneumatic gripper", "parol6_pneumatic.urdf"),
    ("ssg48", "SSG-48", "parol6_ssg48.urdf"),
    ("ssg48_stock", "SSG-48 fin-ray", "parol6_ssg48_stock.urdf"),
    ("msg", "MSG", "parol6_msg.urdf"),
    ("msg_tpu_glue", "MSG soft jaws", "parol6_msg_tpu_glue.urdf"),
]
DEFAULT_TOOL = "pneumatic"        # PAROL6's standard tool in these docs
FINGER_M = 0.0                    # every finger joint at this displacement: 0 is "jaws open" in all six variants
STRUCTURE_RGBA = (0.79216, 0.81961, 0.93333, 1.0)   # parol6_structure: the printed parts, recoloured by the reader
BODY = "body"                     # their node: <part>__body
MAX_FACES = 20000                 # per GLB: the model's meshes are far finer than a web page needs
COLOURS = {"body": {"Grey": "#c9c9c6", "Black": "#1a1a1a", "White": "#f2f2f0", "Orange": "#f08a24"}}
MOVABLE = ("revolute", "continuous", "prismatic")
TOL_M, TOL_RAD = 1e-4, 1e-4       # the variants round the arm's joint origins differently (0.0234207 and 0.023421)


def find_descriptions(arg: str | None) -> Path:
    candidates = [arg, os.environ.get("ROBOT_DESCRIPTIONS_DIR"), ROOT.parent / "robot_descriptions",
                  ROOT.parent.parent / "projects" / "robot_descriptions"]
    for c in candidates:
        if c and (Path(c) / URDF_DIR / ARM_URDF).exists():
            return Path(c)
    sys.exit(f"build_model: no clone of robot_descriptions with {URDF_DIR / ARM_URDF} found; pass --descriptions PATH")


def floats(s: str | None, default="0 0 0") -> list[float]:
    return [float(v) for v in (s or default).split()]


def origin_matrix(el) -> np.ndarray:
    if el is None:
        return np.eye(4)
    xyz, rpy = floats(el.get("xyz")), floats(el.get("rpy"))
    m = trimesh.transformations.euler_matrix(rpy[0], rpy[1], rpy[2], "sxyz")
    m[:3, 3] = xyz
    return m


def to_linear(c: float) -> float:
    """sRGB to linear: glTF colours are linear, the URDF's (like the swatches) are the colours as seen."""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_rgba(hex_colour: str) -> tuple:
    return tuple(int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)) + (1.0,)


def material(name: str, rgba) -> trimesh.visual.TextureVisuals:
    return trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        name=name, baseColorFactor=[to_linear(c) for c in rgba[:3]] + [rgba[3]],
        metallicFactor=0.0, roughnessFactor=0.65, doubleSided=True))


class Model:
    """One URDF: its links, joints and materials, and where each link sits in the viewer."""

    def __init__(self, path: Path):
        self.path = path
        robot = ET.parse(path).getroot()
        self.links = {l.get("name"): l for l in robot.findall("link")}
        self.joints = {j.get("name"): j for j in robot.findall("joint")}
        self.by_child = {j.find("child").get("link"): j for j in self.joints.values()}
        self.colours = {m.get("name"): tuple(floats(m.find("color").get("rgba")))
                        for m in robot.iter("material") if m.find("color") is not None and m.get("name")}

    def under(self, link: str, ancestor: str) -> bool:
        """Whether the link is the ancestor or rides on it."""
        while True:
            if link == ancestor:
                return True
            if link not in self.by_child:
                return False
            link = self.by_child[link].find("parent").get("link")

    def q(self, joint) -> float:
        """The value a tool's joint is baked at: FINGER_M for a prismatic joint, 0 for any other, a mimic joint
        follows its master; it has to lie within the joint's limits."""
        mimic = joint.find("mimic")
        if mimic is not None:
            value = (float(mimic.get("multiplier", 1)) * self.q(self.joints[mimic.get("joint")])
                     + float(mimic.get("offset", 0)))
        else:
            value = FINGER_M if joint.get("type") == "prismatic" else 0.0
        lim = joint.find("limit")
        if joint.get("type") != "continuous" and lim is not None and not (
                float(lim.get("lower", 0)) - 1e-12 <= value <= float(lim.get("upper", 0)) + 1e-12):
            sys.exit(f"build_model: {self.path.name}: {joint.get('name')} = {value} is outside its limits")
        return value

    def motion(self, joint) -> np.ndarray:
        if joint.get("type") not in MOVABLE:
            return np.eye(4)
        axis = np.array(floats(joint.find("axis").get("xyz") if joint.find("axis") is not None else None, "1 0 0"))
        axis = axis / np.linalg.norm(axis)
        if joint.get("type") == "prismatic":
            return trimesh.transformations.translation_matrix(axis * self.q(joint))
        return trimesh.transformations.rotation_matrix(self.q(joint), axis)

    def carrier(self, link: str) -> tuple[str, np.ndarray]:
        """The link the viewer moves this one with, and this link's transform in that link's frame. An arm link
        rides on its moving parent through fixed joints; a link of the tool on TOOL_LINK, through every joint at
        its baked value."""
        t, in_tool = np.eye(4), self.under(link, TOOL_LINK)
        while link in self.by_child and link != TOOL_LINK:
            j = self.by_child[link]
            parent = j.find("parent").get("link")
            if not in_tool and (j.get("type") != "fixed" or parent == "world"):
                break
            t = origin_matrix(j.find("origin")) @ self.motion(j) @ t
            link = parent
        return link, t

    def visuals(self, link: str) -> list[tuple]:
        """(mesh file, scale, origin, material name, rgba) of each mesh visual of the link."""
        out = []
        for vis in self.links[link].findall("visual"):
            mesh = vis.find("geometry/mesh")
            if mesh is None:
                continue
            m = vis.find("material")
            name = (m.get("name") or "") if m is not None else ""
            c = m.find("color") if m is not None else None
            rgba = tuple(floats(c.get("rgba"))) if c is not None else self.colours.get(name)
            if rgba is None:
                sys.exit(f"build_model: {self.path.name}: a visual of {link} has no colour")
            out.append((mesh.get("filename"), floats(mesh.get("scale"), "1 1 1"), origin_matrix(vis.find("origin")),
                        name, rgba))
        return out

    def arm_links(self) -> list[str]:
        return [l for l in self.links if not self.under(l, TOOL_LINK)]

    def arm_joints(self) -> list:
        return [j for j in self.joints.values()
                if j.get("type") in MOVABLE and not self.under(j.find("parent").get("link"), TOOL_LINK)]


def check_arm(arm: Model, other: Model) -> float:
    """Exit unless the other variant has the same arm (links, visuals, movable joints); return the largest
    difference in the joint origins."""
    where = f"build_model: {other.path.name} and {arm.path.name} differ:"
    if sorted(arm.arm_links()) != sorted(other.arm_links()):
        sys.exit(f"{where} arm links {sorted(set(arm.arm_links()) ^ set(other.arm_links()))}")
    for link in arm.arm_links():
        a, b = arm.visuals(link), other.visuals(link)
        if len(a) != len(b) or any(x[0] != y[0] or not np.allclose(x[1], y[1]) or not np.allclose(x[2], y[2], atol=TOL_M)
                                   or not np.allclose(x[4], y[4], atol=1e-3) for x, y in zip(a, b)):
            sys.exit(f"{where} the visuals of {link}")
    worst = 0.0
    theirs = {j.get("name"): j for j in other.arm_joints()}
    for j in arm.arm_joints():
        k = theirs.pop(j.get("name"), None)
        if k is None:
            sys.exit(f"{where} {j.get('name')} is missing")
        same = [j.get("type") == k.get("type"),
                j.find("parent").get("link") == k.find("parent").get("link"),
                j.find("child").get("link") == k.find("child").get("link"),
                np.allclose(floats(j.find("axis").get("xyz")), floats(k.find("axis").get("xyz"))),
                np.allclose([float(j.find("limit").get(x)) for x in ("lower", "upper")],
                            [float(k.find("limit").get(x)) for x in ("lower", "upper")])]
        dx = np.abs(np.subtract(floats(j.find("origin").get("xyz")), floats(k.find("origin").get("xyz")))).max()
        dr = np.abs(np.subtract(floats(j.find("origin").get("rpy")), floats(k.find("origin").get("rpy")))).max()
        if not all(same) or dx > TOL_M or dr > TOL_RAD:
            sys.exit(f"{where} {j.get('name')}")
        worst = max(worst, dx, dr)
    if theirs:
        sys.exit(f"{where} extra arm joints {sorted(theirs)}")
    return worst


def group_name(names: list[str], rgba) -> str:
    """A material's node name: its URDF name, the common part of several (j1_actuator_black and
    j2_actuator_black: actuator_black), else its colour."""
    names = sorted(set(names))
    common = os.path.commonprefix([n[::-1] for n in names])[::-1].strip("_") if all(names) else ""
    name = names[0] if len(names) == 1 and names[0] else common
    return re.sub(r"[^A-Za-z0-9_]+", "_", name) or "rgba_" + "".join(f"{round(c * 255):02x}" for c in rgba[:3])


def collect(model: Model, links: list[str], loaded: dict) -> dict[str, dict]:
    """The meshes of the given links, placed in their carrier's frame and grouped per carrier and material:
    {carrier: {group name: (rgba, [meshes])}}, the printed parts first, as BODY."""
    raw: dict[str, dict] = {}
    for link in links:
        target, t_link = model.carrier(link)
        for filename, scale, origin, name, rgba in model.visuals(link):
            path = model.path.parent / filename
            if path not in loaded:
                loaded[path] = trimesh.load(path, force="mesh")
            mesh = loaded[path].copy()
            mesh.apply_scale(scale)
            mesh.apply_transform(t_link @ origin)
            body = np.allclose(rgba, STRUCTURE_RGBA, atol=2e-3)
            key = BODY if body else tuple(round(c, 3) for c in rgba)
            g = raw.setdefault(target, {}).setdefault(key, {"names": [], "rgba": rgba, "meshes": []})
            g["names"].append(name)
            g["meshes"].append(mesh)
    parts = {}
    for target, groups in raw.items():
        ordered = sorted(groups.items(), key=lambda kv: kv[0] != BODY)
        parts[target] = {(BODY if key == BODY else group_name(g["names"], g["rgba"])): (g["rgba"], g["meshes"])
                         for key, g in ordered}
    return parts


def decimate(parts: list[trimesh.Trimesh]) -> list[trimesh.Trimesh]:
    """Decimate a GLB's materials together to MAX_FACES, as one mesh, so that the faces go where the shape needs
    them (not to the many small details of a motor), and split the result by material again. Replaying the
    collapses fast-simplification reports maps every vertex of the merged mesh to one of the result (a collapse
    never joins two separate meshes); the replay's faces are the same, but it places a few merged vertices
    elsewhere (up to metres away on the MSG soft jaws), so the points come from the simplification itself."""
    if sum(len(p.faces) for p in parts) <= MAX_FACES:
        return parts
    import fast_simplification
    whole = trimesh.util.concatenate(parts)
    vertices, faces = whole.vertices.view(np.ndarray), whole.faces.view(np.ndarray)
    label = np.repeat(np.arange(len(parts)), [len(p.vertices) for p in parts])
    points, kept, collapses = fast_simplification.simplify(vertices, faces, target_count=MAX_FACES,
                                                           return_collapses=True)
    _, replayed, mapping = fast_simplification.replay_simplification(vertices, faces, collapses)
    point_label = np.full(len(points), -1)
    point_label[mapping] = label
    if not np.array_equal(kept, replayed) or np.any(point_label[mapping] != label):
        sys.exit("build_model: cannot tell the materials apart after the decimation")
    face_label = point_label[kept[:, 0]]
    out = []
    for i, part in enumerate(parts):
        m = trimesh.Trimesh(points, kept[face_label == i], process=False)
        m.remove_unreferenced_vertices()
        if len(m.vertices) and (np.any(m.bounds[0] < part.bounds[0] - 0.005) or np.any(m.bounds[1] > part.bounds[1] + 0.005)):
            sys.exit("build_model: the decimation moved vertices out of the part")
        out.append(m)
    return out


def write_glb(path: Path, part: str, groups: dict) -> tuple[int, int, list[str]]:
    """One node <part>__<group> per material, decimated; returns the faces before and after and the node names."""
    merged = [trimesh.util.concatenate(meshes) for _, meshes in groups.values()]
    scene, nodes = trimesh.Scene(), []
    for (name, (rgba, _)), mesh in zip(groups.items(), decimate(merged)):
        if not len(mesh.faces):
            continue
        node = f"{part}__{name}"
        mesh.visual = material(node, hex_rgba(COLOURS["body"]["Grey"]) if name == BODY else rgba)
        scene.add_geometry(mesh, node_name=node, geom_name=node)
        nodes.append(node)
    scene.export(path)
    return sum(len(m.faces) for m in merged), sum(len(g.faces) for g in scene.geometry.values()), nodes


def compress(path: Path) -> str:
    """Meshopt compression with gltfpack (Node.js): the file shrinks to a fraction, the browser decodes it with
    three.js's MeshoptDecoder. Named nodes are kept (-kn), so the viewer still finds the __body nodes. Without
    Node.js the file stays as trimesh wrote it, which the viewer reads as well."""
    exe = os.environ.get("GLTFPACK") or shutil.which("gltfpack")
    npx = shutil.which("npx")
    cmd = [exe] if exe else ([npx, "--yes", "gltfpack@1.3.0"] if npx else None)
    if not cmd:
        print(f"note: no gltfpack (Node.js); {path.name} left uncompressed")
        return "uncompressed"
    packed = path.with_name(path.stem + ".packed.glb")
    subprocess.run(cmd + ["-i", str(path), "-o", str(packed), "-cc", "-kn"], check=True, capture_output=True)
    packed.replace(path)
    return "meshopt"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--descriptions", help="the clone of Source-Robotics/robot_descriptions")
    args = ap.parse_args(argv)
    folder = find_descriptions(args.descriptions) / URDF_DIR
    arm = Model(folder / ARM_URDF)
    variants = {tid: Model(folder / urdf) for tid, _, urdf in TOOLS}
    worst = max(check_arm(arm, m) for m in variants.values())

    if OUT.exists():
        for old in OUT.iterdir():
            old.unlink()
    OUT.mkdir(parents=True, exist_ok=True)
    loaded: dict = {}
    links, report = [], []
    for name, groups in collect(arm, arm.arm_links(), loaded).items():
        before, after, nodes = write_glb(OUT / f"{name}.glb", name, groups)
        links.append({"name": name, "file": f"{name}.glb"})
        report.append(f"{name} {before}->{after} faces [{', '.join(n.split('__')[1] for n in nodes)}]")
    tools = []
    for tid, label, urdf in TOOLS:
        m = variants[tid]
        parts = collect(m, [l for l in m.links if m.under(l, TOOL_LINK)], loaded)
        if list(parts) != [TOOL_LINK]:
            sys.exit(f"build_model: {urdf}: the tool's meshes do not all ride on {TOOL_LINK}: {list(parts)}")
        before, after, nodes = write_glb(OUT / f"tool_{tid}.glb", f"tool_{tid}", parts[TOOL_LINK])
        tools.append({"id": tid, "label": label, "file": f"tool_{tid}.glb", "source": urdf})
        report.append(f"tool_{tid} {before}->{after} faces [{', '.join(n.split('__')[1] for n in nodes)}]")

    joints, root = [], None
    for j in arm.joints.values():
        if j.get("type") == "fixed" and j.find("parent").get("link") == "world":
            root = j.find("child").get("link")
    for j in arm.arm_joints():
        origin, lim = j.find("origin"), j.find("limit")
        joints.append({
            "name": j.get("name"), "type": j.get("type"),
            "parent": j.find("parent").get("link"), "child": j.find("child").get("link"),
            "xyz": floats(origin.get("xyz") if origin is not None else None),
            "rpy": floats(origin.get("rpy") if origin is not None else None),
            "axis": floats(j.find("axis").get("xyz") if j.find("axis") is not None else None, "1 0 0"),
            "lower_deg": round(float(lim.get("lower", -3.1416)) * 180 / np.pi, 1) if lim is not None else -180.0,
            "upper_deg": round(float(lim.get("upper", 3.1416)) * 180 / np.pi, 1) if lim is not None else 180.0,
        })
    package = folder / "package.xml"
    version = re.search(r"<version>([^<]+)</version>", package.read_text(encoding="utf-8")) if package.exists() else None
    config = {
        "source": "robot_descriptions/" + (URDF_DIR / ARM_URDF).as_posix(),
        "version": version.group(1) if version else None,
        "links": links, "joints": joints, "root": root or links[0]["name"], "up": "z",
        "tool_link": TOOL_LINK, "tools": tools, "finger_m": FINGER_M, "body_suffix": "__" + BODY,
        "colors": COLOURS,
        "default": {"body": COLOURS["body"]["Grey"], "tool": DEFAULT_TOOL, "q_deg": [0.0] * len(joints)},
        "camera": {"azimuth_deg": -40, "polar_deg": 65, "fill": 1.15},
    }
    raw = {f.name: f.stat().st_size for f in sorted(OUT.glob("*.glb"))}
    packed = {f.name: compress(f) for f in sorted(OUT.glob("*.glb"))}
    (OUT / "viewer.json").write_text(json.dumps(config, indent=1) + "\n", encoding="utf-8")
    print(f"the arm is the same in all {len(variants)} variants (joint origins within {worst:.1e})")
    print(f"wrote {OUT.relative_to(ROOT)}: " + "; ".join(report) + f"; {len(joints)} joints from {config['root']}")
    sizes = {f.name: f.stat().st_size for f in sorted(OUT.glob("*.glb"))}
    print("files: " + ", ".join(f"{k} {raw[k] // 1024}->{v // 1024} KB ({packed[k]})" for k, v in sizes.items()))
    arm_kb = sum(v for k, v in sizes.items() if not k.startswith("tool_")) / 1024
    print(f"arm {arm_kb:.0f} KB, with the default tool {arm_kb + sizes[f'tool_{DEFAULT_TOOL}.glb'] / 1024:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
