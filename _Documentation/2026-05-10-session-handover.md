# Session handover — 2026-05-10

End-of-session note. The piece is shipped, the writeup is shipped, the
code is annotated, the project is tidied. This file captures what the
session of 2026-05-09 to 2026-05-10 changed and where the loose ends
sit, so a future session (or future archaeologist) can pick up cleanly.

## Where things are

- **Running artefact:** `index.html` at the repo root. Single file,
  ~1080 lines, vanilla JS + canvas. No build step.
- **Live URL:** https://timoarnall.github.io/timeland-2004/ (GitHub
  Pages, auto-deploys from `main` of `timoarnall/timeland-2004`).
- **Embedded on:** `elasticspace.pages.dev` via the
  `2026 - Elasticspace update` repo. Its deploy CI clones this repo
  fresh on every push, so this repo's `main` is the source of truth
  for both surfaces. See bottom of this note for staging deploy
  mechanics.
- **The reference documents:**
  - `_Documentation/2026-archaeology.md` — section-by-section
    technical writeup. Every constant, every decision, every
    audit-chain finding, with `§N.N` references.
  - The published article — *Time that land forgot, an archaeology* —
    canonical CMS source at
    `2026 - Elasticspace update/07-site/content/timeland-archaeology.json`,
    target URL `/2026/05/timeland-archaeology`. Edited live in
    another terminal in a block-based editor. There is also a
    legacy HTML draft in
    `2026 - Elasticspace update/01-content/drafts/draft-timeland-archaeology-2026.html`
    that is now stale; do not edit.
  - `_archive_2004/swfdump_full.txt` — the SWF disassembly.
  - `_archive_2004/time_land_forgot.mov` — the only continuous record
    of the original in motion. In Git LFS.
  - `_Documentation/2004-omnioutliner-source.md` and
    `2004-gpsexperience-source.md` — extractions of two 2004 `.oo3`
    files from
    `/Volumes/Groke/Projects/2001-2017 - Writing and Publications/`.
    The first holds the pre-workshop design brief, the workshop talk
    script, and the line *"How will grandchildren access it in the
    way that I view my family albums?"* — twenty-two years before
    Even said *talking to your grandma in the box*. The second holds
    Timo's GPS field notes from the trip.
- **Cross-conversation memory:** durable preferences saved at
  `/Users/timoarnall/.claude/projects/-Volumes-Groke-Projects-2004---Timeland/memory/`,
  indexed in `MEMORY.md` there. Three worth knowing about before
  picking up the project:
  - *Build ground-truth comparison harness on day one* — symbolic
    reasoning fails silently; build the synced diff before iterating.
    (The thing this session learned the hard way over nine
    side-by-side iterations.)
  - *Don't minimise small visual / behavioural differences* —
    pixel-diff "small" is experiential "load-bearing"; describe what
    each diff does to the felt work, not how small it is in pixels.
  - *Bug-preservation criterion: charm yes, experience-cost no* — the
    criterion in §VII.7. Preserve original bugs that add character;
    revert ones that obstruct reading the data the work is a record
    of.
- **Code annotations:** every constant and every decision in
  `index.html` is now anchored to its archaeology section and, where
  relevant, quotes a phrase from the article. A future reader holding
  archaeology + article + swfdump + .mov should be able to reconstruct
  the same qualities.

## What this session changed

In commit order, most recent first:

1. **`f328a14` — comprehensive code annotations.** Pass through
   `index.html` top to bottom; every constant gets its DoAction line +
   archaeology section. The two non-faithful values (SCALE_CAP=3800,
   +15 % marker bump) are flagged as side-by-side rig calibrations.
   Project preamble at the top of `<script>` names what this is, the
   reading order, and warns against AI's instinct to drift toward
   "tool" affordances when this is a film.
2. **`5b0a4b7` — performance pass.** Render-rate lock to 30 fps to
   match the SWF's actual 2004-hardware rate. Path2D caches replace
   per-frame `beginPath/moveTo/lineTo`. Hot-path `.slice()` calls in
   `cameraAnimate` / `refocus` / `drawMinutes` / `drawHours` replaced
   with array + end-index. Per-marker `save/restore` replaced with
   translate-back. Photo-timer loop breaks early on first future-zero.
   Visuals verified identical at six seek points.
