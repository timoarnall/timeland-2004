# Speculative pass — what we learned

Pipeline built and verified on three datasets. The Timeland renderer transfers cleanly. Same physics, same constants, no tuning needed per-dataset.

## What's in this folder

- `CANDIDATES.md` — the planning report.
- `build_dataset.py` — generic builder. Reads photo dirs + GPX paths from a JSON config, extracts embedded JPEG previews from RAW (.arw/.cr2), resizes to 1024px q70, writes `manifest.json` + `thumbs/`.
- `render.html` — fork of `experiment-2026/index.html`. Same physics, reads `<dataset>/manifest.json`. Open with `?dataset=<name>`.
- One folder per dataset (`bkk-burma-2012/`, `summer-2010/`, `norway-weekend-2013/`).
- `_screenshots/` — headless captures at five seek points per dataset.

## Datasets built (after flight-splitter and elevation lookup)

The initial three "combined" builds were split at flight boundaries (>100km/>30min gap = flight — kept ground-only). BKK-Burma became 4 segments (Bangkok, Yangon, Bagan, Mandalay). Summer 2010 became 6 (2 with meaningful photo counts). Norway weekend is a single clean segment. See `HANDOVER.md` for the full table.

Strongest per source:

| `?dataset=` | Trkpts | Photos | Notes |
|---|---|---|---|
| `bkk-burma-2012__seg2` | 735 | 290 | Yangon Apr 21 — densest single day |
| `summer-2010__seg1` | 1,084 | 548 | Norway 5-day leg |
| `norway-weekend-2013` | 1,900 | 449 | Oppdal, with Kartverket DTM1 elevation |

The legacy names `bkk-burma-2012` and `summer-2010` still work as URLs — they're redirect stubs pointing at the strongest segment.

Total ~270 MB on disk. Nothing in `/Volumes/Groke/Photos/` was touched.

## Run it

In Safari/Chrome (Chrome needs `--allow-file-access-from-files`):

```
file:///Volumes/Groke/Projects/2004 - Timeland/_speculation_other_datasets/render.html?dataset=bkk-burma-2012
```

Replace the `dataset=` value with `summer-2010` or `norway-weekend-2013` for the others. Press space to play. Use the scrub bar to seek. `?seek=0.15` jumps to 15% in.

## What I learned watching them

**BKK-Burma is the clearest hit.** Same Garmin source as Iceland, contained 10-day trip, dense photo days at distinct cities. The renderer reads as "Timeland of Bangkok-Burma" without modification — same red-octagon-and-hour-cross visual language, same bloom-and-shrink rhythm. The seek=0.15 screenshot shows the canonical layered-stack photo behaviour: warm interior, green park, blue train, stacked overlapping with the route stitching through. The "translucent feel from size disparity" that the original work relies on is preserved.

**Summer 2010 stresses the camera in a useful way.** Five weeks of continental motion. The auto-scale spring spends most of the trip near `SCALE_CAP=3800` because the bbox keeps expanding into new countries. At the seek=0.5 capture (Italy, Aug 2, ~42N) the camera is far enough out that individual photos are small and the trail dominates. At seek=0.9 (London, Aug 14) the camera has zoomed in again on London streets and the photo stacks reappear. **This is exactly the "view scales to speed of travel, walking, bus, plane" behaviour the 2004 blog post named.** It works at continental scale despite never being designed for it.

