#!/usr/bin/env python3
"""Generate the 189 dated sessions + .ics for Beerwah@Night 2027 program.
Source of truth: beerwahnight2027program.md (26 Jul 2026)."""
import json, datetime as dt

START = dt.date(2026, 7, 27)  # Week 1 Monday
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# wk: (phase, km, vert, distribution, down, note)
WEEKS = {
    1:  ("0 Ramp", 18, 100, "easy", False, "BASELINE 5km TT"),
    2:  ("0 Ramp", 22, 200, "easy", False, "Rainbow Beach 11km Sat (easy, not raced)"),
    3:  ("0 Ramp", 19, 100, "easy", True,  "Recovery week after the sand"),
    4:  ("0 Ramp", 24, 150, "easy", False, ""),
    5:  ("1 Base", 27, 250, "pyramidal", False, "Heavy lifting begins. Downhill work begins."),
    6:  ("1 Base", 30, 300, "pyramidal", False, ""),
    7:  ("1 Base", 33, 350, "pyramidal", False, ""),
    8:  ("1 Base", 24, 200, "pyramidal", True,  "Down week. 5km TT #2"),
    9:  ("1 Base", 36, 400, "pyramidal", False, ""),
    10: ("1 Base", 39, 450, "pyramidal", False, ""),
    11: ("2 Build", 42, 550, "pyramidal", False, "Plyometrics begin"),
    12: ("2 Build", 32, 350, "pyramidal", True,  "Down week"),
    13: ("2 Build", 44, 650, "pyramidal", False, ""),
    14: ("2 Build", 47, 700, "pyramidal", False, ""),
    15: ("2 Build", 50, 800, "pyramidal", False, ""),
    16: ("2 Build", 38, 500, "pyramidal", True,  "Down week. 5km TT #3. Head torch in use."),
    17: ("2 Build", 52, 850, "pyramidal", False, "Peak lifting load"),
    18: ("3 Specific", 52, 900, "polarized", False, "Night running begins. Head torch required."),
    19: ("3 Specific", 40, 600, "polarized", True,  "Down week. RACE: Beerwah@Daybreak Sun 6 Dec"),
    20: ("3 Specific", 52, 950, "polarized", False, "SEQ summer = natural heat acclimation. Easy runs in daytime heat when convenient."),
    21: ("3 Specific", 52, 1000, "polarized", False, ""),
    22: ("3 Specific", 42, 650, "polarized", True,  "Down week"),
    23: ("3 Specific", 50, 950, "polarized", False, "5km TT #4. Final go/no-go on the A goal."),
    24: ("4 Sharpen", 46, 800, "polarized", False, "Full course rehearsal at Beerwah, at night"),
    25: ("4 Sharpen", 44, 750, "polarized", False, "Last hard descent session. Last heavy lift."),
    26: ("5 Taper", 28, 400, "polarized", False, "Taper: volume ~-45%, intensity + frequency retained. HEAT TOP-UP week: easy runs in the heat of the day + optional 30 min ~40C bath after."),
    27: ("5 Taper", 16, 200, "polarized", False, "RACE SAT 30 JAN 7:00PM. Last heat exposure Wed, nothing after."),
}

KM_SPLIT = {"Tue": .18, "Wed": .13, "Thu": .16, "Fri": .09, "Sat": .32, "Sun": .12}
VERT_SPLIT = {"Tue": .05, "Thu": .35, "Sat": .50, "Sun": .10}

WU_QUALITY = ""
WU_TT = ""
WU_HILL = ""
WU_LONG = ""
WU_STRENGTH = "Done after the run. Before first work set: 2 warm-up sets at ~50% and ~70% of working load."

EASY_TXT = "Easy pace: 6:35-6:55/km, HR under 138, conversational in full sentences. Uphills by effort/HR, never pace. Zones reset at the Week 8 TT."

def phase_no(phase):
    return int(phase.split()[0])

