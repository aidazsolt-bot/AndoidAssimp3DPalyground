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

## BusterDrone (`models/buster-drone/`)

**Mesh and textures are not redistributed** in this repository (CC BY-NC,
large glTF + maps). This folder only has `INFO.txt` and orbit `shots/` from
PingPong2026Assimp’s metallic-roughness path.

| Item | Source | Terms |
|------|--------|--------|
| `scene.gltf` / `scene.bin` / `textures/` | [google/filament](https://github.com/google/filament) `third_party/models/BusterDrone` | **CC BY-NC** (Filament README: LaVADraGoN / Sketchfab; concept Evil Cloud — “Dune Express”) |
| Author page | Sketchfab — search “Buster Drone” / LaVADraGoN | Same CC BY-NC |
| `INFO.txt`, `shots/cheap|khronos/*.png` | Docs + emulator stills for this playground | CC0 documentation |

Upstream links:

- https://github.com/google/filament/tree/main/third_party/models/BusterDrone  
- Tag example: https://github.com/google/filament/tree/v1.77.0/third_party/models/BusterDrone  

**Non-commercial use only** for the model; attribute LaVADraGoN / Evil Cloud when
you redistribute those files yourself.

---

## Gaussian splat samples (`models/gs-*/`) — **links only**

Model bytes (PLY / GLB) are **not** shipped in this repository. Each folder has
`INFO.txt` with expected filenames and download URLs. `INFO.txt` and playground
stills are CC0 documentation.

Stills: `shots/cheap/*.png` = RenderAssimp **Cheap** Gaussian pipe (not reference);
`shots/khronos/*.png` = **Khronos** / KHR ellipse pipe (prefer for expected look).

### gs-garden-table

| Item | Source / URL | Terms |
|------|--------------|--------|
| `mipnerf360_garden_crop_table.ply` (fetch) | Open3D tutorial / `open3d_downloads` 3dgs-1 — https://www.open3d.org/docs/latest/tutorial/visualization/gaussian_splatting.html | Credit Open3D / capture authors when you redistribute the PLY yourself |

### gs-mesh-in-splats / gs-splats-in-mesh

| Item | Source / URL | Terms |
|------|--------------|--------|
| `MeshInSplats.glb`, `SplatsInMesh.glb` (fetch) | https://github.com/user-attachments/files/28266442/gltf-splat-examples-2025-05-26-animation.zip — issue [#2562](https://github.com/KhronosGroup/glTF/issues/2562) | Spec test assets upstream; our `INFO.txt` / stills: CC0 docs |

### gs-rose

| Item | Source / URL | Terms |
|------|--------------|--------|
| `Rose.ply` (fetch) | VVE / philippo24 bachelorarbeit `assets/gaussian-splatting/Rose.ply` | Engine tree **MIT**; attribute that project if you use the asset |

### gs-cactus

| Item | Source / URL | Terms |
|------|--------------|--------|
| cactus `.glb` / `.ply` (fetch) | https://javagl.de/splats/cactus_splat3_30kSteps_142k_splats-2026-04-09.zip — https://note.com/steam_studio/n/ne9736d94f162 | Upstream **CC0**; not mirrored here |

---

## Suggested credit line

> Earth / Moon textures include NASA public-domain imagery (Blue Marble /
> SVS CGI Moon Kit). Earth normal map and specular base from three.js (MIT).
> Meshes and authored materials: CC0 1.0.
> BusterDrone (if used): CC BY-NC — LaVADraGoN / Sketchfab via Filament
> `third_party/models/BusterDrone`; not shipped in this pack.
> Gaussian samples: link-only (Open3D garden, javagl KHR mesh+splat ZIP,
> CC0 cactus ZIP, Rose from VVE/philippo24) — see models/gs-*/INFO.txt.
