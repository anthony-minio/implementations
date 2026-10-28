#!/usr/bin/env python3
# Check the draft customer load against the raw sources, independently of the parser and build.
#   python3 tools/validate_load.py   (run from the customers folder)
import csv, re, collections
import openpyxl
import phonenumbers as pn

REPORT, LIST, SFDC, DRAFT = ("data/sage-customer-list-report-20261025.csv", "data/sage-customers-20261026.csv",
                             "data/sfdc-accounts-customers-20261025.xlsx", "data/customer-load-draft.csv")
LIMITS = {"Company Name": 83, "Customer Invoice Email": 64, "Phone": 21, "Attention": 83, "Addressee": 83,
          "Address 1": 150, "Address 2": 150, "City": 50, "Customer ID": 80, "External ID": 100}
EMAIL = re.compile(r"[\w.+'-]+@[\w-]+(?:\.[\w-]+)+")
# Decisions of 2026-10-27, restated here so the check does not lean on the build.
NOT_LOADED = re.compile(r"C\d+$")  # investor records C00001 to C00016
EXCLUDED = {"C-00036"}  # StoreManager
CAT = {"Direct Sales": "Direct Customer", "Direct Sales with Reseller": "End Customer", "Reseller": "Reseller",
       "Chargebee": "Chargebee", "Marketplace": "Marketplace", "MinIO Training Subscription": "Direct Customer",
       "Event Sponsor": "Other", "Billing Vendor": "Other"}
NISHA = {"C-00381": ("End Customer", "779"), "C-00313": ("Direct Customer", "669"), "C-00414": ("Direct Customer", "754"),
         "C-00333": (None, "695"), "C-00385": (None, "784"), "C-00562": (None, "1026")}
L3_NEW = {"716", "720"}
# Words in Sage's address text that are labels, not address, and words removed on purpose (each named in Flags).
# Corrections confirmed from the full address rather than copied from Sage (each named in Flags): spelling of a place,
# a postal code read from the address, a web-sourced head office address approved on 2026-10-28.
CHECKED_FIX = {"C-00566", "C-00069", "C-00111", "C-00139", "C-00148", "C-00153", "C-00155", "C-00213", "C-00355", "C-00361",
               "C-00376", "C-00437", "C-00448", "C-00481", "C-00532", "C-00569", "C-00075", "C-00136"}
CA_PROVINCES = {"Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Nova Scotia",
                "Northwest Territories", "Nunavut", "Ontario", "Prince Edward Island", "Quebec", "Saskatchewan", "Yukon"}
LABEL_WORDS = {"attn", "attention", "to", "atn", "poc", "vat", "id", "number", "rfc", "postal", "code"}
INTENDED = {"C-00069": {"delatan"}, "C-00075": {"pittsburg"}, "C-00111": {"600", "081"}, "C-00132": {"744", "gt"},
            "C-00136": {"125373", "moscoa"}, "C-00139": {"province"}, "C-00140": {"cep", "rondonia"}, "C-00148": {"francsico"},
            "C-00153": {"110018"}, "C-00155": {"oy7"}, "C-00226": {"ref"}, "C-00227": {"t", "a", "v"}, "C-00317": {"1153"},
            "C-00335": {"cape"}, "C-00361": {"rodonia"}, "C-00369": {"city"}, "C-00376": {"weisbaden"},
            "C-00386": {"luc", "mortier"}, "C-00437": {"sanjose"}, "C-00448": {"gae"}, "C-00481": {"wil"}, "C-00543": {"city"},
            "C-00569": {"t'bilisi"}, "C-00594": {"518057", "city"}, "C-00058": {"e", "mail"},
            "C-00066": {"budapest"}, "C-00115": {"deilver", "digitally"}, "C-00253": {"france"}, "C-00387": {"cincinnati"},
            "C-00108": {"c", "josa", "saeo"}, "C-00374": {"r", "o", "c"}, "C-00291": {"ci"}, "C-00425": {"fi"}}
