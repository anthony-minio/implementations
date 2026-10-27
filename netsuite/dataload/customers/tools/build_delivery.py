#!/usr/bin/env python3
# Build the customer load workbook for circulation: the load table on one tab, the notes on another.
#   python3 tools/build_delivery.py   (run from the customers folder after build_review.py and validate_load.py)
import collections, json, re
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUT = "data/MinIO_Customer_Load_to_NetSuite_20261027.xlsx"
s = open("data/customer-review.html", encoding="utf-8").read()
data = json.loads(s[s.index("const DATA = ") + 13:s.index(";\nconst $")])
cols, review, required = data["cols"], list(data["review"]), set(data["required"])
rows = data["rows"]
# Drop review columns no row uses (Possible Subnet accounts, now that every Subnet ID is assigned).
keep_review = [k for k in range(len(review)) if any(r["review"][k] for r in rows)]
review = [review[k] for k in keep_review]
for r in rows:
    r["review"] = [r["review"][k] for k in keep_review]

# Same colors as the review page (light theme).
FILL = {"sfdc": "E3EDF9", "rule": "DCEFEF", "prop": "FFF2CF", "miss": "FCE5E2"}
INK = {"sfdc": "2B64A8", "rule": "0D6B70", "prop": "8A5D00", "miss": "A8261F"}
GROUPS = [("Identity", 7), ("Billing and contact", 7), ("Address", 10), ("Financial", 7),
          ("Added columns", len(cols) - 31), ("Review (not loaded)", len(review) + 1)]
thin = Side(style="thin", color="D6DEE3")
grid = Border(left=thin, right=thin, top=thin, bottom=thin)
head_fill = PatternFill("solid", fgColor="E8EEF1")
wrap_top = Alignment(wrap_text=True, vertical="top")

wb = openpyxl.Workbook()
ns = wb.active
ns.title = "Notes"
ws = wb.create_sheet("Customers-Draft")
col = 1
for name, span in GROUPS:
    ws.cell(row=1, column=col, value=name.upper())
    ws.merge_cells(start_row=1, start_column=col, end_row=1, end_column=col + span - 1)
    for k in range(col, col + span):
        c = ws.cell(row=1, column=k); c.fill = head_fill; c.border = grid
        c.font = Font(bold=True, size=9, color="5B6874")
    col += span
headers = cols + review + ["Flags"]
for k, h in enumerate(headers, 1):
    c = ws.cell(row=2, column=k, value=h + (" *" if h in required else ""))
    c.font = Font(bold=True); c.fill = head_fill; c.border = grid
    c.alignment = Alignment(vertical="top", wrap_text=True)
for i, r in enumerate(rows, 3):
    vals = [(v, src) for v, src in r["cells"]] + [(v, "") for v in r["review"]] + [("; ".join(r["flags"]), "")]
    for k, (v, src) in enumerate(vals, 1):
        c = ws.cell(row=i, column=k, value=v if v != "" else None)
        c.number_format = "@"
        c.border = grid
        if src in FILL:
            c.fill = PatternFill("solid", fgColor=FILL[src])
            c.font = Font(color=INK[src], italic=(src == "prop"))
        if k > len(cols):
            c.fill = PatternFill("solid", fgColor="F3F6F7") if not c.fill.fgColor.rgb or c.fill.fgColor.rgb == "00000000" else c.fill
widths = {"Company Name": 40, "Addressee": 32, "Address 1": 36, "Address 2": 24, "Customer Invoice Email": 32,
          "Additional Emails": 40, "Second Address": 44, "Third Address": 44, "Reseller Address": 40,
          "Salesforce Partners": 30, "Flags": 70, "Question Categories": 22, "Phone": 20,
          "Duplicate Action": 30, "Billed To (Reseller)": 28, "Parent Company": 26, "Attention": 26}
for k, h in enumerate(headers, 1):
    ws.column_dimensions[get_column_letter(k)].width = widths.get(h, 16)
ws.row_dimensions[2].height = 30
ws.freeze_panes = "E3"
ws.auto_filter.ref = f"A2:{get_column_letter(len(headers))}{len(rows) + 2}"

