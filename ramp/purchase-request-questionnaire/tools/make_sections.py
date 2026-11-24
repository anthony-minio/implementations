#!/usr/bin/env python3
"""Write sections/ from the program capture files and CATEGORIES.md.

Run from the project folder: python3 tools/make_sections.py
"""
import re

PROGRAMS = [("GP", "GENERAL-PROCUREMENT.md", "General Procurement"),
            ("PS", "PROFESSIONAL-SERVICES.md", "Professional Services"),
            ("SW", "SOFTWARE-SAAS.md", "Software / SaaS")]
NAME = {c: n for c, _, n in PROGRAMS}


def question_rows(path):
    s = open(path).read()
    sec = s[s.index("## Questions"):]
    if "\n### " in sec:
        sec = sec[:sec.index("\n### ")]
    out = []
    for line in sec.splitlines():
        if re.match(r"^\| \d+ \| ", line):
            out.append([c.strip() for c in line.strip().strip("|").split(" | ")])
    return out


rows = {}
for code, path, _ in PROGRAMS:
    for r in question_rows(path):
        rows[f"{code}{r[0]}"] = r


def approval(i):
    t = rows[i][5]
    return "approval icon" in t and "no approval icon" not in t


def shown_when(i):
    code = re.match(r"[A-Z]+", i).group(0)
    t = rows[i][5]
    if not t.startswith("Shown"):
        return "Always"
    t = re.split(r" \(condition screenshot|\. Drives|\. Branch| Branch icon", t)[0]
    t = t.rstrip(".")
    t = re.sub(r"#(\d+)", lambda m: f"{code}{m.group(1)}", t)
    # Shorten long option text; the full text is in the program capture files.
    t = re.sub(r'"Yes — I have already discussed[^"]*"', '"Yes"', t)
    t = re.sub(r'"Yes \( Please Explain[^"]*"', '"Yes"', t)
    t = t.replace("is option 1", 'is "Yes"')
    t = re.sub(r'is "Customer-facing sales meeting / dinner", "Marketing event / sponsorship", "Conference / trade show", '
               r'"Internal meeting / team event" or "Training / enablement" \(every option except "Other"\)',
               'is any event type (any option except "Other")', t)
    t = re.sub(r" \(same condition as [A-Z]+\d+\)", "", t)
    return t


def required(i):
    v = rows[i][4]
    return {"Always required": "Yes", "Locked": "Yes (Ramp field)"}.get(v, v)


def programs(ids):
    codes = sorted({re.match(r"[A-Z]+", i).group(0) for i in ids}, key=["GP", "PS", "SW"].index)
    return "All three" if len(codes) == 3 else ", ".join(codes)


# Categories and distinct questions from CATEGORIES.md
cat_text = open("CATEGORIES.md").read()
distinct = cat_text[cat_text.index("# Distinct questions by category"):cat_text.index("# Appendix")]
cats = []
for block in re.split(r"\n## ", distinct)[1:]:
    head = block.splitlines()[0]
    m = re.match(r"(\d+|Other)\.? ?(.*)", head)
    num, name = (m.group(1), m.group(2) or "Other") if m.group(1) != "Other" else ("Other", "Other")
    qs = []
    for line in block.splitlines():
        mm = re.match(r"^\| (D[\dO]+\.\d+) \| (.*?) \| ([A-Z]{2}\d+(?:, [A-Z]{2}\d+)*) \| (.*?) \| (.*?) \|$", line)
        if mm:
            qs.append((mm.group(1), mm.group(2), mm.group(3).split(", "), mm.group(4)))
    cats.append((num, name, qs))

assert sum(len(i) for c in cats for q in c[2] for i in [q[2]]) == 100

L = ["# Summary", ""]
L.append("Program codes: **GP** General Procurement (28 questions), **PS** Professional Services (32), "
         "**SW** Software / SaaS (40). The 100 questions in Ramp today come down to "
         f"{sum(len(c[2]) for c in cats)} distinct questions. **Approval** marks a question Ramp uses in approval conditions.")
L.append("")
L.append("## Categories")
L.append("")
L.append("| **#** | **Category** | **Distinct questions** | **In Ramp today** | **Programs** |")
L.append("|---|---|---|---|---|")
for num, name, qs in cats:
    ids = [i for q in qs for i in q[2]]
    L.append(f"| **{num}** | {name} | {len(qs)} | {len(ids)} | {programs(ids)} |")
L.append("")
L.append("## Distinct questions")
L.append("")
L.append("| **ID** | **Question** | **Programs** | **Asked in** | **Approval** |")
L.append("|---|---|---|---|---|")
for num, name, qs in cats:
    L.append(f"| **{num}. {name}** | | | | |" if num != "Other" else "| **Other** | | | | |")
    for did, text, ids, _ in qs:
        L.append(f"| **{did}** | {text} | {programs(ids)} | {', '.join(ids)} | {'Yes' if any(approval(i) for i in ids) else ''} |")
L.append("")
open("sections/01-SUMMARY.md", "w").write("\n".join(L))

L = ["# All questions", ""]
L.append("Every question as it is in Ramp today, by category. Rows are in the order of the distinct questions in the summary. **Program**: GP General Procurement, PS Professional Services, SW Software / SaaS. Titles are copied from Ramp; `...` means the title was cut off in the screenshot. **Approval** after the type means Ramp uses the answer in approval conditions.")
L.append("")
for num, name, qs in cats:
    L.append(f"## {num}. {name}" if num != "Other" else "## Other")
    L.append("")
    L.append("| **ID** | **Question** | **Program** | **Type** | **Required** | **Shown when** |")
    L.append("|---|---|---|---|---|---|")
    for did, _, ids, _ in qs:
        for i in ids:
            code = re.match(r"[A-Z]+", i).group(0)
            r = rows[i]
            typ = r[2] + (", **Approval**" if approval(i) else "")
            L.append(f"| **{i}** | {r[1]} | {code} | {typ} | {required(i)} | {shown_when(i)} |")
    L.append("")
open("sections/02-ALL-QUESTIONS.md", "w").write("\n".join(L))
print("written")
