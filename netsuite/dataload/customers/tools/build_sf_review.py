#!/usr/bin/env python3
# Salesforce matches by email domain, for review: loaded customers with no Salesforce match whose email domain is a
# Salesforce account's website. Each row carries a recommendation; nothing is applied to the load until Anthony decides.
#   python3 tools/build_sf_review.py   (run from the customers folder after build_review.py)
import collections, csv, difflib, re
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

OUT = "data/MinIO_Customer_Salesforce_Matches_to_Review_20261028.xlsx"
rows = list(csv.DictReader(open("data/customer-load-draft.csv", encoding="utf-8-sig")))
load = [r for r in rows if not r["Duplicate Action"].startswith("Merge into")]
srows = list(openpyxl.load_workbook("data/sfdc-accounts-customers-20261025.xlsx", read_only=True).active.iter_rows(values_only=True))
hdr = next(r for r in srows if r and "Account ID" in r)
accounts = [{k: "" if v in (None, "-") else str(v) for k, v in zip(hdr, r)} for r in srows
            if r and isinstance(r[2], str) and re.match(r"001\w{12}$", r[2])]

def id18(i):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ012345"
    return i + "".join(alpha[sum(1 << n for n, ch in enumerate(i[k:k + 5]) if ch.isupper())] for k in (0, 5, 10))

used = {r["Salesforce Account ID"][:15]: r["Customer ID"] for r in load if r["Salesforce Account ID"]}
by_site = collections.defaultdict(list)
for a in accounts:
    site = re.sub(r"^www\.", "", re.sub(r"^https?://", "", a["Website"].lower())).split("/")[0]
    if site:
        by_site[site].append(a)

# Recommendations from reading each candidate against the Sage record (2026-10-28).
REJECT = {("C-00030", "AT&T"): "AT&T US parent, no Subnet ID; the customer is AT&T Mexico",
          ("C-00100", "IBM India"): "IBM India, not IBM Corporation (US)",
          ("C-00170", "Herzum Inc [C]"): "Herzum is the reseller's domain, not the customer's",
          ("C-00214", "NASA - AMES"): "Another NASA center; JPL is not in Salesforce under this domain",
          ("C-00214", "NASA GSFC"): "Another NASA center; JPL is not in Salesforce under this domain",
          ("C-00277", "RundfunkBerlin-Brandenburg"): "Different organisation sharing the ivz.de domain",
          ("C-00395", "USACE"): "army.mil is shared by the whole US Army; not Yuma Proving Ground",
          ("C-00395", "US Army"): "army.mil is shared by the whole US Army; not Yuma Proving Ground",
          ("C-00286", "US Army"): "USACE has its own account (Subnet 629)",
          ("C-00172", "Orange-RDC"): "Orange RDC is C-00276; Orange-GOS is this customer",
          ("C-00512", "Xerox"): None}  # None: decided by Subnet ID below
GROUP = {"C-00050", "C-00090", "C-00127", "C-00159", "C-00211", "C-00236", "C-00244", "C-00256", "C-00279", "C-00289",
         "C-00310", "C-00540", "C-00558", "C-00590", "C-00612"}
