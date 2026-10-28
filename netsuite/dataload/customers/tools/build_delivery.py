#!/usr/bin/env python3
# Build the customer load workbook for circulation: the load table on one tab, the notes on another.
#   python3 tools/build_delivery.py   (run from the customers folder after build_review.py and validate_load.py)
import collections, json, re
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUT = "data/MinIO_Customer_Load_to_NetSuite_20261028.xlsx"
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
moved_mail = [r for r in load if has_flag(r, "Reseller's email moved")]
domain = [r for r in load if has_flag(r, "Salesforce match by email domain")]
suffixed = [r for r in load if re.search(r" -0\d$", V(r, "Company Name"))]
second_pass = [r for r in load if any("Address fields corrected" in f for f in r["flags"])]
prefix = [r for r in load if has_flag(r, "Postal code country prefix removed")]
filled = [r for r in load if any(f.startswith("No address in Sage; ") for f in r["flags"])]
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
     f"C-00333 is Subnet 695. New customers {ids(split)} are Subnets 716 and 720, copied from C-00333 (address, terms, "
     "TVAR Solutions bill-to), named L3 Technologies Inc. -01 and -02 (Anthony, 2026-10-27). C-00385 is Subnet 784 and C-00562 is Subnet 1026. For SOA: contracts CN-SO0565 and "
     "CN-SO0603 sit under C-00333 in Sage and must be assigned to the new customers on load."),
    ("One-time-use customers",
     "C-00012 TDA GROUP and C-00021 SPMB are flagged One-time use in Sage and were not in the customer list report the load "
     "is built from.",
     "Leave them off: they have no customer category and no invoices (Anthony, 2026-10-27). They are active in Sage, but "
     "Sage has only their name and ID (no address, contact, type or terms), Salesforce has no account for them, and no "
     "invoice for them is in the Sage exports.",
     "Not loaded."),
    ("Due per Contract terms",
     f"{len(due)} customers have the Sage term Due per Contract, which is not a NetSuite term.",
     "Leave their terms blank (2026-10-27).",
     f"Terms left blank for {ids(due)}; each is flagged \"Terms left blank\"."),
    ("Phone numbers (column M)",
     f"Phone numbers were in mixed formats: dashes, dots, spaces, \"(0)\" trunk digits, a leading apostrophe on {apostrophe} Sage "
     f"numbers, and country codes without a \"+\". Salesforce writes every 10-digit number as (999) 999-9999, so some "
     "non-US customers carry a US head-office number.",
     "US numbers of US customers as (999) 999-9999, so accountants can keep entering them that way; every other number, "
     "Canada included, in international format (+44 20 7885 8888, +1 604-709-0008), as the template allows. Numbers that are broken in the source are left out (2026-10-27).",
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
    ("Customers with no address",
     f"{len(no_country) + len(filled)} customers have no address at all in Sage, and Sage shows United States, its default when no "
     "address is entered. Several are not US companies (for example Aegon Emeklilik, National Bank of Cambodia, Nais Sp. z o.o.). "
     "Addresses were looked up in Salesforce (under other account names) and public sources, each with a confidence rating.",
     "Use the high-confidence addresses; for the rest leave the address blank and the country blank, since the country is where "
     "the address is (2026-10-28).",
     f"Address and country added for {ids(filled)} (Salesforce or the head office address; source in Flags). Country left blank "
     f"for {ids(no_country)}, flagged \"Country left blank\": their addresses could not be confirmed."),
    ("VAT ID and International VAT ID",
     "The template has both a VAT ID and an International VAT ID column. In practice they hold the same number (the VAT "
     "number with its country prefix).",
     "Put the same number in both; SOA will keep the column they use (2026-10-28).",
     "International VAT ID now equals VAT ID on every row."),
    ("Country names in NetSuite's spelling",
     "NetSuite's CSV import needs each country's name exactly as NetSuite lists it, and some differ from Sage's.",
     "Use NetSuite's names (Oracle's NetSuite country list, 2026-10-28).",
     "Korea, Republic of to Korea (the Republic of); Moldova, Republic of to Moldova (the Republic of); Congo, Democratic "
     "Republic to Congo (the Democratic Republic of the); Czech Republic to Czechia; Turkey to Türkiye; Vietnam to Viet Nam; "
     "Taiwan to Taiwan (Province of China); Cape Verde to Cabo Verde; Curaçao to Curacao; Palestinian Territory, Occupied to "
     "Palestine (State of). Monte-Carlo moved from France to Monaco and two Hong Kong customers from China to Hong Kong, where "
     "their addresses are."),
    ("Parent Company",
     "Parent Company named the parent as Salesforce spells it, which does not always match the parent customer's name in this "
     "load (BC \"Moldindconbank\" SA is written with different quote marks), so NetSuite could not link them.",
     "Name the parent exactly as in this load and add the parent's Customer ID in its own column. Keep the USAF parent links; "
     "C-00333 and the new L3Harris customers have no parent (2026-10-28).",
     "Parent Company is the parent's name in this load; the added Parent Customer ID column gives its Customer ID."),
    ("Reseller name and contact",
     "Sage writes the bill-to as \"Contact, Company\" (for example \"Corey Sutton, SHI International Corp\"), so Billed To "
     "(Reseller) held a person and a company.",
     "Split them: the company in Billed To (Reseller), the person in a new Reseller Contact column, to start tracking contacts "
     "for a later contacts load (2026-10-28).",
     "Billed To (Reseller) holds the company only; Reseller Contact holds the person where Sage has one."),
    ("Invoices billed to the reseller",
     "For customers billed through a reseller, Sage often holds the reseller's accounts payable address on the customer (for "
     "example VendorInvoices@SHI.com on Baker Hughes).",
     "Invoices go to the reseller, so its addresses belong with the reseller (2026-10-28).",
     f"For {len(moved_mail)} customers the reseller's addresses moved from Customer Invoice Email and Additional Emails to Reseller "
     "Invoice Email (listed in Flags). Customers billed to their own billing entity (for example Kayak Software Corporation) "
     "are unchanged."),
    ("Address review, second pass",
     "A column-by-column review found contacts typed into the street line, a state, county or district in the city field, "
     "Sage typos (San Francsico, Moscoa, Weisbaden), postal codes with a country prefix or a lost leading zero, and US states "
     "written both ways.",
     "Contacts move to Attention; a city fix is made only when the street and postal code confirm the place; typos are fixed "
     "the same way; postal code prefixes are removed and leading zeros restored; a postal code that cannot be worked out is "
     "removed. US states as two-letter codes, Canadian provinces by full name (2026-10-28).",
     f"Corrected addresses are listed in Flags (\"Address fields corrected\"); {len(prefix)} more postal codes lost a country "
     "prefix (\"Postal code country prefix removed\"). Addresses that could not be settled are flagged \"Address to check\"."),
    ("Country that did not match the address",
     "BlueTech (C-00177) had country Georgia, but its address is in Germany: Everswinkel, postal code 48351, a German "
     "GmbH & Co. KG, phone +49 2582 and an email ending .de. Every customer was checked the same way against its city, "
     "postal code, phone and email; the other mismatches are a head office's phone or a contact's email, not the address.",
     "Correct the country where the confidence is high (2026-10-28).",
     "BlueTech's country is Germany. With the earlier fixes (Monte-Carlo to Monaco, two Hong Kong customers), no other "
     "address sits in a different country from its Country field."),
    ("Kayak's address",
     "Kayak Software Corp (C-00019) has a London street (100 New Bridge Street) with city London, state CT and ZIP 06902, "
     "which is Stamford, Connecticut. There is no London, CT, so Sage cannot settle which address is right.",
     "Leave the address blank and note it (2026-10-28).",
     "Address and country blank for C-00019. Its Sage bill-to, Kayak Software Corporation, 7 Market Street, Stamford, CT 06902, "
     "is in the reseller columns."),
    ("Attention repeating the company",
     "Attention is the \"Attn:\" line on the invoice address. On 12 customers Sage had the company's own name there, so "
     "the invoice would read \"Attn: Memory Express / Memory Express\".",
     "Remove it (2026-10-28).",
     "Attention blank on those 12 customers, each flagged \"Attention removed\"."),
    ("Salesforce matches by email domain",
     f"Matching Sage to Salesforce by name left about 300 customers with no Salesforce Account ID or Subnet ID. Some are in "
     "Salesforce under another name (an acronym, a parent company, a former name).",
     "Match by email domain: a Salesforce account whose website is the customer's email domain, each pair reviewed with "
     "evidence (name, city, Salesforce partner against the Sage reseller) on 2026-10-28. Where a company has two Sage records "
     "and two Subnet accounts, pair the one that can be matched with confidence and the other by elimination. Records with "
     "different Subnet IDs are never merged.",
     f"{len(domain)} customers gained a Salesforce Account ID (and Subnet ID where the account has one), flagged \"Salesforce "
     "match by email domain\". C-00097 Aegon Emeklilik merged into C-00208 Aegon_Viennalife, and C-00120 Federal Home Loan "
     "Mortgage Corporation into C-00219 Freddie Mac. Two Chargebee records merged earlier are separate customers again, "
     "each with its own Subnet account: C-00575 Hollister.com (1012, beside C-00640 on 1132) and C-00489 Leidos (895, "
     "beside C-00516 on 972). The count to load is unchanged. C-00480 Senukai Digital was left unmatched."),
    ("Customers with the same name",
     "Some customers share a name but are separate Subnet accounts, so they would look identical in NetSuite.",
     "Add -01, -02 to the name, as for the new L3Harris customers (2026-10-28).",
     f"{len(suffixed)} customers carry a suffix: {', '.join(V(r, 'Customer ID') + ' ' + V(r, 'Company Name') for r in suffixed)}."),
]