def q1(wk, phase):
    p = phase_no(phase)
    if wk == 8:  return ("5km Time Trial #2", "5km TT, maximal. Do it at a Saturday parkrun if the timing works - real competition pacing beats a solo effort. This resets all zones. " + WU_TT, True)
    if wk == 16: return ("5km Time Trial #3", "5km TT, flat, maximal. Progress gate: needs meaningful movement toward 21:30. " + WU_TT, True)
    if wk == 23: return ("5km Time Trial #4", "5km TT, flat, maximal. Final go/no-go on the A goal. " + WU_TT, True)
    if p == 0: return ("Easy + strides", "Easy run at " + EASY_TXT + " Then 6 x 20s strides on flat: build to ~90% speed, tall and relaxed, NOT sprinting. Walk 60-90s between each. Strides train the legs, the easy running trains the engine.", False)
    if p == 1: return ("Hill sprints", "Easy run + 8 x 20s hill sprints (steep), walk-down full recovery. " + WU_HILL, False)
    if p == 2:
        prog = {11: "3 x 8 min @ threshold (5:40-5:50/km), 2 min jog", 12: "2 x 8 min @ threshold, 2 min jog (down week)",
                13: "4 x 8 min @ threshold, 2 min jog", 14: "4 x 8 min @ threshold, 2 min jog",
                15: "5 x 1km @ threshold, 90s jog", 17: "5 x 1km @ threshold, 90s jog"}
        return ("Sub-threshold", prog.get(wk, "Threshold session") + ". CONTROL: comfortably hard, 5:40-5:50/km cap, HR 155-170, you could still say a short sentence. NOT race pace, and if in doubt go slower - the Norwegian rule is that sub-threshold repeated beats threshold exceeded. " + WU_QUALITY, False)
    if p == 3:
        prog = {18: "5 x 3 min hard (5:20-5:25/km), 2 min jog", 19: "4 x 3 min hard, 2 min jog (down week)",
                20: "5 x 3 min hard, 2 min jog", 21: "6 x 3 min hard, 2 min jog", 22: "4 x 3 min hard, 2 min jog (down week)"}
        return ("VO2 intervals", prog.get(wk, "VO2 session") + ". " + WU_QUALITY, False)
    if p == 4: return ("Trail reps", "8 x 90s hard w/ 90s jog, on trail. " + WU_QUALITY, False)
    return ("Taper reps", "4 x 90s hard w/ 90s jog. Same effort as Sharpen, half the volume. " + WU_QUALITY, False)

def q2(wk, phase):
    p = phase_no(phase)
    night = wk >= 18
    if p == 0: return ("Easy rolling terrain", "Easy rolling run on trail, no intensity. " + EASY_TXT + " " + WU_LONG, night)
    if p == 1:
        d = "8-10 x 60s steep uphill (effort, not pace), jog down."
        if wk >= 5: d += " Run each descent controlled and deliberate — downhill exposure starts now."
        return ("Hill reps + descents", d + " " + WU_HILL, night)
    if p == 2: return ("Hill reps + fast descents", "10-12 x 60s uphill hard, FAST controlled descent on each recovery. " + WU_HILL, night)
    if p == 3: return ("Climb + descend" + (" (night)" if night else ""), "6 x 2-3 min climb at effort + fast controlled descent. " + ("After dark, head torch. " if night else "") + WU_HILL, night)
    if p == 4:
        if wk == 25: return ("LAST hard descent session (night)", "5 x 2 min climb at race effort + hard descent. This is the final hard downhill of the block — nothing eccentric after this. " + WU_HILL, True)
        return ("Race-effort climbs (night)", "5 x 2 min climb at race effort + descent. Night, head torch. " + WU_HILL, True)
    return ("Race-effort touches (night)", "3 x 2 min at race effort, night, head torch. " + WU_HILL, True)

