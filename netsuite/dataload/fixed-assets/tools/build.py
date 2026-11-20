#!/usr/bin/env python3
# Build the fixed asset review list and the draft FAM loads from MinIO's fixed asset register (tab ALL FA).
#   python3 tools/build.py   (run from the fixed-assets folder)
# Writes to data/ (not committed):
#   MinIO_Fully_Depreciated_Assets_for_Review_<DATE>.xlsx   the list sent out to confirm which assets still exist
#   MinIO_Fixed_Asset_Load_Working_<DATE>.xlsx              every asset, its treatment, flags, and the open questions
#   MINIO_FAM_CSVTemplate_Mid-life Asset Record - DRAFT <DATE>.xlsx   SOA's template, import tab filled
#   MINIO_ FAM_DHR - DRAFT <DATE>.xlsx                               SOA's template, DHR Import Template tab filled (lump sum)
import calendar, copy, datetime as dt, json, shutil
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

SRC = "data/fixed-assets-oct-2026-recon-E100.xlsx"
AS_OF = dt.date(2026, 10, 31)          # last month depreciated in the register
DATE = "20261117"
MIDLIFE_TPL, DHR_TPL = "MINIO_FAM_CSVTemplate_Mid-life Asset Record.xlsx", "MINIO_ FAM_DHR.xlsx"
OUT_REVIEW = f"data/MinIO_Fully_Depreciated_Assets_for_Review_{DATE}.xlsx"
OUT_WORK = f"data/MinIO_Fixed_Asset_Load_Working_{DATE}.xlsx"
OUT_MIDLIFE = f"data/MINIO_FAM_CSVTemplate_Mid-life Asset Record - DRAFT {DATE}.xlsx"
OUT_DHR = f"data/MINIO_ FAM_DHR - DRAFT {DATE}.xlsx"
ASANA = "https://app.asana.com/1/163565154279805/project/1219443754801875/task/1220361265682450"  # FS-140

SUBSIDIARY = "MinIO, Inc."  # E100; name as in ../README.md reference values
# FAM_Asset Type tab: SOA left Write Off, Write Down and Disposal Cost blank. Ming, 2026-11-13 (Slack, asked for write-off and gain/loss on disposal):
# 79200 (Gain) / Loss on Sale of Asset, 72400 in NetSuite. Write Off: confirmed. Disposal Cost: same account, proposed. Write Down: no account in the COA yet.
GAIN_LOSS = "72400 - (Gain) / Loss on Sale of Asset"
# Write Down: 72400 too (Anthony, 2026-11-20; Ming has the Slack thread).
ASSET_TYPE_ACCOUNTS = {"WRITE OFF ACCOUNT": GAIN_LOSS, "WRITE DOWN ACCOUNT": GAIN_LOSS, "DISPOSAL COST ACCOUNT": GAIN_LOSS}
# Other asset type settings (Anthony, 2026-11-20): Acquisition, the register's practice of depreciating from the month an asset goes
# into service; and the method name exactly as NetSuite lists it (SOA's Dep Method tab: "Straight Line", not "Straightline").
ASSET_TYPE_SETTINGS = {"DEPRECIATION RULES": "Acquisition", "ACCOUNTING METHOD": "Straight Line"}
# Columns added to the mid-life import tab (Anthony, 2026-11-20), named as the NetSuite asset record fields.
MIDLIFE_EXTRA = ["Cumulative Depreciation", "Accounting Method", "Department"]
# Accounting Method per asset, names as on SOA's Dep Method tab. Straight Line is (CC-RV)/AL. The leasehold improvements
# shortened to the lease term need the remaining value over the remaining months: Straight Line Remaining, (NB-RV)/(AL-CP+1).
SL, SLR = "Straight Line", "Straight Line Remaining"
DIMENSIONS = "data/MINIO-Dimensions-from-sage-20260825.xlsx"  # tab Departments Draft v1: Sage code to NetSuite department
# MinIO category (column A) -> SOA asset type (tab FAM_Asset Type of the mid-life template)
ASSET_TYPE = {"Computer Hardware": "Equipment", "Furniture": "Furniture & Fixtures",
              "Lease Improvement": "Leasehold Improvements", "Software": "TBC"}
