#!/usr/bin/env python3
# Build the customer review page: Sage customers mapped to the NetSuite template, enriched from Salesforce.
#   python3 tools/build_review.py   (run from the customers folder; reads data/, writes data/customer-review.html)
import csv, datetime as dt, difflib, json, re, unicodedata
import openpyxl

TODAY = dt.date(2026, 10, 26)
FLAT = "data/sage-customers-flat-20261025.csv"
LIST = "data/sage-customers-20261026.csv"
SFDC = "data/sfdc-accounts-customers-20261025.xlsx"  # Lifecycle = Active or Customer, Classic report copy
PARTNERS = "data/sfdc-accounts-with-partners-20261025.xlsx"

TERMS = {"30 Days": "Net 30", "45 Days": "Net 45", "60 Days": "Net 60", "90 Days": "Net 90",
         "120 Days": "Net 120", "20 Days": "Net 20", "28 days": "Net 28", "Net 30": "Net 30",
         "Due on Receipt": "Due on Receipt"}
CATEGORY = {"Direct Sales": "Direct Customer", "Direct Sales with Reseller": "End Customer", "Reseller": "Reseller"}

def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = re.sub(r"\[c\]", " ", s.lower())
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\b(inc|llc|ltd|limited|corp|corporation|co|plc|gmbh|sa|ag|bv|pte|pvt|the|company|group|holdings?)\b", "", s)
    return " ".join(s.split())

def id18(i):
    """Salesforce 15-character ID to the case-safe 18-character ID."""
    if not i or len(i) != 15:
        return i
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ012345"
    return i + "".join(alpha[sum(1 << n for n, ch in enumerate(i[k:k + 5]) if ch.isupper())] for k in (0, 5, 10))

def val(v):
    return "" if v in (None, "-") else str(v).strip()

def date(s):
    try:
        return dt.datetime.strptime(s, "%m/%d/%Y").date()
    except ValueError:
        return None

sage = list(csv.DictReader(open(FLAT, encoding="utf-8-sig")))
lst = {r["Customer ID"]: r for r in csv.DictReader(open(LIST, encoding="utf-8-sig"))}
srows = list(openpyxl.load_workbook(SFDC, read_only=True).active.iter_rows(values_only=True))
shdr = next(r for r in srows if r and "Account ID" in r)
accounts = [{k: val(v) for k, v in zip(shdr, r)} for r in srows
            if r and isinstance(r[2], str) and re.match(r"001\w{12}$", r[2])]
sf = {}
for a in accounts:
    sf.setdefault(norm(a["Account Name"]), a)
sfkeys = list(sf)
by_id = {a["Account ID"]: a for a in accounts}

def match(name):
    k = norm(name)
    if k in sf:
        return sf[k], "exact"
    best = difflib.get_close_matches(k, sfkeys, n=1, cutoff=0.88)
    return (sf[best[0]], "likely") if best else (None, "")

# Accounts with Partners: link each account to its partner accounts, both directions, by normalized name.
partners = {}
for r in openpyxl.load_workbook(PARTNERS, read_only=True).active.iter_rows(values_only=True):
    if r and isinstance(r[0], str) and re.match(r"001\w{12}$", r[0]) and r[1] and r[2]:
        partners.setdefault(norm(r[1]), set()).add(r[1 + 1])
        partners.setdefault(norm(r[2]), set()).add(r[1])

