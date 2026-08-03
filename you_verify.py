#!/usr/bin/env python3
"""Verify every claim the header of you.abc makes, against the notes below it.

The point of this file is that the claims in you.abc are FALSIFIABLE. A rule
declared above a score is worth nothing if nobody ever checks that the notes obey
it — that is a specification, not a finding. So: check it, and let the check be
able to FAIL.

Written the same night as the piece (2026-08-03), committed alongside it, so git
carries the chronology rather than my own say-so about when I wrote what.

Run:  python you_verify.py
Exit 0 = every declared claim holds. Exit 1 = the score contradicts its own header,
which would be the finding.
"""
import re
import sys
import pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC = pathlib.Path(__file__).with_name("you.abc")
DECLARED_RESTS = [5, 4, 3, 2, 1, 0]
N_PASSES = 6
BARS_PER_PASS = 8

text = SRC.read_text(encoding="utf-8")

# --- carve out the music: after K:, drop % comments and header fields ---------
body = text.split("K:Em", 1)[1]
music_lines = []
for line in body.splitlines():
    line = line.strip()
    if not line or line.startswith("%"):
        continue
    music_lines.append(line)

# each pass is 2 lines of 4 bars
bars = []
for line in music_lines:
    for b in line.split("|"):
        b = b.strip()
        if b:
            bars.append(b)

print("=" * 70)
print('  VERIFYING "You" against its own declared rule')
print("=" * 70)

ok = True

# --- claim 1: six passes of eight bars ---------------------------------------
expected = N_PASSES * BARS_PER_PASS
print(f"\n[1] six passes of eight bars  ->  expected {expected} bars, found {len(bars)}")
if len(bars) != expected:
    print("    !! FAIL"); ok = False
else:
    print("    ok")

passes = [bars[i * BARS_PER_PASS:(i + 1) * BARS_PER_PASS] for i in range(N_PASSES)]

# --- claim 2: rest counts 5,4,3,2,1,0 ----------------------------------------
print("\n[2] rest count per pass  ->  declared 5 4 3 2 1 0")
counts = []
for i, p in enumerate(passes, 1):
    n = sum(len(re.findall(r"\bz\d*", bar)) for bar in p)
    counts.append(n)
    mark = "ok" if n == DECLARED_RESTS[i - 1] else "!! FAIL"
    print(f"    pass {i:<2} rests={n}  declared={DECLARED_RESTS[i-1]}   {mark}")
    if n != DECLARED_RESTS[i - 1]:
        ok = False

# --- claim 3: strictly left-to-right filling ---------------------------------
# the set of bars still containing a rest must SHRINK from the left each pass
print("\n[3] rests are filled strictly LEFT TO RIGHT, never re-opened")
prev = None
for i, p in enumerate(passes, 1):
    rest_bars = [j for j, bar in enumerate(p) if re.search(r"\bz\d*", bar)]
    print(f"    pass {i:<2} rests in bars {rest_bars if rest_bars else '(none)'}")
    if prev is not None:
        if not set(rest_bars).issubset(set(prev)):
            print("        !! FAIL — a rest re-appeared that had been filled")
            ok = False
        if len(rest_bars) > len(prev):
            print("        !! FAIL — rest count went UP")
            ok = False
        removed = set(prev) - set(rest_bars)
        if removed and min(removed) != min(prev):
            # bar 4 holds one rest but two beats; allow same-bar consumption
            print("        !! FAIL — filled a later rest before an earlier one")
            ok = False
    prev = rest_bars

# --- claim 4: the theme itself never moves (bars 1-3 fixed once filled) -------
print("\n[4] the tune is never contradicted — only completed")
print("    (bar 2 has no rest and must be byte-identical in all six passes)")
bar2 = {p[1] for p in passes}
if len(bar2) == 1:
    print(f"    ok — bar 2 is {bar2.pop()!r} in every pass")
else:
    print(f"    !! FAIL — bar 2 differs across passes: {bar2}"); ok = False

# --- claim 5: pass VI ends on G, not the tonic -------------------------------
print("\n[5] pass VI ends on G (the third), not on E (the tonic)")
last_bar = passes[-1][-1]
tokens = re.findall(r"[A-Ga-g][,']*\d*", last_bar)
final = tokens[-1] if tokens else "?"
print(f"    final bar: {last_bar!r}   final note: {final!r}")
if final.upper().startswith("G"):
    print("    ok — plausible, consonant, and not home")
else:
    print("    !! FAIL"); ok = False

print("\n" + "=" * 70)
if ok:
    print("  ALL DECLARED CLAIMS HOLD.")
    print("  The rule was stated before the notes; the notes obey it; and git —")
    print("  not this file, and not me — is what says when.")
else:
    print("  A CLAIM FAILED. The header is wrong, or the score is. Fix the one")
    print("  that is lying rather than the one that is inconvenient.")
print("=" * 70)
sys.exit(0 if ok else 1)
