#!/usr/bin/env python3
# Build the vendor review page and load files: active Sage vendors mapped to the SOA vendor template, enriched from Ramp.
#   python3 tools/build_review.py   (run from the vendors folder; reads data/, writes data/)
# Bank account details are never written to the page. Tax IDs are masked on the page and full in the load file.
import csv, datetime as dt, json, re
import openpyxl

TODAY = dt.date(2026, 10, 26)
ACTIVE_FROM = dt.date(2024, 10, 26)
SAGE = "data/sage-vendors-all-detail-20261025.csv"
EXPORT = "data/sage-vendors-active-export-20261025.csv"
REPORT = "data/sage-vendor-list-report-20261025.csv"
RAMP = "data/ramp-vendors-sensitive-20261025.csv"
COA = "data/coa-sage-map.json"  # Sage account -> COA Draft v1 account, from the dimensions workbook

CATEGORY = {"1099 Vendor": "1099 Vendor", "AR reseller": "AR Reseller", "Audit and Compliance": "Audit and Compliance",
            "Consultants and Advisers": "Consultants and Advisers", "Consultants-Contractors": "Consultants-Contractors",
            "Credit Cards": "Credit Cards", "Customer Reimbursements": "Customer Reimbursements", "Events": "Events",
            "Events Incidental Expenses": "Events Incidental Expenses", "Law Firms": "Law Firms", "Legal": "Legal",
            "MinIO employee": "MinIO Employee", "Public Relations": "Public Relations", "Tax": "Tax agency"}

def term(t):
    t = (t or "").strip()
    if not t:
        return ""
    if t.lower() == "due on receipt":
        return "Due on Receipt"
    m = re.match(r"(?:net\s*)?(\d+)(?:\s*days?)?$", t, re.I)
    return f"Net {m.group(1)}" if m else t

def date(s):
    for f in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime((s or "")[:10], f).date()
        except ValueError:
            pass
    return None

rows = list(csv.reader(open(SAGE, encoding="utf-8-sig")))
H = rows[0]
first = {}
for i, c in enumerate(H):
    first.setdefault(c, i)
sage = [r for r in rows[1:] if r and r[0].strip()]
G = lambda r, f: r[first[f]].strip()
ramp_rows = list(csv.DictReader(open(RAMP, encoding="utf-8-sig")))
ramp = {r["Sage Intacct ID"].strip(): r for r in ramp_rows if r["Sage Intacct ID"].strip()}
coa = json.load(open(COA))
code_to_country = {G(r, "Country code"): G(r, "Country") for r in sage if G(r, "Country code") and G(r, "Country")}

COLS = [c.value for c in openpyxl.load_workbook("MINIO_Vendor_Template_10192026.xlsx")["Vendor Template"][2] if c.value]
FIELDS = [c.value for c in openpyxl.load_workbook("MINIO_Vendor_Template_10192026.xlsx")["Vendor Template"][1] if c.value]
assert len(COLS) == len(FIELDS) == 61
REQUIRED = {"companyName"}
ADDED = ["Question Categories", "Sage Vendor ID", "Ramp Vendor ID", "In Ramp", "Bank Details"]
REVIEW = ["Sage type", "Last activity", "Ramp 365-day spend", "Ramp category", "Ramp owner", "Ramp department"]

# Vendor ID: keep V-#####; older V##### and Ramp-created RMP_# get the next numbers after the highest V-#####.
std = [int(G(r, "Vendor ID")[2:]) for r in sage if re.match(r"V-\d{5}$", G(r, "Vendor ID"))]
nxt = max(std) + 1
renumber = {}
def sortkey(i):
    m = re.match(r"(\D+?)_?(\d+)$", i)
    return (m.group(1), int(m.group(2)))
for i in sorted((G(r, "Vendor ID") for r in sage if not re.match(r"V-\d{5}$", G(r, "Vendor ID"))), key=sortkey):
    renumber[i] = f"V-{nxt:05d}"
    nxt += 1

