# Placenames removed from the map experience — 2026-07-05

Timo's call from the morning page: placenames are not part of the experience.
Don't add place-name labels to the map, neither all-at-once nor timed. Drop that
direction.

## State

The mainline render (`_speculation_other_datasets/render.html` on
`experiment/2026-update`) never carried place labels. It draws four things:
photos blooming at their moment, the minute octagons, the hour clock-hands, and
the date / lat-lon / elevation readout. No place names anywhere.

The place-label work only ever lived on two speculation branches, kept as an
archive in case the direction is ever wanted again:

- `overnight/2026-07-04-place-labels` — labels appear all at once.
- `overnight/2026-07-05-place-labels-timed` — labels bloom with the clock.

Both added `extract_places.py`, a per-dataset `places.js`, a `drawPlaces()` pass,
a `loadPlacesScript()` loader, and a "places" toggle in the controls. None of that
is in the mainline. This branch, `experiment/2026-no-placenames`, is the mainline
render confirmed clean of place labels, plus the gif below.

## To see it

`_Documentation/norway-weekend-2013-noplacenames.gif` — the Norway weekend
(Oppdal, 5–7 July 2013) rendered in motion with no placenames: the trail draws
itself south to north and back, the camera follows the head, photos bloom at
their moment, and the last frame pulls back to the whole route.

Rebuild it from the render:

    cd _speculation_other_datasets && python3 -m http.server 8137
    # then drive render.html?dataset=norway-weekend-2013&nocontrols=1&bg=white
    # across seek=0..1 and assemble the frames with ffmpeg.