LEASE_END = dt.date(2028, 6, 30)  # month the Hudson Pacific leasehold improvements finish in the register (FA-076, 082, 088)
# Assets still in use: answers from the review, keyed by Ref. "Yes" loads the asset as Fully Depreciated.
IN_USE = {}

def eom(y, m):
    return dt.date(y, m, calendar.monthrange(y, m)[1])
def add_months(d, n):
    y, m = divmod(d.year * 12 + d.month - 1 + n, 12)
    return eom(y, m + 1)
def months_between(a, b):  # inclusive count of months a..b
    return (b.year - a.year) * 12 + b.month - a.month + 1
def d(v):
    return v.date() if isinstance(v, dt.datetime) else v
def r2(v):
    return None if v is None else round(float(v) + 0.0, 2)
def txt(v):
    return " ".join(str(v).split()) if v not in (None, "") else ""

wb = openpyxl.load_workbook(SRC, data_only=True)
ws = wb["ALL FA"]
# Monthly blocks of three columns (Dep, Acc Dep at, NBV at) from column Q; the month is in row 5.
blocks = []
for c in range(17, ws.max_column + 1, 3):
    m = d(ws.cell(5, c).value)
    if isinstance(m, dt.date):
        blocks.append((eom(m.year, m.month), c))
assert blocks[-1][0] == AS_OF, blocks[-1]
last_c = blocks[-1][1]

assets = []
for r in range(6, ws.max_row + 1):
    cat = txt(ws.cell(r, 1).value)
    cost = ws.cell(r, 14).value
    if not cat or not isinstance(cost, (int, float)):
        continue
    g = lambda c: ws.cell(r, c).value
    a = dict(ref=f"FA-{r:03d}", row=r, category=cat, fa_acct=g(2), ad_acct=g(3), entity=txt(g(4)), dept=txt(g(5)),
             gl_date=d(g(6)), purchase=d(g(7)), vendor=txt(g(8)), project=txt(g(9)), comment=txt(g(10)),
             location=txt(g(11)), dep_date=d(g(12)), description=txt(g(13)), cost=r2(cost), life=g(15),
             monthly=r2(g(16)), dep_col=r2(g(last_c)) or 0.0, accum=r2(g(last_c + 1)) or 0.0, nbv=r2(g(last_c + 2)))
    # Depreciation for a month is the change in accumulated depreciation: some rows carry Dep formulas in months
    # before the asset was bought that are not added to the accumulated total (FA-087).
    sched, prev = [], None
    for m, c in blocks:
        acc = r2(g(c + 1)) or 0.0
        sched.append((m, round(acc - prev, 2) if prev is not None else 0.0, acc, r2(g(c + 2))))
        prev = acc
    dep_months = [m for m, dep, _, _ in sched if abs(dep) >= 0.005]
    a["first_dep"] = dep_months[0] if dep_months else None
    a["last_dep"] = dep_months[-1] if dep_months else None
    a["last_dep_amt"] = next((dep for m, dep, _, _ in sched if m == a["last_dep"]), None)
    a["first_nbv"] = sched[0][3]
    a["dep_last"] = sched[-1][1]
    if abs(a["dep_last"] - a["dep_col"]) >= 0.02:
        a.setdefault("pre", []).append(f"Dep column {a['dep_col']} differs from the change in accumulated depreciation {a['dep_last']}")
    a["flags"] = a.pop("pre", [])
    # The leadsheet counts leasehold improvements only with a GL date from 2022 (15300 in Sage holds those alone).
    if cat == "Lease Improvement" and a["gl_date"] and a["gl_date"] < dt.date(2022, 1, 1):
        a["status"] = "Not in GL"
    elif abs(a["nbv"]) < 0.05:
        a["status"] = "Fully Depreciated"
    elif not a["accum"]:
        a["status"] = "Not yet depreciating"
    else:
        a["status"] = "Depreciating"
    # Month the asset reached zero
    if a["status"] in ("Fully Depreciated", "Not in GL"):
        if a["first_nbv"] is not None and abs(a["first_nbv"]) < 0.05 and not dep_months:
            a["fd_month"] = add_months(a["dep_date"], a["life"] - 1) if a["dep_date"] else None
            a["fd_basis"] = "Before 2021: Dep Date plus useful life"
        else:
            a["fd_month"] = a["last_dep"]
            a["fd_basis"] = "Last month with depreciation in the register"
    assets.append(a)

