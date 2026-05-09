# Todo: undo the preserved SWF bugs

The 2026 recreation currently preserves two SWF v19 display bugs verbatim.
Timo wants these corrected so he can read the data faithfully.

## 1. Clock reads +2h ahead

The .mov shows `13:43:52 GMT+0200` for a trkpt whose true UTC value is
`13:43:52Z`. This is a Flash 6 `setHours` quirk — the SWF reinterpreted
the GPX `Z` value as local CEST and then displayed it suffixed with
`GMT+0200`. The recreation reproduces that label literally
(`fmtFlashDate` outputs raw `Z` text labelled `GMT+0200`).

**Fix:** display true Iceland local time. Iceland was on GMT year-round in
2004, so the trkpt at `13:43:52Z` should display `13:43:52 GMT` (or
`Sat Jul 03 13:43:52 GMT 2004`). The label suffix should also change
from `GMT+0200` to `GMT`.

Edit: `fmtFlashDate` in `index.html`. No GPX/EXIF data shifts — both are
already true UTC.

## 2. Longitude shows mid-Atlantic value

The .mov shows `10.963852W` for a trkpt at true `−21.927704W` in
Reykjavik. SWF v19 has a typo in its display formula —
`display._lat = lon / gLatScale` divides longitude by `gLatScale (-800)`
instead of `gLonScale (400)`. So `−21.93 × 400 / −800 = 10.96`.

**Fix:** display true longitude. `(-trkpt.raw_lon).toFixed(6) + 'W'` is
correct for negative longitudes. Drop the `/-800` rendering path.

Edit: `drawDisplay` in `index.html`, the line writing the lon column.

## Why these were preserved until now

Strict archival fidelity to the .mov ground truth — to make the
side-by-side comparison videos line up label-for-label. Now that the
mechanics are settled, the labels can be corrected so the artefact
reads as truth, not as the SWF's bug-frozen text.
