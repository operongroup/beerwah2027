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

# --- session self-consistency check (added 8 Sep 2026) ---------------------
# A session's brief is spread over several fields. Editing one and forgetting
# the others shipped a card that said "one hard climb" in the title and "2
# climbs hard" in the WHERE block. This catches that class of mistake.
import re
WORD = {"one":1,"1":1,"two":2,"2":2,"three":3,"3":3,"four":4,"4":4}
PAT  = re.compile(r"\b(one|two|three|four|[1-4])\s+(?:of the\s+)?climbs?\b", re.I)
warnings = []
for s_ in json.loads(open("sessions.json", encoding="utf-8").read()):
    counts = {}
    for f in ("title", "prescription", "opt_out", "route_note"):
        found = {WORD[m.lower()] for m in PAT.findall(s_.get(f) or "")}
        if found:
            counts[f] = found
    # flag only when two fields each name exactly one, different, number
    single = {f: list(v)[0] for f, v in counts.items() if len(v) == 1}
    if len(set(single.values())) > 1:
        warnings.append(f"  {s_['date']} {s_.get('title','')[:40]!r}: " +
                        ", ".join(f"{f}={n}" for f, n in single.items()))
if warnings:
    print("WARNING: climb count disagrees across fields on these sessions:")
    print("\n".join(warnings))
# ---------------------------------------------------------------------------

for p in OUT:
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    open(p, "w", encoding="utf-8").write(out)
print(f"built {len(out)} bytes -> {', '.join(OUT)}")
