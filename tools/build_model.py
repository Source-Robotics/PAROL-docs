#!/usr/bin/env python3
"""Build the 3D model the landing page's arm viewer shows, from PAROL6's URDF in robot_descriptions.

    python tools/build_model.py [--descriptions PATH]

Reads urdf/parol6_description/parol6_flange.urdf from a clone of Source-Robotics/robot_descriptions (--descriptions,
else $ROBOT_DESCRIPTIONS_DIR, else ../../projects/robot_descriptions), the same model the kinematics sheets come
from. Writes docs/assets/models/parol6/: one GLB per moving link in the link's own frame (all its visual meshes
merged, links on fixed joints such as the flange folded into their moving parent), decimated for the web, and
viewer.json: the kinematic chain of the movable joints (each joint's parent and child link, origin, axis and
limits), the colour swatches, the default joint angles and the camera. docs/javascripts/arm-viewer.js reads them
and moves the joints. Needs trimesh (with fast-simplification) and numpy.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "models" / "parol6"
URDF = Path("urdf") / "parol6_description" / "parol6_flange.urdf"
MAX_FACES = 20000          # per link: the model's meshes are far finer than a landing page needs
COLOURS = {"body": {"Grey": "#c9c9c6", "Black": "#1a1a1a", "White": "#f2f2f0", "Orange": "#f08a24"}}
MOVABLE = ("revolute", "continuous", "prismatic")


def find_descriptions(arg: str | None) -> Path:
    candidates = [arg, os.environ.get("ROBOT_DESCRIPTIONS_DIR"), ROOT.parent / "robot_descriptions",
                  ROOT.parent.parent / "projects" / "robot_descriptions"]
    for c in candidates:
        if c and (Path(c) / URDF).exists():
            return Path(c)
    sys.exit(f"build_model: no clone of robot_descriptions with {URDF} found; pass --descriptions PATH")


def floats(s: str | None, default="0 0 0") -> list[float]:
    return [float(v) for v in (s or default).split()]


def origin_matrix(el) -> np.ndarray:
    if el is None:
        return np.eye(4)
    xyz, rpy = floats(el.get("xyz")), floats(el.get("rpy"))
    m = trimesh.transformations.euler_matrix(rpy[0], rpy[1], rpy[2], "sxyz")
    m[:3, 3] = xyz
    return m


def material(hex_colour: str):
    rgb = [int(hex_colour[i:i + 2], 16) for i in (1, 3, 5)]
    return trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        baseColorFactor=rgb + [255], metallicFactor=0.0, roughnessFactor=0.65, doubleSided=True))


def compress(path: Path) -> str:
    """Meshopt compression with gltfpack (Node.js): the file shrinks to a fraction, the browser decodes it with
    three.js's MeshoptDecoder. Named nodes are kept (-kn). Without Node.js the file stays as trimesh wrote it,
    which the viewer reads as well."""
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
    urdf = find_descriptions(args.descriptions) / URDF
    robot = ET.parse(urdf).getroot()
    by_child = {j.find("child").get("link"): j for j in robot.findall("joint")}

    def carrier(link: str) -> tuple[str, np.ndarray]:
        """The moving link a link rides on, and the link's transform in that link's frame."""
        t = np.eye(4)
        while link in by_child and by_child[link].get("type") == "fixed" and by_child[link].find("parent").get("link") != "world":
            j = by_child[link]
            t = origin_matrix(j.find("origin")) @ t
            link = j.find("parent").get("link")
        return link, t

    parts: dict[str, list] = {}
    for link in robot.findall("link"):
        target, t_link = carrier(link.get("name"))
        for vis in link.findall("visual"):
            mesh_el = vis.find("geometry/mesh")
            if mesh_el is None:
                continue
            mesh = trimesh.load(urdf.parent / mesh_el.get("filename"), force="mesh")
            if mesh_el.get("scale"):
                mesh.apply_scale(floats(mesh_el.get("scale")))
            mesh.apply_transform(t_link @ origin_matrix(vis.find("origin")))
            parts.setdefault(target, []).append(mesh)

    links, sizes = [], {}
    if OUT.exists():
        for old in OUT.iterdir():
            old.unlink()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, meshes in parts.items():
        mesh = trimesh.util.concatenate(meshes)
        faces = len(mesh.faces)
        if faces > MAX_FACES:
            mesh = mesh.simplify_quadric_decimation(face_count=MAX_FACES)
        mesh.visual = material(COLOURS["body"]["Grey"])
        scene = trimesh.Scene()
        scene.add_geometry(mesh, node_name=name, geom_name=name)
        scene.export(OUT / f"{name}.glb")
        sizes[name] = (faces, len(mesh.faces), (OUT / f"{name}.glb").stat().st_size // 1024)
        links.append({"name": name, "file": f"{name}.glb"})

    joints, root = [], None
    for j in robot.findall("joint"):
        parent, child = j.find("parent").get("link"), j.find("child").get("link")
        if j.get("type") == "fixed" and parent == "world":
            root = child
            continue
        if j.get("type") not in MOVABLE:
            continue
        origin = j.find("origin")
        lim = j.find("limit")
        joints.append({
            "name": j.get("name"), "type": j.get("type"), "parent": parent, "child": child,
            "xyz": floats(origin.get("xyz") if origin is not None else None),
            "rpy": floats(origin.get("rpy") if origin is not None else None),
            "axis": floats(j.find("axis").get("xyz") if j.find("axis") is not None else None, "0 0 1"),
            "lower_deg": round(float(lim.get("lower", -3.1416)) * 180 / np.pi, 1) if lim is not None else -180.0,
            "upper_deg": round(float(lim.get("upper", 3.1416)) * 180 / np.pi, 1) if lim is not None else 180.0,
        })
    config = {
        "source": "robot_descriptions/" + URDF.as_posix(),
        "links": links, "joints": joints, "root": root or links[0]["name"], "up": "z",
        "colors": COLOURS, "default": {"body": COLOURS["body"]["Grey"], "q_deg": [0.0] * len(joints)},
        "camera": {"azimuth_deg": -40, "polar_deg": 65, "fill": 1.15},
    }
    packed = {f.name: compress(f) for f in sorted(OUT.glob("*.glb"))}
    sizes_after = {f.name: f.stat().st_size // 1024 for f in sorted(OUT.glob("*.glb"))}
    (OUT / "viewer.json").write_text(json.dumps(config, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: " + ", ".join(f"{k} {a}->{b} faces {kb} KB" for k, (a, b, kb) in sizes.items())
          + f"; {len(joints)} joints from {config['root']}")
    print("after compression: " + ", ".join(f"{k} {v} KB ({packed[k]})" for k, v in sizes_after.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