def longrun(wk, phase, km):
    p = phase_no(phase)
    night = p == 3 and wk % 2 == 0  # 18, 20, 22
    if wk == 2:  return ("RACE (easy): Rainbow Beach 11km", "8:00am start, Phil Rogers Park. NOT raced — conversational effort, WALK the dunes, finish feeling like you could do it again. Highest injury-risk day of the early block. Expect 2-4 days calf soreness.", False, 11)
    if wk == 19: return ("Shakeout + strides", "4km easy + 4 x 20s strides. Race is TOMORROW morning.", False, 4)
    if wk == 24: return ("FULL COURSE REHEARSAL — Beerwah, night", "Full course at Beerwah, at night, full race kit: 500+ lumen dual-beam head torch (flood for footing, spot for descents) + backup, trail shoes, caffeine at 6pm, water only. Run the Dungeon at race effort, power-hike the steep walls, practise FAST descending in torchlight - that is where the field loses 30-90s/km. Rehearse the 4pm snack + 6pm caffeine timing too.", True, 12)
    if wk == 25: return ("Long run w/ race-effort blocks", "14km with 2 x 10 min at race effort on trail. " + WU_LONG, False, 14)
    if wk == 26: return ("Taper long run", "12km easy trail with 3-4 strides late. " + WU_LONG, False, 12)
    if wk == 27: return ("RACE: BEERWAH@NIGHT 10km - 7:00PM", "THE ONE. Official course: ~10.4km / 294m gain. Day plan: carb-heavy lunch, light carb snack ~4pm, caffeine ~250-400mg at 6pm, pre-load fluids + electrolytes (humid 25C+ start). WU: 15 min easy + drills + 3 strides, done by 6:45pm. START POSITION: seed yourself top 10 into the first single track - passing in torchlight is expensive. Pace the first climb conservatively, race the mostly-uphill final 3km: that is where this course is decided. Power-hike the Dungeon walls. Water only on course. A goal: sub-50.", True, 12)
    if p == 0: return ("Long easy trail", f"{km}km easy trail. Walk the steep parts. " + EASY_TXT + " " + WU_LONG, False, km)
    if p == 1: return ("Long trail + hard descent", f"{km}km easy trail with real climbing; run ONE descent segment hard. " + WU_LONG, False, km)
    if p == 2: return ("Long progressive trail", f"{km}km on technical ground, final 20% progressive to steady. " + WU_LONG, False, km)
    if p == 3: return ("Long w/ race-effort" + (" (night)" if night else ""), f"{km}km with 2 x 10 min at race effort. " + ("Night run, head torch. " if night else "") + WU_LONG, night, km)
    return ("Long run", f"{km}km. " + WU_LONG, False, km)

REST = {"dbfloor":90, "pushup":60, "latraise":60, "dbrow":75, "hollow":45, "rdfly":60, "carry":75, "situp":45,
        "squat":150, "rdl":120, "bss":90, "calf_str":90, "calf_bent":60, "deadbug":45, "plank":45,
        "stepup":90, "slrdl":90, "hipthrust":90, "backext":60, "dbpress":90, "pallof":45,
        "pogo":90, "splitjump":90, "slhop":90,
        "wallsit":60, "stepdown":60, "tib":60, "sl_balance":30, "hip9090":30, "couch":0}

def ex(k, name, scheme, note="", load=True):
    try: sets = int(scheme.strip().split(" x ")[0])
    except Exception: sets = 3
    return dict(k=k, name=name, scheme=scheme, note=note, load=load, sets=sets, rest=REST.get(k, 90))

PLYOS = [ex("pogo", "Pogo hops", "3 x 20", "do these FIRST, straight after warm-up", False),
         ex("splitjump", "Split jumps", "3 x 10 each leg", "", False),
         ex("slhop", "Single-leg hops", "3 x 8 each leg", "", False)]

def strength_a(p, down):
    if down:
        sq = ex("squat", "Back squat (high bar, wide grip)", "2 x 5", "deload week: moderate load, nothing hard")
        sets = "2"
    elif p <= 0:
        sq = ex("squat", "Back squat (high bar, wide grip)", "3 x 8", "stop 3 reps short of failure")
        sets = "3"
    elif p <= 2:
        sq = ex("squat", "Back squat (high bar, wide grip)", "4 x 5", "heavy (~80-85%): stop 1-2 reps short of failure. At the 115kg plate ceiling, progress with a 3-sec lower + 2-sec pause, not load")
        sets = "3"
    else:
        sq = ex("squat", "Back squat (high bar, wide grip)", "3 x 4", "maintenance: stop 2-3 reps short of failure")
        sets = "2"
    n = int(sets)
    return [sq,
        ex("rdl", "Romanian deadlift", f"{min(n,3)} x {6 if p>=1 and not down else 8}", "moderate load, hinge not squat, replaces conventional deadlifts (back rule)"),
        ex("bss", "Bulgarian split squat", f"{min(n,3) if not down else 2} x 8 each leg", "22.5kg dumbbells"),
        ex("calf_str", "Calf raise, straight knee", f"{'2' if down else ('4' if p<=2 else '3')} x 12", "3-second slow lower" + ("" if p<1 else ", loaded")),
        ex("calf_bent", "Calf raise, bent knee (soleus)", ("2" if down else "3") + " x 15", "", False),
        ex("deadbug", "Dead bug", ("2" if down or p>=3 else "3") + " x 10", "", False),
        ex("plank", "Side plank", ("2" if down or p>=3 else "3") + (" x 30s each side" if p<=0 else " x 40s each side"), "", False)]

