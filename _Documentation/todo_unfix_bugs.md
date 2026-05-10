# Done: the two preserved SWF display bugs, reverted

The 2026 recreation originally preserved two SWF v19 display bugs
verbatim. Timo decided 2026-05-09 to correct both so he could read
the data faithfully (see `2026-archaeology.md` §VII.7 for the
charm-vs-experience-cost criterion). Both are now reverted in code.

## 1. Longitude shows mid-Atlantic value — DONE

Was: the .mov shows `10.963852W` for a trkpt at true `−21.927704W`
in Reykjavik. SWF v19 has a typo in its display formula —
`display._lat = lon / gLatScale` divides longitude by `gLatScale (-800)`
instead of `gLonScale (400)`. So `−21.93 × 400 / −800 = 10.96`.

**Reverted in code.** `drawDisplay` in `index.html` now writes
`(-trkpt.raw_lon).toFixed(6) + 'W'` for the lon column, which gives
the true value. Section VII.1 of the archaeology covers the bug and
the revert.

## 2. Clock reads +2h ahead — DONE

Was: the .mov shows `13:43:52 GMT+0200` for a trkpt whose true UTC
value is `13:43:52Z`. This is a Flash 6 `setHours` quirk — the SWF
reinterpreted the GPX `Z` value as local CEST and then displayed it
suffixed with `GMT+0200`.

**Reverted in code.** `fmtFlashDate` in `index.html` now emits the
suffix `GMT` instead of `GMT+0200`. The underlying time variable
was always true UTC, so this was a label-format change only, not a
recomputation. Section VII.2 of the archaeology covers the bug and
the revert.

## Why these were preserved until now

Strict archival fidelity to the .mov ground truth — to make the
side-by-side comparison videos line up label-for-label. Now that
the mechanics are settled, the labels read as truth, not as the
SWF's bug-frozen text. This file is kept as a record of the
decision and the diff.
