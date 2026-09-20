#!/usr/bin/env python3
"""Minimal Wavefront OBJ → Discreet 3DS exporter (single/multi material).

Writes TEXMAP / BUMPMAP / SPECMAP (0xA204) when map_Kd / bump / map_Ks are set.
3DS limits: ≤65535 vertices and ≤65535 faces per mesh object.
"""
from __future__ import annotations

import argparse
import os
import struct
from dataclasses import dataclass, field


CHUNK_MAIN = 0x4D4D
CHUNK_OBJMESH = 0x3D3D
CHUNK_MASTER_SCALE = 0x0100
CHUNK_OBJBLOCK = 0x4000
CHUNK_TRIMESH = 0x4100
CHUNK_VERTLIST = 0x4110
CHUNK_FACELIST = 0x4120
CHUNK_FACEMAT = 0x4130
CHUNK_MAPLIST = 0x4140
CHUNK_TRMATRIX = 0x4160
CHUNK_MAT_MATERIAL = 0xAFFF
CHUNK_MAT_MATNAME = 0xA000
CHUNK_MAT_AMBIENT = 0xA010
CHUNK_MAT_DIFFUSE = 0xA020
CHUNK_MAT_SPECULAR = 0xA030
CHUNK_MAT_SHININESS = 0xA040
CHUNK_MAT_SHADING = 0xA100
CHUNK_MAT_TEXTURE = 0xA200
CHUNK_MAT_SPECMAP = 0xA204
CHUNK_MAT_BUMPMAP = 0xA230
CHUNK_MAPFILE = 0xA300
CHUNK_RGBF = 0x0010
CHUNK_PERCENTF = 0x0031
CHUNK_KEYFRAMER = 0xB000


@dataclass
class Material:
    name: str
    Ka: tuple[float, float, float] = (0.2, 0.2, 0.2)
    Kd: tuple[float, float, float] = (0.8, 0.8, 0.8)
    Ks: tuple[float, float, float] = (0.0, 0.0, 0.0)
    Ns: float = 10.0
    map_Kd: str | None = None
    map_Ks: str | None = None
    bump: str | None = None


@dataclass
class MeshPart:
    name: str
    mat_name: str
    positions: list[tuple[float, float, float]] = field(default_factory=list)
    uvs: list[tuple[float, float]] = field(default_factory=list)
    faces: list[tuple[int, int, int]] = field(default_factory=list)


class ChunkWriter:
    def __init__(self, buf: bytearray, chunk_type: int):
        self.buf = buf
        self.start = len(buf)
        buf += struct.pack("<HI", chunk_type, 0xDEADBEEF)

    def close(self) -> None:
        size = len(self.buf) - self.start
        struct.pack_into("<I", self.buf, self.start + 2, size)


def write_cstr(buf: bytearray, s: str) -> None:
    buf += s.encode("ascii", errors="replace") + b"\x00"


def write_rgb(buf: bytearray, parent_type: int, rgb: tuple[float, float, float]) -> None:
    c = ChunkWriter(buf, parent_type)
    inner = ChunkWriter(buf, CHUNK_RGBF)
    buf += struct.pack("<fff", *rgb)
    inner.close()
    c.close()


def write_percent(buf: bytearray, parent_type: int, value: float) -> None:
    c = ChunkWriter(buf, parent_type)
    inner = ChunkWriter(buf, CHUNK_PERCENTF)
    buf += struct.pack("<f", value)
    inner.close()
    c.close()


def write_texture(buf: bytearray, chunk_type: int, path: str) -> None:
    c = ChunkWriter(buf, chunk_type)
    pf = ChunkWriter(buf, CHUNK_PERCENTF)
    buf += struct.pack("<f", 1.0)
    pf.close()
    mf = ChunkWriter(buf, CHUNK_MAPFILE)
    write_cstr(buf, os.path.basename(path))
    mf.close()
    c.close()


def parse_mtl(path: str) -> dict[str, Material]:
    mats: dict[str, Material] = {}
    cur: Material | None = None
    if not os.path.isfile(path):
        return mats
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            key = parts[0]
            if key == "newmtl":
                cur = Material(name=parts[1])
                mats[cur.name] = cur
            elif cur is None:
                continue
            elif key == "Ka":
                cur.Ka = (float(parts[1]), float(parts[2]), float(parts[3]))
            elif key == "Kd":
                cur.Kd = (float(parts[1]), float(parts[2]), float(parts[3]))
            elif key == "Ks":
                cur.Ks = (float(parts[1]), float(parts[2]), float(parts[3]))
            elif key == "Ns":
                cur.Ns = float(parts[1])
            elif key == "map_Kd":
                cur.map_Kd = parts[1]
            elif key == "map_Ks":
                cur.map_Ks = parts[1]
            elif key in ("bump", "map_bump"):
                cur.bump = parts[1]
    return mats


