# Android Assimp 3D Playground — Models

Public sample pack of **Earth**, **Moon**, **SciFi orb**, and **ClockSample**
models for Assimp-based viewers and Android / OpenGL ES playgrounds.

Each model ships as **Wavefront OBJ + MTL** and **Discreet 3DS**, with maps /
textures where applicable, plus a short `INFO.txt`.

## Layout

```
models/
  earth/          Earth globe — albedo, bump, normal, specular
  moon/           Moon globe — NASA SVS CGI Moon Kit maps
  scifi-orb/      Multi-material sci-fi orb (materials only, no maps)
  clock-sample/   POV clock scene + moon prop (self-contained maps)
tools/
  obj_to_3ds.py   Small OBJ→3DS helper used for Earth / Moon
```

| Model | OBJ / MTL | 3DS | Maps |
|-------|-----------|-----|------|
| Earth | yes | yes | albedo, bump, normal, specular |
| Moon | yes | yes | albedo, bump, normal, specular |
| SciFi orb | yes | yes | none (Ka/Kd/Ks/Ke) |
| ClockSample | yes | yes | checker, stripe, Moon_* |

## Quick start

1. Clone or download this repository.
2. Point your Assimp (or other) loader at e.g. `models/earth/Earth.obj` or
   `models/earth/Earth.3DS`.
3. Keep texture files **next to** the mesh (paths in MTL / 3DS are basenames).
4. Read `models/<name>/INFO.txt` for map meanings and usage tips.

### Recommended load flags (Assimp-style)

- OBJ: enable diffuse + specular + specular-map + bump/height + normals.
- 3DS: same, but expect **generated** mesh normals (no NORMALS chunk); bump /
  height and specular maps are present for Earth, Moon, and ClockSample’s moon.

## Licensing

- **Original content** (meshes, authored maps, docs, packaging):
  [CC0 1.0](LICENSE) — public domain dedication.
- **NASA imagery** (Moon kit, Earth Blue Marble lineage): public domain;
  please credit NASA / GSFC / SVS when practical.
- **three.js** Earth normal map and specular *base*: **MIT** — see
  [ATTRIBUTION.md](ATTRIBUTION.md).

## Model notes (short)

**Earth** — Unit sphere with ocean sunglint / polar ice specular authored on
top of a MIT ocean mask; land stays near-matte. See `models/earth/INFO.txt`.

**Moon** — LROC albedo + LOLA-derived bump/normal (radius-matched strength) and
a soft PD-authored regolith specular. See `models/moon/INFO.txt`.

**SciFi orb** — Dense hard-surface orb; metals + emissive accents, no textures.

**ClockSample** — Checker ground, striped clock, moon using the same Moon maps
(copies included under `models/clock-sample/`).

## Regenerating Earth / Moon `.3DS`

```bash
python3 tools/obj_to_3ds.py models/earth/Earth.obj -o models/earth/Earth.3DS
python3 tools/obj_to_3ds.py models/moon/Moon.obj   -o models/moon/Moon.3DS
```

(SciFi orb and ClockSample `.3DS` files are pre-built; SciFi exceeds a single
3DS mesh face limit and was exported with mesh splitting.)
