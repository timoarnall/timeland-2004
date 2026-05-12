# Other datasets that could be rendered Timeland-style

Speculative exploration. Nothing here touches the photo archive, GPS archive, or the original Timeland data. Everything reads from existing sources and writes only into this `_speculation_other_datasets/` folder.

## What Timeland actually does (so we know what we're transferring)

A Timeland render needs three things from a dataset:

1. **A continuous spatial track** — GPS or similar, sampled densely enough that consecutive points feel like motion, not jumps.
2. **A set of time-tagged events** that drop *into* that track at moments along it. In 2004 these were 241 photos; they don't have to be photos.
3. **A clock** — a single timeline the camera advances along. The track and the events both project onto that clock.

The piece's signature behaviour: a camera scoped to the last 15 minutes; events blooming up to ~1.0 alpha at their moment then fading at 1.2/frame; map scale auto-fitting to the speed of the recent track ("walking" zoom vs "plane" zoom).

So any candidate dataset needs (a) a track with timestamps and (b) something to "bloom" at moments along that track. Photos are the obvious thing, but heart rate, audio recordings, tweets, emails, transactions, weather samples, are all candidates structurally.

## Data inventory found

GPX/KMZ/KML/TCX/FIT files on the drive: **6,890** total. Most useful collections:

| Source | Files | Date range | Character |
|---|---|---|---|
| Moves app daily-walking | 1,068 | 2013-02-04 → 2016-08-01 | Phone-pocket GPS, ~10s cadence, walking only |
| Moves app daily-storyline | 1,257 | same | Same period, walking + transport + place stops |
| Moves app daily-transport | 738 | same | Trains/cars/bikes — different speed regimes |
| Master GPS named-trips | 58 | 2010-2012 | Garmin eTrex, ~1s cadence, complete trips (Norway, Italy, Brussels-London, BKK-Burma) |
| 2012 GPX Master logs | 29 | 2012-01 → 2013-11 | Per-day standalone tracks |

Photo archive density (top dense days where date-stamped filenames let me count by day):

| Photo Archive 2b (2004-2006) | Photo Archive (2006-2018) |
|---|---|
| 2004-07-03 — 892 (Iceland Geysir day) | 2017-06-26 — 1295 (no GPS) |
| 2005-05-15 — 533 | 2014-03-19 — 942 (Madrid) |
| 2004-07-01 — 451 (Iceland start) | 2013-07-06 — 654 (London weekend) |
| 2005-07-07 — 427 | 2010-11-03 — 647 |
| 2005-05-14 — 337 | 2009-11-19 — 641 |

## Candidates, ranked

### 1. BKK–Burma 2012 — 10-day Asian trip (STRONGEST)

