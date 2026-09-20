# Android Assimp 3D Playground — Models

Public sample pack of **Earth**, **Moon**, **SciFi orb**, **ClockSample**, and a
**BusterDrone** reference entry (docs + shots only — glTF not redistributed)
for Assimp-based viewers and Android / Vulkan playgrounds.

Each local mesh model ships as **Wavefront OBJ + MTL** and **Discreet 3DS**, with
maps / textures where applicable, plus a short `INFO.txt`. BusterDrone is
**link-only** (CC BY-NC upstream).

## Layout

```
models/
  earth/          Earth globe — albedo, bump, normal, specular + shots/
  moon/           Moon globe — NASA SVS CGI Moon Kit maps + shots/
  scifi-orb/      Multi-material sci-fi orb (materials only) + shots/
  clock-sample/   POV clock scene + moon prop + shots/
  buster-drone/   INFO + shots only — glTF from Filament / Sketchfab (CC BY-NC)
tools/
  obj_to_3ds.py   Small OBJ→3DS helper used for Earth / Moon
```

| Model | OBJ / MTL | 3DS | Maps | Shots |
|-------|-----------|-----|------|-------|
| Earth | yes | yes | albedo, bump, normal, specular | [01](models/earth/shots/01.png) … [10](models/earth/shots/10.png) ([folder](models/earth/shots/)) |
| Moon | yes | yes | albedo, bump, normal, specular | [01](models/moon/shots/01.png) … [10](models/moon/shots/10.png) ([folder](models/moon/shots/)) |
| SciFi orb | yes | yes | none (Ka/Kd/Ks/Ke) | [01](models/scifi-orb/shots/01.png) … [10](models/scifi-orb/shots/10.png) ([folder](models/scifi-orb/shots/)) |
| ClockSample | yes | yes | checker, stripe, Moon_* | [01](models/clock-sample/shots/01.png) … [10](models/clock-sample/shots/10.png) ([folder](models/clock-sample/shots/)) |
| BusterDrone | **no** (link) | **no** | PBR MR upstream | [01](models/buster-drone/shots/01.png) … [10](models/buster-drone/shots/10.png) ([folder](models/buster-drone/shots/)) |

### Orbit stills (representative)

| Earth | Moon | SciFi orb | ClockSample | BusterDrone |
|-------|------|-----------|-------------|-------------|
| [![Earth](models/earth/shots/05.png)](models/earth/shots/) | [![Moon](models/moon/shots/05.png)](models/moon/shots/) | [![SciFi](models/scifi-orb/shots/05.png)](models/scifi-orb/shots/) | [![Clock](models/clock-sample/shots/02.png)](models/clock-sample/shots/) | [![Buster](models/buster-drone/shots/04.png)](models/buster-drone/shots/) |

Each model has **10** emulator screenshots (`shots/01.png`–`10.png`) from the
Vulkan SceneViewer (orbit auto-spin). How they were captured — and that this
pack grew out of an **AI-assisted** Android/Assimp lighting workflow — is under
[How the shots were made](#how-the-shots-were-made).
(Emulator MP4s were dropped: headless `screenrecord` was too janky to keep.)

## Quick start

1. Clone or download this repository.
2. Point your Assimp (or other) loader at e.g. `models/earth/Earth.obj` or
   `models/earth/Earth.3DS`.
3. Keep texture files **next to** the mesh (paths in MTL / 3DS are basenames).
4. Read `models/<name>/INFO.txt` for map meanings and usage tips.
5. **BusterDrone:** fetch `scene.gltf` from Filament (see
   `models/buster-drone/INFO.txt`) — not included here.

### Recommended load flags (Assimp-style)

- OBJ: enable diffuse + specular + specular-map + bump/height + normals.
- 3DS: same, but expect **generated** mesh normals (no NORMALS chunk); bump /
  height and specular maps are present for Earth, Moon, and ClockSample’s moon.
- glTF (BusterDrone): glTF importer + Draco (or decode first);
  `aiProcess_PreTransformVertices`; metallic-roughness shading (not Blinn-only).

## How the shots were made

These stills are **not** offline renders. They come from the same Vulkan
SceneViewer used while iterating Earth/Moon specular, sunglint, and normal maps
in an **AI-assisted coding session** (Cursor agent + human review on a headless
Android/NDK host). The goal was a quick, honest look at how the meshes light in
a real Assimp → Vulkan path — the kind of check that showed up repeatedly while
doing that AI-related lighting/asset work.

Short-lived emulator MP4s (`adb screenrecord` + orbit swipes) were recorded the
same way, but they stuttered badly on the headless AVD, so only PNG frames
remain in the repo.

### Pipeline (short)

1. Start AVD `medium_phone` **headless** (`emulator -avd medium_phone -no-audio -no-window`).
2. Install the debug APK of **PingPong2026Assimp** (debuggable so prefs can be
   written via `run-as`).
3. Launch `.SceneViewerActivity` once so `assets/bundled_models/` extract under
   the app’s `files/bundled_models/`.
4. For each model, force-stop the app, write SharedPreferences (`mesh_id=6` +
   `custom_obj_path` → `Earth.obj` / `Moon.obj` / `SciFiOrb.obj` /
   `ClockSample.obj` / `BusterDrone/scene.gltf`, material/map toggles on,
   `camera_engine=orbit`), then start the viewer again.
5. Wait for orbit auto-spin, then capture **10** frames over ~25 s via
   `adb exec-out screencap -p` / `android screen capture` (AVD ~1080×2400).
6. Store as `models/<name>/shots/01.png` … `10.png`.

Helper scripts for start/install/stop on this host live under the parent
workspace skill `emulator-adb-workflow` (not required to use the model files
themselves).

## Licensing

- **Original content** (meshes, authored maps, docs, packaging, screenshot
  PNGs as documentation): [CC0 1.0](LICENSE) — public domain dedication.
- **NASA imagery** (Moon kit, Earth Blue Marble lineage): public domain;
  please credit NASA / GSFC / SVS when practical.
- **three.js** Earth normal map and specular *base*: **MIT** — see
  [ATTRIBUTION.md](ATTRIBUTION.md).
- **BusterDrone** mesh/textures: **CC BY-NC** (not in this repo) — see
  `models/buster-drone/INFO.txt` and [ATTRIBUTION.md](ATTRIBUTION.md).

## Model notes (short)

**Earth** — Unit sphere with ocean sunglint / polar ice specular authored on
top of a MIT ocean mask; land stays near-matte. See `models/earth/INFO.txt`.

**Moon** — LROC albedo + LOLA-derived bump/normal (radius-matched strength) and
a soft PD-authored regolith specular. See `models/moon/INFO.txt`.

**SciFi orb** — Dense hard-surface orb; metals + emissive accents, no textures.

**ClockSample** — Checker ground, striped clock, moon using the same Moon maps
(copies included under `models/clock-sample/`).

**BusterDrone** — Filament / Sketchfab glTF (PBR, optional Draco). Docs + orbit
stills only here; download the assets from Google’s Filament tree. Animation
not shown in stills. See `models/buster-drone/INFO.txt`.

## Regenerating Earth / Moon `.3DS`

```bash
python3 tools/obj_to_3ds.py models/earth/Earth.obj -o models/earth/Earth.3DS
python3 tools/obj_to_3ds.py models/moon/Moon.obj   -o models/moon/Moon.3DS
```

(SciFi orb and ClockSample `.3DS` files are pre-built; SciFi exceeds a single
3DS mesh face limit and was exported with mesh splitting.)
