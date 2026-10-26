#!/usr/bin/env python3
# Flatten the Sage Intacct "Customer list" report (one header row per customer, then contact blocks) to one row per customer.
# Each contact block prints: name line ("Person, Company" when a contact person is set), a street line holding Sage's
# address line 1 and 2, a "city, state, postal code, country" line, then Phone / Email / Fax / Mobile phone / URL lines.
import csv, re, sys

src, out = sys.argv[1], sys.argv[2]
rows = list(csv.reader(open(src, encoding="utf-8-sig")))
hdr = rows[0]
customers, cur, block = [], None, None
for r in rows[1:]:
    r = r + [""] * (len(hdr) - len(r))
    if re.match(r"C-?\d+$", r[0].strip()):
        cur = dict(zip(hdr, [v.strip() for v in r]))
        cur["_contacts"] = {}
        customers.append(cur)
        block = None
    elif cur is not None and r[1].strip().endswith("contact:"):
        block = r[1].strip()[:-len(" contact:")].lower().replace("-", "")
        cur["_contacts"][block] = {"name": r[2], "lines": []}
    elif cur is not None and block and not r[0] and not r[1] and r[2].strip():
        cur["_contacts"][block]["lines"].append(r[2])

LABEL = re.compile(r"(Phone|Email|Fax|Mobile phone|URL):\s*(.*)", re.I)
ATTN = re.compile(r"(attention to|attention|attn|atn|att|poc)\s*:\s*(.*)", re.I)
TAX = re.compile(r"(?:^|\s*-\s*|\s+)(VAT(?: ID| Number)?|RFC|GSTIN|Head Office GSTIN)\s*:\s*([A-Z0-9][A-Z0-9 -]*[A-Z0-9])\s*;?,?\s*", re.I)
EMAIL = re.compile(r"[\w.+'-]+@[\w-]+(?:\.[\w-]+)+")

def contact(c):
    raw = c.get("name", "")
    if raw.strip() == "..":
        return {}
    d = {"name": raw.strip(), "company": raw.strip(), "attention": "", "taxid": "", "phone": "", "emails": [], "line1": "", "line2": "",
         "citystatezip_country": "", "country": ""}
    # A leading space marks "Contact person, Company".
    if raw.startswith(" ") and ", " in raw.strip():
        d["attention"], d["company"] = [x.strip() for x in raw.strip().split(", ", 1)]
    addr = []
    for l in c.get("lines", []):
        m = LABEL.match(l.strip())
        if m:
            k = m.group(1).lower()
            if k in ("phone", "mobile phone") and not d["phone"]:
                d["phone"] = m.group(2).strip()
            if k in ("email", "url"):
                d["emails"] += EMAIL.findall(m.group(2))
        else:
            addr.append(l)
    if addr:
        d["citystatezip_country"] = addr[-1].strip()
        d["country"] = addr[-1].split(",")[-1].strip()
    if len(addr) >= 2:
        street = " ".join(addr[:-1])
        if ",, " in street + " ":
            fields = [f.strip(" ,") for f in (street + " ").split(",, ")]
        else:
            fields = [street.strip(" ,")]
        fields = [f for f in fields if f]
        out_fields = []
        for f in fields:
            t = TAX.search(f)
            if t:
                d["taxid"] = d["taxid"] or f"{t.group(1)}: {t.group(2)}"
                f = (f[:t.start()] + " " + f[t.end():]).strip(" ,;")
            mid = re.search(r",\s*(?:attention to|attention|attn|atn)\s*:\s*(.+)$", f, re.I)
            if mid:
                d["attention"] = d["attention"] or mid.group(1).strip(" ,")
                f = f[:mid.start()].strip(" ,")
            m = ATTN.match(f)
            if m:
                rest = m.group(2).strip(" ,")
                # "Attn: Name, street" on a line without Sage's double-comma field breaks
                if len(fields) == 1 and ", " in rest:
                    rest, street_part = rest.split(", ", 1)
                    out_fields.append(street_part.strip(" ,"))
                d["attention"] = d["attention"] or rest
                continue
            if f:
                out_fields.append(f)
        fields = out_fields
        d["line1"] = fields[0] if fields else ""
        d["line2"] = ", ".join(fields[1:])
    return d

KEYS = ("name", "company", "attention", "taxid", "line1", "line2", "citystatezip_country", "country", "phone", "email")
with open(out, "w", newline="", encoding="utf-8-sig") as o:
    w = csv.writer(o)
    w.writerow(hdr + [f"{kind}_{k}" for kind in ("display", "primary", "billto", "shipto") for k in KEYS])
    for c in customers:
        row = [c.get(h, "") for h in hdr]
        for kind in ("display", "primary", "billto", "shipto"):
            d = contact(c["_contacts"].get(kind, {}))
            row += [d.get(k, "") if k != "email" else "; ".join(d.get("emails", [])) for k in KEYS]
        w.writerow(row)
print(f"{len(customers)} customers -> {out}")