NOTES = [
    ("Customer count",
     f"Bridge from Sage's active customers to this file. Sage active customers (Sage's active customer list): {B['first']}. "
     f"Less 16 investor records, C00001 to C00016 (not customers): {B['first'] - 16}. "
     f"Less 1, StoreManager (C-00036; no invoices and no address, left out per Nisha): {B['first'] - 17}. "
     f"Less {len(B['onetime'])} one-time-use customers with no category and no invoices "
     f"({', '.join(f'{i} {n}' for i, n in B['onetime'])}): {B['first'] - len(B['excluded'])}. "
     f"Plus {B['split']} new L3Harris customers split from C-00333 ({ids(split)}): {B['rows']}, the rows on the "
     f"Customers-Draft tab. Less {B['merged']} duplicates merged into {B['kept']} other customers: {B['load']} customers to load. "
     f"The merged duplicates are already merged: their Sage IDs, addresses and emails are on the customer they merge into. "
     f"They stay on the tab, marked \"Merge into\" in Duplicate Action, only so the merge can be checked, and must be "
     f"filtered out before the import. {B['merged']} duplicates merge into {B['kept']} customers because two customers each "
     f"had two duplicates: Scotia BNS Canadian Banking (C-00405) merges C-00039 and C-00049, and Ministry of Defence UK "
     f"(C-00481) merges C-00497 and C-00629. Sage's customer list report also has 4 inactive customers, not counted above "
     f"and not loaded: {', '.join(i for i, _ in B['inactive'])}."),
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
     "VAT ID and International VAT ID hold VAT or GST registration numbers only, with the country prefix (Sage \"813089973\" for a German customer "
     "becomes DE813089973). India GSTINs, Mexico RFCs and Saudi and UAE VAT numbers are kept as Sage has them. Other tax IDs "
     "in Sage (US EINs, company registration numbers) are in the added Other Tax ID column."),
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
     "NetSuite's CSV import needs the country's full name exactly as NetSuite lists it; it rejects ISO codes (\"Invalid "
     "country reference key US\"). Every country in the file is checked against NetSuite's list."),
]

