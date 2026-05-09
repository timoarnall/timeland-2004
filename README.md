# Time that land forgot

A 2004 Flash piece by Timo Arnall and Even Westvang, recreated in 2026 as plain HTML/Canvas.

**Live:** https://timoarnall.github.io/timeland-2004/

A "camera" rides along a GPS track, centring itself on the advancing now while keeping the last 20–30 minutes of route in view. Photographs surface at the locations they were taken — first huge and pixelated at the moment of presence, then receding into the timeline as time moves on. Red ring markers accumulate as the trip unfolds; brown crosshairs mark the hours.

The original was made in ten days at the Iceland *Inside and Out* workshop in Höfn, July 2004. 241 photographs along a 1,500 km GPS trail, 30 June – 6 July.

## Sources

- `data/timo_iceland_noflight.gpx` — GPS track from Garmin eTrex
- `data/imageData.xml` — EXIF timestamps of the 241 photos
- `data/photos/` — the 320×213 JPEGs as published in 2004
- `archive/timeland19.swf` — original compiled Flash
- `time_land_forgot.mov` — the original 192-second screen recording (via Git LFS)

## Recreation notes

Mechanics ported literally from the decompiled AS2:

- **Physics tick at 30 fps** — matches the SWF's actual rate on 2004 hardware (5869 trkpts ÷ 192s = 30.6/sec)
- **TimeKeeper damped spring** — `timeD += (t − tDest) × 4; timeD *= 0.1; t -= timeD;` (verbatim AS2)
- **Camera spring** — CAMDRAWING `vel += err/40; vel *= 0.69`, EXTENTS `vel += err/3; vel *= 0.59`
- **Trail window** — last 14 of 15 minutes (`slice(-15, -1)`)
- **Image scale** — `3.5 + 9_000_000 / (|now − photoTime| + 1)`
- **Image fade** — `_alpha = timer; timer += 1.2 / frame` (reaches 100 in 2.77s real)
- **Trkpt-paced playback** — one GPX trkpt per physics frame, so pauses dwell and motion races, exactly as the SWF did

Key archival findings during the rebuild:

- The .mov's displayed clock is 2h earlier than reality due to a Flash 6 `setHours` quirk — both GPX `Z` timestamps and EXIF strings were silently reinterpreted as local CEST. The recreation displays the true Iceland local time (CEST) instead.
- The .mov's "10.95W mid-Atlantic" longitude was a SWF display bug (`lat / gLatScale` used `gLatScale` instead of `gLonScale`). Same Iceland data either way.
- Camera time was set to GPS UTC at the time — confirmed empirically by detecting the Geysir pause (Sat Jul 03 12:30–13:02 UTC at lat 64.313, lon −20.297) and matching it to 5 photos in the data with Geysir content (warning sign, steaming pool, tourists with cameras, geothermal pool).

## Source

Original blog post: https://www.elasticspace.com/2004/07/timeland
