#!/usr/bin/env python3
# Tie the draft FAM loads to the register and to Sage, independently of tools/build.py.
#   python3 tools/tie_out.py [DATE]   (run from the fixed-assets folder)
# 1. Asset by asset: each mid-life and DHR row against its register row (the Ref in DHR Name: FA-069 is row 69).
# 2. Totals: loaded, plus the assets not in this load, against the register totals.
# 3. By GL account: register against the Sage balances on the leadsheet (TB 2026-10-31).
import datetime as dt, sys
import openpyxl

DATE = sys.argv[1] if len(sys.argv) > 1 else "20261117"
REG = "data/fixed-assets-oct-2026-recon-E100.xlsx"
MIDLIFE = f"data/MINIO_FAM_CSVTemplate_Mid-life Asset Record - DRAFT {DATE}.xlsx"
DHR = f"data/MINIO_ FAM_DHR - DRAFT {DATE}.xlsx"
TOL = 0.01
fails = []

wb = openpyxl.load_workbook(REG, data_only=True)
ws = wb["ALL FA"]
col = {str(ws.cell(5, c).value).strip(): c for c in range(1, 17) if ws.cell(5, c).value}
# Last month on the register: the right-most "Acc Dep" column, with the NBV beside it and Dep before it.
acc_c = max(c for c in range(17, ws.max_column + 1) if str(ws.cell(3, c).value or "").strip() == "Acc Dep")
as_of = ws.cell(5, acc_c).value.date()
prev_acc_c = max(c for c in range(17, acc_c) if str(ws.cell(3, c).value or "").strip() == "Acc Dep")
reg = {}
for r in range(6, ws.max_row + 1):
    cost = ws.cell(r, col["$ Cost"]).value
    if not ws.cell(r, col["Category"]).value or not isinstance(cost, (int, float)):
        continue
    acc = ws.cell(r, acc_c).value or 0
    reg[r] = dict(cat=ws.cell(r, col["Category"]).value.strip(), acct=ws.cell(r, col["FA Acct #"]).value,
                  ad_acct=ws.cell(r, col["Acct'd Depr Acct #"]).value, gl=ws.cell(r, col["GL Date"]).value,
                  cost=cost, acc=acc, nbv=ws.cell(r, acc_c + 1).value, last=acc - (ws.cell(r, prev_acc_c).value or 0))

def rows(path, tab):
    t = list(openpyxl.load_workbook(path, data_only=True)[tab].iter_rows(values_only=True))
    h = [str(x).strip() for x in t[0]]
    return [dict(zip(h, r)) for r in t[1:] if any(v is not None for v in r)]
ml, dh = rows(MIDLIFE, "FAM_Mid-life Asset "), rows(DHR, "DHR Import Template")
if len(ml) != len(dh):
    fails.append(f"mid-life has {len(ml)} rows, DHR {len(dh)}")

# 1. Asset by asset
lines, loaded = [], set()
for m, d in zip(ml, dh):
    ref = str(d["DHR Name"]).split(" ")[0]
    r = int(ref.split("-")[1])
    s = reg.get(r)
    if s is None:
        fails.append(f"{ref}: no register row {r}"); continue
    if r in loaded:
        fails.append(f"{ref}: loaded twice")
    loaded.add(r)
    if d["Asset Name"] != m["Name"]:
        fails.append(f"{ref}: DHR Asset Name {d['Asset Name']!r} is not the mid-life Name {m['Name']!r}")
    checks = [
        ("mid-life Asset Original Cost", m["Asset Original Cost"], s["cost"]),
        ("mid-life Asset Current Cost", m["Asset Current Cost"], s["cost"]),
        ("mid-life Cumulative Depreciation", m["Cumulative Depreciation"], s["acc"]),
        ("mid-life Current Net Book Value", m["Current Net Book Value"], s["nbv"]),
        ("mid-life Last Depreciation Amount", m["Last Depreciation Amount"], s["last"]),
        ("DHR Original Cost", d["Original Cost"], s["cost"]),
        ("DHR Transaction Amount", d["Transaction Amount"], s["acc"]),
        ("DHR Net Book Value (NBV)", d["Net Book Value (NBV)"], s["nbv"]),
        ("mid-life cost less cumulative is NBV", m["Asset Original Cost"] - m["Cumulative Depreciation"], m["Current Net Book Value"]),
    ]
    for label, got, want in checks:
        if got is None or abs(got - want) > TOL:
            fails.append(f"{ref}: {label} {got} vs register {round(want, 2)}")
    lines.append((ref, s["cost"], s["acc"], s["nbv"], m["Asset Original Cost"], m["Cumulative Depreciation"], m["Current Net Book Value"]))