def strength_b(down):
    s = "2" if down else "3"
    return [ex("stepup", "Dumbbell step-ups", f"{s} x 10 each leg"),
        ex("slrdl", "Single-leg Romanian deadlift", f"{s} x 8 each leg"),
        ex("hipthrust", "Hip thrust (shoulders on bench)", f"{s} x 12"),
        ex("backext", "Back extension", f"{s} x 12", "", False),
        ex("dbpress", "Neutral-grip dumbbell press", f"{s} x 8", "SKIP if the elbow objects"),
        ex("pallof", "Pallof press", f"{s} x 10 each side", "band or cable", False)]

MONDAY_COND = [
    ex("wallsit", "Wall sit", "3 x 45s", "quad + knee-tendon isometric, builds patellar tendon capacity", False),
    ex("stepdown", "Slow step-downs", "3 x 10 each leg", "off a low step, 3-second lower, knee tracking over the toes", False),
    ex("tib", "Tibialis raises", "3 x 15", "toes-up against a wall, shin and ankle armour for descents", False),
    ex("sl_balance", "Single-leg balance", "2 x 30s each leg", "eyes open then closed, ankle-proprioception for night trails", False),
    ex("hip9090", "90/90 hip switches", "2 x 8 each side", "", False),
    ex("couch", "Couch stretch + ankle rocks", "2 min each side", "hip flexors + ankle dorsiflexion", False),
]

def upper_a(down):
    s2 = "2" if down else "3"
    return ("Upper A - chest, shoulders, core",
        "Keeps the upper-body progress without touching leg recovery. Moderate loads, stop 2-3 reps short of failure. Elbow rules: neutral grips only, skip anything that twinges.",
        [ex("dbfloor", "Neutral-grip DB bench press", f"{s2} x 10", "palms facing each other - the easiest press on the elbows"),
         ex("pushup", "Push-ups", "2 x max minus 2", "stop 2 short of failure", False),
         ex("latraise", "Lateral raises", f"{s2} x 12", "light DBs, strict, no swinging"),
         ex("dbrow", "Single-arm DB row", f"{s2} x 10 each side", "neutral grip, other hand braced on the bench - SKIP if the elbow objects"),
         ex("hollow", "Hollow hold", f"{s2} x 20s", "lower back pressed flat into the floor", False)])

def upper_b(down):
    s2 = "2" if down else "3"
    return ("Upper B - shoulders, back, core",
        "Second upper day. Rule: never at the cost of a run. If you're flat, THIS is the session that gets dropped, not the km.",
        [ex("dbpress", "Neutral-grip DB shoulder press", f"{s2} x 8", "SKIP if the elbow objects"),
         ex("rdfly", "Rear-delt fly", f"{s2} x 12", "light, hinge forward or chest on an incline bench"),
         ex("pushup", "Push-up burnout", "2 x max minus 2", "", False),
         ex("carry", "Farmer carry", "2 x 40m", "22.5kg DBs, tall posture, crush the grip - elbow-safe arm work"),
         ex("situp", "Weighted sit-up", f"{s2} x 10", "plate hugged to chest", False)])

def strength(wk, day, down):
    p = phase_no(WEEKS[wk][0])
    if wk >= 27: return None  # race week: nothing
    if wk == 26:
        if day == "Tue":
            return ("Strength taper - neuromuscular maintenance", "10 days out. Keeps the economy gains without fatigue: intensity stays, volume halves. Last barbell session of the block.",
                [ex("squat", "Back squat (high bar, wide grip)", "2 x 4", "same load as last week, crisp reps, stop 3 short of failure"),
                 ex("calf_str", "Calf raise, straight knee", "2 x 12", "loaded"),
                 ex("pogo", "Pogo hops", "2 x 15", "springy, low effort", False)])
        return ("Plyo touch (5 min)", "4-5 days of light spring only from here. No weights.",
                [ex("pogo", "Pogo hops", "2 x 12", "", False),
                 ex("slhop", "Single-leg hops", "2 x 6 each leg", "springy, effortless", False)])
    if day == "Tue":
        exs = (PLYOS if (wk >= 11 and not down) else []) + strength_a(p, down)
        return ("Strength A — heavy lower" + (" (deload)" if down else ""),
                "After the run, evening if possible. Warm up each big lift with 2 ramp-up sets (~50% then ~70% of working weight). Squat grip: high bar, wide grip, elbows down and back (elbow rule).", exs)
    else:
        return ("Strength B — single leg" + (" (deload)" if down else ""),
                "After the run. Lighter day: single-leg control, not grinding. 2 ramp-up sets before anything heavy.", strength_b(down))

def km_for(wk, day, km_week):
    v = round(km_week * KM_SPLIT.get(day, 0) * 2) / 2
    return v

