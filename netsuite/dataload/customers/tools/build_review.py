#!/usr/bin/env python3
# Build the customer review page: Sage customers mapped to the NetSuite template, enriched from Salesforce.
#   python3 tools/build_review.py   (run from the customers folder; reads data/, writes data/customer-review.html)
import csv, datetime as dt, json, re
import openpyxl

TODAY = dt.date(2026, 10, 26)
CUTOFF = dt.date(2024, 10, 26)  # invoiced in the last 2 years
FLAT = "data/sage-customers-flat-20261025.csv"
LIST = "data/sage-customers-20261026.csv"
SFDC = "data/sfdc-accounts-20261025.xlsx"

TERMS = {"30 Days": "Net 30", "45 Days": "Net 45", "60 Days": "Net 60", "90 Days": "Net 90",
         "120 Days": "Net 120", "20 Days": "Net 20", "28 days": "Net 28", "Net 30": "Net 30",
         "Due on Receipt": "Due on Receipt"}
CATEGORY = {"Direct Sales": "Direct Customer", "Direct Sales with Reseller": "End Customer", "Reseller": "Reseller"}

def norm(s):
    s = re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())
    s = re.sub(r"\b(inc|llc|ltd|limited|corp|corporation|co|plc|gmbh|sa|ag|bv|pte|pvt|the|company|group|holdings?)\b", "", s)
    return " ".join(s.split())

def date(s):
    try:
        return dt.datetime.strptime(s, "%m/%d/%Y").date()
    except ValueError:
        return None

sage = list(csv.DictReader(open(FLAT, encoding="utf-8-sig")))
lst = {r["Customer ID"]: r for r in csv.DictReader(open(LIST, encoding="utf-8-sig"))}
ws = openpyxl.load_workbook(SFDC, read_only=True).active
srows = list(ws.iter_rows(values_only=True))
sf = {norm(r[0]): dict(zip(srows[0], r)) for r in srows[1:] if r and r[0]}

names, near = {}, {}
for r in sage:
    names.setdefault(r["Customer name"].strip().lower(), []).append(r["Customer ID"])
    near.setdefault(norm(r["Customer name"]), []).append(r["Customer ID"])

COLS = ["External ID", "Subnet ID", "Customer ID", "Company Name", "Parent Company", "Subsidiary", "Status",
        "Primary Currency", "Additional Currencies", "Customer Invoice Email", "Individual (Type)", "Customer Category",
        "Phone", "Email Preference", "Attention", "Addressee", "Address 1", "Address 2", "City", "Province/State",
        "Postal Code/Zip", "Country", "Default Billing", "Default Shipping", "Account", "Terms", "VAT ID",
        "International VAT ID", "Taxable", "Avalara Entity", "Exemption Certificate No."]
REQUIRED = {"Customer ID", "Company Name", "Subsidiary", "Status", "Primary Currency", "Customer Category"}
REVIEW = ["Sage type", "Last invoice", "Balance", "Sage bill-to", "Salesforce match"]

out = []
for r in sage:
    if r["Status"] != "Active":
        continue
    cid = r["Customer ID"]
    c = {k: ["", ""] for k in COLS}
    S = lambda k, v, src="sage": c.__setitem__(k, [v, src if v else ""])
    flags = []
    investor = bool(re.match(r"C\d+$", cid))
    last, bal = date(r["Last invoice date"]), float(r["Balance"] or 0)
    in_scope = not investor and ((last and last >= CUTOFF) or bal != 0)
    m = sf.get(norm(r["Customer name"]))

    S("Customer ID", cid)
    S("Company Name", r["Customer name"])
    if m and m.get("Subnet Account Id") is not None:
        S("Subnet ID", str(m["Subnet Account Id"]), "sfdc")
    S("Subsidiary", "MinIO, Inc.", "prop")
    if r["Default currency"]:
        S("Primary Currency", r["Default currency"])
    else:
        S("Primary Currency", "USD", "prop")
    billto = r["billto_name"] and r["billto_name"] != r["display_name"]
    email = (r["billto_email"] if billto and r["billto_email"] else r["display_email"])
    S("Customer Invoice Email", email)
    if email and (re.search(r"[;/ ,]", email.strip()) or len(email) > 64):
        flags.append("Several emails")
    S("Individual (Type)", "FALSE", "prop")
    cat = CATEGORY.get(r["Customer type"], "")
    S("Customer Category", cat, "prop")
    if r["Customer type"] and not cat:
        flags.append("Category to decide")
    phone = r["display_phone"]
    if phone:
        S("Phone", phone)
    elif m and m.get("Phone"):
        S("Phone", str(m["Phone"]), "sfdc")
    S("Addressee", r["display_name"])
    S("Address 1", r["display_line1"].rstrip(","))
    S("Address 2", r["display_line2"].rstrip(","))
    l = lst.get(cid, {})
    S("City", l.get("City", "").rstrip(", ").strip())
    S("Province/State", l.get("State or territory", ""))
    S("Postal Code/Zip", l.get("ZIP or postal code", ""))
    S("Country", r["display_country"])
    if r["display_line1"]:
        S("Default Billing", "TRUE", "prop")
        S("Default Shipping", "TRUE", "prop")
    else:
        flags.append("No street address")
    if r["Term"]:
        t = TERMS.get(r["Term"], "")
        if t:
            S("Terms", t, "prop" if t != r["Term"] else "sage")
        else:
            S("Terms", r["Term"])
            flags.append("Terms to map")
    S("VAT ID", r["Tax ID"])
    for k in REQUIRED:
        if not c[k][0]:
            c[k][1] = "miss"

    if investor:
        flags.append("Investor or non-sales")
    dup = [x for x in names[r["Customer name"].strip().lower()] if x != cid]
    if dup:
        flags.append("Duplicate name: " + ", ".join(dup))
    else:
        nd = [x for x in near[norm(r["Customer name"])] if x != cid]
        if nd:
            flags.append("Similar name: " + ", ".join(nd))
    if billto:
        flags.append("Billed to another party")
    if not m:
        flags.append("No Salesforce match")
    if not r["Customer type"] and not investor:
        flags.append("No customer type")
    if not last:
        flags.append("No invoice in Sage")

    review = [r["Customer type"], last.isoformat() if last else "", f"{bal:,.2f}" if bal else "",
              r["billto_name"] if billto else "", m["Account Name"] if m else ""]
    out.append({"scope": bool(in_scope), "cells": [c[k] for k in COLS], "review": review, "flags": flags})

data = {"cols": COLS, "required": sorted(REQUIRED), "review": REVIEW, "rows": out,
        "built": TODAY.isoformat(), "cutoff": CUTOFF.isoformat()}
tpl = open("tools/review-template.html", encoding="utf-8").read()
open("data/customer-review.html", "w", encoding="utf-8").write(
    tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")))
print(f"{len(out)} active customers, {sum(r['scope'] for r in out)} in scope -> data/customer-review.html")