3. **`1903982` — tidy and audit.** Top-level reorg:
   - `archive/*` and `timeland/*` consolidated into `_archive_2004/`,
     with a `README.md` indexing each historical artefact.
   - 11 intermediate comparison videos moved to
     `_Documentation/_intermediate_comparisons/`; v13 + side_by_side
     stay prominent.
   - Root duplicates removed (`changelog.txt`, `license.txt`,
     `README.txt`, `flash/`, `exif2xml/` — all duplicated `timeland/`
     contents).
   - `time_land_forgot.mov` moved into `_archive_2004/` (still LFS).
   - All `.DS_Store` files cleaned.
   - Root `README.md` rewritten with the new layout and the corrected
     "displays GMT" note.
4. **`2bb9a11` — undid the GMT+0200 bug.** Followed `cace6db` thinking;
   the underlying time variable was always true UTC, so this was a
   label change, not a recomputation.
5. **`0b3dbdf` — synced archaeology** with the §X.11 SCALE_CAP work,
   §X.9 bbox-snap, and the 2004 source findings (the outline contents
   recovered from the FLA strings dump and the OmniOutliner notes).
6. **`6f4b647` — fill the container.** Stage + canvas now `width: 100%`
   with `aspect-ratio: 1`. ResizeObserver syncs the drawing buffer to
   `clientWidth × DPR`, so the artefact stays sharp on hosts wider than
   500 px. `canvasScale` replaces the constant DPR multiply.
7. **`94c5b2e` — explicit body bg per colour scheme.** Safari does not
   always paint a transparent iframe through to the host page bg, so
   `--body-bg` is white in light mode and `#111` (elasticspace's
   `--paper`) in dark mode. The artefact stage stays warm off-white in
   both. (User-edited; was a fix on top of `6352026`.)
8. **`9ec9c23` — 3 px corner rounding** on stage + canvas.
9. **`6352026`** earlier transparent-bg attempt that Safari didn't
   honour reliably, superseded by `94c5b2e` above.
10. **`3a4371e`** — first dark-mode aware controls (replaced).
11. **Reverted the longitude /-800 display bug** (`drawDisplay`) —
    same logic as the GMT+0200 revert: the lat/lon are values a viewer
    reads off the screen to follow the trip; reading wrong values made
    the piece illegible as a record of Iceland in July 2004. Section
    `_Documentation/2026-archaeology.md` §VII.7 names the criterion.

The reversion criterion (charm vs experience-cost) is the most
important conceptual move of the session. It is documented in
`§VII.7` of the archaeology and in *What I did, that AI could not* /
"Two" of the article. Every future bug-vs-feature call should be
tested against it.

## What is still open

- **No fresh side-by-side video** has been recorded since the un-bug
  fixes. Mine's labels now diverge from the .mov by +2 h and ~+11 ° lon.
  The labels in `_intermediate_comparisons/` videos are stale on
  purpose — they are a record of the rebuild iteration, not the final
  state. If a writeup or comparison artefact needs to ship that
  references the live page, re-record. The harness lives in this
  session's notes; rebuild it from `?seek=` URL params + headless
  Chrome.
- **The article cites three figure GIFs** that aren't in the article's
  CDN yet: `comparison-01-first-attempt.gif`,
  `comparison-05-mid-iteration.gif`, `comparison-09-synced.gif`. The
  intermediate comparison videos in `_Documentation/_intermediate_comparisons/`
  are the source material; choose three representative moments and
  export. Not blocking publication if the article is fine without
  them.
- **Even's *boring overnight pauses* observation** (postscript of the
  article) is folded into `§X.7` of the archaeology. The recreation
  already does the right thing (trkpt-paced playback). No code change
  needed; this is a documentation correction.
- **Test in real-world Safari** for dark mode — Chrome headless doesn't
  exercise the Safari-specific transparent-iframe issue that drove the
  body-bg-per-scheme change. The CSS *should* work in Safari now (the
  hand-edit user made on `94c5b2e` was specifically for Safari) but a
  manual check on the deployed elasticspace.pages.dev preview is
  worth doing once the site lands there.