sessions = []
sid = 0
for wk in range(1, 28):
    phase, km_w, vert_w, dist, down, note = WEEKS[wk]
    monday = START + dt.timedelta(days=(wk - 1) * 7)
    for i, day in enumerate(DAYS):
        date = monday + dt.timedelta(days=i)
        heat = wk in (26,) and day in ("Wed", "Fri")
        base = dict(week=wk, phase=phase, date=date.isoformat(), day=day, is_down=down, is_night=False, is_test=False, is_race=False, km=0, vert=0, type="rest")
        entries = []
        if day == "Mon":
            if wk == 1:
                entries.append(dict(base, type="test", is_test=True, title="Baseline 5km TT — DONE",
                    prescription="Completed 27 Jul: 5.01km in 27:46 (5:33/km), avg HR 169, 90% effort. Est. max 26:40. Zones set from this.", km=5, done=True))
            elif wk >= 26:
                entries.append(dict(base, type="rest", title="Rest / light mobility only", prescription="Taper: full rest or a 20 min walk and light stretching. No conditioning circuit now, freshness is the goal."))
            else:
                entries.append(dict(base, type="cond", title="Joint conditioning + mobility (~20 min)", prescription="Rest day from running. This circuit is the knee/ankle/tendon insurance policy: light, controlled, never to failure.", exercises=MONDAY_COND))
                if wk <= 25:
                    ua = upper_a(down)
                    entries.append(dict(base, type="strength", title=ua[0], prescription=ua[1], exercises=ua[2]))
        elif day == "Tue":
            t, p, is_tt = q1(wk, phase)
            k = 5 if is_tt else km_for(wk, day, km_w)
            entries.append(dict(base, type="quality", is_test=is_tt, title=t, prescription=p, km=k, vert=round(vert_w * VERT_SPLIT.get("Tue", 0) / 10) * 10))
            s = strength(wk, "Tue", down)
            if s: entries.append(dict(base, type="strength", title=s[0], prescription=s[1], exercises=s[2]))
        elif day == "Wed":
            entries.append(dict(base, type="easy", title="Easy run" + (" (heat)" if heat else ""), km=km_for(wk, day, km_w),
                prescription=("HEAT TOP-UP: run in the heat of the day, easy only, and consider a 30 min hot bath (~40C) straight after. " if heat else "") + "Conversational, 6:35-6:55/km, HR under 138. Flat or gently rolling. NO grey zone."))
        elif day == "Thu":
            t, p, night = q2(wk, phase)
            entries.append(dict(base, type="terrain", is_night=night, title=t, prescription=p, km=km_for(wk, day, km_w), vert=round(vert_w * VERT_SPLIT["Thu"] / 10) * 10))
            s = strength(wk, "Thu", down)
            if s: entries.append(dict(base, type="strength", title=s[0], prescription=s[1], exercises=s[2]))
        elif day == "Fri":
            entries.append(dict(base, type="easy", title="Easy run (optional)" + (" (heat)" if heat else ""), km=km_for(wk, day, km_w),
                prescription=("HEAT TOP-UP run if taken: heat of the day, easy only. " if heat else "") + "Optional recovery run, conversational. FIRST session to drop when fatigue accumulates."))
            if wk <= 25:
                ub = upper_b(down)
                entries.append(dict(base, type="strength", title=ub[0], prescription=ub[1], exercises=ub[2]))
        elif day == "Sat":
            t, p, night, k = longrun(wk, phase, km_for(wk, day, km_w))
            is_race = wk in (2, 27)
            entries.append(dict(base, type="long" if not is_race else "race", is_race=is_race, is_night=night, title=t, prescription=p, km=k, vert=round(vert_w * VERT_SPLIT["Sat"] / 10) * 10))
        else:  # Sun
            if wk == 19:
                entries.append(dict(base, type="race", is_race=True, title="RACE: Beerwah@Daybreak 10km", km=10, vert=210,
                    prescription="Dress rehearsal, same course, daylight. TARGET 50:00-51:30. GO/NO-GO gate: sub-51:30 ahead of schedule; 51:30-53 on plan; 53-56 A needs a perfect 8 weeks; over 56 recalibrate to B/C. Full race-day routine."))
            elif wk == 27:
                entries.append(dict(base, type="rest", title="Rest. It's done.", prescription="Recovery. Debrief when ready."))
            else:
                entries.append(dict(base, type="easy", title="Recovery run", km=km_for(wk, day, km_w),
                    prescription="Easy recovery, conversational, flat. 6:35-6:55/km, HR under 138.", vert=round(vert_w * VERT_SPLIT.get("Sun", 0) / 10) * 10))
        for e in entries:
            sid += 1
            e["id"] = sid
            sessions.append(e)

