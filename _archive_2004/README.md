# 2004 originals

The historical artefacts behind the 2026 recreation. **Read-only**:
nothing here is modified by the running artwork. The recreation lives
at `../index.html`; this folder is the source-of-truth it was
reconstructed from.

## The originals (irreplaceable)

| File | What it is |
|---|---|
| `timeland19.swf` | The compiled Flash 6 SWF that played in 2004. 27 KB, 500 × 500, 120 fps declared. The thing that actually shipped. |
| `time_land_forgot.mov` | 192-second QuickTime screen-recording of the SWF playing on Even Westvang's CEST-set Mac. The only ground truth for how it *looked*. Stored in Git LFS. |
| `timeland.fla` | The Flash MX source file. Truncated to 64 KB on the original disk — OLE2 directory destroyed — so the symbol tree is unrecoverable. Only `strings -n 6` is readable. |
| `index_original.html` | The 2004 elasticspace WordPress page that embedded the SWF. Textpattern markup, `<object>` + `<embed>` tags. |
| `noimages.html` | The "low" variant page (no photos, just GPX trail). |
| `index_map.html` | An alternative experimental page (Leaflet dark map). Side-by-side with the canonical version. |
| `README_2004.txt`, `license.txt`, `changelog.txt` | The 2004 release docs. |
| `exif2xml/` | The 2004 Python tools that produced `imageData.xml` from photo EXIF. `EXIF.py` is the library, `process.py` is the runner. |
| `timo_iceland_short.gpx` | A 2004 truncated copy of the GPS data; the runtime `../data/timo_iceland_noflight.gpx` is the longer version. Kept here as a historical 2004 artefact. |

## 2026 recovery / decompilation outputs

| File | What it is |
|---|---|
| `swfdump_full.txt` | swftools `swfdump -atp` output — 3,757 lines of decompiled SWF bytecode. The primary source of truth for the mechanics in `index.html`. |
| `mov_frames/` | 192 frames extracted from `time_land_forgot.mov` at 1 fps for label-by-label comparison. |
| `mov_frames_2fps/` | 384 frames extracted at 2 fps for tighter comparison. |

## What's NOT here

- The original GPX with the Norway → Iceland flight included. Lost — the runtime `../data/timo_iceland_noflight.gpx` is missing the trans-Atlantic leg. See `../README.md`.
- The Flash 6 IDE that produced this. Macromedia long gone.

The accompanying writeup of how this was reconstructed lives at
`../_Documentation/2026-archaeology.md`.