**Norway weekend reads as the weakest of the three.** Moves storyline data is sparser (one trkpt every minute when stationary, every 10s when walking). Many trkpts are zero-elevation (Moves doesn't record elevation reliably). The piece shows three days in one valley around Oppdal — visually it's a small spatial extent with dense photos. **Useful as a corner case:** what does Timeland look like when the spatial story is "we didn't go very far"? Answer: the photos dominate and the route reads as decoration. The accent colour came out blue (`#1a44c4`) which works against the muted Norwegian elevation.

## What broke and what was fixed

- **Moves GPX uses `lon` before `lat`** in trkpt attributes, where Garmin uses `lat` first. Parser fixed to tolerate either order.
- **Moves GPX time format includes milliseconds and `+offset`** (`2013-07-05T12:15:27.000+01:00`) where Garmin uses `Z`. Parser fixed to handle both.
- **The "London weekend 2013" label was wrong** — I'd seen a 2013-02 Moves file at London coords (Feb walking commute) and assumed July 2013 was the same place. The July 2013 photos are actually at Oppdal, Norway. Renamed to `norway-weekend-2013` in all files.
- **Headless screenshots at mid-trip seek don't show all photos** — the renderer only prefetches photos near the moving cursor, and a `?seek=` jump doesn't have time to walk through all the prior photos. Live playback in a real browser shows them all correctly; the screenshots underrepresent what a played-back render looks like. To get a watchable artifact we'd want to record live playback (next step).
- **Continental zoom-out at flights** was pulling the camera far back for Summer 2010. Fix: split GPX at any consecutive-pair gap of >100km & >30min. Each segment becomes its own dataset. See `build_dataset.py:split_segments` and `HANDOVER.md` decision #2. Timo's rule was explicit: car/train/bus/walking only.
- **Moves GPX has no `<ele>`** — every Oppdal trkpt loaded as elevation 0. Fix: `lookup_elevation.py` calls Norwegian Kartverket's DTM1 point service post-hoc (1877 unique points, all fetched successfully). Only Norway; global DEMs would need a different source.
- **Norway's mountain markers were absurd** — the SWF's `(ele × 0.8 + 80) / 100` formula gave 18× markers at 2200m. Capped at 1.6× in `render.html:drawMinutes`. Preserves variation up to ~125m elevation then plateaus.
- **Legacy URLs 404-ed after the split** — `?dataset=bkk-burma-2012` broke because the combined folder was replaced with per-segment folders. Fix: `<name>/manifest.js` is now a redirect stub that swaps `dataset=` to the strongest segment and preserves other query params.
- **Safari/Chrome block `fetch()` from `file://`** — the first version used `fetch("manifest.json")` and hung at "loading…". Fix: manifests are `manifest.js` (JSONP-style `window.__MANIFEST = {…};`) loaded via `<script>` tag, which is exempt from same-origin policy.

## What this confirms

- The renderer is portable. The data adapter is the only thing that needs to change per-source.
- The visual language survives the transplant — minute octagons, hour crosses, photo bloom-and-fade all read as the same piece regardless of which trip you feed it.
- The auto-scale camera handles dataset scales the original was never tested on (continental scale for Summer 2010, valley scale for Norway).
- Three new "Timeland of X" pieces exist now as data + manifests; the live HTML renders them on demand.

## What's still open

- **Live-playback video capture** — would let us evaluate the time dimension properly. Current screenshots are static and underrepresent the piece. ffmpeg + headless Chrome with `?play=1` and screen-record at 30 fps would do it, ~3-min clips per dataset.
- **The projection isn't latitude-aware.** SWF's `gLatScale=-800, gLonScale=400` was tuned for Iceland's ~64°N. At Bangkok's 13°N the natural lat:lon ratio is closer to 1:1, but the renderer still applies the 2:1 squash. The result is "Bangkok rendered in the Iceland projection" — defensible as a style, but worth flagging if we ever want geographic accuracy. **An overnight branch (`overnight/2026-05-14-projection-latitude-aware`, commit `6fc9db1`) has a first attempt at this, not merged.**
- **Discoverability.** Right now you have to know the exact `?dataset=<name>` string. An index.html menu would help. **`overnight/2026-05-15-speculation-index` (commit `12578b1`) looks like it addresses this, not merged.**
- **The "place" entries in Moves storyline data are unused.** They carry Foursquare venue names (Hotel, Datacenter, "Place in Urbanización Los Espartales"). Could render as a fourth visual element (faint labelled markers) alongside the photo frames. New vocabulary.
- **Other media as events.** The pipeline is structurally indifferent to what the event is. A heart-rate spike, an audio recording, a text message, a transaction — anything time-stamped and spatial-by-association can bloom-and-fade through the same physics.

See `HANDOVER.md` for the full state at session end, including the four unmerged `overnight/*` branches.