# Mid-life values for assets still depreciating
for a in assets:
    if a["status"] != "Depreciating":
        continue
    a["periods"] = months_between(a["first_dep"], AS_OF)
    a["remaining"] = round(a["nbv"] / a["dep_last"]) if a["dep_last"] else None
    a["lifetime"] = a["periods"] + a["remaining"]
    a["start"] = a["dep_date"] if a["dep_date"] and (a["dep_date"].year, a["dep_date"].month) == (a["first_dep"].year, a["first_dep"].month) else a["first_dep"].replace(day=1)
    if a["lifetime"] != a["life"]:
        a["flags"].append(f"Depreciation rate changed: {a['remaining']} months left at {a['dep_last']:,.2f} ends "
                          f"{add_months(AS_OF, a['remaining']):%Y-%m}; lifetime set to {a['lifetime']} ({a['periods']} done + {a['remaining']} left) instead of {a['life']}")
    if a["dep_date"] and a["start"] != a["dep_date"]:
        a["flags"].append(f"Dep Date in the register is {a['dep_date']} but depreciation starts {a['first_dep']:%Y-%m}")
    if a["dep_date"] is None:
        a["flags"].append("No Dep Date in the register; start taken from the first month depreciated")
    if a["purchase"] and a["first_dep"] and months_between(a["purchase"], a["first_dep"]) > 3:
        a["flags"].append(f"Purchased {a['purchase']} but depreciation starts {a['first_dep']:%Y-%m}")

# Data checks worth a question
by_cost = {}
for a in assets:
    by_cost.setdefault(a["cost"], []).append(a)
for a in assets:
    if a["status"] == "Not yet depreciating":
        a["flags"].append("No depreciation taken yet (NBV equals cost); held out of the load until the start date is confirmed")
    if a["description"].startswith(("V-", "V0")) or "--" in a["description"]:
        a["flags"].append(f"GL date {a['gl_date']}, " + (f"depreciation from {a['first_dep']:%Y-%m}" if a["first_dep"] else "no depreciation") + "; description is a Sage vendor string, no vendor, comment or Dep Date")
names = {}
for a in assets:
    names.setdefault(a["description"].lower(), []).append(a["ref"])
for a in assets:
    same = [x for x in names[a["description"].lower()] if x != a["ref"]]
    if same and a["status"] == "Depreciating":
        a["flags"].append("Same name as " + ", ".join(same) + ": NetSuite asset names should be unique for the DHR to find the asset")
for k, grp in by_cost.items():
    if len(grp) > 1:
        for a in grp:
            a["flags"].append("Same cost as " + ", ".join(f"{x['ref']} ({x['vendor'] or x['description']})" for x in grp if x is not a) + ": possible duplicate")
for a in assets:
    if a["category"] == "Lease Improvement" and a["status"] == "Depreciating" and add_months(AS_OF, a["remaining"]) > LEASE_END:
        a["flags"].append(f"Ends {add_months(AS_OF, a['remaining']):%Y-%m}, after the other leasehold improvements ({LEASE_END:%Y-%m}); the register says they should be fully depreciated by the end of the lease term")
    if a["category"] == "Software":
        a["flags"].append("No matching NetSuite asset type: SOA's types have Internally Developed Software only (this is purchased software, account 15100)")

# Department: Sage code to the NetSuite department's full name (parent : child), from Departments Draft v1.
def dept_map():
    ws = openpyxl.load_workbook(DIMENSIONS, read_only=True, data_only=True)["Departments Draft v1"]
    out, parents = {}, {}
    for row in ws.iter_rows(min_row=4, values_only=True):
        sage, level, code, desc = row[:4]
        if not isinstance(level, (int, float)) or code is None: continue
        level, name = int(level), f"{int(code)} {str(desc).strip()}"
        parents[level] = name
        full = " : ".join([parents[l] for l in range(1, level)] + [name])
        for c in str(sage or "").replace(" historic only", "").replace(" historic", "").replace("(", "").replace(")", "").split(","):
            c = c.strip()
            if c: out[c] = full
    return out