# Full country names as NetSuite and Sage write them; a cut-off name ("Republic of") fails.
# NetSuite's country names for CSV import (Country enumeration in Oracle's NetSuite help, given by Anthony 2026-10-28).
COUNTRIES = set("""Afghanistan|Åland Islands|Albania|Algeria|American Samoa|Andorra|Angola|Anguilla|Antarctica|Antigua and Barbuda|Argentina|Armenia|Aruba|Australia|Austria|Azerbaijan|Bahamas|Bahrain|Bangladesh|Barbados|Belarus|Belgium|Belize|Benin|Bermuda|Bhutan|Bolivia (Plurinational State of)|Bonaire, Sint Eustatius and Saba|Bosnia and Herzegovina|Botswana|Bouvet Island|Brazil|British Indian Ocean Territory|Brunei Darussalam|Bulgaria|Burkina Faso|Burundi|Cabo Verde|Cambodia|Cameroon|Canada|Canary Islands|Cayman Islands|Central African Republic|Ceuta and Melilla|Chad|Chile|China|Christmas Island|Cocos (Keeling) Islands|Colombia|Comoros|Congo|Congo (the Democratic Republic of the)|Cook Islands|Costa Rica|Côte d'Ivoire|Croatia|Cuba|Curacao|Cyprus|Czechia|Denmark|Djibouti|Dominica|Dominican Republic|Ecuador|Egypt|El Salvador|Equatorial Guinea|Eritrea|Estonia|Eswatini|Ethiopia|Falkland Islands (Malvinas)|Faroe Islands|Fiji|Finland|France|French Guiana|French Polynesia|French Southern Territories|Gabon|Gambia|Georgia|Germany|Ghana|Gibraltar|Greece|Greenland|Grenada|Guadeloupe|Guam|Guatemala|Guernsey|Guinea|Guinea-Bissau|Guyana|Haiti|Heard Island and McDonald Islands|Holy See|Honduras|Hong Kong|Hungary|Iceland|India|Indonesia|Iran (Islamic Republic of)|Iraq|Ireland|Isle of Man|Israel|Italy|Jamaica|Japan|Jersey|Jordan|Kazakhstan|Kenya|Kiribati|Korea (the Democratic People's Republic of)|Korea (the Republic of)|Kosovo|Kuwait|Kyrgyzstan|Lao, People's Democratic Republic|Latvia|Lebanon|Lesotho|Liberia|Libya|Liechtenstein|Lithuania|Luxembourg|Macao|Madagascar|Malawi|Malaysia|Maldives|Mali|Malta|Marshall Islands|Martinique|Mauritania|Mauritius|Mayotte|Mexico|Micronesia (Federated States of)|Moldova (the Republic of)|Monaco|Mongolia|Montenegro|Montserrat|Morocco|Mozambique|Myanmar|Namibia|Nauru|Nepal|Netherlands|New Caledonia|New Zealand|Nicaragua|Niger|Nigeria|Niue|Norfolk Island|Northern Mariana Islands|North Macedonia|Norway|Oman|Pakistan|Palau|Palestine (State of)|Panama|Papua New Guinea|Paraguay|Peru|Philippines|Pitcairn|Poland|Portugal|Puerto Rico|Qatar|Réunion|Romania|Russian Federation|Rwanda|Saint Barthélemy|Saint Helena, Ascension and Tristan da Cunha|Saint Kitts and Nevis|Saint Lucia|Saint Martin (French part)|Saint Pierre and Miquelon|Saint Vincent and the Grenadines|Samoa|San Marino|Sao Tome and Principe|Saudi Arabia|Senegal|Serbia|Seychelles|Sierra Leone|Singapore|Sint Maarten (Dutch part)|Slovakia|Slovenia|Solomon Islands|Somalia|South Africa|South Georgia and the South Sandwich Islands|South Sudan|Spain|Sri Lanka|Sudan|Suriname|Svalbard and Jan Mayen|Sweden|Switzerland|Syrian Arab Republic|Taiwan (Province of China)|Tajikistan|Tanzania, the United Republic of|Thailand|Timor-Leste|Togo|Tokelau|Tonga|Trinidad and Tobago|Tunisia|Türkiye|Turkmenistan|Turks and Caicos Islands|Tuvalu|Uganda|Ukraine|United Arab Emirates|United Kingdom|United States|United States Minor Outlying Islands|Uruguay|Uzbekistan|Vanuatu|Venezuela (Bolivarian Republic of)|Viet Nam|Virgin Islands (British)|Virgin Islands (U.S.)|Wallis and Futuna Islands|Western Sahara|Yemen|Zambia|Zimbabwe""".split("|"))
# Sage's spelling to NetSuite's, for tracing a country back to the Sage text.
SAGE_TO_NS = {"Korea, Republic of": "Korea (the Republic of)", "Moldova, Republic of": "Moldova (the Republic of)",
              "Congo, Democratic Republic": "Congo (the Democratic Republic of the)", "Cape Verde": "Cabo Verde",
              "Czech Republic": "Czechia", "Curaçao": "Curacao", "Turkey": "Türkiye", "Vietnam": "Viet Nam",
              "Taiwan": "Taiwan (Province of China)", "Palestinian Territory, Occupied": "Palestine (State of)"}
