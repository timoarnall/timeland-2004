# Experiment: Timeland 2026 update

Self-contained spike on branch `experiment/2026-update`. The 2004
archaeology version is unchanged at the project root; this experiment
lives in `experiment-2026/` and uses its own photos, XML, and copy of
`index.html`.

## What changed

| | Archaeology | Experiment-2026 |
|---|---|---|
| Photo source | curated 320×213 thumbnails | 1024×683 (sips, q=85) from originals |
| Photo count | 241 | 1200 |
| Source originals | `data/photos/` (already shipped in 2004) | `/Volumes/Groke/Photos/Photo Archive 2b/2004-*.jpg` (Sony DSC-P120, 2592×1728) |
| Camera handling | unchanged | unchanged |
| GPX | unchanged | same file, same bounds |
| Disk | ~10 MB photo dir | ~183 MB photo dir |

No code logic changed. The HTML file is a verbatim copy. The drawImage
destination rect is still 320×213 design coords; higher-resolution
source flows through naturally and shows up only when camera + photo
scale push the photo above 320 px on screen (i.e. at peak zoom).

## Pipeline

- `experiment-2026/build_imagedata.py` — scans the archive, reads EXIF
  DateTimeOriginal (treated as UTC, matching the camera-was-UTC finding),
  filters to GPX time window 2004-06-30T13:51:31Z…2004-07-05T19:40:08Z,
  dedupes by md5 (the archive holds many UTC-named/CEST-named pairs of
  the same content), writes `data/imageData.xml`.
- One-liner resize (~12 s, 8-way parallel):
  ```sh
  cat /tmp/timeland_filelist.txt \
    | xargs -P 8 -I{} sips --resampleWidth 1024 -s formatOptions 80 \
        "/Volumes/Groke/Photos/Photo Archive 2b/{}" \
        --out experiment-2026/data/photos/{}
  ```
- GPX copied from `data/timo_iceland_noflight.gpx`.

## Counts

- 1458 clean-stem trip-window candidates
- 138 dropped: outside GPX time window (mostly pre-13:51 UTC on 30 June, before the GPS started recording)
- 120 dropped as content duplicates (same md5 under both UTC and CEST naming)
- **1200 kept**

## Visual findings (4-seek smoke test)

`/tmp/timeland_2026_seek_*.png` vs `/tmp/timeland_orig_seek_*.png`
at seek=0.05 / 0.30 / 0.55 / 0.80.

- **Density.** With 5× the photos, the trail of historical frames is a
  long comet tail rather than a small cluster. Mid-trip moments
  (seek=0.30) show a continuous diagonal stack of dozens of frames where
  the archaeology shows ~6.
- **Sharpness at peak.** Close-up moments (rocks at seek=0.80,
  bus interior at seek=0.55) look qualitatively sharper — the 1024
  source carries through where 320 was upscaled to mush. This is the
  effect the experiment was set up to test, and it works.
- **Quiet moments stay quiet.** Early-trip seek=0.05 (~22:39 UTC on
  30 June) shows mostly outline frames in the experiment because the
  current cursor isn't near a photo, and the more-numerous historical
  frames have decayed to faint outlines. The archaeology happened to
  have a single closer-in-time photo at this exact seek and so reads
  more confidently.
- **Felt tone shifts.** Photos look slightly paler in the experiment
  side-by-side. Likely a render-size artefact (the experiment canvas
  filled the viewport in the test rig while the archaeology landed
  smaller), not an alpha-math change. Worth re-testing at matched
  canvas sizes before claiming this is a real difference.

## Open questions / next moves if pursued

- Is the tail-of-history a feature or a smear? The 2004 piece used 241
  photos in part because the artists curated them. 1200 is *what was on
  the camera*; the photo stream becomes more diaristic and less edited.
  Either reading is interesting.
- Pre-flight Oslo airport photos (138 dropped) need a GPX with the
  trans-Atlantic leg to be placeable. Still missing.
- Alpha cap may want re-tuning once photo overlap is this high. Current
  `PHOTO_ALPHA_CAP = 0.2` was chosen for the 241-photo density.
- 1200 photos × 150 KB ≈ 180 MB. Fine on a modern machine; would need
  thumbnail tiers or progressive loading for public web.