# --- reconcile weekly totals with targets ---
def wk_sessions(wk):
    return [s for s in sessions if s["week"] == wk and s["type"] != "strength"]

# Ramp weeks 1-4: explicit consolidated splits — no junk 2km runs, Fri/Sun rest instead.
# Weekly totals unchanged (wk1 incl 5km TT, wk2 incl 11km race).
OVERRIDE = {
    1: {"Tue": 3, "Wed": 3, "Thu": 3, "Fri": 0, "Sat": 4, "Sun": 0},
    2: {"Tue": 3.5, "Wed": 4, "Thu": 3.5, "Fri": 0, "Sun": 0},  # Sat = race 11km
    3: {"Tue": 3.5, "Wed": 4, "Thu": 3.5, "Fri": 0, "Sat": 5, "Sun": 3},
    4: {"Tue": 4, "Wed": 4, "Thu": 4, "Fri": 3, "Sat": 6, "Sun": 3},
    27: {"Tue": 5, "Wed": 4, "Thu": 4, "Fri": 3, "Sat": 12, "Sun": 0},
}
for wk, days in OVERRIDE.items():
    for s in wk_sessions(wk):
        if s["is_test"] or s["is_race"]: continue
        if s["day"] in days: s["km"] = days[s["day"]]
# All other weeks: 3km floor on any run (Fri drops to rest instead), then reconcile totals.
for wk in range(5, 27):
    target = WEEKS[wk][1]
    for s in wk_sessions(wk):
        if s["type"] in ("easy",) and 0 < s["km"] < 3:
            s["km"] = 0 if s["day"] == "Fri" else 3
    adjustable = [s for s in wk_sessions(wk) if s["type"] == "easy" and s["km"] > 0]
    guard = 0
    while adjustable and guard < 60:
        delta = target - sum(s["km"] for s in wk_sessions(wk))
        if abs(delta) < 0.5: break
        step = 0.5 if delta > 0 else -0.5
        moved = False
        for s in sorted(adjustable, key=lambda x: x["km"], reverse=(delta < 0)):
            if step < 0 and s["km"] <= 3: continue
            s["km"] = round((s["km"] + step) * 2) / 2
            moved = True
            break
        if not moved: break
        guard += 1
# Convert any zeroed easy runs to proper rest days
for s in sessions:
    if s["type"] == "easy" and s["km"] == 0:
        s["type"] = "rest"; s["title"] = "Rest"
        s["prescription"] = "Scheduled rest — this week's volume is consolidated into fewer, longer runs. A 20-30 min walk is fine."

# --- Week 2 adjustment (3 Aug 2026): flu return + unplanned birthday run ---
# Mitch ran 3.5km @5:26/km (HR 171, RPE ~8.5) Mon arvo instead of cond+Upper A.
# Mon = the run (done). Cond + Upper A move to Tue. Tue strides run + Strength A dropped
# (missed sessions drop, never stack; no heavy lower 3 days post-flu with a race Sat).
# Thu Strength B lightened. Fri Upper B dropped -> pure rest before Rainbow Beach.
_moved = [s for s in sessions if s["date"] == "2026-08-03" and s["type"] in ("cond", "strength")]
for s in _moved:
    s["date"] = "2026-08-04"; s["day"] = "Tue"
for s in sessions:
    if s["date"] == "2026-08-04" and s["title"] == "Easy + strides":
        s["date"] = "2026-08-03"; s["day"] = "Mon"; s["type"] = "easy"
        s["title"] = "Run - DONE (birthday run)"
        s["prescription"] = ("Completed: 3.5km at 5:26/km, avg HR 171, RPE ~8.5. Unplanned afternoon run, "
            "first session back after the flu. Felt strong, natural stride, slightly puffed late. "
            "Counts as this week's Tuesday run - do NOT run again Tuesday.")