DEPT = dept_map()
# D110 (Sales, historic) is not on the tab: the sales laptops go to 2100 Sales - Leadership (Anthony, 2026-11-20).
DEPT["D110"] = DEPT["D-S110"]
assert DEPT["D110"].endswith("2100 Sales - Leadership"), DEPT["D110"]
for a in assets:
    if a["status"] == "Depreciating":
        a["method"] = SLR if a["lifetime"] != a["life"] else SL
        if a["dept"] not in DEPT:
            a["flags"].append(f"Department {a['dept']} is not on Departments Draft v1; Department left blank")
    else:
        a["method"] = SL

def load_rows():
    """Assets that go to NetSuite: still depreciating, plus fully depreciated assets confirmed in use."""
    out = []
    for a in assets:
        if a["status"] == "Depreciating":
            out.append(a)
        elif a["status"] == "Fully Depreciated" and IN_USE.get(a["ref"]) == "Yes":
            out.append(a)
    return out
# Asset names shortened for brevity and clarity (Anthony, 2026-11-20), from the register's own words; acronyms are not expanded.
# The register Description is kept in Asset Description after the existing text, prefixed "Original name:".
# Assets not listed keep the register Description as the name.
NAMES = {
    "FA-069": "AMAX AceleMax NVIDIA GPU server",
    "FA-070": "Laptop - Petr Kobalicek",
    "FA-071": "Laptop - Piotr Wyderski",
    "FA-072": "SuperMicro X13SET-G servers (2)",
    "FA-073": "Additional power, 275 Shoreline Ste 100",
    "FA-074": "Computers & equipment - MIRAPATH",
    "FA-075": "NVIDIA Spectrum-3 SN4700 switch",
    "FA-076": "Suite 100 tenant overage (TWA 1)",
    "FA-077": "Dell PowerEdge R7615 server 2024-12-06",
    "FA-078": "Dell PowerEdge R7615 server 2024-12-10",
    "FA-079": "Dell PowerEdge XE968 server",
    "FA-080": "Dell hardware - Center of Excellence",
    "FA-082": "Suite 100 blinds (TWA 2)",
    "FA-084": "NVIDIA CX-7 400Gb NIC cards (18)",
    "FA-085": "Mellanox CX-7 support and warranty, 3 yrs",
    "FA-086": "NVIDIA 400GbE transceivers and cables",
    "FA-087": "Rahi data center hardware, March 2025",
    "FA-088": "Suite 100 doors (TWA 3)",
    "FA-089": "Laptop - Ali Yaldaz",
    "FA-090": "FS.COM transceiver",
    "FA-092": "SanDisk storage cards (192)",
    "FA-093": "Supermicro CUST 2XX550 480GB",
    "FA-094": "NVIDIA Spectrum-4 switch and networking",
    "FA-095": "NVIDIA CX-7 NIC card with warranty",
    "FA-096": "NADDOD purchase, September 2026",
    "FA-097": "MacBooks for new hires (5)",
    "FA-098": "AMAX purchase (Sage V-00545)",
    "FA-099": "Amazon purchase (Sage V00021)",
    "FA-100": "Ramp users - other expenses",
}
def asset_name(a):
    return NAMES.get(a["ref"], a["description"])
def asset_description(a):
    parts = [a["vendor"]] + [x for x in (a["comment"],) if x and x != a["description"]]
    text = " - ".join(p for p in parts if p)
    if asset_name(a) != a["description"]:
        text = (text + ". " if text else "") + "Original name: " + a["description"]
    return text
def midlife(a):
    fd = a["status"] == "Fully Depreciated"
    return [asset_name(a), asset_description(a), 1, SUBSIDIARY, ASSET_TYPE[a["category"]], a["status"],
            a["life"] if fd else a["lifetime"], a["cost"], a["cost"], 0, 0,
            a["dep_date"] if fd else a["start"], a["fd_month"] if fd else AS_OF,
            a["life"] if fd else a["periods"], a["last_dep_amt"] if fd else a["dep_last"], 0 if fd else a["nbv"],
            a["cost"] if fd else a["accum"], a["method"], DEPT.get(a["dept"])]