# Figures for the notes, counted from the table itself.
ix = {c: k for k, c in enumerate(cols)}
V = lambda r, c: r["cells"][ix[c]][0]
load = [r for r in rows if not V(r, "Duplicate Action").startswith("Merge into")]
B = data["bridge"]
by_type = collections.Counter(r["review"][0] for r in load)
has_flag = lambda r, p: any(f.startswith(p) for f in r["flags"])
ids = lambda rs: ", ".join(V(r, "Customer ID") for r in rs)
phones = [r for r in load if V(r, "Phone")]
ph_out = [r for r in load if has_flag(r, "Phone left out")]
ph_other = [r for r in load if has_flag(r, "Phone is a ")]
addr_fixed = [r for r in load if has_flag(r, "Address fields corrected")]
country_moved = [r for r in addr_fixed if any("Country was" in f for f in r["flags"])]
state_zip = [r for r in addr_fixed if r["cells"][ix["Province/State"]][1] == "rule" and V(r, "Country") == "United States"
             and not any("Province/State was '" in f for f in r["flags"])]
addr_check = [r for r in load if has_flag(r, "Address to check")]
no_country = [r for r in load if has_flag(r, "Country left blank")]
comma = [r for r in rows if V(r, "Country") in ("Korea, Republic of", "Moldova, Republic of", "Congo, Democratic Republic")
         and r["cells"][ix["Country"]][1] == "sage"]
due = [r for r in load if has_flag(r, "Terms left blank")]
cat_missing = [r for r in load if not V(r, "Customer Category")]
TERMS_LIST = {"Due on Receipt", "Net 10", "Net 15", "Net 30", "Net 45", "Net 60", "Net 150"}
nt = collections.Counter(V(r, "Terms") for r in load if V(r, "Terms") and V(r, "Terms") not in TERMS_LIST)
new_terms = ", ".join(f"{t} ({nt[t]})" for t in sorted(nt, key=lambda t: int(t.split()[1])))
split = [r for r in load if V(r, "Duplicate Action").startswith("New: split")]
no_terms = sum(1 for r in load if not V(r, "Terms") and not has_flag(r, "Terms left blank"))
apostrophe = sum(1 for r in load if any(f.startswith("Phone formatted from \"'") for f in r["flags"]))

