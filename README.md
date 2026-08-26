# beerwah2027

Training app for Beerwah@Night 2027. Live at https://operongroup.github.io/beerwah2027/

## Source of truth

The deployed app is `index.html`. It is BUILT, never hand-edited.

| File | What it is |
|---|---|
| `template.html` | The app itself: markup, CSS, all JS. Carries three placeholders. |
| `sessions.json` | Every session in the 27-week plan. |
| `weeks.json` | Per-week targets (km, vert, phase, down-week flag). |
| `content.json` | The Content tab: weekly shot list, talking points, change log. |
| `build.py` | Injects the three JSON files into the template placeholders. |

## Building

    python3 build.py

Writes `beerwah-dashboard.html` locally and `/mnt/user-data/outputs/site/index.html`
for upload. The build refuses to write if a placeholder survives or a declaration
is duplicated, which is what caused the blank-page bug on 22 Aug.

## Deploying

Upload the built file to this repo as `index.html`. GitHub Pages serves it.

## Rule

**Commit the sources with every deploy, not just `index.html`.** On 27 Aug the working
container was recycled and the source files were lost, because only the built app had
been pushed. Everything was recoverable from `index.html` by extracting the three JSON
blobs and restoring the placeholders, but that should never be necessary twice.