# Customer ID: keep Sage C-##### numbers; give non-conforming Sage IDs the next numbers after the highest C-#####.
std = [int(x["Customer ID"][2:]) for x in sage if re.match(r"C-\d{5}$", x["Customer ID"])]
nxt = max(std) + 1
renumber = {}
for x in sorted((x for x in sage if x["Status"] == "Active" and not re.match(r"C-\d{5}$", x["Customer ID"])), key=lambda x: x["Customer ID"]):
    renumber[x["Customer ID"]] = f"C-{nxt:05d}"
    nxt += 1

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
ADDED = ["Sage Customer ID", "Salesforce Account ID", "Billed To (Reseller)", "Reseller Address", "Reseller Invoice Email", "Salesforce Partners"]
REVIEW = ["Sage type", "Last invoice", "Balance", "Salesforce match"]

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
    in_scope = True  # every customer not marked inactive in Sage
    m, how = match(r["Customer name"])

    if cid in renumber:
        S("Customer ID", renumber[cid], "prop")
        flags.append(f"Renumbered from Sage {cid}")
    else:
        S("Customer ID", cid)
    S("External ID", c["Customer ID"][0], c["Customer ID"][1])
    S("Company Name", r["Customer name"])
    if m:
        S("Subnet ID", m["Subnet Account Id"], "sfdc")
        if m["Parent Account ID"]:
            par = by_id.get(m["Parent Account ID"])
            S("Parent Company", m["Parent Account"], "sfdc")
            if not par or not any(norm(par["Account Name"]) == norm(x["Customer name"]) for x in sage):
                flags.append("Parent not in load")
    S("Subsidiary", "MinIO, Inc.", "prop")
    if r["Default currency"]:
        S("Primary Currency", r["Default currency"])
    else:
        S("Primary Currency", "USD", "prop")
    billto = r["billto_name"] and r["billto_name"] != r["display_name"]
    email = r["display_email"]
    S("Customer Invoice Email", email)
    if email and (re.search(r"[;/ ,]", email.strip()) or len(email) > 64):
        flags.append("Several emails")
    S("Status", "CUSTOMER-Closed Won", "prop")
    S("Individual (Type)", "FALSE", "prop")
    cat = CATEGORY.get(r["Customer type"], "")
    S("Customer Category", cat, "prop")
    if r["Customer type"] and not cat:
        flags.append("Category to decide")
    phone = r["display_phone"]
    if phone:
        S("Phone", phone)
    elif m and m["Phone"]:
        S("Phone", m["Phone"], "sfdc")
    S("Addressee", r["display_name"])
    S("Address 1", r["display_line1"].rstrip(","))
    S("Address 2", r["display_line2"].rstrip(","))
    l = lst.get(cid, {})
    S("City", l.get("City", "").rstrip(", ").strip())
    S("Province/State", l.get("State or territory", ""))
    S("Postal Code/Zip", l.get("ZIP or postal code", ""))
    S("Country", r["display_country"])
    if not r["display_line1"] and m and m["Billing Street"]:
        S("Address 1", m["Billing Street"], "sfdc")
        S("City", m["Billing City"], "sfdc")
        S("Province/State", m["Billing State/Province"], "sfdc")
        S("Postal Code/Zip", m["Billing Zip/Postal Code"], "sfdc")
        S("Country", m["Billing Country"], "sfdc")
    if c["Address 1"][0]:
        S("Default Billing", "TRUE", "prop")
        S("Default Shipping", "TRUE", "prop")
    else:
        flags.append("No street address")
    if m and m["Billing Country"] and r["display_country"] and m["Billing Country"].lower() != r["display_country"].lower():
        flags.append(f"Country differs in Salesforce: {m['Billing Country']}")
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
    if not m:
        flags.append("No Salesforce match")
    elif how == "likely":
        flags.append("Likely Salesforce match, confirm")
    if not r["Customer type"] and not investor:
        flags.append("No customer type")
    if not last:
        flags.append("No invoice in Sage")

    added = [["", ""] for _ in ADDED]
    added[0] = [cid, "sage"]
    if m:
        added[1] = [id18(m["Account ID"]), "sfdc" if how == "exact" else "prop"]
    if billto:
        addr = ", ".join(x.strip(" ,") for x in [r["billto_line1"], r["billto_line2"], r["billto_citystatezip_country"]] if x.strip(" ,"))
        added[2] = [r["billto_name"], "sage"]
        added[3] = [addr.replace(",,", ","), "sage" if addr else ""]
        added[4] = [r["billto_email"], "sage" if r["billto_email"] else ""]
    p = partners.get(norm(r["Customer name"]))
    if not p and m:
        p = partners.get(norm(m["Account Name"]))
    if p:
        added[5] = ["; ".join(sorted(p)), "sfdc"]
    review = [r["Customer type"], last.isoformat() if last else "", f"{bal:,.2f}" if bal else "",
              (m["Account Name"] + (" (likely)" if how == "likely" else "")) if m else ""]
    out.append({"scope": bool(in_scope), "cells": [c[k] for k in COLS] + added, "review": review, "flags": flags})

# Flag Sage customers that matched the same Salesforce account.
SFI = len(COLS) + 1
seen = {}
for x in out:
    e = x["cells"][SFI][0].lower()
    if e:
        seen.setdefault(e, []).append(x["cells"][2][0])
for x in out:
    ids = seen.get(x["cells"][SFI][0].lower(), [])
    if len(ids) > 1:
        x["flags"].append("Same Salesforce account as " + ", ".join(i for i in ids if i != x["cells"][2][0]))

data = {"cols": COLS + ADDED, "required": sorted(REQUIRED), "review": REVIEW, "rows": out, "built": TODAY.isoformat(),
        "renumber": renumber, "last_std": f"C-{max(std):05d}", "next_id": f"C-{nxt:05d}"}
tpl = open("tools/review-template.html", encoding="utf-8").read()
open("data/customer-review.html", "w", encoding="utf-8").write(
    tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")))
matched = {norm(x["review"][3].replace(" (likely)", "")) for x in out if x["review"][3]}
print(f"{len(out)} customers; Salesforce exact {sum(1 for x in out if x['review'][3] and '(likely)' not in x['review'][3])}, likely {sum('(likely)' in x['review'][3] for x in out)}, none {sum(not x['review'][3] for x in out)}")
print(f"Salesforce accounts with no Sage customer: {sum(1 for a in accounts if norm(a['Account Name']) not in matched)} of {len(accounts)}")