- Track: `2003-2016 - Mapping and Cartography/.../GPS/BKK-Burma.gpx` — 2,514 trkpts, **2012-04-18 23:50 → 2012-04-27 13:00 UTC**.
- Photos: ~1,996 in `Photo Archive/Photo/2012/2012-04-{18..27}/`. Daily counts: 20, 137, 52, **557**, 189, **358**, 163, 74, 65, **381**.
- Why this works:
  - Self-contained trip with clear start and end (mirrors Iceland's structure exactly).
  - Long, slow movement across distinct cities (Bangkok → Burma) — the auto-scale camera will visibly shift between walking-zoom inside cities and travel-zoom between them.
  - 5× the photo budget of the original 241. The bloom-and-fade rhythm holds even at higher density.
  - GPS is Garmin eTrex (same source as the Iceland track), so the rendering pipeline literally takes the same input shape.
- What's surprising about it: tropical light vs Iceland's cold light. Same render code, completely different felt object.
- Risk: 2012-era photos may not have EXIF DateTimeOriginal in the same form as the 2004 set — sample three and verify before bulk loading.

### 2. Summer 2010 — Norway → Italy → Brussels → London (CONTINENTAL SCALE)

- Tracks (named, contiguous, 5 weeks):
  - `Norway july 2010.gpx` — 2010-07-16 → 2010-07-20, 11,014 trkpts
  - `Italy party.gpx` — 2010-07-21 → 2010-08-03, 22,450 trkpts
  - `Brussels London.gpx` — 2010-08-04 → 2010-08-11, 12,037 trkpts
  - `London June 2010 1.gpx` — 2010-08-11 → 2010-08-16, 4,700 trkpts
- Photos in `Photo Archive/Photo/2010/`: peak days 2010-07-17 (451), 2010-07-18 (205), 2010-07-25 (141), 2010-07-30 (147). Total ~1,300 across 5 weeks.
- Why this works: shows the camera at **continental scale** — what does Timeland look like when the track is 2,000 km long and the events are sparser per day but spread across countries? The auto-zoom should pull back to a different reading.
- Test before committing: merge the four GPX files in time order and verify there's no gap larger than the camera-spring can absorb at the inter-country handoffs.

### 3. The London Weekend, 5–7 July 2013 (MOVES-ERA MICRO-TIMELAND)

- Tracks (in Moves export):
  - `walking_20130705.gpx` 269 trkpts, `walking_20130706.gpx` **2,046 trkpts**, `walking_20130707.gpx` 747 trkpts
  - Plus storylines with bus/train segments and named place stops (Foursquare-derived).
- Photos in `Photo Archive/Photo/2013/2013-07-{05,06,07}/`: 188 + **654** + 238 = 1,080 photos over a single weekend.
- Why this works: same-city scale to Iceland-Reykjavík segments, but it's a *non-event* weekend — pure life, not a workshop. Question worth asking: does Timeland still read as a record if the underlying days weren't a Trip? The original artist intent ("centring on the advancing now") doesn't require a destination.
- Bonus: storyline GPX has named Foursquare venues as `<wpt>` elements. Those could render as a fourth element type (faint labelled markers) alongside the photos. New visual vocabulary.

### 4. Long-form Moves slice — pick any week 2013–2016 (DAILY-LIFE PROBE)

- Track: 1,068 daily walking files + 738 transport files cover 1,275 days.
- Photos: cross-reference with date-stamped folders in `Photo Archive/Photo/2013…2016/`.
- Why this works: lets us ask "what does a *normal* month look like through this lens"? The original is about a holiday; running it on regular life is a different proposition.
- Render thought: the camera-window concept may need tuning — 15 minutes is right for a 3-min replay of a 5-day trip, not for a 5-min replay of 30 days. Worth treating the window as a function of speedup ratio.

### 5. The Madrid conference, 19–20 March 2014 (NEGATIVE CASE / DIAGNOSTIC)

- Track: `walking_20140319.gpx` only 8 trkpts, `walking_20140320.gpx` 32 trkpts (mostly indoors, GPS sleeping).
- Photos: 942 + 634 = 1,576 in two days.
- Why this is here despite being weak: it's the **failure mode** — high event density on a near-empty track. Useful to render anyway, to see what Timeland does when the spatial dimension collapses. May expose what's load-bearing about the *spatial* read vs the temporal one.

## What to render (proposed)

A small standalone HTML page next to this report — fork of `experiment-2026/index.html` but reading from a JSON manifest instead of `imageData.xml` and `timo_iceland_noflight.gpx`. The manifest specifies:

- `tracks`: list of GPX paths to merge in time order
- `events`: list of `{ time, lat?, lon?, label?, image? }` entries (lat/lon optional; if missing, the renderer interpolates from the track at `time`)
- `meta`: title, replay duration in seconds, accent colour

Renders are pure-data — no copies of the original files, just paths.

Day-one tests:

1. **Candidate 1 (BKK-Burma)** — full trip, image bloom from photo midpoints, 4-minute replay.
2. **Candidate 3 (London weekend)** — Moves walking + photos. Verify the higher GPS cadence reads cleanly.
3. **Candidate 5 (Madrid)** — render *without* photos first (just track + place wpt names) to see the spatial collapse. Then add photos.

If those three each produce a watchable 1-minute clip, the pipeline is real and we can pick the strongest candidate to push further.

## Read-only contract

- Photo archive paths read directly. No XMP writes, no thumbnails copied.
- GPX paths read directly. No edits, no clean-up.
- All intermediate files (manifests, frame caches, reports) live in this folder.
- Photos referenced by `file://` URLs in the manifest, or by symlink into a `_thumbs/` subfolder if the browser can't read outside the project root. Symlinks only — never copies.