def dhr(a):
    # Depreciation Period: the asset's Last Depreciation Period (Anthony, 2026-11-20); Period-1 as SOA's formula, J-1.
    # DHR Name: any value without "|" (Oracle). Asset Name: Oracle's format is the NetSuite asset ID plus the name
    # (FAM00001 Chairs), so it is completed once the assets are imported and have IDs.
    fd = a["status"] == "Fully Depreciated"
    period = a["life"] if fd else a["periods"]
    when = a["fd_month"] if fd else AS_OF
    return [f"{a['ref']} Depreciation to {when:%Y-%m-%d}", asset_name(a), SUBSIDIARY, 1, ASSET_TYPE[a["category"]], "Depreciation",
            when, a["cost"] if fd else a["accum"], 0 if fd else a["nbv"], period, period - 1,
            a["life"] if fd else a["lifetime"], a["purchase"], a["cost"]]

# ---------- styling ----------
thin = Side(style="thin", color="D6DEE3")
grid = Border(left=thin, right=thin, top=thin, bottom=thin)
head_fill = PatternFill("solid", fgColor="E8EEF1")
ask_fill = PatternFill("solid", fgColor="FFF2CF")
wrap_top = Alignment(wrap_text=True, vertical="top")
MONEY, DATEF = "#,##0.00", "yyyy-mm-dd"

def table(ws, headers, rows, widths, start=1, ask=()):
    for k, h in enumerate(headers, 1):
        c = ws.cell(row=start, column=k, value=h)
        c.font = Font(bold=True); c.fill = ask_fill if h in ask else head_fill; c.border = grid; c.alignment = wrap_top
        ws.column_dimensions[get_column_letter(k)].width = widths.get(h, 14)
    for i, row in enumerate(rows, start + 1):
        for k, v in enumerate(row, 1):
            c = ws.cell(row=i, column=k, value=v)
            c.border = grid; c.alignment = wrap_top
            if isinstance(v, float): c.number_format = MONEY
            if isinstance(v, dt.date): c.number_format = DATEF
            if headers[k - 1] in ask: c.fill = ask_fill
    ws.freeze_panes = ws.cell(row=start + 1, column=1)
    ws.auto_filter.ref = f"A{start}:{get_column_letter(len(headers))}{start + len(rows)}"

def notes(ws, title, lines):
    ws["A1"] = title; ws["A1"].font = Font(bold=True, size=14)
    ws.column_dimensions["A"].width = 120
    for i, line in enumerate(lines, 3):
        c = ws.cell(row=i, column=1, value=line); c.alignment = Alignment(wrap_text=True, vertical="top")
        if line and not line.startswith(("-", " ")) and line.endswith(":"): c.font = Font(bold=True)

fd = sorted([a for a in assets if a["status"] == "Fully Depreciated"], key=lambda a: (a["category"], a["purchase"] or dt.date.min))
dep = [a for a in assets if a["status"] == "Depreciating"]
held = [a for a in assets if a["status"] == "Not yet depreciating"]
gone = [a for a in assets if a["status"] == "Not in GL"]
tot = lambda xs, k: round(sum(a[k] for a in xs), 2)

# ---------- 1. Review list (sent out) ----------
rv = openpyxl.Workbook()
n = rv.active; n.title = "About"
notes(n, "MinIO fixed assets: fully depreciated, still in use?", [
    f"These {len(fd)} assets are on MinIO's fixed asset register (E100, MinIO, Inc.) and are fully depreciated as of {AS_OF}. "
    "Original cost " + f"{tot(fd, 'cost'):,.2f}" + ", net book value 0.",
    "We are moving the register to NetSuite. Assets still in use are loaded to NetSuite; assets no longer here are not.",
    "",
    "Please fill in the yellow columns on the Assets tab:",
    "- Still in use?: Yes or No.",
    "- Where / who has it: the person, office or data center, if known.",
    "- Notes: anything else, for example disposed, sold, lost, or replaced.",
    "",
    "Ref is the row on the ALL FA tab of the register (FA-022 is row 22). Source: 15000-16999 - Fixed Assets - Oct 2026 - recon E100 entity, "
    "prepared by Richard Li, reviewed by Ming Fu, 2026-11-06.",
    f"Asana FS-140: {ASANA}",
])
rh = ["Ref", "Category", "Purchase Date", "Vendor", "Description", "Comment", "Physical Location", "Department",
      "Cost", "Useful Life (months)", "Fully Depreciated", "Still in use?", "Where / who has it", "Notes"]
