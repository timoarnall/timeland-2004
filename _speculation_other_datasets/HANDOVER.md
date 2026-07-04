# Speculative pass — handover

Session started 2026-05-11, wrapped 2026-05-14 as a WIP commit (`27b5205 Save work in progress 2026-05-14`). Since then, four overnight branches have added speculative followup work that is **not yet on `experiment/2026-update`**. See "Unmerged overnight followups" below.

## The premise

Timo asked whether the Timeland renderer could be applied to other photo/GPS sources — a "visualisation tool" reading. The pass here says yes: the renderer is portable; the data adapter is the only thing that changes per-source; the visual language survives the transplant.

## What's in this folder (state as of the 2026-05-14 WIP commit)

- `CANDIDATES.md` — planning report, ranked candidates.
- `FINDINGS.md` — what the pass learned. Slightly out of date (see below).
- `build_dataset.py` — generic builder. JSON config in → thumbs + manifest out.
- `lookup_elevation.py` — post-hoc elevation from Norwegian Kartverket DTM1 (Norway only).
- `render.html` — fork of `experiment-2026/index.html`. Same physics; reads `<dataset>/manifest.js` via `<script>` tag (see "Chrome/Safari" below).
- Dataset folders (see next section).
- `bkk-burma-2012/manifest.js` and `summer-2010/manifest.js` — **redirect stubs** for legacy URLs. They send the tab to the strongest segment (`__seg2` / `__seg1`) preserving other query params.
- `_screenshots/` — headless captures per dataset at multiple `?seek=` values.

## Datasets on disk

| Dataset name (`?dataset=`) | Trkpts | Photos | Thumbs | Notes |
|---|---|---|---|---|
| `bkk-burma-2012__seg1` | 639 | 122 | 15 MB | Bangkok Apr 18-20 (pre-Yangon flight) |
| `bkk-burma-2012__seg2` | 735 | **290** | 42 MB | Yangon Apr 21 (strongest — dense photos) |
| `bkk-burma-2012__seg3` | 650 | 233 | 38 MB | Bagan/central Burma Apr 22-23 |
| `bkk-burma-2012__seg4` | 241 | 140 | 17 MB | Mandalay Apr 24-26 |
| `summer-2010__seg1` | 1,084 | **548** | 58 MB | Norway Jul 16-21 (strongest overall — 5 days, dense photos) |
| `summer-2010__seg2` | 323 | 14 | 1.5 MB | Italy arrival short |
| `summer-2010__seg3` | 1,768 | 250 | 26 MB | Italy proper Jul 24 – Aug 3 |
| `summer-2010__seg4` | 217 | 2 | 264 KB | Italy → Brussels transit |
| `summer-2010__seg5` | 930 | 8 | 680 KB | Brussels-London |
| `summer-2010__seg6` | 551 | 25 | 2.3 MB | London Aug 10-16 |
| `norway-weekend-2013` | 1,900 | 449 | 68 MB | Oppdal Jul 5-7 (Moves storyline, has post-hoc elevation) |

Total ~270 MB on disk. Nothing in `/Volumes/Groke/Photos/` was touched. Thumbs are all 1024px q70 JPEGs; RAW previews extracted via `exiftool -b -PreviewImage` then `sips`-resized.

## How to run

Safari (permissive on `file://`):

```
open "file:///Volumes/Groke/Projects/2004%20-%20Timeland/_speculation_other_datasets/render.html?dataset=norway-weekend-2013"
```

Chrome (needs `--allow-file-access-from-files` for `<img>` loading):

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --allow-file-access-from-files \
  "file:///Volumes/Groke/Projects/2004%20-%20Timeland/_speculation_other_datasets/render.html?dataset=norway-weekend-2013"
```

URL params: `?dataset=<name>` (required), `?seek=0..1`, `?play=1`, `?bg=white`, `?nocontrols=1`, `?fps=1`.

## Session-critical decisions (not obvious from reading the code)

**1. Manifest loading is via `<script>` tag, not `fetch()`.** Safari and Chrome both block `fetch("manifest.json")` from a `file://` origin. `<script>` tags are exempt (not subject to CORS). Each `manifest.js` is `window.__MANIFEST = {…};` and `render.html`'s `loadManifestScript()` injects a `<script>` and reads the global. First working version used `fetch()` and showed "loading…" forever — spent time confused about this.

**2. Flight-splitter is on by default.** The build script splits GPX at any consecutive-pair gap of `>100 km AND >30 min` and writes each segment as `<name>__segN`. Timo's rule was "car, train, bus, walking — no flights." Detection is speed-agnostic and instead uses distance+time (a 1000-km jump in 3 hours is a flight; a 300 km/h Eurostar sample is only 2 km at 0.4 min — kept). Tunable via `split_jump_km` and `split_jump_min` in the JSON config; `min_segment_hours` (default 4) drops short splinters.

**3. The `bkk-burma-2012` and `summer-2010` folder-level `manifest.js` files are redirect stubs, not manifests.** They point at `__seg2` and `__seg1` respectively so old bookmarks keep working. If you rename a segment, update the stub. The real manifests live in `__segN/manifest.js`.