def unmangle(v):
    if re.search(r"Ã|Â|â€", v or ""):
        try:
            return v.encode("cp1252").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return v
    return v
squash = lambda x: re.sub(r"[\s,;]+", " ", unmangle(x or "")).strip().lower()

# Raw Sage report: header row and contact blocks per customer.
raw, cur, blk = {}, None, None
for r in csv.reader(open(REPORT, encoding="utf-8-sig")):
    r = r + [""] * 20
    if re.match(r"C-?\d+$", r[0].strip()):
        cur = raw.setdefault(r[0].strip(), {"head": r, "blocks": {}}); blk = None
    elif cur and r[1].strip().endswith("contact:"):
        blk = r[1].strip(); cur["blocks"][blk] = [r[2]]
    elif cur and blk and not r[0] and not r[1] and r[2].strip():
        cur["blocks"][blk].append(r[2])
head = next(csv.reader(open(REPORT, encoding="utf-8-sig")))
lst = {r["Customer ID"]: r for r in csv.DictReader(open(LIST, encoding="utf-8-sig"))}
srows = list(openpyxl.load_workbook(SFDC, read_only=True).active.iter_rows(values_only=True))
shdr = next(r for r in srows if r and "Account ID" in r)
val = lambda v: "" if v in (None, "-") else str(v).strip()
sf = {r[2]: {k: val(v) for k, v in zip(shdr, r)} for r in srows if r and isinstance(r[2], str) and re.match(r"001\w{12}$", r[2])}

import sys
rows = list(csv.reader(open(sys.argv[1] if len(sys.argv) > 1 else DRAFT, encoding="utf-8-sig")))
cols = [c for c in rows[0] if not c.startswith("_src:")]
n = len(cols)
draft = [(dict(zip(cols, r[:n])), dict(zip(cols, r[n:]))) for r in rows[1:]]
issues = collections.defaultdict(list)
issues_lost = {}
def bad(check, cid, detail):
    issues[check].append(f"{cid}: {detail}")

active = {k for k, v in raw.items() if v["head"][head.index("Status")] == "Active" and not NOT_LOADED.match(k) and k not in EXCLUDED}
# one-time-use customers (active, but not in the report) are left out: no category and no invoices
loaded = {d["Sage Customer ID"] for d, _ in draft if d["Sage Customer ID"]}
if loaded != active:
    bad("Row set", "-", f"missing {sorted(active - loaded)[:10]}, extra {sorted(loaded - active)[:10]}")
new_rows = [d for d, _ in draft if not d["Sage Customer ID"]]
if {d["Subnet ID"] for d in new_rows} != L3_NEW or len(new_rows) != 2:
    bad("Row set", "-", f"new rows {[(d['Customer ID'], d['Subnet ID']) for d in new_rows]}")
c333 = next(d for d, _ in draft if d["Sage Customer ID"] == "C-00333")
for d in new_rows:
    same = {k for k in cols if k not in ("External ID", "Customer ID", "Subnet ID", "Salesforce Account ID", "Sage Customer ID", "Duplicate Action", "Merged Sage IDs", "Company Name")}
    if not re.fullmatch(re.escape(c333["Company Name"]) + r" -0[12]", d["Company Name"]):
        bad("L3Harris split rows", d["Customer ID"], f"name {d['Company Name']!r}")
    diff = [k for k in same if d[k] != c333[k]]
    if diff or d["External ID"] != d["Customer ID"] or not re.fullmatch(r"C-006\d\d", d["Customer ID"]):
        bad("L3Harris split rows", d["Customer ID"], f"differs from C-00333 in {diff}")
    a = sf.get(d["Salesforce Account ID"][:15])
    if not a or a["Subnet Account Id"] != d["Subnet ID"]:
        bad("L3Harris split rows", d["Customer ID"], "Salesforce Account ID does not carry this Subnet ID")