table(rv.create_sheet("Assets"), rh,
      [[a["ref"], a["category"], a["purchase"], a["vendor"], a["description"], a["comment"] if a["comment"] != a["description"] else "",
        a["location"], a["dept"], a["cost"], a["life"], a["fd_month"], None, None, None] for a in fd],
      {"Vendor": 26, "Description": 44, "Comment": 34, "Where / who has it": 26, "Notes": 30, "Physical Location": 14},
      ask=("Still in use?", "Where / who has it", "Notes"))
rv.save(OUT_REVIEW)

# ---------- 2. SOA templates, filled ----------
loads = load_rows()
shutil.copy(MIDLIFE_TPL, OUT_MIDLIFE)
m = openpyxl.load_workbook(OUT_MIDLIFE)
t = m["FAM_Mid-life Asset "]
t.delete_rows(2, t.max_row)
last = t.max_column
for k, h in enumerate(MIDLIFE_EXTRA, last + 1):
    c = t.cell(row=1, column=k, value=h)
    c._style = copy.copy(t.cell(row=1, column=last)._style)
    t.column_dimensions[get_column_letter(k)].width = t.column_dimensions[get_column_letter(last)].width or 14
for i, a in enumerate(loads, 2):
    for k, v in enumerate(midlife(a), 1):
        c = t.cell(row=i, column=k, value=v)
        if isinstance(v, dt.date): c.number_format = "mm/dd/yyyy"
t = m["FAM_Asset Type"]
cols = {str(c.value).strip(): c.column for c in t[1] if c.value}
for r in range(3, t.max_row + 1):
    if t.cell(r, 1).value and t.cell(r, cols["ASSET ACCOUNT"]).value and t.cell(r, cols["DEPRECIATION ACCOUNT"]).value != "N/A":
        for col, acct in {**ASSET_TYPE_ACCOUNTS, **ASSET_TYPE_SETTINGS}.items():
            t.cell(r, cols[col], value=acct)
m.save(OUT_MIDLIFE)

shutil.copy(DHR_TPL, OUT_DHR)
h = openpyxl.load_workbook(OUT_DHR)
t = h["DHR Import Template"]
t.delete_rows(2, t.max_row)
for i, a in enumerate(loads, 2):
    for k, v in enumerate(dhr(a), 1):
        c = t.cell(row=i, column=k, value=v)
        if isinstance(v, dt.date): c.number_format = "mm/dd/yyyy"
h.save(OUT_DHR)

