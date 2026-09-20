# Attribution & third-party sources

This repository packages ready-to-load 3D models for Assimp / Vulkan
playgrounds. Original meshes, MTL finishes, authored specular layers, docs,
and packaging are dedicated to the **public domain (CC0 1.0)** — see `LICENSE`.

NASA / U.S. government imagery used here is generally **public domain**.
Please credit the agencies and instruments as noted below (courtesy, not a
legal requirement for PD works).

---

## Earth (`models/earth/`)

| File | Source | Terms |
|------|--------|--------|
| `Earth_albedo.png` | Derived from [turban/webgl-earth](https://github.com/turban/webgl-earth) `2_no_clouds_4k.jpg` (NASA Blue Marble lineage) | NASA imagery: public domain |
| `Earth_bump.png` | Derived from NASA Earth Observatory Blue Marble topo/bathy (`world.topo.bathy.200412…`) — [Visible Earth](https://visibleearth.nasa.gov) | Public domain (NASA) |
| `Earth_normal.png` | [mrdoob/three.js](https://github.com/mrdoob/three.js) `examples/textures/planets/earth_normal_2048.jpg` | **MIT** |
| `Earth_specular.png` | Base ocean mask from three.js `earth_specular_2048.jpg` (**MIT**), then locally authored water / ice / land specular layers | MIT base + CC0 authored layers |
| `Earth.obj` / `Earth.mtl` / `Earth.3DS` | Mesh + material packaging for this repo | CC0 |

## Moon (`models/moon/`)

| File | Source | Terms |
|------|--------|--------|
| `Moon_albedo.png` | NASA SVS [CGI Moon Kit #4720](https://svs.gsfc.nasa.gov/4720) — `lroc_color_poles_4k.tif` (LROC WAC + LDAM poles) | Public domain (NASA / GSFC / SVS) |
| `Moon_bump.png`, `Moon_normal.png` | Height from SVS `ldem_16_uint.tif` (LOLA); normal map baked locally to lunar radius | Public domain source + CC0 bake |
| `Moon_specular.png` | Authored locally from PD albedo (soft regolith; no cool-water chroma) | CC0 |
| `Moon.obj` / `Moon.mtl` / `Moon.3DS` | Mesh + material packaging | CC0 |

SVS policy: https://svs.gsfc.nasa.gov/help/  
NASA media: https://www.nasa.gov/nasa-brand-center/images-and-media/

**Credit:** NASA / GSFC / Scientific Visualization Studio (LROC, LOLA).

## SciFi orb (`models/scifi-orb/`)

Original multi-material orb (no image maps). **CC0**.

## ClockSample (`models/clock-sample/`)

Clock / ground layout adapted from a POV-Ray clock sample; checker & stripe
maps and packaging authored here (**CC0**). Moon prop uses the same NASA SVS
maps as `models/moon/` (public domain) — copies are included so the folder is
self-contained.

---

## Suggested credit line

> Earth / Moon textures include NASA public-domain imagery (Blue Marble /
> SVS CGI Moon Kit). Earth normal map and specular base from three.js (MIT).
> Meshes and authored materials: CC0 1.0.