DECISIONS = [
    ("Investor records",
     "Sage had 16 active records numbered C00001 to C00016 for investors and note holders (for example General Catalyst, "
     "Index Ventures, Interest Accrued on Notes), not customers.",
     "Delete all. Do not import (meeting with Ming, Nisha, Richard, Tory and Sheng, 2026-10-27).",
     "The 16 records are removed. No renumbering is needed any more: every customer keeps its Sage C-##### number."),
    ("Customer Category",
     "The template's four categories (Direct Customer, Reseller, End Customer, OEM/MSP) had no match for the Sage types "
     "Chargebee, Marketplace, MinIO Training Subscription, Event Sponsor and Billing Vendor, and 4 customers had no Sage type.",
     "Create three new categories: Chargebee (direct customers, kept as their own group so Ming can report on them), "
     "Marketplace (customers through the AWS, Azure and GCP marketplaces) and Other (Event Sponsor and Billing Vendor). "
     "MinIO Training Subscription is Direct Customer (meeting, 2026-10-27).",
     f"Category set from the Sage type for every customer: Chargebee {by_type['Chargebee']}, Marketplace {by_type['Marketplace']}, "
     f"Other {by_type['Event Sponsor'] + by_type['Billing Vendor']}, MinIO Training Subscription to Direct Customer "
     f"{by_type['MinIO Training Subscription']}. Chargebee, Marketplace and Other must be created in NetSuite before the load."),
    ("Customers with no Sage type",
     "Four customers had no Sage type, so no category: AEG Worldwide (C-00381), Exness Global Limited (C-00313), "
     "M S International (C-00414) and StoreManager (C-00036).",
     "Per Nisha (Slack, 2026-10-27): AEG Worldwide is an End Customer through Trace3, Subnet 779; Exness is a Direct "
     "Customer, Subnet 669; M S International is a Direct Customer, Subnet 754; StoreManager is left out (no invoices or address).",
     "Category and Subnet ID set for the three; StoreManager removed. The meeting note in Asana gives AEG's Subnet ID as 77; "
     "Nisha's Slack message gives 779, which is used here."),
    ("L3Harris",
     "Sage has three L3Harris customers and Salesforce has five L3Harris Subnet accounts (695, 716, 720, 784, 1026). Each "
     "Subnet account is its own NetSuite customer, so two Subnet accounts had no customer.",
     "Nisha confirmed from the Sage contracts (Slack, 2026-10-27): C-00333 holds three 3-year contracts running at the same "
     "time, one per Subnet account (CN-SO0548, CN-SO0565, CN-SO0603). Split C-00333 into three customers to keep one Subnet "
     "ID per customer.",
     f"C-00333 is Subnet 695. New customers {ids(split)} are Subnets 716 and 720, copied from C-00333 (name, address, terms, "
     "TVAR Solutions bill-to). C-00385 is Subnet 784 and C-00562 is Subnet 1026. For SOA: contracts CN-SO0565 and "
     "CN-SO0603 sit under C-00333 in Sage and must be assigned to the new customers on load."),
    ("One-time-use customers",
     "C-00012 TDA GROUP and C-00021 SPMB are flagged One-time use in Sage and were not in the customer list report the load "
     "is built from.",
     "Load them if they are active in Sage (2026-10-27). They are: Sage's active customer list includes them and leaves out "
     "the 4 inactive customers.",
     "Both added. Sage has only their name and ID (no address, contact, type or terms) and Salesforce has no account for "
     "them, so their Customer Category is missing (open item below)."),
    ("Due per Contract terms",
     f"{len(due)} customers have the Sage term Due per Contract, which is not a NetSuite term.",
     "Leave their terms blank (2026-10-27).",
     f"Terms left blank for {ids(due)}; each is flagged \"Terms left blank\"."),
    ("Phone numbers (column M)",
     f"Phone numbers were in mixed formats: dashes, dots, spaces, \"(0)\" trunk digits, a leading apostrophe on {apostrophe} Sage "
     f"numbers, and country codes without a \"+\". Salesforce writes every 10-digit number as (999) 999-9999, so some "
     "non-US customers carry a US head-office number.",
     "US numbers as (999) 999-9999, so accountants can keep entering them that way; every other number in international "
     "format (+44 20 7885 8888), as the template allows. Numbers that are broken in the source are left out (2026-10-27).",
     f"{len(phones)} numbers written in the standard format, Sage first and Salesforce where Sage has none; the source value "
     f"is in Flags (\"Phone formatted from\"). {len(ph_out)} broken numbers left out: {ids(ph_out)} (each in Flags with the "
     f"reason). {len(ph_other)} numbers belong to a different country than the address, mostly a head office's number in "
     "Salesforce; they are kept and flagged (\"Phone is a ... number\")."),
    ("Country names with a comma",
     "Sage writes some countries with a comma (Korea, Republic of). The draft cut these to the last part: \"Republic of\" "
     "(8 Korea, 1 Moldova) and \"Democratic Republic\" (1 Congo).",
     "Correct them.",
     f"Full names restored for {len(comma)} customers. No other field was affected: city, state and postal code come from "
     "a separate Sage export."),
    ("Address parts in the wrong field",
     "Some Sage addresses had the city, postal code or country typed into the street lines, a street or postal code in the "
     "city field, or a city in the state field. Some customers abroad, mostly Chargebee portal customers, had the country "
     "left at Sage's default, United States.",
     "Each field holds only its own part, and the country is where the address is (2026-10-27).",
     f"{len(addr_fixed)} addresses corrected by moving each part of the Sage text to its own field; nothing is retyped, and "
     f"each change is listed in Flags (\"Address fields corrected from the Sage text\"). Country corrected for "
     f"{len(country_moved)}: {ids(country_moved)}. US state added from the ZIP code for {len(state_zip)}; City set to "
     "Singapore for Singapore addresses. Two Singapore postal codes and one German street (Duravit, whose Sage street line "
     f"was a delivery note) come from Salesforce. {len(addr_check)} addresses to check are flagged \"Address to check\"."),
    ("Country with no address",
     f"{len(no_country)} customers have no address at all in Sage, and Sage shows United States, its default when no address "
     "is entered. Several are not US companies (for example Aegon Emeklilik, National Bank of Cambodia, Nais Sp. z o.o.).",
     "The country is where the address is; with no address there is no country to load.",
     f"Country left blank for {ids(no_country)}, flagged \"Country left blank\"."),
]