# Sensitive values (bank numbers, tax IDs) from both systems: masked wherever they appear on the page.
SECRET_FIELDS = ("ACH account number", "ACH bank routing number", "Bank routing number", "Wire transfer account number")
bank_numbers = {r[H.index(f)].strip() for r in sage for f in SECRET_FIELDS if len(r[H.index(f)].strip()) >= 5}
bank_numbers |= {r[k].strip() for r in ramp_rows for k in ("Default ACH routing number", "Default ACH account number",
                 "Default wire routing number", "Default wire account number") if len(r[k].strip()) >= 5}
tax_ids = {r[i].strip() for r in sage for i, h in enumerate(H) if h == "Tax ID" and len(re.sub(r"\W", "", r[i])) >= 6}
tax_ids |= {r["Taxpayer identification number (TIN)"].strip() for r in ramp_rows if len(r["Taxpayer identification number (TIN)"].strip()) >= 5}
SECRETS = sorted(bank_numbers | tax_ids, key=len, reverse=True)
def mask(v):
    for x in SECRETS:
        if x in v:
            v = v.replace(x, "•••" + re.sub(r"\W", "", x)[-4:])
    return v

names = {}
for r in sage:
    names.setdefault(re.sub(r"[^a-z0-9]", "", G(r, "Vendor name").lower()), []).append(G(r, "Vendor ID"))

