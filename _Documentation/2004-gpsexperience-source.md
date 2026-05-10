# 2004 OmniOutliner notes — `gpsexperience.oo3`

Source file: `/Volumes/Groke/Projects/2001-2017 - Writing and Publications/gpsexperience.oo3`
Extracted 2026-05-09 from the `.oo3` bundle.

Field notes from carrying a Garmin eTrex around in 2004. The companion to
`2004-omnioutliner-source.md`: that document is the *design intent* for what
to do with photographs and a GPS trail; this one is the *lived experience*
of using the GPS itself. The phenomenology of the device.

Worth reading alongside the archaeology because it grounds the choices in
the SWF in real conditions: why one trkpt per minute, why the Garmin loses
the trail in cities, why the camera/spring system has to compensate for
abrupt deviations.

---

## GPS experience

- not a passive tracking device
- needs constant attention
- found a way to use it in a bag: in a mobile phone pocket where the aerial sticks out: and I can place it in windows of buses
- urban tracking is very difficult
- fast turns make wild deviations: re-configuration of satellites is the problem
- sit on the outside of buses and trains: to get a wider expanse of road: sky area
- constantly aware of sky cover
- need a road that aligns well with a variety of satellites
- would like more explanation of how the gps (garmin) calculates lost tracks: it seems to use the last bearing and speed to guess new tracks, but this is very unreliable.
- The location of satellites is beginning to have an effect on the side of the street that I walk on.
- I sometimes walk in the middle of the street, have had a couple of near misses with cars — the map is just too interesting.
- the track is as useful (or more useful than) a detailed map: it shows my personal space and personal routes, I know where I have been and can use it to retrace routes. Popular routes build up in blackness and thickness. Home area becomes an abstract scatter plot of routes, but it's very familiar.

---

## Notes for the archaeology

A few hooks that connect this to what's in the SWF and the recreation:

- **"fast turns make wild deviations"** — the abrupt mid-trip re-projections
  in the .mov (the camera lurching to catch a sudden GPS jump) aren't a
  rendering bug, they're the camera spring honestly chasing what the
  Garmin actually output. The wildness is in the data, not in the playback.
- **"the track is as useful (or more useful than) a detailed map"** —
  this is the design rationale for why Timeland's "map" is *not* a
  Mercator projection but a personal trail. The squashed lon×400 / lat×−800
  projection (preserved in §VII.3 of the archaeology) follows from the
  view that the trail itself is the map; the geography is incidental.
- **"Popular routes build up in blackness and thickness"** — the
  red-octagon-per-minute trail markers accumulating in the SWF behave
  exactly this way: dwell long enough at a location and the markers
  cluster into a dark dense thicket. Stopping points are visible without
  any extra encoding.
- **"the map is just too interesting" / near misses with cars** — the
  attention-pulling power of the live trail is a known felt thing, not
  a metaphor. Worth keeping in mind when judging the recreation: the
  question *"does the trail feel as compelling as the original?"* has a
  ground truth in this kind of bodily report.
- **"needs constant attention" / "place it in windows of buses"** —
  explains the gaps in the GPX. The trail isn't continuous; the device
  was being shielded, repositioned, lost, regained. The 5,869-trkpt log
  carries the trace of all of that.

The outline reads as an artist's lab notebook, written in the device's
language. It is the closest thing to a 2004 spec sheet for the kind of
GPS data the SWF was built to consume.