sessions[:] = [s for s in sessions if not (s["date"] == "2026-08-04" and s["title"].startswith("Strength A"))]
sessions[:] = [s for s in sessions if not (s["date"] == "2026-08-07" and s["title"].startswith("Upper B"))]
for s in sessions:
    if s["date"] == "2026-08-04" and s["type"] == "cond":
        s["prescription"] = ("Moved from Monday. No running today - yesterday's run covered it. " + s["prescription"])
    if s["date"] == "2026-08-06" and s["title"].startswith("Strength B"):
        s["title"] = "Strength B (light) - single leg"
        s["prescription"] = ("First lift back after the flu and the race is in 2 days: 2 sets of everything at "
            "~80% of your usual weights, 3+ reps in reserve (reps you could still do). Crisp, controlled, "
            "nothing close to grinding. The point is to switch the legs back on, not load them.")
        for e in s.get("exercises", []):
            e["sets"] = min(e.get("sets", 2), 2)
            if " x " in e.get("scheme", ""):
                e["scheme"] = "2 x " + e["scheme"].split(" x ", 1)[1]
    if s["date"] == "2026-08-08" and s.get("is_race"):
        s["prescription"] += (" POST-FLU RULE: start only if you feel 100% on the morning and resting HR is back "
            "at baseline. Cap HR at 155 the whole way, walk the dunes, treat it as a supported long run.")

# --- structured warm-ups / cool-downs ---
SWINGS_FB = ["Leg swings, front-back", "10 each leg", "Hold a wall, swing one leg forward and back like a pendulum. Relaxed, a little bigger each rep."]
SWINGS_SIDE = ["Leg swings, side-to-side", "10 each leg", "Face the wall, swing the leg across your body then out wide. Opens the hips."]
SWEEPS = ["Hamstring sweeps", "10 total, walking", "The ground-sweep one: step a heel forward with the leg straight, hinge and sweep both hands down past your foot as you rock over it. Alternate legs walking forward."]
ANKLE = ["Ankle wall rocks", "10 each side", "Foot about 10cm from a wall, drive the knee forward to touch the wall, heel stays down. Preps the ankle and calf for load."]
ASKIP = ["A-skips", "2 x 20m", "A rhythmic skip driving one knee up tall each step. Light, springy, off the ground fast."]
HIGHKNEES = ["High knees", "2 x 20m", "Fast little steps driving knees to hip height, tall posture, arms pumping."]
STRIDES4 = ["Strides", "4 x 20s", "Build to ~90% of top speed, tall and relaxed, NOT sprinting. Walk back between each. Do the last one 2 min before the session starts."]
STRIDES_HILL = ["2 strides on the hill", "2 x 15s", "On the grade you are about to work on, at a fast-but-relaxed effort. Wakes the calves up for climbing."]
CLAM = ["Clamshells", "10 each side", "Lie on your side, knees bent, heels together. Lift the top knee like a clam opening without rolling your hips back. You should feel the side of your glute switch on."]
BRIDGE = ["Glute bridges", "10 slow", "On your back, knees bent, drive hips up and squeeze the glutes hard at the top for 2 seconds."]
BWSQUAT = ["Bodyweight squats", "10 slow", "Full depth, controlled, arms out front. Greases the exact pattern before load goes on."]
JOG10 = ["Easy jog", "10 min", "Properly easy for 8 min, building to steady over the last 2. This is most of the warm-up."]
JOG_HILL = ["Easy jog to the hill", "10-15 min", "Use the run to the bottom of the hill as the warm-up. Arrive warm, not fresh off the car seat."]
WALK3 = ["Brisk walk", "2-3 min", "Just get the blood moving before the drills."]
SLOWK = ["First km at shuffle pace", "", "Slower than easy pace. This IS part of the warm-up, not wasted time."]
SLOW2K = ["First 2km slower than easy", "", "Ease into it. Long-run injuries happen in cold first kilometres."]
TT_PRIME = ["Pace primer", "2 min at target pace", "Then 3 min easy, then start. Tells the legs what is coming so the first km is not a shock."]
RAMPUP = ["Ramp-up sets", "2 sets", "Before the first heavy exercise: one set at ~50% of working weight, one at ~70%. Then work sets."]

CD_WALK = ["Walk it off", "3-5 min", "Do not stop dead at the driveway. Walk until breathing is normal."]
CD_JOG = ["Easy jog down", "10 min", "Genuinely easy. This is where the session gets absorbed."]
CD_CALF_STR = ["Calf stretch, straight knee", "30s each side", "Hands on wall, back leg straight, heel down, lean in until the big calf muscle pulls."]
CD_CALF_BENT = ["Calf stretch, bent knee", "30s each side", "Same position, bend the back knee. Moves the stretch to the soleus, the deep calf that trail running hammers."]
CD_QUAD = ["Standing quad stretch", "30s each side", "Grab the ankle behind you, knees together, push the hips slightly forward."]
CD_HIPFLEX = ["Hip flexor stretch", "30s each side", "Half-kneel, tuck the tailbone, shift forward until the front of the back hip pulls."]
CD_HAM = ["Gentle hamstring stretch", "30s each side", "Heel on a low step, straight back, hinge at the hips. Gentle, never yanked."]