def parse_obj(path: str) -> tuple[list[MeshPart], dict[str, Material]]:
    positions: list[tuple[float, float, float]] = []
    uvs: list[tuple[float, float]] = []
    materials: dict[str, Material] = {}
    cur_mat = "default"
    parts: dict[str, MeshPart] = {}
    vert_maps: dict[str, dict[tuple, int]] = {}

    def part_for(mat: str) -> MeshPart:
        if mat not in parts:
            # Object names in practice often stay short; keep readable prefix.
            parts[mat] = MeshPart(name=(mat[:10] or "Mesh"), mat_name=mat)
            vert_maps[mat] = {}
        return parts[mat]

    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            toks = line.split()
            key = toks[0]
            if key == "mtllib":
                mtl_path = os.path.join(os.path.dirname(path) or ".", toks[1])
                materials = parse_mtl(mtl_path)
            elif key == "usemtl":
                cur_mat = toks[1]
                if cur_mat not in materials:
                    materials[cur_mat] = Material(name=cur_mat)
            elif key == "v" and len(toks) >= 4:
                positions.append((float(toks[1]), float(toks[2]), float(toks[3])))
            elif key == "vt" and len(toks) >= 3:
                uvs.append((float(toks[1]), float(toks[2])))
            elif key == "f" and len(toks) >= 4:
                idxs: list[int] = []
                mp = part_for(cur_mat)
                vmap = vert_maps[cur_mat]
                for tok in toks[1:]:
                    bits = tok.split("/")
                    vi = int(bits[0]) - 1
                    ti = int(bits[1]) - 1 if len(bits) > 1 and bits[1] else -1
                    key_t = (vi, ti)
                    if key_t not in vmap:
                        vmap[key_t] = len(mp.positions)
                        mp.positions.append(positions[vi])
                        if 0 <= ti < len(uvs):
                            u, v = uvs[ti]
                            mp.uvs.append((u, 1.0 - v))
                        else:
                            mp.uvs.append((0.0, 0.0))
                    idxs.append(vmap[key_t])
                for i in range(1, len(idxs) - 1):
                    mp.faces.append((idxs[0], idxs[i], idxs[i + 1]))

    mesh_list = list(parts.values())
    for m in mesh_list:
        if len(m.positions) > 0xFFFF or len(m.faces) > 0xFFFF:
            raise SystemExit(
                f"Mesh '{m.name}' exceeds 3DS 16-bit limit "
                f"(v={len(m.positions)} f={len(m.faces)})"
            )
    return mesh_list, materials


def write_material(buf: bytearray, mat: Material) -> None:
    root = ChunkWriter(buf, CHUNK_MAT_MATERIAL)
    name_c = ChunkWriter(buf, CHUNK_MAT_MATNAME)
    write_cstr(buf, mat.name)
    name_c.close()
    write_rgb(buf, CHUNK_MAT_AMBIENT, mat.Ka)
    write_rgb(buf, CHUNK_MAT_DIFFUSE, mat.Kd)
    write_rgb(buf, CHUNK_MAT_SPECULAR, mat.Ks)
    write_percent(buf, CHUNK_MAT_SHININESS, min(1.0, max(0.0, mat.Ns / 1000.0)))
    sh = ChunkWriter(buf, CHUNK_MAT_SHADING)
    buf += struct.pack("<H", 3)  # phong
    sh.close()
    if mat.map_Kd:
        write_texture(buf, CHUNK_MAT_TEXTURE, mat.map_Kd)
    if mat.map_Ks:
        write_texture(buf, CHUNK_MAT_SPECMAP, mat.map_Ks)
    if mat.bump:
        write_texture(buf, CHUNK_MAT_BUMPMAP, mat.bump)
    root.close()


def write_mesh(buf: bytearray, mesh: MeshPart, mat: Material) -> None:
    obj = ChunkWriter(buf, CHUNK_OBJBLOCK)
    write_cstr(buf, mesh.name)
    tri = ChunkWriter(buf, CHUNK_TRIMESH)

    vl = ChunkWriter(buf, CHUNK_VERTLIST)
    buf += struct.pack("<H", len(mesh.positions))
    for x, y, z in mesh.positions:
        buf += struct.pack("<fff", x, y, z)
    vl.close()

    if mesh.uvs:
        ml = ChunkWriter(buf, CHUNK_MAPLIST)
        buf += struct.pack("<H", len(mesh.uvs))
        for u, v in mesh.uvs:
            buf += struct.pack("<ff", u, v)
        ml.close()

    fl = ChunkWriter(buf, CHUNK_FACELIST)
    buf += struct.pack("<H", len(mesh.faces))
    for a, b, c in mesh.faces:
        buf += struct.pack("<HHHH", a, b, c, 0)
    fm = ChunkWriter(buf, CHUNK_FACEMAT)
    write_cstr(buf, mat.name)
    buf += struct.pack("<H", len(mesh.faces))
    for i in range(len(mesh.faces)):
        buf += struct.pack("<H", i)
    fm.close()
    fl.close()

    tm = ChunkWriter(buf, CHUNK_TRMATRIX)
    for v in (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0):
        buf += struct.pack("<f", v)
    tm.close()

    tri.close()
    obj.close()


def export_3ds(obj_path: str, out_path: str) -> None:
    meshes, materials = parse_obj(obj_path)
    if not meshes:
        raise SystemExit("no meshes found")

    buf = bytearray()
    main = ChunkWriter(buf, CHUNK_MAIN)
    mesh_chunk = ChunkWriter(buf, CHUNK_OBJMESH)

    scale = ChunkWriter(buf, CHUNK_MASTER_SCALE)
    buf += struct.pack("<f", 1.0)
    scale.close()

    used = {m.mat_name for m in meshes}
    for name in used:
        write_material(buf, materials.get(name, Material(name=name)))

    for mesh in meshes:
        write_mesh(buf, mesh, materials.get(mesh.mat_name, Material(name=mesh.mat_name)))

    mesh_chunk.close()
    kf = ChunkWriter(buf, CHUNK_KEYFRAMER)
    kf.close()
    main.close()

    with open(out_path, "wb") as fh:
        fh.write(buf)
    print(f"Wrote {out_path} ({len(buf)} bytes, {len(meshes)} mesh(es))")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("obj")
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()
    export_3ds(args.obj, args.output)


if __name__ == "__main__":
    main()
