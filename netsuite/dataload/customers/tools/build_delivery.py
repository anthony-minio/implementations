#!/usr/bin/env python3
# Build the file delivered to SOA: the customer import template filled with the load, the added columns, a Notes tab
# (text taken from the review page so the two match) and a Review tab with every Sage record and what happened to it.
#   python3 tools/build_delivery.py   (run from the customers folder after build_review.py)
import copy, csv, json, re, subprocess, sys
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

OUT = "data/MinIO_Customer_Load_20261026.xlsx"
wb = openpyxl.load_workbook("Customer_Import_Template_-_Updated_1.xlsx")
ws = wb["CustomerTemplate"]
s = open("data/customer-review.html", encoding="utf-8").read()
data = json.loads(s[s.index("const DATA = ") + 13:s.index(";\nconst $")])
cols, review = data["cols"], data["review"]
TEMPLATE_N = 31
ADDED = cols[TEMPLATE_N:]
ADDED_NOTE = {
    "Question Categories": "Added. Why this customer needs a look: Investor, Subnet ID to assign, SOA Category Unknown.",
    "Duplicate Action": "Added. What happened to Sage duplicates of this customer.",
    "Merged Sage IDs": "Added. Sage customers folded into this one (not loaded separately).",
    "Second Address": "Added. Address of a merged Sage record, where different.",
    "Third Address": "Added. Address of a second merged Sage record, where different.",
    "Sage Customer ID": "Added. Customer ID in Sage.",
    "Salesforce Account ID": "Added. 18-character case-safe Salesforce Account ID.",
    "Additional Emails": "Added. Every other email Sage holds for the customer.",
    "Other Tax ID": "Added. Tax IDs in Sage that are not VAT numbers, for example a US EIN.",
    "Billed To (Reseller)": "Added. Reseller Sage invoices for this customer.",
    "Reseller Address": "Added. Reseller billing address from Sage.",
    "Reseller Invoice Email": "Added. Reseller billing email from Sage.",
    "Salesforce Partners": "Added. Partners linked to the account in Salesforce.",
}

# Remove the template's sample rows and footer, keep the header block (rows 1 to 6).
ws.delete_rows(7, ws.max_row - 6)
added_fill = PatternFill("solid", fgColor="FFF2CC")
for i, name in enumerate(ADDED):
    col = TEMPLATE_N + 1 + i
    for r, v in ((1, re.sub(r"[^A-Za-z]", "", name)), (2, name), (3, ADDED_NOTE.get(name, "Added."))):
        c = ws.cell(row=r, column=col, value=v)
        src = ws.cell(row=r, column=TEMPLATE_N)
        c.font = copy.copy(src.font); c.alignment = copy.copy(src.alignment); c.border = copy.copy(src.border)
        c.fill = added_fill
    ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 28

# Review-only columns after the added ones: what reviewers need to answer the questions. Not NetSuite fields.
review_fill = PatternFill("solid", fgColor="E7E6E6")
REVIEW_COLS = review + ["Flags"]
for i, name in enumerate(REVIEW_COLS):
    col = len(cols) + 1 + i
    for r, v in ((1, ""), (2, name), (3, "Review only. Not for import.")):
        c = ws.cell(row=r, column=col, value=v)
        src = ws.cell(row=r, column=TEMPLATE_N)
        c.font = copy.copy(src.font); c.alignment = copy.copy(src.alignment); c.border = copy.copy(src.border)
        c.fill = review_fill
    ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 60 if name == "Flags" else 22

load = [r for r in data["rows"] if not r["cells"][cols.index("Duplicate Action")][0].startswith("Merge into")]
for i, r in enumerate(load):
    for j, v in enumerate([c[0] for c in r["cells"]] + r["review"] + ["; ".join(r["flags"])]):
        c = ws.cell(row=7 + i, column=j + 1, value=v if v != "" else None)
        c.number_format = "@"
ws.freeze_panes = "E7"

# Notes tab: the Open decisions and Notes sections as rendered on the review page.
js = """
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.argv[1]);
const t=await p.evaluate(()=>[...document.querySelectorAll('.decisions')].map(s=>({h:s.querySelector('h2').innerText,items:[...s.querySelectorAll('li')].map(l=>l.innerText)})));
console.log(JSON.stringify(t));await b.close()})()"""
import os
notes = json.loads(subprocess.run(["node", "-e", js, os.path.abspath("data/customer-review.html")], capture_output=True, text=True, check=True).stdout)
ns = wb.create_sheet("Notes", 0)
ns.column_dimensions["A"].width = 6; ns.column_dimensions["B"].width = 120
ns["A1"] = "MinIO customer load: notes for SOA"; ns["A1"].font = Font(bold=True, size=14)
ns["A2"] = (f"{len(load)} customers on the CustomerTemplate tab. Columns after Exemption Certificate No. shaded yellow are added by MinIO; "
            "columns shaded grey at the far right are for review only and are removed before import. All fields marked in red on the template are mandatory.")
row = 4
for sec in (x for x in notes if not (len(x["items"]) == 1 and x["items"][0].startswith("None"))):
    ns.cell(row=row, column=1, value=sec["h"]).font = Font(bold=True, size=12); row += 1
    for n, item in enumerate(sec["items"], 1):
        ns.cell(row=row, column=1, value=n if len(sec["items"]) > 1 or not item.startswith("None") else None)
        c = ns.cell(row=row, column=2, value=item); c.alignment = Alignment(wrap_text=True, vertical="top")
        ns.cell(row=row, column=1).alignment = Alignment(vertical="top")
        row += 1
    row += 1

# Review tab: every active Sage customer and what happened to it.
rs = wb.create_sheet("Review")
head = ["Customer ID", "Sage Customer ID", "Company Name", "Duplicate Action", "Question Categories"] + review + ["Flags"]
rs.append(head)
for c in rs[1]:
    c.font = Font(bold=True)
for r in data["rows"]:
    g = lambda k: r["cells"][cols.index(k)][0]
    rs.append([g("Customer ID"), g("Sage Customer ID"), g("Company Name"), g("Duplicate Action"), g("Question Categories")] + r["review"] + ["; ".join(r["flags"])])
rs.freeze_panes = "D2"
for col, w in zip("ABCDEFGHIJKLM", (12, 14, 40, 34, 26, 26, 14, 12, 14, 40, 50, 80)):
    rs.column_dimensions[col].width = w

wb.active = wb.sheetnames.index("CustomerTemplate")
wb.save(OUT)
print(f"{len(load)} customers, {len(data['rows'])} review rows -> {OUT}")
