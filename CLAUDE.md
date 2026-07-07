# Working in this repo

A 2026 recreation of a 2004 Flash piece. The main port at `index.html` is shipped and embedded on elasticspace. The experiment branch widens it with a 5× denser photo corpus drawn from the original Sony archive. A side-folder explores whether the same renderer carries any GPS-plus-photos trip.

## Two missions, kept separate

- **Preservation**: `index.html`, `data/`, `_archive_2004/`, `_Documentation/`. The 2004 piece, recreated as plain HTML/Canvas. The piece is shipped. Future work on it is rare and small.
- **Experiment**: `experiment-2026/`. Same piece, 5× photo density. The perf chapter is closed. Open question is whether 1200 photos reads as a road shown or a road taken.
- **Speculation**: `_speculation_other_datasets/`. Side-folder. Tool spun out of the renderer to see if it generalises. Not Timeland canon.

When changing one, name which one. Don't drift between them in a single session.

## The criterion that drives bug calls

The SWF has bugs that give it charm. The SWF has bugs that obstruct reading the trip. Preserve the first kind. Revert the second. The rule lives in `_Documentation/2026-archaeology.md §VII.7` and is acted on in `_Documentation/todo_unfix_bugs.md`. When in doubt, ask which side of "experience cost" a bug falls on.

## Ground-truth-first

Symbolic reasoning fails silently on this codebase. Before iterating on rendering or physics, build the sync diff against the 2004 reference recording (`_archive_2004/time_land_forgot.mov` or `mov_frames/`). Visual comparison decides. The `_Documentation/_intermediate_comparisons/` folder is the canonical record of those comparisons.

## Don't minimise small differences

A pixel-diff that looks small reads as load-bearing in the felt work. Describe what each diff does to the experience, not its size. "The +15% marker bump makes hours land an octave louder" is the form. "Tiny visual change" is not.

## Sensitive paths

Default to read-only on these, copy rather than overwrite, dry-run before any batch operation:

- `/Volumes/Groke/Photos/` — multi-decade photo archive. Nothing in this repo should ever write here.
- `data/photos/` — the 241 JPEGs are the original 2004 set, irreplaceable in this form.
- `_archive_2004/` — the original SWF, FLA, MOV, and decompilation. Read-only.
- `_speculation_other_datasets/<dataset>/thumbs/` — generated from photo archive; treat as cache, regenerate rather than edit.

## Branch hygiene

- Main port work goes on the working branch (currently `experiment/2026-update`).
- Overnight speculative work goes on `overnight/YYYY-MM-DD-<slug>` branches. Reversible — `git branch -D` if not useful.
- The main artefact at `index.html` is the shipped piece. Changes to it want explicit before-state captures in `_Documentation/_intermediate_comparisons/`.

## Voice and design

- One font, one weight, two sizes (body and 2× for headings). Style in a single variable block at the top of any new HTML file.
- Plain language in any prose written for the repo or in commit messages. Avoid AI tics ("delve", "leverage", "robust", "seamless", "comprehensive", em-dashes used as scaffolding). Match the voice already in `_Documentation/`.

## What lives where

```
index.html, data/                  shipped 2004 port
_archive_2004/                     original Flash materials + decompilation (read-only)
_Documentation/                    archaeology, perf audits, briefings, comparisons
experiment-2026/                   1200-photo experiment, perf chapter closed
_speculation_other_datasets/       side-folder, three trips rendered; see its own README.md
```
