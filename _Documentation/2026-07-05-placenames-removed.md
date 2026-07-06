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

Open `_Documentation/2026-07-05-map-in-motion-noplacenames.html` — one self-contained
page (gifs inlined, no server needed) showing the no-placenames render in motion across
three trips, so the piece can be judged by eye instead of from text.

The three loops, also saved as standalone gifs next to the page:

- `norway-weekend-2013-noplacenames.gif` — Norway weekend (Oppdal, 5–7 July 2013).
  The trail draws itself south to north and back, photos bloom at their moment, the
  last frame pulls back to the whole route.
- `bkk-burma-2012-noplacenames.gif` — Bangkok → Burma 2012, the densest trip. Minute
  octagons crowd the city, then the route stretches across the country.
- `summer-2010-noplacenames.gif` — Summer 2010, the longest run of photos, sparser trail.

None carry a single place-name label. The readout keeps only date, lat-lon and elevation.

Rebuild any of them from the render:

    cd _speculation_other_datasets && python3 -m http.server 8137
    # then drive render.html?dataset=<name>&nocontrols=1&bg=white across seek=0..1
    # (norway-weekend-2013, bkk-burma-2012__seg2, summer-2010__seg1) and assemble
    # the frames with ffmpeg. Capture/build scripts used: /tmp/capture_gif2.sh + build_page.py.