WUCD = {
  "easy":    (4,  [SWINGS_FB, SWINGS_SIDE, ANKLE, SLOWK],                       4, [CD_WALK, CD_CALF_STR, CD_CALF_BENT]),
  "quality": (18, [JOG10, SWINGS_FB, SWEEPS, ASKIP, HIGHKNEES, STRIDES4],       13, [CD_JOG, CD_CALF_STR, CD_CALF_BENT, CD_QUAD]),
  "terrain": (15, [JOG_HILL, SWINGS_FB, SWEEPS, STRIDES_HILL],                  13, [CD_JOG, CD_CALF_STR, CD_CALF_BENT, CD_HIPFLEX]),
  "long":    (5,  [WALK3, SWINGS_FB, ANKLE, SLOW2K],                            6, [CD_WALK, CD_CALF_STR, CD_CALF_BENT, CD_QUAD, CD_HIPFLEX]),
  "race":    (20, [JOG10, SWINGS_FB, SWEEPS, STRIDES4],                         8, [CD_WALK, CD_CALF_STR, CD_CALF_BENT, CD_HAM]),
  "strength":(5,  [BRIDGE, CLAM, BWSQUAT, RAMPUP],                              0, []),
}
for s in sessions:
    ty = s["type"]
    if ty == "quality" and s.get("is_test"):
        m, items, cm, citems = WUCD["quality"]
        s["wu"] = {"mins": m, "items": items + [TT_PRIME]}
        s["cd"] = {"mins": cm, "items": citems}
    elif ty in WUCD:
        m, items, cm, citems = WUCD[ty]
        s["wu"] = {"mins": m, "items": items}
        if citems: s["cd"] = {"mins": cm, "items": citems}

# --- sanity: weekly km sums vs target
for wk in range(1, 28):
    tot = sum(s["km"] for s in sessions if s["week"] == wk and s["type"] != "strength")
    print(f"wk{wk}: target {WEEKS[wk][1]}km -> planned {tot}km")

with open("sessions.json", "w") as f:
    json.dump(sessions, f, indent=1)
print(f"\n{len(sessions)} session entries, {len(set(s['date'] for s in sessions))} days")

# --- ICS ---
def ics_escape(s):
    return s.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")

lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Beerwah2027//Training//EN", "CALSCALE:GREGORIAN",
         "X-WR-CALNAME:Beerwah@Night 2027 Training", "X-WR-TIMEZONE:Australia/Brisbane"]
by_date = {}
for s in sessions:
    by_date.setdefault(s["date"], []).append(s)
for date, entries in sorted(by_date.items()):
    d = date.replace("-", "")
    nxt = (dt.date.fromisoformat(date) + dt.timedelta(days=1)).isoformat().replace("-", "")
    runs = [e for e in entries if e["type"] != "strength"]
    lifts = [e for e in entries if e["type"] == "strength"]
    main = runs[0]
    title = f"W{main['week']} {main['title']}"
    if main.get("km"): title += f" ({main['km']}km)"
    if lifts: title += " + " + ("Str A" if "A" in lifts[0]["title"] else "Str B")
    desc = main["prescription"]
    for l in lifts:
        desc += "\n\n" + l["title"] + ": " + l["prescription"]
    ev = ["BEGIN:VEVENT", f"UID:beerwah27-{d}@claude", f"DTSTAMP:{d}T000000Z"]
    if main["week"] == 27 and main["day"] == "Sat":
        ev += [f"DTSTART;TZID=Australia/Brisbane:{d}T190000", f"DTEND;TZID=Australia/Brisbane:{d}T210000"]
    elif main["week"] == 2 and main["day"] == "Sat":
        ev += [f"DTSTART;TZID=Australia/Brisbane:{d}T080000", f"DTEND;TZID=Australia/Brisbane:{d}T100000"]
    else:
        ev += [f"DTSTART;VALUE=DATE:{d}", f"DTEND;VALUE=DATE:{nxt}"]
    ev += [f"SUMMARY:{ics_escape(title)}", f"DESCRIPTION:{ics_escape(desc)}", "END:VEVENT"]
    lines += ev
lines.append("END:VCALENDAR")
with open("beerwah-2027-plan.ics", "w") as f:
    f.write("\r\n".join(lines) + "\r\n")
print("ics written")