out, load_rows = [], []
for r in sage:
    sid = G(r, "Vendor ID")
    rp = ramp.get(sid)
    c = {f: ["", ""] for f in FIELDS}
    flags, qc = [], []
    def S(f, v, src="sage"):
        v = (v or "").strip()
        c[f] = [v, src if v else ""]
    vid = renumber.get(sid, sid)
    S("vendorId", vid, "rule" if sid in renumber else "sage")
    S("externalId", vid, "rule")
    if sid in renumber:
        flags.append(f"Renumbered from Sage {sid}")
    person = G(r, "This vendor is an individual person") == "Yes"
    S("isPerson", "TRUE" if person else "FALSE", "sage" if person else "rule")
    if person:
        S("firstName", G(r, "First name")); S("middleName", G(r, "Middle name")); S("lastName", G(r, "Last name"))
        if not (G(r, "First name") and G(r, "Last name")):
            flags.append("Individual without first and last name")
    S("companyName", G(r, "Vendor name"))
    t = G(r, "Vendor type ID")
    if t:
        cat = CATEGORY.get(t)
        if cat:
            S("category", cat, "sage" if cat == t else "rule")
        else:
            flags.append(f"Vendor type not on the category list: {t}")
    S("subsidiary", "MinIO, Inc.", "rule")
    cur = G(r, "Default currency")
    if cur in ("INR", "SGD"):
        qc.append("Subsidiary to confirm")
        c["subsidiary"][1] = "prop"
    S("phone", G(r, "Phone number"))
    if not c["phone"][0] and rp and rp["Contact phone number"].strip():
        S("phone", rp["Contact phone number"].strip().lstrip("'"), "ramp")
    S("fax", G(r, "Fax number"))
    S("email", G(r, "Email address"))
    if not c["email"][0] and rp and rp["Contact email"].strip():
        S("email", rp["Contact email"], "ramp")
    S("comments", G(r, "Comments"))
    # Address 1: the Sage main address, else Ramp's check mailing address. Address 2: Sage pay-to address where different.
    if G(r, "Address line 1"):
        S("address1_line1", G(r, "Address line 1"))
        S("address1_line2", ", ".join(x for x in (G(r, "Address line 2"), G(r, "Address line 3")) if x))
        S("address1_city", G(r, "City")); S("address1_state", G(r, "State or territory"))
        S("address1_zipCode", G(r, "ZIP or postal code")); S("address1_country", G(r, "Country"))
    elif rp and rp["Check mailing address line 1"].strip():
        S("address1_line1", rp["Check mailing address line 1"], "ramp"); S("address1_line2", rp["Check mailing address line 2"], "ramp")
        S("address1_city", rp["Check mailing city"].strip(" ,"), "ramp"); S("address1_state", rp["Check mailing state/province/region"], "ramp")
        S("address1_zipCode", rp["Check mailing zip/postal code"], "ramp")
        S("address1_country", code_to_country.get(rp["Check mailing country code"].strip(), rp["Check mailing country code"]), "ramp")
    else:
        S("address1_country", G(r, "Country"))
        flags.append("No street address")
    if c["address1_line1"][0]:
        S("address1_addressee", G(r, "Vendor name"), "rule")
        S("address1_defaultBilling", "TRUE", "rule")
        S("address1_defaultShipping", "TRUE", "rule")
        S("address1_addressName", "Main", "rule")
    pay = G(r, "Pay-to contact address: Line 1")
    if pay and pay.lower() != c["address1_line1"][0].lower():
        S("address2_addressName", "Remit-to", "rule"); S("address2_addressee", G(r, "Vendor name"), "rule")
        S("address2_line1", pay); S("address2_line2", G(r, "Pay-to contact address: Line 2"))
        S("address2_city", G(r, "Pay-to contact address: City")); S("address2_state", G(r, "Pay-to contact address: State or territory"))
        S("address2_zipCode", G(r, "Pay-to contact address: ZIP or postal code")); S("address2_country", G(r, "Pay-to contact address: Country"))
        S("address2_defaultBilling", "TRUE", "rule"); S("address2_defaultShipping", "FALSE", "rule")
        c["address1_defaultBilling"] = ["FALSE", "rule"]
    S("legalName", rp["Vendor legal name"] if rp and rp["Vendor legal name"].strip() else G(r, "1099 name"),
      "ramp" if rp and rp["Vendor legal name"].strip() else "sage")
    acct = G(r, "Number")
    if acct in bank_numbers:
        flags.append("Sage account number field holds a bank account number; not loaded")
    else:
        S("accountNumber", acct)
    if any(x in G(r, "Address line 1") + G(r, "Address line 2") for x in tax_ids):
        flags.append("Tax ID written in the Sage address")
    if G(r, "Term"):
        S("terms", term(G(r, "Term")), "sage" if term(G(r, "Term")) == G(r, "Term") else "rule")
    elif rp and rp["Net payment terms (days)"].strip():
        S("terms", term(rp["Net payment terms (days)"]), "ramp")
    exp = G(r, "Default expense account")
    if exp:
        mapped = coa.get(exp.split()[0].split("-")[0])
        if mapped:
            S("defaultExpenseAccount", mapped, "rule")
        else:
            flags.append(f"Sage expense account {exp} has no COA Draft v1 mapping")
    S("defaultPayablesAccount", "20100 Accounts Payable - Trade", "rule")
    tax = G(r, "Tax ID") or r[[i for i, h in enumerate(H) if h == "Tax ID"][1]].strip()
    if tax:
        S("taxIdNum", tax)
    elif rp and rp["Taxpayer identification number (TIN)"].strip():
        S("taxIdNum", rp["Taxpayer identification number (TIN)"].strip(), "ramp")
    if len(re.sub(r"\D", "", c["taxIdNum"][0])) > 15:
        flags.append("Tax ID longer than 15 characters")
    if G(r, "Form 1099 type") or t == "1099 Vendor":
        S("is1099Eligible", "TRUE", "sage" if G(r, "Form 1099 type") else "rule")
    S("currency", cur or "USD", "sage" if cur else "rule")
    S("Legacy Vendor ID", sid)
    S("Source System", "Sage Intacct; Ramp" if any(v[1] == "ramp" for v in c.values()) else "Sage Intacct", "rule")
    c["companyName"][1] = c["companyName"][1] or "miss"

    last = max([d for d in (date(G(r, "Last bill created on")), date(G(r, "Last payment made on")),
                            date(rp["Last spend date"]) if rp else None) if d], default=None)
    sb = bool(G(r, "ACH account number"))
    rb = bool(rp and rp["Default ACH account number"].strip())
    if sb and rb:
        same = G(r, "ACH account number")[-4:] == rp["Default ACH account number"].strip()[-4:]
        bank = "Sage and Ramp, same" if same else "Sage and Ramp, differ"
        if not same:
            flags.append("Bank account differs between Sage and Ramp")
    else:
        bank = "Sage" if sb else "Ramp" if rb else ""
    k = re.sub(r"[^a-z0-9]", "", G(r, "Vendor name").lower())
    dup = [x for x in names[k] if x != sid]
    if dup:
        flags.append("Duplicate name: " + ", ".join(dup))
        qc.append("Duplicate to review")
    if not c["email"][0]:
        flags.append("No email")
    if not last:
        flags.append("No activity recorded")
    added = [["; ".join(qc), "rule" if qc else ""], [sid, "sage"], [rp["Vendor ID"] if rp else "", "ramp" if rp else ""],
             ["Yes" if rp else "No", "rule"], [bank, "rule" if bank else ""]]
    review = [t, last.isoformat() if last else "", f"{float(rp['Total 365 day spend'] or 0):,.2f}" if rp else "",
              rp["Ramp category"] if rp else "", rp["Owner name"] if rp else "", rp["Department"] if rp else ""]
    cells = [c[f] for f in FIELDS] + added
    load_rows.append(cells)
    page = [[mask(v), src] for v, src in cells]
    ti = FIELDS.index("taxIdNum")
    if page[ti][0]:
        page[ti][0] = "•••" + re.sub(r"\W", "", cells[ti][0])[-4:]
    flags = [mask(f) for f in flags]
    out.append({"cells": page, "review": review, "flags": flags, "active": bool(last and last >= ACTIVE_FROM)})