## The lay essay JSON (the other surface)

If the next session needs to edit the published article rather than
the artefact, the canonical file is:

```
/Volumes/Groke/Projects/2026 - Elasticspace update/07-site/content/timeland-archaeology.json
```

Title: *Time that land forgot, again*. ~86 blocks. Edited live in
the elasticspace editor in another terminal, parallel to anything
an agent does. Worth knowing:

- **Always re-read before editing.** `_savedAt` shifts often as the
  user edits; blocks get added or trimmed by the editor's own
  activity. Conflicts are silent.
- **Edit the structure with Python**, not the `Edit` tool. The
  stale-state detection on `Edit` fights with the editor's parallel
  saves. Validate after every write
  (`python3 -c "import json; json.load(open(p))"`).
- **The editor's HTML sanitiser strips `<ins data-edit="ai">` and
  `<del data-edit="ai">` tags on save.** Surrounding content
  survives but the markers don't. So if you wrap proposed edits
  in those tags expecting a review UI, the user will see the
  content as accepted, not as a diff to approve. The split between
  `t64` (with `<del>`) and `b605vb2` (with `<ins>`) in the
  postscript is a one-off that escaped the sanitiser by being two
  separate blocks; not a generic mechanism.
- **Block IDs.** Existing IDs use a short alphanumeric pattern
  (`bj8vgp7`, `bycu0lx`, `b605vb2`, `bspqc4v`). New blocks added in
  this session use `bair*` (Two paragraph + field-context coda),
  `bw04*` (the 2004 mechanics quote), and `bgrnd*` (the
  grandchildren loop). Match the editor's pattern for any new
  blocks.

What's currently in the lay essay vs the technical writeup:

- The lay essay does NOT include the SCALE_CAP / bbox-snap /
  responsive-embed work. Those are inside-baseball and live only
  in the technical writeup (§X.11, §X.9, §VI.7). Don't move them
  across unless asked.
- The lay essay DOES include the *grandchildren / family albums*
  loop (postscript blocks `bgrnd1` `bgrnd2` `bgrnd3`) and the 2004
  mechanics quote (writeup-section blocks `bw04tlk` `bw04qot`).
  Both came from the .oo3 extractions in
  `_Documentation/2004-omnioutliner-source.md`.

## Staging deploy

Three layers, depending on which "staging" is meant:

1. **Local Astro dev (`localhost:4321`)** — `07-site/public/timeland-2004`
   is a symlink to this project. Astro serves files live; just refresh.
2. **Local static preview** — from
   `2026 - Elasticspace update/07-site/`:
   ```
   npm run build:static
   npm run preview:static
   ```
   `build-static.mjs` dereferences the symlink and copies real files
   into `.static-build/dist/`, stripping `.git`, `_Documentation/`,
   `README.md`. The `.gitignore` change protects against accidental
   commit.
3. **Cloudflare Pages staging (`elasticspace.pages.dev`)** — workflow at
   `07-site/.github/workflows/deploy.yml` runs on push to `main` of the
   elasticspace repo. The job does its own `git clone --depth=1
   https://github.com/timoarnall/timeland-2004.git` so it always pulls
   this repo's latest `main`. To trigger without a no-op commit:
   ```
   cd "/Volumes/Groke/Projects/2026 - Elasticspace update/07-site"
   gh workflow run deploy.yml
   ```

## The principle to remember

> Bug-fidelity is a tactic, not the goal. Archival fidelity to a piece
> of work is fidelity to *what the work was trying to do*, not to every
> byte of how it once did it. When the tactic and the goal point
> opposite directions, the goal wins.
>
> — `_Documentation/2026-archaeology.md` §VII.7

The 2026 recreation has corrected the bugs that obstructed reading
the trip and preserved the bugs that give it character. The squashed
projection stays. The clock and longitude read as truth. If a later
recreation is needed in 2046 or 2056, this is the call to remake from
scratch against whatever ground truth survives, not to defer to.