NOTES = [
    ("Customer count",
     f"Sage's active customer list has {B['first']} customers. Left out: the 16 investor records and StoreManager "
     f"({B['first']} - 17 = {B['first'] - 17}). Added: the two new L3Harris customers ({B['first'] - 17} + 2 = {B['rows']}, the "
     f"rows on the Customers-Draft tab). {B['merged']} of those are duplicates merged into {B['kept']} other customers, "
     f"leaving {B['load']} customers to load ({B['rows']} - {B['merged']} = {B['load']}). Sage's customer list report also "
     f"has 4 inactive customers, not loaded: {', '.join(i for i, _ in B['inactive'])}."),
    ("Customer ID and External ID",
     "Customer ID is the Sage C-##### number. External ID is the same value, so later loads and updates can find each "
     "customer by it. The two new L3Harris customers take the next numbers after the highest Sage number (C-00641)."),
    ("New customers",
     f"After the load, NetSuite should auto-number new customers as C-##### from {data['next_id']}. In NetSuite: Setup > "
     f"Company > Auto-Generated Numbers, Entities subtab, Customer: prefix C-, minimum 5 digits, initial number "
     f"{int(data['next_id'][2:])}. Allow Override must be on during the import so the loaded numbers are kept. If SOA "
     "prefers C##### without the hyphen, that change is fine."),
    ("Duplicate customers",
     "Some companies appear more than once in Sage: under the same or a similar name, matched to the same Salesforce "
     "account, or sharing an email domain. Each is loaded once. The record kept is the one invoiced most recently, which "
     "also carries any open balance; where none was invoiced, the one with more data, then the lower ID. The other records "
     "are not loaded: their Sage IDs go in Merged Sage IDs, their addresses become the Second and Third Address where "
     "different, and their emails are added to Additional Emails. Records with different Subnet IDs are never merged, and "
     f"two records both invoiced from different countries are kept as separate customers. {B['kept']} groups merged."),
    ("Status", "Every customer is active in Sage, so every customer is CUSTOMER-Closed Won. Renewals can be changed to "
     "CUSTOMER-Renewal when deal data is loaded."),
    ("Customer Invoice Email",
     "Where Sage has an accounts payable or purchasing address (ap@, accounts.payable@, invoices@, purchasing@), that address "
     "is used; otherwise the first address Sage has. Every other address goes to Additional Emails."),
    ("Reseller billing",
     "For customers Sage invoices through a reseller, the reseller is in Billed To (Reseller), Reseller Address and Reseller "
     "Invoice Email, with Salesforce partners alongside, so it can be set up to best practice."),
    ("Subsidiary", "The Sage exports record no entity for any customer. All customers load to MinIO, Inc., the parent subsidiary."),
    ("Terms",
     "Sage terms are mapped to the NetSuite list (Due on Receipt, Net 10, Net 15, Net 30, Net 45, Net 60, Net 150): Sage "
     "\"30 Days\" becomes Net 30, and so on. Day counts with no match on the list become new terms of the same length, to "
     f"create in NetSuite before the load: {new_terms}. Sage \"5 years\" becomes Net 1825. {no_terms} customers have no terms in Sage."),
    ("VAT ID",
     "VAT ID holds VAT or GST registration numbers only, with the country prefix (Sage \"813089973\" for a German customer "
     "becomes DE813089973). India GSTINs, Mexico RFCs and Saudi and UAE VAT numbers are kept as Sage has them. Other tax IDs "
     "in Sage (US EINs, company registration numbers) are in the added Other Tax ID column. International VAT ID is blank."),
    ("Parent Company",
     f"Salesforce links some accounts to a parent. For {data['parents_dropped']} customers the parent is not a Sage customer "
     "(no billing history), so it is not loaded and Parent Company is blank. Parent links are kept where the parent is "
     "itself in this load."),
    ("Salesforce matching",
     "Customers are matched to Salesforce accounts by name. 37 close but not identical names were reviewed on 2026-10-26: "
     "35 confirmed; Ministry of Defence (Singapore) and Bae Systems left unmatched as different companies."),
    ("Sage data corrections",
     "Corrected in the load only; Sage is unchanged. Proctor & Gamble: city Lodz (the address is in Poland). Orange Côte "
     "d'Ivoire: country Côte d'Ivoire (Sage had France), city Abidjan. NSN Brasil: city, postal code and attention. "
     "Garbled accents repaired (MontrÃ©al to Montréal). US postal codes that lost their leading zero restored (7936 to 07936). "
     "Address and country corrections of 2026-10-27 are in the decisions above."),
    ("Country names",
     "Countries are written as Sage writes them (Korea, Republic of; Moldova, Republic of; Congo, Democratic Republic; "
     "Côte d'Ivoire; Palestinian Territory, Occupied). NetSuite's CSV import needs its own country names, so these should "
     "be checked against NetSuite's list when the import is mapped."),
]