# ---------- 3. Working workbook ----------
w = openpyxl.Workbook()
n = w.active; n.title = "Notes"
ls = wb["15000-16300 Leadsheet - E100"]
gl_cost, gl_ad = ls["E7"].value, ls["E15"].value  # balances per Sage TB 2026-10-31
lines = [
    f"Source: {SRC.split('/')[-1]}, tab ALL FA, depreciated through {AS_OF}. Asana FS-140: {ASANA}",
    "",
    "Assets on the register:",
    f"- Depreciating, in both loads now: {len(dep)}, cost {tot(dep, 'cost'):,.2f}, accumulated {tot(dep, 'accum'):,.2f}, NBV {tot(dep, 'nbv'):,.2f}",
    f"- Fully depreciated, out for review (loaded only if still in use): {len(fd)}, cost {tot(fd, 'cost'):,.2f}",
    f"- Not yet depreciating, held: {len(held)}, cost {tot(held, 'cost'):,.2f} (" + ", ".join(a['ref'] for a in held) + ")",
    f"- Not in the GL, not loaded: {len(gone)} leasehold improvements with a GL date before 2022, cost {tot(gone, 'cost'):,.2f}, fully depreciated. "
    "The leadsheet leaves them out of 15300 and 16300, so Sage no longer carries them",
    f"- Total on the register: {len(assets)}, cost {tot(assets, 'cost'):,.2f}",
    "",
    "Ties to Sage (leadsheet, TB 2026-10-31):",
    f"- Cost in the GL {gl_cost:,.2f} = register {tot(assets, 'cost'):,.2f} less not in GL {tot(gone, 'cost'):,.2f} = {tot(assets, 'cost') - tot(gone, 'cost'):,.2f}",
    f"- NBV in the GL {gl_cost + gl_ad:,.2f}; register {tot(assets, 'nbv'):,.2f}",
    "",
    "How the loads are filled (SOA's two templates):",
    "- Mid-life Asset Record: one row per asset, creates the asset in NetSuite part way through its life. NetSuite carries on depreciating from Last Depreciation Period.",
    "- DHR (depreciation history record): the depreciation already taken, so NetSuite's asset reports show it. Filled as SOA's lump sum example: one Depreciation row per asset for the accumulated depreciation to date. "
    "The register holds monthly figures only from 2021-01, so a monthly DHR for older assets would have to be rebuilt.",
    "- Name: the register's Description. Asset Description: vendor, then the register's Comment when it differs from the Description.",
    f"- Subsidiary {SUBSIDIARY}; Quantity 1; residual 0; Asset Original Cost and Asset Current Cost both the register's cost.",
    "- Asset type: Computer Hardware to Equipment, Furniture to Furniture & Fixtures, Lease Improvement to Leasehold Improvements. Software: TBC.",
    "- Depreciation Start Date: the register's Dep Date when it is in the first month depreciated, else the 1st of that month. "
    f"Last Depreciation Period: months from the first month depreciated to {AS_OF:%Y-%m}. Last Depreciation Amount and Current NBV: the {AS_OF:%Y-%m} figures.",
    "- Asset Lifetime: the register's useful life, except where the monthly rate was raised (leasehold improvements shortened to the lease term): periods done plus months left.",
    "- DHR: Transaction Date the last depreciation date, Transaction Amount the accumulated depreciation, Depreciation Period 1 and Period-1 0 as in SOA's lump sum example; DHR Name blank, as in the example.",
    "",
    "Before the load: the register must be rolled to the month before go-live, then this is rebuilt.",
]
notes(n, "MinIO fixed asset load to NetSuite: working notes", lines)

wh = ["Ref", "Treatment", "Category", "FA Acct", "Dept", "GL Date", "Purchase Date", "Vendor", "Description", "Comment",
      "Physical Location", "Dep Date", "Cost", "Useful Life", "Monthly Dep", "First Month Depreciated", "Last Month Depreciated",
      f"Dep {AS_OF:%Y-%m}", f"Accumulated {AS_OF:%Y-%m}", f"NBV {AS_OF:%Y-%m}", "Fully Depreciated", "Basis",
      "NS Asset Type", "NS Lifetime", "NS Last Dep Period", "Months Left", "Flags"]
treat = {"Depreciating": "Load", "Fully Depreciated": "Review", "Not yet depreciating": "Held", "Not in GL": "Not loaded"}
rows = []
for a in assets:
    f = lambda m: m.strftime("%Y-%m") if m else None
    rows.append([a["ref"], treat[a["status"]], a["category"], a["fa_acct"], a["dept"], a["gl_date"], a["purchase"], a["vendor"],
                 a["description"], a["comment"], a["location"], a["dep_date"], a["cost"], a["life"], a["monthly"],
                 f(a["first_dep"]), f(a["last_dep"]), a["dep_last"], a["accum"], a["nbv"], f(a.get("fd_month")), a.get("fd_basis"),
                 ASSET_TYPE[a["category"]], a.get("lifetime"), a.get("periods"), a.get("remaining"), "\n".join(a["flags"])])