for col in ("Customer ID", "External ID"):
    dup = [k for k, v in collections.Counter(d[col].lower() for d, _ in draft if d[col]).items() if v > 1]
    if dup:
        bad("Unique IDs", col, dup)

for d, src in draft:
    sid = d["Sage Customer ID"]
    if sid in NISHA:
        cat, sn = NISHA[sid]
        if sn != d["Subnet ID"] or (cat and cat != d["Customer Category"]):
            bad("Nisha's Subnet ID or category", sid, f"{d['Subnet ID']} / {d['Customer Category']}")
    if d["Country"] and d["Country"] not in COUNTRIES:
        bad("Country not a full country name", sid or d["Customer ID"], d["Country"])
    ph = d["Phone"]
    if ph:
        base, _, ext = ph.partition(" x")
        try:
            num = pn.parse(base, "US" if base.startswith("(") else None)
            ok = pn.is_valid_number(num)
        except pn.NumberParseException:
            ok = False
        us = ok and pn.region_code_for_number(num) == "US" and d["Country"] in ("United States", "")
        if not ok or (base.startswith("(") and not us) or (not base.startswith("(") and (us or not base.startswith("+"))):
            bad("Phone format", sid or d["Customer ID"], ph)
        elif sid in raw or sid == "":
            srcs = [l for l in (raw[sid]["blocks"].get("Display contact:", []) if sid else []) if re.match(r"\s*(Phone|Mobile phone):", l)]
            a = sf.get(d["Salesforce Account ID"][:15]) if d["Salesforce Account ID"] else None
            want = pn.format_number(num, pn.PhoneNumberFormat.E164)[1:]
            pool = [re.sub(r"\D", "", re.sub(r"\(0\)", "", x.split(":", 1)[1].split("xt")[0])) for x in srcs] + \
                   ([re.sub(r"\D", "", a["Phone"])] if a and a["Phone"] else [])
            if not sid:  # split rows copy C-00333
                pool = [re.sub(r"\D", "", c333["Phone"].split(" x")[0])]
            # a trunk 0 written after the country code (+46 072...) is dropped in international format
            variants = {v for p in pool for v in [p, p.lstrip("0")] + [p[:k] + p[k + 1:] for k in (1, 2, 3) if p[k:k + 1] == "0"]}
            if not any(v and (want.endswith(v) or v.endswith(want)) for v in variants):
                bad("Phone not traced to Sage or Salesforce", sid or d["Customer ID"], f"{ph} from {pool}")
    if not sid or sid not in raw:
        if sid and d["Company Name"] != lst[sid]["Customer name"]:
            bad("Company Name", sid, d["Company Name"])
        continue
    R = raw[sid]; H = dict(zip(head, [x.strip() for x in R["head"]]))
    want_cat = CAT.get(H["Customer type"], "")
    if sid not in NISHA and d["Customer Category"] != want_cat:
        bad("Customer Category vs Sage type", sid, f"{d['Customer Category']!r} from {H['Customer type']!r}")
    disp = R["blocks"].get("Display contact:", []) + R["blocks"].get("Primary contact:", [])
    btxt = squash(" ".join(disp))
    base_name = re.sub(r" -0\d$", "", d["Company Name"])
    twins = [e for e, _ in draft if re.sub(r" -0\d$", "", e["Company Name"]) == base_name and not e["Duplicate Action"].startswith("Merge into")]
    separate = len(twins) > 1 and len({e["Subnet ID"] for e in twins}) == len(twins) and all(e["Subnet ID"] for e in twins)
    if separate and d["Company Name"] == base_name and sid != "C-00333":
        bad("Same name, separate Subnet accounts, no suffix", sid, d["Company Name"])
    if d["Company Name"] != base_name and not separate:
        bad("Name suffix without separate Subnet accounts", sid, d["Company Name"])
    if base_name != unmangle(H["Customer name"]):
        bad("Company Name", sid, f"{d['Company Name']!r} vs Sage {H['Customer name']!r}")
    if re.match(r"C-\d{5}$", sid) and d["Customer ID"] != sid:
        bad("Customer ID", sid, d["Customer ID"])
    if d["External ID"] != d["Customer ID"]:
        bad("External ID", sid, d["External ID"])
    for col in ("Address 1", "Address 2", "Attention", "Addressee"):
        v = re.sub(r" x(\d+)$", r" \1", d[col]) if col == "Phone" else d[col]
        raw_txt = btxt if "Garbled" not in v else btxt
        if v and src[col] == "sage" and re.sub(r"\bext\b", "", squash(v.replace(":", " "))).split() != [] and \
                " ".join(re.sub(r"\bext\b", "", squash(v.replace(":", " "))).split()) not in " ".join(re.sub(r"\bext\b", "", btxt.replace(":", " ")).split()):
            bad(f"{col} not in Sage text", sid, d[col])
    L = lst.get(sid, {})
    for col, f in (("City", "City"), ("Province/State", "State or territory"), ("Postal Code/Zip", "ZIP or postal code")):
        want = unmangle(L.get(f, "").strip(" ,"))
        if col == "Postal Code/Zip" and src[col] == "rule" and d["Country"] == "United States" and want and sid not in CHECKED_FIX:
            want = re.sub(r"^(\d{3,4})", lambda m: m.group(1).zfill(5), want)
            if d[col] != want:
                bad(f"{col} vs Sage list", sid, f"{d[col]!r} vs {L.get(f)!r}")
        elif src[col] == "sage" and d[col] != want and sid not in CHECKED_FIX:
            bad(f"{col} vs Sage list", sid, f"{d[col]!r} vs {L.get(f)!r}")
    if src["Country"] == "sage" and not any(l.strip().endswith(d["Country"]) or
                                            any(l.strip().endswith(k) and v == d["Country"] for k, v in SAGE_TO_NS.items()) for l in disp):
        bad("Country not in Sage text", sid, d["Country"])
    # Address fields moved by rule: every word must come from Sage's own text for this customer (Salesforce values are
    # tagged sfdc and checked against Salesforce below), and no word of Sage's address may be lost.
    W = lambda t: set(re.findall(r"[\w']+", t))
    sage_words = W(squash(" ".join(disp) + " " + " ".join(lst.get(sid, {}).values())))
    sage_words |= {w.zfill(5) for w in sage_words if re.fullmatch(r"\d{4}", w)}  # US ZIPs with the lost leading zero
    addr_cols = ("Attention", "Address 1", "Address 2", "City", "Province/State", "Postal Code/Zip")
    for col in addr_cols:
        if src[col] == "rule" and d[col] and src["Address 1"] != "sfdc":  # an address from Salesforce is checked there
            extra = W(squash(d[col])) - sage_words
            if extra and not (col == "Province/State" and d["Country"] == "United States" and re.fullmatch(r"[A-Z]{2}", d[col])) \
                    and not (col == "City" and d[col] in ("Singapore", "Berlin")) and sid != "C-00108" and sid not in CHECKED_FIX \
                    and not (col == "Province/State" and d["Country"] == "Canada" and d[col] in CA_PROVINCES):  # C-00108 corrected 2026-10-26
                bad("Moved address text not in Sage", sid, f"{col}: {d[col]!r} ({sorted(extra)})")
    got_words = W(squash(" ".join(d[c] for c in addr_cols + ("Country", "Second Address", "Third Address"))))
    street = [l for b in ("Display contact:",) for l in R["blocks"].get(b, [])[1:]
              if not re.match(r"\s*(Phone|Email|Fax|Mobile phone|URL):", l)]
    lost = W(squash(" ".join(street) + " " + " ".join(lst.get(sid, {}).get(k, "") for k in ("City", "State or territory", "ZIP or postal code")))) - got_words
    lost -= {"united", "states", "usa"} | set(squash(H["Tax ID"]).split()) | {w for w in lost if re.search(r"@|\.(com|net|org)", w)}
    lost -= W(squash(d["Other Tax ID"] + " " + d["VAT ID"] + " " + d["Customer Invoice Email"] + " " + d["Additional Emails"]))
    # Words that change with a decided rewrite: Sage's country name where NetSuite spells it differently or the country was
    # corrected, a US state written as its code or a Canadian code as its name, and country prefixes on postal codes.
    if src["Country"] != "sage" or d["Country"] in SAGE_TO_NS.values():
        lost -= W(squash(" ".join(k for k, v in SAGE_TO_NS.items() if v == d["Country"]) + " " +
                         " ".join(l.split(",")[-1] for l in street)))
    if d["Country"] in ("United States", "Canada") and src["Province/State"] == "rule":
        lost -= W(squash(" ".join(l.split(",")[-2] if l.count(",") > 1 else "" for l in street) + " " +
                         lst.get(sid, {}).get("State or territory", "") + " " + lst.get(sid, {}).get("City", "")))
    if src["Postal Code/Zip"] == "rule":
        lost -= {"d", "b", "l", "ch", "se", "fi", "it", "gt", "lon", "sverige", "li", "md", "fo"}
    lost -= LABEL_WORDS | INTENDED.get(sid, set()) | {w for w in lost if re.fullmatch(r"\d{4}", w) and w.zfill(5) in got_words}
    lost -= {w for w in lost if w in re.sub(r"[^a-z0-9]", "", d["VAT ID"].lower())}
    if sid == "C-00019":
        lost = set()  # Kayak: address left blank on purpose (2026-10-28)
    if lost and src["Address 1"] != "sfdc":
        issues_lost[sid] = sorted(lost)
    own = set(e.lower() for e in EMAIL.findall(" ".join(disp)))
    bt = R["blocks"].get("Bill-to contact:", [])
    if bt and bt[0].strip() not in ("..", "") and bt[0].strip() == (disp[0].strip() if disp else ""):
        own |= set(e.lower() for e in EMAIL.findall(" ".join(bt)))
    got = set(e.lower() for e in [d["Customer Invoice Email"]] + d["Additional Emails"].split("; ") if e)
    for m in [i for i in d["Merged Sage IDs"].split(", ") if i]:
        mb = raw[m]["blocks"]
        own |= set(e.lower() for e in EMAIL.findall(" ".join(mb.get("Display contact:", []) + mb.get("Primary contact:", []))))
        mbt = mb.get("Bill-to contact:", [])
        if mbt and mbt[0].strip() == (mb.get("Display contact:", [""])[0].strip()):
            own |= set(e.lower() for e in EMAIL.findall(" ".join(mbt)))
    to_reseller = {e.lower() for e in d["Reseller Invoice Email"].split("; ") if e}
    if d["Merged Sage IDs"] and got <= own and (d["Customer Invoice Email"].lower() in own or not d["Customer Invoice Email"]):
        pass
    elif got <= own and (own - got) <= to_reseller and got.isdisjoint(to_reseller):
        pass  # the reseller's addresses Sage held on the customer moved to Reseller Invoice Email
    elif got != own:
        bad("Emails vs Sage", sid, f"missing {sorted(own - got)}, extra {sorted(got - own)}")
    for col in ("Second Address", "Third Address"):
        if d[col]:
            m = re.search(r"\(from (C-?\d+)(, address from Salesforce)?\)$", d[col])
            if not m or m.group(1) not in d["Merged Sage IDs"].split(", "):
                bad("Extra address source", sid, d[col])
            else:
                mt = squash(" ".join(raw[m.group(1)]["blocks"].get("Display contact:", [])))
                for part in ([] if m.group(2) else d[col][:m.start()].split(", ")):
                    part = re.sub(r"^0(\d{4})$", r"\1", part)
                    if part and squash(part) not in mt and squash(part) not in squash(" ".join(lst.get(m.group(1), {}).values())) \
                            and part.strip() not in COUNTRIES and not re.fullmatch(r"[A-Z]{2}", part.strip()):
                        bad("Extra address not in merged Sage record", sid, part)
    if d["Reseller Invoice Email"]:
        rb = set(e.lower() for e in EMAIL.findall(" ".join(bt + disp)))
        if not set(e.lower() for e in EMAIL.findall(d["Reseller Invoice Email"])) <= rb:
            bad("Reseller email vs Sage bill-to", sid, d["Reseller Invoice Email"])
    t = H["Term"]
    m = re.match(r"(?:Net\s*)?(\d+)\s*days?$|Net\s*(\d+)$", t, re.I); y = re.match(r"(\d+)\s*years?$", t, re.I)
    want = f"Net {m.group(1) or m.group(2)}" if m else f"Net {int(y.group(1)) * 365}" if y else t if t == "Due on Receipt" else ""
    if d["Terms"] != want:
        bad("Terms vs Sage", sid, f"{d['Terms']!r} from {t!r}")
    if d["Primary Currency"] != (H["Default currency"] or "USD"):
        bad("Currency vs Sage", sid, d["Primary Currency"])
    core = lambda t: re.sub(r"[^A-Z0-9]", "", (t or "").upper())
    sage_tax = core(H["Tax ID"] + " " + " ".join(disp))
    for col in ("VAT ID", "Other Tax ID"):
        v = core(re.sub(r"^US EIN ", "", d[col]))
        if v and not any(v[k:] in sage_tax for k in range(0, 4)):
            bad(f"{col} vs Sage", sid, d[col])
    if d["International VAT ID"] != d["VAT ID"]:
        bad("International VAT ID differs from VAT ID", sid, d["International VAT ID"])
    if d["Reseller Contact"] and squash(d["Reseller Contact"]) not in squash(" ".join(bt + disp)):
        bad("Reseller Contact not in Sage text", sid, d["Reseller Contact"])
    if d["Reseller Contact"] and squash(d["Reseller Contact"]) in squash(d["Billed To (Reseller)"]):
        bad("Billed To still holds the contact", sid, d["Billed To (Reseller)"])
    if d["Billed To (Reseller)"] and squash(d["Billed To (Reseller)"]) not in squash(" ".join(bt[:1])):
        bad("Billed To not the Sage bill-to company", sid, d["Billed To (Reseller)"])
    if H["Tax ID"] and not (d["VAT ID"] or d["Other Tax ID"]):
        bad("Sage Tax ID not loaded", sid, H["Tax ID"])
    if d["Salesforce Account ID"]:
        a = sf.get(d["Salesforce Account ID"][:15])
        if not a:
            bad("Salesforce ID not in Salesforce", sid, d["Salesforce Account ID"])
        else:
            if d["Subnet ID"] != a["Subnet Account Id"]:
                bad("Subnet ID vs Salesforce", sid, f"{d['Subnet ID']!r} vs {a['Subnet Account Id']!r}")
            if d["Parent Company"]:
                par = [e for e, _ in draft if e["Customer ID"] == d["Parent Customer ID"]]
                nq = lambda t: re.sub(r"[^a-z0-9]", "", unmangle(t).lower())
                if len(par) != 1 or par[0]["Company Name"] != d["Parent Company"] or not (
                        par[0]["Salesforce Account ID"][:15] == a["Parent Account ID"] or nq(par[0]["Company Name"]) == nq(a["Parent Account"])):
                    bad("Parent vs Salesforce", sid, f"{d['Parent Company']} / {d['Parent Customer ID']}")
    for col, v in d.items():
        if not v:
            continue
        if v != v.strip() or v.endswith(",") or ",," in v or re.search(r"[\x00-\x1f]", v):
            bad("Stray spaces, commas or control characters", sid, f"{col}: {v!r}")
        if col in ("Address 1", "Address 2", "City", "Country", "Addressee", "Attention") and re.search(r"\b(Phone|Email|Fax|URL|Attn|VAT|RFC|GSTIN)\s*:", v, re.I):
            bad("Label text left in address", sid, f"{col}: {v!r}")
        if re.search(r"Ã|Â|â€|A\(C\)|SAEo", v):
            bad("Garbled characters (encoding)", sid, f"{col}: {v!r}")
        if col in LIMITS and len(v) > LIMITS[col]:
            bad("Too long for NetSuite field", sid, f"{col} ({len(v)} > {LIMITS[col]}): {v[:60]}")

for sid, words in issues_lost.items():
    bad("Sage address words not in the load", sid, words)
print(f"Checked {len(draft)} rows against {len(raw)} Sage report records, {len(lst)} Sage list rows, {len(sf)} Salesforce accounts.")
for k in sorted(issues):
    print(f"\n{k}: {len(issues[k])}")
    for e in issues[k][:80]:
        print("   ", e)
if not issues:
    print("No issues.")