**4. Marker scale is capped at 1.6×.** The SWF's `(ele × 0.8 + 80) / 100` was tuned for Iceland (sea level → 400m). At Norway's 2200m peaks it produces 18× markers that swamp the canvas. Cap sits at the render level in `drawMinutes()`. Iceland's own renderer (`experiment-2026/index.html`) is unaffected.

**5. Moves GPX has no `<ele>`.** `lookup_elevation.py` fills it in by querying `ws.geonorge.no/hoydedata/v1/punkt` (Norwegian national 1-m lidar DEM, no auth, ~200ms per point, dedupe by rounded lat/lon before querying). Runs at 8-way concurrency. Only useful for Norway; for other regions you'd want a different DEM (Open-Elevation is global but returned 0 for the Oppdal test point — unreliable).

**6. Moves GPX has `lon` before `lat`** in attribute order, and time strings look like `2013-07-05T12:15:27.000+01:00` (Garmin uses `Z`). Parser tolerates both.

**7. The "London weekend 2013-07-05" candidate in `CANDIDATES.md` is actually Oppdal, Norway.** I conflated a 2013-02 London Moves trace with the July 2013 photos. Renamed to `norway-weekend-2013` everywhere, including `CANDIDATES.md` (titles corrected 2026-07-04).

**8. The projection isn't latitude-aware.** The renderer uses SWF's `gLatScale=-800, gLonScale=400` (2:1 squash tuned for Iceland's ~64°N). Applied verbatim to Bangkok (~13°N) it stretches east-west more than reality. Defensible as a style but flagged.

## What works, what doesn't

Verified working in Safari with photos loading:
- `norway-weekend-2013` (with post-hoc elevation, capped markers)
- `bkk-burma-2012__seg2` (Yangon)
- `summer-2010__seg1` (Norway leg)

Not verified end-to-end (built but not screenshotted at multiple seeks):
- `bkk-burma-2012__seg1`, `__seg3`, `__seg4`
- `summer-2010__seg2`..`__seg6` (mostly too few photos to be worth watching)

Known limitation:
- Headless-Chrome screenshots at mid-trip `?seek=` don't show all past photos — the renderer only prefetches around the moving cursor. Live playback in a real browser is the right way to evaluate. Watchable-video capture (ffmpeg + headless play-through) is a good next step.

## Unmerged overnight followups (on separate branches)

Four `overnight/*` branches carry speculative work that hasn't been merged into `experiment/2026-update`:

- `overnight/2026-05-14-projection-latitude-aware` — `6fc9db1 latitude-aware projection`. Addresses decision #8 above. Look here first if the Bangkok squash reads wrong.
- `overnight/2026-05-14-speculation-readme` — `a86821a speculation folder README`.
- `overnight/2026-05-15-speculation-index` — `12578b1 speculation folder index`. Likely an `index.html` menu; Timo asked for something like this in this session.
- `overnight/2026-05-16-projection-preview` — `f7c80de projection preview tool with on/off screenshots`. Probably an A/B viewer for the projection question.

Bring these into the working tree if you want to iterate on them; the overnight-prep skill is what created them and they were kept speculative deliberately.

## Open threads worth picking up

- **Elevation lookup for non-Norway data.** BKK-Burma and Summer 2010 use Garmin — they already have `<ele>`. If you ever run a Moves-era London or Barcelona set, you'll need a global DEM. Options: SRTM 90m tiles (offline), OpenTopoData (`api.opentopodata.org`, batched), or Google Elevation API (needs key).
- **`?dataset=<name>` menu.** Right now the user has to know the exact segment name. A single `index.html` listing all datasets + links + seek presets would remove that friction. See the `overnight/2026-05-15-speculation-index` branch.
- **Live-playback video capture.** ~3 min per segment. `--headless=new --autoplay-policy=no-user-gesture-required` + a screen-recorder wrapper. Would let us present the work as videos rather than the live prototype.
- **Foursquare place labels from Moves storyline `<wpt>` blocks.** Currently unused. Would introduce a fourth visual element and read as "the day looked like this: hotel → café → museum → hotel."
- ~~**Bug fixes in the redirect stubs.**~~ Checked 2026-07-04: no version of the committed stubs doubles `location.hash` — it is appended once, correctly. Nothing to fix.

## For the next agent

If the user says "keep going on the visualisation-tool thing," start here:

1. Read `CANDIDATES.md` for the planning framing.
2. Look at the four unmerged overnight branches — one of them (index) probably solves the URL discoverability, and one (projection) probably solves the squash question.
3. If they want a new dataset, write a JSON config alongside `bkk-burma-2012.json`, run `build_dataset.py`, and open the resulting `?dataset=` URL. That's the whole loop.
4. If they want a *watchable* deliverable (video, share link), the missing piece is the ffmpeg-record path. Live playback + `?play=1` is the input; screen-record for 3 min at 30 fps to `.mp4`.

If they want to stop this thread and go back to the main Timeland recreation (`experiment-2026/`), the speculation folder is inert — nothing here changes the main renderer or data.