QI = len(FIELDS)
rank = {"Subsidiary to confirm": 0, "Duplicate to review": 1}
out.sort(key=lambda x: (min([rank.get(q, 9) for q in x["cells"][QI][0].split("; ") if q] or [9]), x["cells"][1][0]))

export = list(csv.reader(open(EXPORT, encoding="utf-8-sig")))
rep = [x for x in csv.reader(open(REPORT, encoding="utf-8-sig")) if re.match(r"(V-?\d+|RMP_\d+)$", x[0].strip())]
bridge = {"export": len(export) - 1, "onetime": [(x[0], x[1]) for x in export[1:] if x[7] == "True"],
          "report": len(rep), "inactive": sum(1 for x in rep if x[8] != "Active"), "active": len(out),
          "in_ramp": sum(1 for x in out if x["cells"][QI + 3][0] == "Yes"), "ramp_total": len(ramp_rows),
          "ramp_only": [r["Vendor name"] for r in ramp_rows if not r["Sage Intacct ID"].strip()]}
data = {"cols": COLS + ADDED, "fields": FIELDS + ADDED, "required": ["Company Name"], "review": REVIEW, "rows": out,
        "renumber": renumber, "last_std": f"V-{max(std):05d}", "next_id": f"V-{nxt:05d}", "bridge": bridge}
tpl = open("tools/review-template.html", encoding="utf-8").read()
open("data/vendor-review.html", "w", encoding="utf-8").write(
    tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")))
with open("data/vendor-load.csv", "w", newline="", encoding="utf-8-sig") as o:
    w = csv.writer(o)
    w.writerow(FIELDS + ADDED)
    w.writerow(COLS + ADDED)
    for cells in load_rows:
        if cells[QI + 3][0] == "No":
            w.writerow([x[0] for x in cells])
print(f"{len(out)} active Sage vendors; {bridge['in_ramp']} in Ramp; {len(out) - bridge['in_ramp']} to load -> data/vendor-load.csv")
print(f"renumbered {len(renumber)} ({min(renumber.values())} to {max(renumber.values())}); next {data['next_id']}")