table(w.create_sheet("All Assets"), wh, rows, {"Description": 40, "Vendor": 24, "Comment": 30, "Flags": 70, "Basis": 24})
QUESTIONS = [
    ("SOA", "Reading of the templates", "Mid-life Asset Record creates the assets; DHR loads the depreciation already taken. Confirm."),
    ("SOA", "Lump sum DHR", "Decided: lump sum (Anthony, 2026-11-20). Oracle's current help says to create a DHR for every depreciation entry (monthly, quarterly or annually); older Oracle help and practitioners use one catch-up record. Confirm it loads."),
    ("SOA", "DHR Asset Name and load order", "Oracle: Asset Name is the NetSuite asset ID plus the name (FAM00001 Chairs), and assets are imported before DHRs. Plan: import assets, export their IDs, complete Asset Name, import DHRs. Confirm."),
    ("SOA", "Added columns", "Cumulative Depreciation, Accounting Method and Department were added to the mid-life import tab (Anthony, 2026-11-20). They are NetSuite asset record fields; Oracle's import field list does not show Accounting Method. Confirm they import."),
    ("SOA", "Straight Line Remaining", "Used for FA-076 and FA-082, shortened to the lease term: (NB-RV)/(AL-CP+1) gives 519.63 and 247.78. Oracle describes it as a method linked after another. Confirm it works as an asset's own method."),
    ("SOA", "Server scripts on CSV import", "Oracle: with Run Server SuiteScript and Trigger Workflows and FAM's Run Server Scripts on CSV Import both on, Cumulative Depreciation, Last Depreciation Date and Last Depreciation Period import as 0. Check the settings."),
    ("SOA", "Name mapping", "Oracle: delete the default Name = ID mapping; a Name over 30 characters in ID errors. 17 of the 32 names are still over 30 characters after shortening (longest 41). Is there a length limit on Asset Description? The longest here is 295 characters."),
    ("SOA", "Sample Asset Records", "The DHR file's Sample Asset Records tab looks like the full asset record field list. Is it a load, or an example? Not filled."),
    ("Richard / Ming", "FA-098 to FA-101", "GL date 2022-10, depreciation from 2026-10 (FA-101 none), Sage vendor string as description. What are they? FA-098 has the same cost and vendor as FA-094 (AMAX, 63,995.00): duplicate? FA-101 is held until its start date is known."),
    ("Richard / Ming", "FA-096, FA-097 Dep Date", "Dep Date 2027-10-01 but depreciation started 2026-10. Loaded from 2026-10."),
    ("Richard / Ming", "FA-093 start", "Bought 2025-03-05, depreciation from 2026-03. Loaded as in the register."),
    ("Richard / Ming", "FA-073 lease term", "Finishes 2029-03, after the lease ends 2028-06. ASC 842 has leasehold improvements depreciated over the shorter of useful life and remaining lease term. Shorten it like FA-076 and FA-082?"),
    ("Sendhil Mandala", "Disposed assets", "Per the Asana task: which assets have been disposed of."),
]
DECISIONS = [
    "2026-11-20 (Anthony): lump sum DHR; DHR Depreciation Period is the asset's Last Depreciation Period; DHR Name filled; Accounting Method, Department and Cumulative Depreciation columns added; Depreciation Rules Acquisition; Write Down Account 72400; load as of 2026-10-31 for now; D110 sales laptops (FA-070, FA-071, FA-089) to 2100 Sales - Leadership; asset names shortened, register Description kept in Asset Description after \"Original name:\"; fully depreciated assets a separate load; asset type default lifetimes left to Ming once NetSuite is in use.",
    "2026-11-13 (Ming, Slack): write-off and gain/loss on disposal use 79200 (Gain) / Loss on Sale of Asset, 72400 in NetSuite.",
]
q = w.create_sheet("Questions")
table(q, ["For", "Topic", "Question"], [list(x) for x in QUESTIONS], {"For": 16, "Topic": 28, "Question": 110})
r0 = len(QUESTIONS) + 3
q.cell(row=r0, column=1, value="Decided").font = Font(bold=True)
for k, d in enumerate(DECISIONS, r0 + 1):
    q.cell(row=k, column=1, value=d).alignment = Alignment(wrap_text=False)
w.save(OUT_WORK)

json.dump({"assets": [{k: (v.isoformat() if isinstance(v, dt.date) else v) for k, v in a.items()} for a in assets]},
          open("data/assets.json", "w"), indent=1, default=str)
print(f"assets {len(assets)}: depreciating {len(dep)}, fully depreciated {len(fd)}, held {len(held)}, not in GL {len(gone)}")
print(f"cost: all {tot(assets,'cost'):,.2f} dep {tot(dep,'cost'):,.2f} fd {tot(fd,'cost'):,.2f} held {tot(held,'cost'):,.2f} gone {tot(gone,'cost'):,.2f}")
print(f"nbv: all {tot(assets,'nbv'):,.2f} dep {tot(dep,'nbv'):,.2f}")
for a in assets:
    if a["flags"]: print(a["ref"], a["status"], "|", " / ".join(a["flags"]))
