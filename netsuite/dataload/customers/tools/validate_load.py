#!/usr/bin/env python3
# Check the draft customer load against the raw sources, independently of the parser and build.
#   python3 tools/validate_load.py   (run from the customers folder)
import csv, re, collections
import openpyxl

REPORT, LIST, SFDC, DRAFT = ("data/sage-customer-list-report-20261025.csv", "data/sage-customers-20261026.csv",
                             "data/sfdc-accounts-customers-20261025.xlsx", "data/customer-load-draft.csv")
LIMITS = {"Company Name": 83, "Customer Invoice Email": 64, "Phone": 21, "Attention": 83, "Addressee": 83,
          "Address 1": 150, "Address 2": 150, "City": 50, "Customer ID": 80, "External ID": 100}
EMAIL = re.compile(r"[\w.+'-]+@[\w-]+(?:\.[\w-]+)+")
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

rows = list(csv.reader(open(DRAFT, encoding="utf-8-sig")))
cols = [c for c in rows[0] if not c.startswith("_src:")]
n = len(cols)
draft = [(dict(zip(cols, r[:n])), dict(zip(cols, r[n:]))) for r in rows[1:]]
issues = collections.defaultdict(list)
def bad(check, cid, detail):
    issues[check].append(f"{cid}: {detail}")

active = {k for k, v in raw.items() if v["head"][head.index("Status")] == "Active"}
loaded = {d["Sage Customer ID"] for d, _ in draft}
if loaded != active:
    bad("Row set", "-", f"missing {sorted(active - loaded)[:10]}, extra {sorted(loaded - active)[:10]}")
for col in ("Customer ID", "External ID"):
    dup = [k for k, v in collections.Counter(d[col].lower() for d, _ in draft if d[col]).items() if v > 1]
    if dup:
        bad("Unique IDs", col, dup)

for d, src in draft:
    sid = d["Sage Customer ID"]
    R = raw[sid]; H = dict(zip(head, [x.strip() for x in R["head"]]))
    disp = R["blocks"].get("Display contact:", []) + R["blocks"].get("Primary contact:", [])
    btxt = squash(" ".join(disp))
    if d["Company Name"] != unmangle(H["Customer name"]):
        bad("Company Name", sid, f"{d['Company Name']!r} vs Sage {H['Customer name']!r}")
    if re.match(r"C-\d{5}$", sid) and d["Customer ID"] != sid:
        bad("Customer ID", sid, d["Customer ID"])
    if d["External ID"] != d["Customer ID"]:
        bad("External ID", sid, d["External ID"])
    for col in ("Address 1", "Address 2", "Attention", "Addressee", "Phone"):
        v = re.sub(r" x(\d+)$", r" \1", d[col]) if col == "Phone" else d[col]
        raw_txt = btxt if "Garbled" not in v else btxt
        if v and src[col] == "sage" and re.sub(r"\bext\b", "", squash(v.replace(":", " "))).split() != [] and \
                " ".join(re.sub(r"\bext\b", "", squash(v.replace(":", " "))).split()) not in " ".join(re.sub(r"\bext\b", "", btxt.replace(":", " ")).split()):
            bad(f"{col} not in Sage text", sid, d[col])
    L = lst.get(sid, {})
    for col, f in (("City", "City"), ("Province/State", "State or territory"), ("Postal Code/Zip", "ZIP or postal code")):
        want = unmangle(L.get(f, "").strip(" ,"))
        if col == "Postal Code/Zip" and src[col] == "rule" and d["Country"] == "United States" and want:
            want = re.sub(r"^(\d{3,4})", lambda m: m.group(1).zfill(5), want)
            if d[col] != want:
                bad(f"{col} vs Sage list", sid, f"{d[col]!r} vs {L.get(f)!r}")
        elif src[col] == "sage" and d[col] != want:
            bad(f"{col} vs Sage list", sid, f"{d[col]!r} vs {L.get(f)!r}")
    if src["Country"] == "sage":
        tails = {l.split(",")[-1].strip() for l in disp}
        if d["Country"] not in tails:
            bad("Country not in Sage text", sid, d["Country"])
    own = set(e.lower() for e in EMAIL.findall(" ".join(disp)))
    bt = R["blocks"].get("Bill-to contact:", [])
    if bt and bt[0].strip() not in ("..", "") and bt[0].strip() == (disp[0].strip() if disp else ""):
        own |= set(e.lower() for e in EMAIL.findall(" ".join(bt)))
    got = set(e.lower() for e in [d["Customer Invoice Email"]] + d["Additional Emails"].split("; ") if e)
    if got != own:
        bad("Emails vs Sage", sid, f"missing {sorted(own - got)}, extra {sorted(got - own)}")
    if d["Reseller Invoice Email"]:
        rb = set(e.lower() for e in EMAIL.findall(" ".join(bt)))
        if not set(e.lower() for e in EMAIL.findall(d["Reseller Invoice Email"])) <= rb:
            bad("Reseller email vs Sage bill-to", sid, d["Reseller Invoice Email"])
    t = H["Term"]
    m = re.match(r"(?:Net\s*)?(\d+)\s*days?$|Net\s*(\d+)$", t, re.I); y = re.match(r"(\d+)\s*years?$", t, re.I)
    want = f"Net {m.group(1) or m.group(2)}" if m else f"Net {int(y.group(1)) * 365}" if y else t
    if d["Terms"] != want:
        bad("Terms vs Sage", sid, f"{d['Terms']!r} from {t!r}")
    if d["Primary Currency"] != (H["Default currency"] or "USD"):
        bad("Currency vs Sage", sid, d["Primary Currency"])
    if d["VAT ID"] and squash(d["VAT ID"]) not in squash(H["Tax ID"] + " " + " ".join(disp)):
        bad("VAT ID vs Sage", sid, d["VAT ID"])
    if d["Salesforce Account ID"]:
        a = sf.get(d["Salesforce Account ID"][:15])
        if not a:
            bad("Salesforce ID not in Salesforce", sid, d["Salesforce Account ID"])
        else:
            if d["Subnet ID"] != a["Subnet Account Id"]:
                bad("Subnet ID vs Salesforce", sid, f"{d['Subnet ID']!r} vs {a['Subnet Account Id']!r}")
            if d["Parent Company"] and d["Parent Company"] != a["Parent Account"]:
                bad("Parent vs Salesforce", sid, d["Parent Company"])
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

print(f"Checked {len(draft)} rows against {len(raw)} Sage report records, {len(lst)} Sage list rows, {len(sf)} Salesforce accounts.")
for k in sorted(issues):
    print(f"\n{k}: {len(issues[k])}")
    for e in issues[k][:8]:
        print("   ", e)
if not issues:
    print("No issues.")
