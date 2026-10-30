#!/usr/bin/env python3
"""Build the 3D model the landing page's arm viewer shows, from the robot repository's URDF.

    python tools/build_model.py [--repo PATH]

Writes docs/assets/models/parol6/: one GLB per link (base_link, L1 to L6) in the link's own frame, decimated for
the web, and viewer.json: the kinematic chain (each joint's parent and child link, origin, axis and limits), the
colour swatches, the default joint angles and the camera. docs/javascripts/arm-viewer.js reads them and moves
the joints. Needs trimesh (with fast-simplification) and numpy.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "models" / "parol6"
URDF = Path("PAROL6_URDF") / "parol6" / "urdf" / "parol6.urdf"
MESHES = Path("PAROL6_URDF") / "parol6" / "meshes"
MAX_FACES = 20000          # the URDF meshes have up to 60 000 faces each: too many for a landing page
COLOURS = {"body": {"Grey": "#c9c9c6", "Black": "#1a1a1a", "White": "#f2f2f0", "Orange": "#f08a24"}}


def find_repo(arg: str | None) -> Path:
    candidates = [arg, os.environ.get("PAROL6_DIR"), ROOT.parent / "PAROL6-Desktop-robot-arm",
                  ROOT.parent.parent / "projects" / "PAROL6-Desktop-robot-arm"]
    for c in candidates:
        if c and (Path(c) / URDF).exists():
            return Path(c)
    sys.exit(f"build_model: no clone of PAROL6-Desktop-robot-arm with {URDF} found; pass --repo PATH")


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


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", help="the clone of the robot repository")
    args = ap.parse_args(argv)
    repo = find_repo(args.repo)
    robot = ET.parse(repo / URDF).getroot()

    links, sizes = [], {}
    if OUT.exists():
        for old in OUT.iterdir():
            old.unlink()
    OUT.mkdir(parents=True, exist_ok=True)
    for link in robot.findall("link"):
        mesh_el = link.find("visual/geometry/mesh")
        if mesh_el is None:
            continue
        name = link.get("name")
        path = repo / MESHES / Path(mesh_el.get("filename")).name
        mesh = trimesh.load(path, force="mesh")
        faces = len(mesh.faces)
        if faces > MAX_FACES:
            mesh = mesh.simplify_quadric_decimation(face_count=MAX_FACES)
        mesh.apply_transform(origin_matrix(link.find("visual/origin")))
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
        "links": links, "joints": joints, "root": root or links[0]["name"], "up": "z",
        "colors": COLOURS, "default": {"body": COLOURS["body"]["Grey"], "q_deg": [0.0] * len(joints)},
        "camera": {"azimuth_deg": -40, "polar_deg": 65, "fill": 1.15},
    }
    (OUT / "viewer.json").write_text(json.dumps(config, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: " + ", ".join(f"{k} {a}->{b} faces {kb} KB" for k, (a, b, kb) in sizes.items())
          + f"; {len(joints)} joints from {config['root']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
