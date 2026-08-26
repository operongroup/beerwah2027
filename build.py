#!/usr/bin/env python3
"""Build the Beerwah dashboard from template.html + the three data files."""
import json, os, sys

TPL = "template.html"
OUT = ["beerwah-dashboard.html", "/mnt/user-data/outputs/site/index.html"]
DATA = {"/*__SESSIONS__*/": "sessions.json",
        "/*__WEEKS__*/":    "weeks.json",
        "/*__CONTENT__*/":  "content.json"}

tpl = open(TPL, encoding="utf-8").read()
out = tpl
for ph, path in DATA.items():
    raw = open(path, encoding="utf-8").read().strip()
    json.loads(raw)                                  # fail loudly on bad JSON
    if tpl.count(ph) != 1:
        sys.exit(f"ERROR: expected exactly one {ph} in {TPL}")
    out = out.replace(ph, raw)

for bad in ("const SESSIONS = const", "const WEEKS = const", "const CONTENT = const",
            "/*__SESSIONS__*/", "/*__WEEKS__*/", "/*__CONTENT__*/"):
    if bad in out:
        sys.exit(f"ERROR: bad build, found {bad!r}")
for decl in ("const SESSIONS =", "const WEEKS =", "const CONTENT ="):
    if out.count(decl) != 1:
        sys.exit(f"ERROR: {decl} appears {out.count(decl)} times")

for p in OUT:
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    open(p, "w", encoding="utf-8").write(out)
print(f"built {len(out)} bytes -> {', '.join(OUT)}")