OPEN = [
    "Create the customer categories Chargebee, Marketplace and Other in NetSuite before the load (Setup > Accounting > "
    "Accounting Lists > New > Customer Category).",
    f"Terms not on SOA's list: {new_terms}. Create them in NetSuite, or say which existing term each should use. The "
    f"{sum(nt.values())} customers concerned are marked \"New NetSuite term\" in Question Categories.",
    "VAT ID and International VAT ID: SOA to confirm what each field is for, and whether Other Tax ID (US EINs and company "
    "registration numbers) should be loaded anywhere.",
    "L3Harris: assign contracts CN-SO0565 and CN-SO0603 to the new customers C-00642 (Subnet 716) and C-00643 (Subnet 720) "
    "when contracts are loaded.",
    f"Customer Category for {', '.join(V(r, 'Customer ID') + ' ' + V(r, 'Company Name') for r in cat_missing)}: Sage has only their names, so there is no type to set it "
    "from. They are marked \"Category missing\" in Question Categories.",
]

ns.column_dimensions["A"].width = 5
ns.column_dimensions["B"].width = 26
ns.column_dimensions["C"].width = 55
ns.column_dimensions["D"].width = 55
ns.column_dimensions["E"].width = 60
ns["A1"] = "MinIO customer load to NetSuite: notes"; ns["A1"].font = Font(bold=True, size=14)
ns["A2"] = (f"Built {data['built']} from the Sage and Salesforce exports of 2026-10-25 and 2026-10-26 (attached to the Asana "
            f"task). The Customers-Draft tab has {B['rows']} rows: {B['load']} customers to load and {B['merged']} duplicates "
            "marked \"Merge into\" in Duplicate Action, which are not loaded. Columns marked * are required. Flags (last "
            "column) lists everything changed or worth checking on each row. Cell colors show where each value comes from:")
ns.merge_cells("A2:E2"); ns["A2"].alignment = wrap_top; ns.row_dimensions[2].height = 48
row = 3
for label, key in (("From Sage", None), ("From Salesforce", "sfdc"), ("Set by rule or decision", "rule"),
                   ("Proposed", "prop"), ("Required, missing", "miss")):
    c = ns.cell(row=row, column=2, value=label)
    if key:
        c.fill = PatternFill("solid", fgColor=FILL[key]); c.font = Font(color=INK[key], italic=(key == "prop"))
    c.border = grid
    row += 1
row += 1

def heading(text):
    global row
    ns.cell(row=row, column=1, value=text).font = Font(bold=True, size=12)
    row += 1

heading("Decisions")
for k, h in enumerate(["#", "Topic", "Scenario or question", "Decision", "What changed in this file"], 1):
    c = ns.cell(row=row, column=k, value=h); c.font = Font(bold=True); c.fill = head_fill; c.border = grid
row += 1
for n, d in enumerate(DECISIONS, 1):
    for k, v in enumerate((n,) + d, 1):
        c = ns.cell(row=row, column=k, value=v); c.alignment = wrap_top; c.border = grid
        if k == 2:
            c.font = Font(bold=True)
    row += 1
row += 1
heading("How the file was built")
for n, (topic, text) in enumerate(NOTES, 1):
    ns.cell(row=row, column=1, value=n).alignment = wrap_top
    ns.cell(row=row, column=2, value=topic).font = Font(bold=True)
    ns.cell(row=row, column=2).alignment = wrap_top
    ns.cell(row=row, column=3, value=text).alignment = wrap_top
    ns.merge_cells(start_row=row, start_column=3, end_row=row, end_column=5)
    ns.row_dimensions[row].height = max(30, 15 * (len(text) // 150 + 1))
    row += 1
row += 1
heading("Open items for SOA")
for n, text in enumerate(OPEN, 1):
    ns.cell(row=row, column=1, value=n).alignment = wrap_top
    ns.cell(row=row, column=2, value=text).alignment = wrap_top
    ns.merge_cells(start_row=row, start_column=2, end_row=row, end_column=5)
    ns.row_dimensions[row].height = max(30, 15 * (len(text) // 170 + 1))
    row += 1

wb.save(OUT)
print(f"{len(rows)} rows ({len(load)} to load), {len(headers)} columns -> {OUT} (tabs: {wb.sheetnames})")
