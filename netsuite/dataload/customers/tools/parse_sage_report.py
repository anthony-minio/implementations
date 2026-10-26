#!/usr/bin/env python3
# Flatten the Sage Intacct "Customer list" report (one header row per customer, then contact blocks) to one row per customer.
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
        cur["_contacts"][block] = {"name": r[2].strip(), "lines": []}
    elif cur is not None and block and not r[0] and not r[1] and r[2].strip():
        cur["_contacts"][block]["lines"].append(r[2].strip())

def contact(c):
    name, lines = c.get("name", ""), c.get("lines", [])
    if name == "..":
        return {}
    d = {"name": name, "phone": "", "email": "", "fax": "", "addr": []}
    for l in lines:
        m = re.match(r"(Phone|Email|Fax|Mobile|Cell|Pager|URL):\s*(.*)", l)
        if m:
            d[m.group(1).lower()] = m.group(2).strip()
        else:
            d["addr"].append(l)
    # Last address line ends with the country.
    d["country"] = d["addr"][-1].split(",")[-1].strip() if d["addr"] else ""
    if len(d["addr"]) >= 2:
        parts = [p.strip() for p in d["addr"][0].split(",") if p.strip()]
        d["line1"] = parts[0] if parts else ""
        d["line2"] = ", ".join(parts[1:])
    else:
        d["line1"] = d["line2"] = ""
    return d

fields = hdr + []
extra = []
for kind in ("display", "primary", "billto", "shipto"):
    extra += [f"{kind}_{k}" for k in ("name", "line1", "line2", "citystatezip_country", "country", "phone", "email")]
with open(out, "w", newline="", encoding="utf-8-sig") as o:
    w = csv.writer(o)
    w.writerow(fields + extra)
    for c in customers:
        row = [c.get(h, "") for h in hdr]
        for kind in ("display", "primary", "billto", "shipto"):
            d = contact(c["_contacts"].get(kind, {}))
            csz = d.get("addr", [""])[-1] if len(d.get("addr", [])) >= 2 else (d.get("addr", [""]) or [""])[0]
            row += [d.get("name", ""), d.get("line1", ""), d.get("line2", ""), csz, d.get("country", ""), d.get("phone", ""), d.get("email", "")]
        w.writerow(row)
print(f"{len(customers)} customers -> {out}")
