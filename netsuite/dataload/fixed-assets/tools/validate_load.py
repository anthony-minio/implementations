#!/usr/bin/env python3
# Check the review list and the two filled SOA templates against the register, independently of tools/build.py.
#   python3 tools/validate_load.py [DATE]   (run from the fixed-assets folder; DATE defaults to the build's)
# Reads the register by header text rather than by fixed column, and checks every output row back to its source row.
import datetime as dt, sys
import openpyxl

DATE = sys.argv[1] if len(sys.argv) > 1 else "20261117"
SRC = "data/fixed-assets-oct-2026-recon-E100.xlsx"
REVIEW = f"data/MinIO_Fully_Depreciated_Assets_for_Review_{DATE}.xlsx"
WORK = f"data/MinIO_Fixed_Asset_Load_Working_{DATE}.xlsx"
MIDLIFE = f"data/MINIO_FAM_CSVTemplate_Mid-life Asset Record - DRAFT {DATE}.xlsx"
DHR = f"data/MINIO_ FAM_DHR - DRAFT {DATE}.xlsx"
issues = []
def bad(msg): issues.append(msg)
def close(a, b, tol=0.015): return a is not None and b is not None and abs(float(a) - float(b)) <= tol
def day(v): return v.date() if isinstance(v, dt.datetime) else v

wb = openpyxl.load_workbook(SRC, data_only=True)
ws = wb["ALL FA"]
hdr = {str(ws.cell(5, c).value).strip(): c for c in range(1, 17) if ws.cell(5, c).value}
C = lambda name: hdr[name]
# Accumulated depreciation columns: row 3 says "Acc Dep", row 5 holds the month.
acc_cols = sorted((day(ws.cell(5, c).value), c) for c in range(17, ws.max_column + 1)
                  if str(ws.cell(3, c).value or "").strip() == "Acc Dep")
(as_of, acc_c), (prev_m, prev_c) = acc_cols[-1], acc_cols[-2]
src = {}
for r in range(6, ws.max_row + 1):
    cost = ws.cell(r, C("$ Cost")).value
    if ws.cell(r, C("Category")).value and isinstance(cost, (int, float)):
        acc = ws.cell(r, acc_c).value or 0
        src[f"FA-{r:03d}"] = dict(row=r, cat=ws.cell(r, C("Category")).value.strip(), cost=cost, acc=acc,
                                  nbv=ws.cell(r, acc_c + 1).value, last=acc - (ws.cell(r, prev_c).value or 0),
                                  desc=" ".join(str(ws.cell(r, C("Description")).value or "").split()),
                                  gl=day(ws.cell(r, C("GL Date")).value), life=ws.cell(r, C("Useful life in Months")).value,
                                  purchase=day(ws.cell(r, C("Purchase Date")).value),
                                  accs=[ws.cell(r, c).value or 0 for _, c in acc_cols])
ls = wb["15000-16300 Leadsheet - E100"]
gl_cost, gl_ad = ls["E7"].value, ls["E15"].value

# Every register row is treated exactly once.
wk = list(openpyxl.load_workbook(WORK, read_only=True)["All Assets"].iter_rows(values_only=True))
wh = wk[0]; work = {r[0]: dict(zip(wh, r)) for r in wk[1:]}
if set(work) != set(src): bad(f"working rows {len(work)} vs register rows {len(src)}: {set(work) ^ set(src)}")
for ref, w in work.items():
    s = src[ref]
    if not close(w["Cost"], s["cost"]): bad(f"{ref} working cost {w['Cost']} vs {s['cost']}")
    off_gl = s["cat"] == "Lease Improvement" and s["gl"] < dt.date(2022, 1, 1)
    want = "Not loaded" if off_gl else "Review" if abs(s["nbv"]) < 0.05 else "Held" if not s["acc"] else "Load"
    if w["Treatment"] != want: bad(f"{ref} treatment {w['Treatment']}, expected {want}")

# GL tie: everything except the leasehold improvements left out of the leadsheet.
in_gl = [s for ref, s in src.items() if work[ref]["Treatment"] != "Not loaded"]
if not close(sum(s["cost"] for s in in_gl), gl_cost, 0.5): bad(f"cost in GL {gl_cost} vs register {sum(s['cost'] for s in in_gl)}")
if not close(sum(s["nbv"] for s in in_gl), gl_cost + gl_ad, 0.5): bad(f"NBV in GL {gl_cost + gl_ad} vs register {sum(s['nbv'] for s in in_gl)}")

# Review list: exactly the fully depreciated assets, values from the source row.
rv = list(openpyxl.load_workbook(REVIEW, read_only=True)["Assets"].iter_rows(values_only=True))
rh = rv[0]; review = [dict(zip(rh, r)) for r in rv[1:]]
want = {ref for ref, w in work.items() if w["Treatment"] == "Review"}
got = [r["Ref"] for r in review]
if len(got) != len(set(got)) or set(got) != want: bad(f"review list refs differ: {set(got) ^ want}")
for r in review:
    s = src[r["Ref"]]
    if not close(r["Cost"], s["cost"]) or r["Description"] != s["desc"] or day(r["Purchase Date"]) != s["purchase"]:
        bad(f"{r['Ref']} review row does not match register row {s['row']}")
    if abs(s["nbv"]) >= 0.05: bad(f"{r['Ref']} on review list with NBV {s['nbv']}")
    if any(r[k] for k in ("Still in use?", "Where / who has it", "Notes")): bad(f"{r['Ref']} review columns not blank")

