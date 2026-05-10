# Time that land forgot

A 2004 Flash piece by Timo Arnall and Even Westvang, recreated in 2026 as plain HTML/Canvas.

**Live:** https://timoarnall.github.io/timeland-2004/

A "camera" rides along a GPS track, centring itself on the advancing now while keeping the last 20–30 minutes of route in view. Photographs surface at the locations they were taken — first huge and pixelated at the moment of presence, then receding into the timeline as time moves on. Red ring markers accumulate as the trip unfolds; brown crosshairs mark the hours.

The original was made in ten days at the Iceland *Inside and Out* workshop in Höfn, July 2004. 241 photographs along a 1,500 km GPS trail, 30 June – 6 July.

## Repository layout

```
index.html              ← the running 2026 artefact
data/                   ← runtime data (used by index.html)
  ├── timo_iceland_noflight.gpx  · the GPS track
  ├── imageData.xml              · photo EXIF index
  └── photos/                    · the 241 JPEGs
_archive_2004/          ← the original 2004 materials + 2026 decompilation
  ├── timeland19.swf             · the compiled Flash file
  ├── time_land_forgot.mov       · the 192-s screen recording (Git LFS)
  ├── timeland.fla               · the truncated Flash source
  ├── index_original.html        · the 2004 elasticspace page
  ├── swfdump_full.txt           · the SWF bytecode dump
  ├── mov_frames/                · reference frames at 1 fps
  └── README.md                  · index of what's where
_Documentation/         ← rebuild notes (archaeology)
  ├── 2026-archaeology.md        · the main writeup
  ├── todo_unfix_bugs.md
  └── _intermediate_comparisons/ · iteration-by-iteration comparison videos
```

## Recreation notes

Mechanics ported literally from the decompiled AS2:

- **Physics tick at 30 fps** — matches the SWF's actual rate on 2004 hardware (5869 trkpts ÷ 192s = 30.6/sec)
- **TimeKeeper damped spring** — `timeD += (t − tDest) × 4; timeD *= 0.1; t -= timeD;` (verbatim AS2)
- **Camera spring** — CAMDRAWING `vel += err/40; vel *= 0.69`, EXTENTS `vel += err/3; vel *= 0.59`
- **Trail window** — last 14 of 15 minutes (`slice(-15, -1)`)
- **Image scale** — `3.5 + 9_000_000 / (|now − photoTime| + 1)`
- **Image fade** — `_alpha = timer; timer += 1.2 / frame` (reaches 100 in 2.77s real)
- **Trkpt-paced playback** — one GPX trkpt per physics frame, so pauses dwell and motion races, exactly as the SWF did

The recreation reads the data faithfully — both bugs the original SWF carried in its display layer have been corrected:

- The .mov's clock was 2h earlier than reality due to a Flash 6 `setHours` quirk that reinterpreted GPX `Z` text and EXIF strings as local CEST. Iceland is on GMT year-round, so the recreation displays the true GPS UTC value labelled `GMT`.
- The .mov's "10.95W mid-Atlantic" longitude was a SWF display bug — `display._lat = lon / gLatScale` divided longitude by `gLatScale (-800)` instead of `gLonScale (400)`. The recreation displays the true Reykjavik longitudes (~−21.9°W) directly.

Camera time was set to GPS UTC at the time — confirmed empirically by detecting the Geysir pause (Sat Jul 03 12:30–13:02 UTC at lat 64.313, lon −20.297) and matching it to 5 photos in the data with Geysir content (warning sign, steaming pool, tourists with cameras, geothermal pool).

## Source

Original blog post: https://www.elasticspace.com/2004/07/timeland