CONFLICT = {
    "C-00219": "Salesforce account already matched to C-00120 Federal Home Loan Mortgage Corporation: Freddie Mac is the same company, so C-00219 and C-00120 may be duplicates",
    "C-00303": "Equinix (Subnet 691) also matches C-00364 Equinix (US) Enterprises: one Subnet account, two Sage customers",
    "C-00364": "Equinix (Subnet 691) also matches C-00303 Equinix Services: one Subnet account, two Sage customers",
    "C-00167": "Disney Entertainment & Sports (Subnet 385) also matches C-00218: one Subnet account, two Sage customers",
    "C-00218": "Disney Entertainment & Sports (Subnet 385) also matches C-00167: one Subnet account, two Sage customers",
    "C-00208": "Viennalife (Subnet 329) also fits C-00097 Aegon Emeklilik (same address): C-00097 may be a duplicate of C-00208",
    "C-00116": "ZATCA has four Subnet accounts in Salesforce (371, 715, 731, 852; 852 is matched to C-00445): which is this customer?",
    "C-00516": "Leidos has three accounts in Salesforce (Leidos-1 Subnet 895, Leidos-2 Subnet 972, Leidos-3 no Subnet): which is this customer?",
    "C-00640": "Hollister has two Subnet accounts in Salesforce (1012 Hollister - Credit Card, 1132 Hollister Inc.): which is this customer?",
}
norm = lambda s: re.sub(r"[^a-z0-9 ]", " ", s.lower())
out = []
for r in load:
    if r["Salesforce Account ID"]:
        continue
    domains = {e.split("@")[1].lower() for e in (r["Customer Invoice Email"] + "; " + r["Additional Emails"]).split("; ")
               if "@" in e} - {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com"}
    seen = set()
    for d in sorted(domains):
        for site, accs in by_site.items():
            if site != d and not d.endswith("." + site):
                continue
            for a in accs:
                if a["Account ID"] in seen:
                    continue
                seen.add(a["Account ID"])
                key = (r["Customer ID"], a["Account Name"])
                if key in REJECT and REJECT[key]:
                    rec, why = "Reject", REJECT[key]
                elif r["Customer ID"] == "C-00512":
                    rec, why = ("Same company: accept", "Xerox France account with a Subnet ID; the contact is French") if a["Subnet Account Id"] \
                        else ("Reject", "Xerox US head office, no Subnet ID")
                elif r["Customer ID"] in CONFLICT:
                    rec, why = "Decide", CONFLICT[r["Customer ID"]]
                elif a["Account ID"] in used:
                    rec, why = "Decide", f"Salesforce account already matched to {used[a['Account ID']]}"
                elif r["Customer ID"] in GROUP:
                    rec, why = "Same group: decide", "Parent or affiliate of the customer, not the same legal entity"
                else:
                    rec, why = "Same company: accept", ""
                out.append([r["Customer ID"], r["Company Name"], r["City"], r["Country"], d, a["Account Name"], id18(a["Account ID"]),
                            a["Subnet Account Id"], a["Billing City"], a["Billing Country"], used.get(a["Account ID"], ""), rec, why, ""])
# Aegon Emeklilik has no email in Sage, so no domain; it was found by name (Viennalife, formerly Aegon).
via = next(a for a in accounts if a["Account Name"].startswith("Viennalife"))
c97 = next(r for r in load if r["Customer ID"] == "C-00097")
out.append(["C-00097", c97["Company Name"], c97["City"], c97["Country"], "(name: formerly Aegon)", via["Account Name"],
            id18(via["Account ID"]), via["Subnet Account Id"], via["Billing City"], via["Billing Country"], "", "Decide",
            "Same account fits C-00208 Aegon_Viennalife (same address): C-00097 may be a duplicate of C-00208", ""])

thin = Side(style="thin", color="D6DEE3")
grid = Border(left=thin, right=thin, top=thin, bottom=thin)
FILL = {"Same company: accept": "DCEFEF", "Same group: decide": "FFF2CF", "Decide": "FFF2CF", "Reject": "FCE5E2"}
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Matches to review"
ws["A1"] = ("Salesforce accounts found by email domain for customers in the load with no Salesforce match. Accepting a row sets "
            "the customer's Salesforce Account ID and Subnet ID. Fill in Your decision (Accept or Reject); nothing is applied until then.")
ws.merge_cells("A1:N1"); ws["A1"].alignment = Alignment(wrap_text=True); ws.row_dimensions[1].height = 32
heads = ["Customer ID", "Customer (Sage)", "City", "Country", "Matched on", "Salesforce account", "Salesforce Account ID",
         "Subnet ID", "Salesforce city", "Salesforce country", "Already matched to", "Recommendation", "Why", "Your decision"]
for k, h in enumerate(heads, 1):
    c = ws.cell(row=2, column=k, value=h); c.font = Font(bold=True); c.fill = PatternFill("solid", fgColor="E8EEF1"); c.border = grid
order = {"Decide": 0, "Same group: decide": 1, "Reject": 2, "Same company: accept": 3}
for i, row in enumerate(sorted(out, key=lambda x: (order[x[11]], x[0])), 3):
    for k, v in enumerate(row, 1):
        c = ws.cell(row=i, column=k, value=v or None); c.border = grid; c.alignment = Alignment(vertical="top", wrap_text=k in (2, 6, 13))
    ws.cell(row=i, column=12).fill = PatternFill("solid", fgColor=FILL[row[11]])
for k, w in enumerate([10, 34, 16, 14, 22, 34, 20, 9, 16, 14, 12, 20, 60, 14], 1):
    ws.column_dimensions[openpyxl.utils.get_column_letter(k)].width = w
ws.freeze_panes = "C3"
ws.auto_filter.ref = f"A2:N{len(out) + 2}"
wb.save(OUT)
print(len(out), "candidate rows for", len({x[0] for x in out}), "customers:", collections.Counter(x[11] for x in out), "->", OUT)

# The same rows as an interactive review page (data/, not committed): decisions save to the page's database.
import json
REC_KEY = {"Same company: accept": "accept", "Same group: decide": "group", "Decide": "decide", "Reject": "reject"}
data = [dict(zip(["cid", "cname", "ccity", "ccountry", "domain", "sfname", "sfid", "subnet", "sfcity", "sfcountry", "used", "rec", "why"],
                 row[:13]), rec=REC_KEY[row[11]]) for row in out]
tpl = open("tools/sf-review-template.html", encoding="utf-8").read()
open("data/sf-match-review.html", "w", encoding="utf-8").write(
    tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
print("review page -> data/sf-match-review.html")