# Mid-life load: each row traced to one register row by name and cost.
def rows(path, tab):
    t = list(openpyxl.load_workbook(path)[tab].iter_rows(values_only=True))
    return [dict(zip([str(h).strip() for h in t[0]], r)) for r in t[1:] if any(v is not None for v in r)]
ml = rows(MIDLIFE, "FAM_Mid-life Asset ")
loaded = {ref for ref, w in work.items() if w["Treatment"] == "Load"}
matched = []
for r in ml:
    cands = [ref for ref in loaded if src[ref]["desc"] == r["Name"] and close(src[ref]["cost"], r["Asset Original Cost"]) and ref not in matched]
    if not cands: bad(f"mid-life row {r['Name']!r} {r['Asset Original Cost']} not found among loaded register rows"); continue
    ref = cands[0]; matched.append(ref); s = src[ref]
    if r["Subsidiary"] != "MinIO, Inc." or r["Quantity"] != 1: bad(f"{ref} subsidiary or quantity")
    want_type = {"Computer Hardware": "Equipment", "Furniture": "Furniture & Fixtures", "Lease Improvement": "Leasehold Improvements"}.get(s["cat"])
    if r["Asset Type"] != want_type: bad(f"{ref} asset type {r['Asset Type']}")
    if r["Asset Status"] != "Depreciating": bad(f"{ref} status {r['Asset Status']}")
    if not close(r["Asset Current Cost"], s["cost"]): bad(f"{ref} current cost")
    if r["Residual Value Percentage"] != 0 or r["Residual Value"] != 0: bad(f"{ref} residual")
    if not close(r["Current Net Book Value"], s["nbv"]): bad(f"{ref} NBV {r['Current Net Book Value']} vs {s['nbv']}")
    if not close(r["Current Net Book Value"], s["cost"] - s["acc"]): bad(f"{ref} NBV is not cost less accumulated")
    if not close(r["Last Depreciation Amount"], s["last"]): bad(f"{ref} last amount {r['Last Depreciation Amount']} vs {s['last']:.2f}")
    if day(r["Last Depreciation Date"]) != as_of: bad(f"{ref} last date {r['Last Depreciation Date']}")
    # Months depreciated, counted from the accumulated column.
    months = sum(1 for a, b in zip([0] + s["accs"][:-1], s["accs"]) if abs(b - a) >= 0.005)
    if r["Last Depreciation Period"] != months: bad(f"{ref} period {r['Last Depreciation Period']} vs {months} months with depreciation")
    start = day(r["Depreciation Start Date"])
    if (as_of.year - start.year) * 12 + as_of.month - start.month + 1 != r["Last Depreciation Period"]:
        bad(f"{ref} start {start} does not give period {r['Last Depreciation Period']}")
    # NetSuite should finish exactly: months left at the last amount covers the NBV.
    left = r["Asset Lifetime"] - r["Last Depreciation Period"]
    if left <= 0 or not close(left * r["Last Depreciation Amount"], r["Current Net Book Value"], 0.02 * left + 0.05):
        bad(f"{ref} lifetime {r['Asset Lifetime']} leaves {left} months for NBV {r['Current Net Book Value']} at {r['Last Depreciation Amount']}")
    if r["Asset Lifetime"] != s["life"] and s["cat"] != "Lease Improvement": bad(f"{ref} lifetime {r['Asset Lifetime']} vs useful life {s['life']}")
if set(matched) != loaded: bad(f"loaded register rows missing from mid-life: {loaded - set(matched)}")

# DHR: one lump sum row per mid-life row, same order, amounts tie.
dh = rows(DHR, "DHR Import Template")
if len(dh) != len(ml): bad(f"DHR rows {len(dh)} vs mid-life rows {len(ml)}")
for r, m, ref in zip(dh, ml, matched):
    s = src[ref]
    if r["Asset Name"] != m["Name"] or r["Asset Type"] != m["Asset Type"] or r["Subsidiary"] != m["Subsidiary"]: bad(f"{ref} DHR identity")
    if r["Transaction Type"] != "Depreciation" or day(r["Transaction Date"]) != as_of: bad(f"{ref} DHR type or date")
    if not close(r["Transaction Amount"], s["acc"]): bad(f"{ref} DHR amount {r['Transaction Amount']} vs accumulated {s['acc']}")
    if not close(r["Transaction Amount"] + r["Net Book Value (NBV)"], r["Original Cost"]): bad(f"{ref} DHR amount plus NBV is not cost")
    if r["Asset Lifetime"] != m["Asset Lifetime"] or day(r["Purchase Date"]) != s["purchase"]: bad(f"{ref} DHR lifetime or purchase date")

# SOA's reference tabs survive untouched.
for path, tpl in ((MIDLIFE, "MINIO_FAM_CSVTemplate_Mid-life Asset Record.xlsx"), (DHR, "MINIO_ FAM_DHR.xlsx")):
    a, b = openpyxl.load_workbook(path), openpyxl.load_workbook(tpl)
    if a.sheetnames != b.sheetnames: bad(f"{path} tabs changed")
    for name in b.sheetnames:
        if name in ("FAM_Mid-life Asset ", "DHR Import Template"):
            if [c.value for c in a[name][1]] != [c.value for c in b[name][1]]: bad(f"{path} {name} header changed")
            continue
        if [[c.value for c in r] for r in a[name].iter_rows()] != [[c.value for c in r] for r in b[name].iter_rows()]: bad(f"{path} tab {name} changed")

print(f"register {len(src)} rows; review {len(review)}; mid-life {len(ml)}; DHR {len(dh)}; as of {as_of}")
print("\n".join(issues) if issues else "no issues")
sys.exit(1 if issues else 0)
