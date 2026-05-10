# 2004 OmniOutliner notes — `homebrew photo mapping.oo3`

Source file: `/Volumes/Groke/Projects/2001-2017 - Writing and Publications/homebrew photo mapping.oo3`
Extracted 2026-05-09 from the `.oo3` bundle (gzipped OmniOutliner v3 XML).

This is the design brief for what became *Time that land forgot*, written by Timo
in his own 2004 words. Three sections, each load-bearing for the archaeology:

1. **Homebrew photographic mapping** — the practical to-do list, before Iceland.
2. **Beyond the technology** — conceptual aims. Note the line about
   grandchildren and family albums that lands the same idea Even named in
   2026 as "talking to your grandma in the box".
3. **Results of Icelandic workshop** — the talk script delivered in Iceland,
   which describes the piece's mechanics in the artist's own 2004 words.
   This is the closest thing we have to a contemporaneous design spec.

---

## Homebrew photographic mapping

- set the time and date of the camera to a few seconds accuracy
- record a continuous (1 minute interval) GPS data route for any journey
- create a tab delineated text file of the route including location and time data
- export a list of photos from the journey to tab delineated including time and filename
- link the two together and relink back into illustrator using mappro or other GIS solution
- then use GIS data to pull in relevant place information
- Use applescript?
- Use a server application would be perfect
- what about directional information?
- Try and get hold of a Garmin
- find out how long a gps receiver can record for constantly, at what resolution...

## Beyond the technology

- The gps trails are a byproduct of my intention to have a gps time-stamp for every image
- I am intensely interested in the trails, but have found that they are not effective as a way of giving the images context, for other people.
- Perhaps the gps trails are only useful to the person that created them, meaningless as communication, so how can we make them useful?
- What about the long term use of images and location data: how will the next generation access this stuff? How will grandchildren access it in the way that I view my family albums?
- Think about the interesting and useful ways that my diary is used by friends and family and website visitors...
- Want to know more intricate relationships and context for the images: what is the relationship between them, why do I see an image of an airport followed by a picture of a curtain?
- Ultimately would like a picture frame that shows the latest images, with context: like the Nokia image frame and lifeblog
- For the website simple captions and context can be enough: what about using nearest cities or altitude or direction as ways of giving images context and narrative
- set up a set of metadata strategies for images
  - People: relationships
  - Places: locations, relationships, movement
  - Narrative: invisible hand controlling flow
    - Start, end, setting, establishing, problem, question, detail, resolution, enigma
    - Scott McCloud's definition (from *Understanding Comics*)
      - Moment to moment — almost filmic detail of one moment
      - Action to action — shows people or objects in action
      - Subject to subject — sequence of related things
      - Scene to scene — establishing and resolution shots: linking separate moments
      - Aspect to aspect — assembling single moments into scattered fragments
      - Non-sequitur — unrelated or abstracted
    - Most of my images are aspect to aspect, moment to moment or non-sequiturs
    - Set up a way of accessing these axes in ways that form narrative development (perhaps similar to MIT Context/Dexter)

## Results of Icelandic workshop

- Interaction designer, working in london, working with mobile devices, interactive television, and digital archive projects.
- Have been recording daily experience through photography for the last 5 years
- An archive of 60,000 images
- Real problems with archiving all of this material, only with time
- Recently recording location using gps receiver
- Exciting because it allows really powerful filtering: seeing places as well as time
- GPS: pull out personal geographic histories, visualisations of movement and space
- While here we have looked at visualising both photographic and geographic histories.
- Our original intention was to make a simple interface that gave images some kind of spatial context
- What you see is a work in progress, showing time and space in a way that gives an idea of how we explored the landscape, and where we took the images.
- Circles indicate every nth point along a continuous tracklog, the circles scale according to altitude, so you can see when we were climbing a mountain. The red ticks indicate hours, an idea of time in space. The outline boxes indicate photographs, giving a sense of where images were taken.
- We hope to include images as part of the texture of the landscape
- We will continue to work on the interaction design, so that we can make a useful interface for browsing personal histories, and hopefully make it available as a tool on the web.

---

## Notes for the archaeology

A few specifics that are useful when reading the SWF and the .mov against this:

- **"red ticks indicate hours"** — confirms the brown crosshairs in the
  SWF and in the recreation are the *hour* markers, exactly as we found
  in DoAction_5.as. The 2004 description and the 2004 code agree.
- **"circles scale according to altitude"** — interesting find. The
  shipped SWF v19 markers are octagons at fixed size that scale only
  with the camera, not with altitude. So altitude-as-marker-scale was
  in the design intent and got dropped or simplified before v19. This
  is one of the *features Claude got wrong as bugs* candidates that
  turns out to be a feature that never shipped.
- **"every nth point along a continuous tracklog"** — confirms the
  trkpt-paced playback design intent (one trkpt per animation frame),
  which is what makes the trail "alive" in the recreation. Section
  X.7 of `2026-archaeology.md` describes how this took several
  iterations to recover from the SWF.
- **"How will grandchildren access it in the way that I view my family
  albums?"** — written by Timo in 2004 as a design provocation for the
  piece. In 2026 Even, watching the recreation, used the phrase
  *"talking to your grandma in the box"* to describe what the
  recreation actually is. Two readings of the same idea, twenty-two
  years apart, by the two collaborators.
- **The tab-delineated workflow** in the first section — `imageData.xml`
  in the project folder is the eventual output of that pipeline. The
  outline names the workflow before the file format settled.

The outline is dated by context (workshop in early July 2004, plus the
"have been recording daily experience through photography for the last
5 years" line which puts it at ~1999 onwards, and the closing line
about "make it available as a tool on the web" which dates it to
before the elasticspace post on 30 July 2004).

Original `.oo3` is preserved at the source path above. This markdown
extraction lives in `_Documentation/` so that the prose is
searchable, version-controlled, and readable without OmniOutliner
(which itself is on a longer timeline of becoming hard to open).