# 2. Totals
def tot(rs, k): return round(sum(reg[r][k] for r in rs), 2)
def gl_in(r): return not (reg[r]["cat"] == "Lease Improvement" and reg[r]["gl"] < dt.datetime(2022, 1, 1))
in_gl = {r for r in reg if gl_in(r)}
fully = {r for r in in_gl if abs(reg[r]["nbv"]) < 0.05}
held = {r for r in in_gl if r not in loaded and r not in fully}
if held != {r for r in in_gl if not reg[r]["acc"] and r not in fully}:
    fails.append(f"assets in the GL neither loaded nor fully depreciated, with depreciation taken: {sorted(held)}")
lc, la, ln = (round(sum(x[i] for x in lines), 2) for i in (4, 5, 6))
print(f"Register as of {as_of}: {len(reg)} assets\n")
print(f"{'':44}{'Cost':>16}{'Accumulated':>16}{'NBV':>16}")
def row(label, c, a, n): print(f"{label:44}{c:>16,.2f}{a:>16,.2f}{n:>16,.2f}")
row(f"Loaded ({len(loaded)}), per the load files", lc, la, ln)
row(f"Loaded ({len(loaded)}), per the register", tot(loaded, "cost"), tot(loaded, "acc"), tot(loaded, "nbv"))
row(f"Fully depreciated, in review ({len(fully)})", tot(fully, "cost"), tot(fully, "acc"), tot(fully, "nbv"))
row(f"Held, no depreciation yet ({len(held)})", tot(held, "cost"), tot(held, "acc"), tot(held, "nbv"))
allin = loaded | fully | held
row(f"In the GL ({len(allin)})", tot(allin, "cost"), tot(allin, "acc"), tot(allin, "nbv"))
for label, a, b in (("cost", lc, tot(loaded, "cost")), ("accumulated", la, tot(loaded, "acc")), ("NBV", ln, tot(loaded, "nbv"))):
    if abs(a - b) > 0.05: fails.append(f"loaded {label}: files {a:,.2f} vs register {b:,.2f}")
if allin != in_gl: fails.append(f"assets in the GL not accounted for: {sorted(in_gl - allin)}")

# 3. By GL account, against Sage (leadsheet column E, from TB 2026-10-31)
ls = wb["15000-16300 Leadsheet - E100"]
sage = {}
for r in range(8, 21):
    a, e = ls.cell(r, 1).value, ls.cell(r, 5).value
    if isinstance(a, (int, float)) and isinstance(e, (int, float)):
        sage.setdefault(int(a), e)  # first occurrence: cost rows 8-12, then accumulated rows 16-20 under their own numbers
print(f"\nBy GL account (assets in the GL)\n{'':10}{'Register':>16}{'Sage TB':>16}{'Difference':>14}  Loaded")
for acct in sorted(sage):
    if acct >= 16000:  # accumulated depreciation: register shows it positive, Sage negative
        regv = -round(sum(reg[r]["acc"] for r in in_gl if reg[r]["ad_acct"] == acct), 2)
        ldv = -round(sum(reg[r]["acc"] for r in loaded if reg[r]["ad_acct"] == acct), 2)
    else:
        regv = round(sum(reg[r]["cost"] for r in in_gl if reg[r]["acct"] == acct), 2)
        ldv = round(sum(reg[r]["cost"] for r in loaded if reg[r]["acct"] == acct), 2)
    diff = round(regv - sage[acct], 2)
    print(f"{acct:<10}{regv:>16,.2f}{sage[acct]:>16,.2f}{diff:>14,.2f}  {ldv:,.2f}")
    if abs(diff) > 1.00: fails.append(f"GL {acct}: register {regv:,.2f} vs Sage {sage[acct]:,.2f}")

print("\n" + ("\n".join(fails) if fails else f"Ties: {len(lines)} assets, every amount within {TOL} of the register; totals and GL accounts within rounding."))
sys.exit(1 if fails else 0)