OPEN = [
    "Create the customer categories Chargebee, Marketplace and Other in NetSuite before the load (Setup > Accounting > "
    "Accounting Lists > New > Customer Category).",
    f"Terms not on SOA's list: {new_terms}. Create them in NetSuite, or say which existing term each should use. The "
    f"{sum(nt.values())} customers concerned are marked \"New NetSuite term\" in Question Categories.",
    "VAT ID and International VAT ID carry the same number; SOA to keep the column they use, and say whether Other Tax ID "
    "(US EINs and company registration numbers) should be loaded anywhere.",
    "Standard Chartered Bank: C-00048 (London, last invoiced 2026-05-28) and C-00641 (Singapore, last invoiced 2026-10-15, "
    "open balance 2,104,668.00) share Subnet ID 775. Kept as two customers for now; to decide whether to merge them or "
    "give them -01 and -02.",
    "ZATCA: Salesforce has Subnet accounts 715 (ZATCA-Certscan Platform, partners EG&G Middle East and Accelerated "
    "Solutions) and 731 (ZATCA-Rapiscan, partner EG&G Middle East) with no Sage customer; neither reseller is in Sage. "
    "Nisha to confirm whether they were ever invoiced and need customers of their own.",
    "Leidos: C-00489 (Chargebee) was given Subnet 895 (Leidos-1) by elimination; Salesforce lists CDW as Leidos-1's partner. "
    "Nisha to confirm.",
    "L3Harris: assign contracts CN-SO0565 and CN-SO0603 to the new customers C-00642 (Subnet 716) and C-00643 (Subnet 720) "
    "when contracts are loaded.",
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
