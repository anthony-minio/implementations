#!/usr/bin/env python3
# Build the customer review page: Sage customers mapped to the NetSuite template, enriched from Salesforce.
#   python3 tools/build_review.py   (run from the customers folder; reads data/, writes data/customer-review.html)
import csv, datetime as dt, difflib, json, re, unicodedata
import openpyxl
import phonenumbers as pn  # pip install phonenumbers

TODAY = dt.date(2026, 10, 27)
FLAT = "data/sage-customers-flat-20261025.csv"
LIST = "data/sage-customers-20261026.csv"
SFDC = "data/sfdc-accounts-customers-20261025.xlsx"  # Lifecycle = Active or Customer, Classic report copy
PARTNERS = "data/sfdc-accounts-with-partners-20261025.xlsx"

# NetSuite terms list (Anthony, 2026-10-26): Due on Receipt, Net 10, Net 15, Net 30, Net 45, Net 60, Net 150.
# Any other Sage "N Days" term becomes a new Net N term; terms that are not a day count stay as Sage has them.
TERMS_LIST = ["Due on Receipt", "Net 10", "Net 15", "Net 30", "Net 45", "Net 60", "Net 150"]

def term(t):
    y = re.match(r"(\d+)\s*years?$", t.strip(), re.I)
    if y:
        return f"Net {int(y.group(1)) * 365}"
    m = re.match(r"(?:Net\s*)?(\d+)\s*days?$|Net\s*(\d+)$", t.strip(), re.I)
    if m:
        return f"Net {m.group(1) or m.group(2)}"
    return "Due on Receipt" if t.strip().lower() == "due on receipt" else ""
AP = re.compile(r"(^|[._-])(ap|accounts?[._-]?payables?|payables?|invoices?|vendorinvoices?|billing|bills?|purchas\w*|procure\w*|po|finance|accounting|acct|payments?)([._-]|\d|@|$)", re.I)

def split_emails(*fields):
    seen = []
    for f in fields:
        for e in re.split(r"[;/,\s]+", f or ""):
            e = e.strip().strip(".")
            if "@" in e and e.lower() not in [x.lower() for x in seen]:
                seen.append(e)
    return seen
# Customer Category from the Sage customer type. Chargebee, Marketplace and Other are new categories for SOA to create
# (meeting with Ming, Nisha, Richard, Tory and Sheng, 2026-10-27).
CATEGORY = {"Direct Sales": "Direct Customer", "Direct Sales with Reseller": "End Customer", "Reseller": "Reseller",
            "Chargebee": "Chargebee", "Marketplace": "Marketplace", "MinIO Training Subscription": "Direct Customer",
            "Event Sponsor": "Other", "Billing Vendor": "Other"}
NEW_CATEGORIES = ["Chargebee", "Marketplace", "Other"]
# Customers with no Sage type: category and Subnet ID confirmed by Nisha (Slack, 2026-10-27).
NO_TYPE = {"C-00381": ("End Customer", "779"), "C-00313": ("Direct Customer", "669"), "C-00414": ("Direct Customer", "754")}
# Not loaded (2026-10-27): the 16 investor records (C00001 to C00016) and StoreManager (no invoices or address).
EXCLUDE = {"C-00036": "StoreManager: no invoices and no address in Sage"}

# Phone: US numbers as (999) 999-9999, all others in international format (+44 20 7885 8888), as the template allows.
# NetSuite phone fields hold 21 characters; extensions are written " x123".
REGION = {"United States": "US", "USA": "US", "Canada": "CA", "Germany": "DE", "France": "FR", "Switzerland": "CH",
          "Saudi Arabia": "SA", "United Kingdom": "GB", "India": "IN", "Netherlands": "NL", "Belgium": "BE",
          "United Arab Emirates": "AE", "Turkey": "TR", "Italy": "IT", "Sweden": "SE", "Singapore": "SG", "China": "CN",
          "Brazil": "BR", "Poland": "PL", "Finland": "FI", "Hungary": "HU", "Japan": "JP", "Indonesia": "ID",
          "Luxembourg": "LU", "Georgia": "GE", "Czech Republic": "CZ", "Mexico": "MX", "Australia": "AU", "Spain": "ES",
          "Armenia": "AM", "Oman": "OM", "Austria": "AT", "New Zealand": "NZ", "Norway": "NO", "Taiwan": "TW",
          "Cyprus": "CY", "Slovakia": "SK", "Russian Federation": "RU", "Vietnam": "VN", "Côte d'Ivoire": "CI",
          "Morocco": "MA", "Hong Kong": "HK", "Denmark": "DK", "Ireland": "IE", "Faroe Islands": "FO",
          "Moldova, Republic of": "MD", "Korea, Republic of": "KR", "Congo, Democratic Republic": "CD", "Senegal": "SN",
          "Ecuador": "EC", "South Africa": "ZA", "Argentina": "AR", "Iraq": "IQ", "Croatia": "HR",
          "Palestinian Territory, Occupied": "PS", "Iceland": "IS", "Lithuania": "LT", "Zambia": "ZM", "Israel": "IL",
          "Guatemala": "GT", "Liechtenstein": "LI", "Bangladesh": "BD", "Bosnia and Herzegovina": "BA", "Ethiopia": "ET",
          "Portugal": "PT", "Estonia": "EE", "Cape Verde": "CV", "Uganda": "UG", "Nigeria": "NG", "Mozambique": "MZ",
          "Mongolia": "MN", "Malaysia": "MY", "Isle of Man": "IM", "Curaçao": "CW", "Lebanon": "LB", "Pakistan": "PK",
          "Kazakhstan": "KZ", "Qatar": "QA"}
# Numbers that pass the format check but are broken in the source.
PHONE_BROKEN = {"C-00451": "97156437 is too short: 971 is the UAE country code and 5 digits remain"}

def phone(raw, country):
    """Return (number, note). number is '' when the source value is not a valid phone number."""
    s = raw.strip().lstrip("'").strip()
    ext = ""
    m = re.search(r"\s*(?:x|ext\.?|extension)\s*:?\s*(\d+)$", s, re.I)
    if m:
        ext, s = m.group(1), s[:m.start()]
    s = re.sub(r"^\+\s+", "+", re.sub(r"\(0\)", "", s)).strip()
    digits, reg = re.sub(r"\D", "", s), REGION.get(country)
    def p(t, r=None):
        try:
            n = pn.parse(t, r)
            return n if pn.is_valid_number(n) else None
        except pn.NumberParseException:
            return None
    if s.startswith("+"):
        n = p(s)
    elif re.fullmatch(r"\(\d{3}\) \d{3}-\d{4}", s):
        n = p(s, "US")  # Salesforce writes every 10-digit number this way, so these are US numbers
    elif reg in ("US", "CA") and (len(digits) == 10 or len(digits) == 11 and digits[0] == "1"):
        n = p(digits, reg)
    elif s[:1] in "0(":
        n = p(s, reg) if reg else None  # national format with a trunk prefix
    else:
        n = p("+" + digits) or (p(s, reg) if reg else None)  # digits that start with the country code
    if not n:
        return "", f"Phone left out: {raw!r} is not a valid phone number"
    nreg = pn.region_code_for_number(n)
    us = nreg == "US" and reg in ("US", None)  # a US number for a customer outside the US is written internationally
    out = pn.format_number(n, pn.PhoneNumberFormat.NATIONAL if us else pn.PhoneNumberFormat.INTERNATIONAL)
    if ext:
        out += f" x{ext}"
        if len(out) > 21:
            out = pn.format_number(n, pn.PhoneNumberFormat.E164) + f" x{ext}"
    note = ""
    if reg and nreg != reg:
        note = f"Phone is a {nreg} number (+{n.country_code}); the address is in {country}"
    return out, note

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

def unmangle(v):
    """Repair UTF-8 text that Sage stored as if it were Windows-1252 (MontrÃ©al -> Montréal)."""
    if re.search(r"Ã|Â|â€", v or ""):
        try:
            return v.encode("cp1252").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return v
    return v

# VAT ID holds VAT or GST registration numbers only, in the standard format with the country prefix.
# Other tax IDs Sage holds (US EIN, company registration numbers) go to Other Tax ID.
VAT_PREFIX = {"Austria": "AT", "Belgium": "BE", "Croatia": "HR", "Cyprus": "CY", "Denmark": "DK", "Finland": "FI",
              "France": "FR", "Germany": "DE", "Ireland": "IE", "Italy": "IT", "Luxembourg": "LU", "Netherlands": "NL",
              "Norway": "NO", "Poland": "PL", "Portugal": "PT", "Spain": "ES", "Sweden": "SE", "Switzerland": "CHE",
              "United Kingdom": "GB"}
VAT_SHAPE = {"AT": r"U\d{8}", "BE": r"[01]\d{9}", "HR": r"\d{11}", "CY": r"\d{8}[A-Z]", "DK": r"\d{8}", "FI": r"\d{8}",
             "FR": r"[0-9A-Z]{2}\d{9}", "DE": r"\d{9}", "IE": r"\d{7}[A-Z]{1,2}", "IT": r"\d{11}", "LU": r"\d{8}",
             "NL": r"\d{9}B\d{2}", "NO": r"\d{9}(MVA)?", "PL": r"\d{10}", "PT": r"\d{9}", "ES": r"[0-9A-Z]\d{7}[0-9A-Z]",
             "SE": r"\d{12}", "CHE": r"\d{9}", "GB": r"\d{9}(\d{3})?"}

def tax_id(country, raw):
    """Return (vat_id, other_tax_id, note) for a Sage tax ID."""
    raw = raw.strip()
    clean = re.sub(r"[\s.\-]", "", raw).upper()
    if country == "United States" and re.fullmatch(r"\d{9}", clean):
        return "", f"US EIN {clean[:2]}-{clean[2:]}", "US employer ID, not a VAT number"
    p = VAT_PREFIX.get(country)
    if p:
        body = clean[len(p):] if clean.startswith(p) else clean
        if p == "BE" and re.fullmatch(r"\d{9}", body):
            body = "0" + body
        if re.fullmatch(VAT_SHAPE[p], body):
            return p + body, "", "" if p + body == raw else f"formatted from {raw}"
        return "", raw, f"not a {country} VAT number format"
    if country in ("Saudi Arabia", "United Arab Emirates") and re.fullmatch(r"3\d{13}3|1\d{14}", clean):
        return clean, "", ""
    if country == "India" and re.fullmatch(r"\d{2}[A-Z]{5}\d{4}[A-Z][0-9A-Z]Z[0-9A-Z]", clean):
        return clean, "", ""  # GSTIN, India's GST registration
    if country == "Mexico" and re.fullmatch(r"[A-Z&]{3,4}\d{6}[0-9A-Z]{3}", clean):
        return clean, "", ""  # RFC, Mexico's taxpayer ID used on invoices
    return "", raw, "not recognized as a VAT number"

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

# Likely name matches reviewed by Anthony on 2026-10-26: all confirmed except these, which are not the same company.
NOT_MATCHED = {"C-00044": "Ministry of Defence (Singapore), not Ministry of Defence UK",
               "C-00142": "Bae Systems, kept separate from BAE Systems US"}
REVIEWED = "2026-10-26"
# Sage data errors corrected in the load (confirmed by Anthony on 2026-10-26).
CORRECT = {"C-00387": {"City": "Lodz", "Address 1": "Ul. Nowy Jozefow 70"},
           "C-00253": {"City": "Abidjan", "Country": "Côte d'Ivoire", "Address 2": "REPUBLIQUE"},
           "C-00108": {"Address 1": "Rodovia BR116 Contorno Leste 7000", "City": "Sao Jose dos Pinhais",
                       "Postal Code/Zip": "83085-058", "Attention": "5011207568/Recieri Netto"}}
# Addresses Sage holds in the wrong fields (2026-10-27): city, postal code or country typed into the street lines,
# a street in the city field, a city in the state field, or the country left at Sage's default (United States) for an
# address abroad. Each value is moved from the Sage text into its own field; nothing is retyped. A tuple marks a value
# taken from Salesforce ("sfdc") or filled by rule, such as a US state from the ZIP code ("rule").
SG = {"City": "Singapore"}  # Singapore is a city-state
ADDRESS_FIX = {
    "C-00597": {"Address 1": "Herderstraße 70", "City": "Köln", "Postal Code/Zip": "50931", "Country": "Germany"},
    "C-00598": {"Address 1": "1 Fusionopolis Way #20-10", "Address 2": "Connexis North Tower", "City": "Singapore",
                "Postal Code/Zip": ("138632", "sfdc"), "Country": "Singapore"},
    "C-00599": {"Address 1": "38 Armeneasca St", "City": "Chisinau", "Postal Code/Zip": "MD-2012", "Country": "Moldova, Republic of"},
    "C-00630": {"Address 1": "Elias Sarkis Avenue, Achrafieh", "City": "Beirut", "Country": "Lebanon"},
    "C-00601": {"Address 1": "10th Floor Lakson Square Building No. 3 Sarwar Shaheed Road", "City": "Karachi",
                "Postal Code/Zip": "74200", "Country": "Pakistan"},
    "C-00602": {"Address 1": "78 SW 7th St. Ste 500", "City": "Miami", "Province/State": "Florida", "Postal Code/Zip": "33130"},
    "C-00603": {"Address 1": "4150 152nd Street Northeast", "City": "Marysville", "Province/State": "Washington", "Postal Code/Zip": "98271"},
    "C-00604": {"Address 1": "UNALAN MAH. AYAZMA CAD CAMLYCA YÞ MERKEZI - B3 BLOK USKUDAR", "City": "Istanbul",
                "Postal Code/Zip": "34700", "Country": "Turkey"},
    "C-00605": {"Address 1": "36 Švitrigailos gatvė", "City": "Vilnius", "Postal Code/Zip": "03228", "Country": "Lithuania"},
    "C-00606": {"Address 1": "Taşyoncası Sok. Maslak 1453 Sitesi No: 1G İç Kapı No: B12", "City": "Istanbul",
                "Postal Code/Zip": "34398", "Country": "Turkey"},
    "C-00607": {"Address 1": "Dieselstraße 22", "City": "Karben", "Postal Code/Zip": "61184", "Country": "Germany"},
    "C-00608": {"Address 1": "3100 Southwest 145th Avenue", "City": "Miramar", "Province/State": "Florida", "Postal Code/Zip": "33027"},
    "C-00609": {"Address 1": "57 Rue de la Convention", "City": "Paris", "Postal Code/Zip": "75015", "Country": "France"},
    "C-00631": {"Address 1": "Via Giulio Pocobelli 6", "City": "Lugano", "Postal Code/Zip": "6900"},
    "C-00632": {"Address 1": "Ataturk Havalimani Dis Hatlar Terminali Yesilkoy Mah", "Address 2": "Bakirkoy", "City": "Istanbul",
                "Postal Code/Zip": "34149"},
    "C-00633": {"Address 1": "6200 South Main Street", "City": "Aurora", "Province/State": "Colorado", "Postal Code/Zip": "80016"},
    "C-00634": {"Address 1": "Gogol St 253/4", "City": "Almaty", "Postal Code/Zip": "050026", "Country": "Kazakhstan"},
    "C-00635": {"City": "Singapore", "Postal Code/Zip": ("338729", "sfdc")},
    "C-00636": {"Address 1": "Am Kaiserkai 69", "City": "Hamburg", "Postal Code/Zip": "20457"},
    "C-00637": {"Address 1": "Plzenska 3351/19", "City": "Praha 5-Smichov", "Postal Code/Zip": "150 00"},
    "C-00004": SG, "C-00044": SG, "C-00143": SG, "C-00252": SG, "C-00350": SG, "C-00378": SG, "C-00498": SG, "C-00641": SG,
    "C-00144": {"Address 2": "", "City": "Singapore", "Postal Code/Zip": "048946"},
    "C-00020": {"Country": "Kazakhstan"},
    "C-00024": {"Address 1": "1111 Bagby St Suite 4500", "City": "Houston", "Province/State": "Texas"},
    "C-00031": {"Address 1": "Rue de Spa 8", "City": "Brussel", "Province/State": "Brussels Hoofdstedtelijk Gewest"},
    "C-00052": {"Address 1": "Europaallee 39", "City": "Zurich", "Postal Code/Zip": "8004"},
    "C-00057": {"City": "Genève 73", "Postal Code/Zip": "1211"},
    "C-00059": {"City": "Beijing"},
    "C-00060": {"Address 1": "Valencia Cami Antic, 54", "City": "Barcelona"},
    "C-00066": {"Address 1": "6-8 Házgyári út", "City": "Veszprém", "Province/State": "", "Postal Code/Zip": "8200"},
    "C-00067": {"Address 1": "1000 Continental Drive", "City": "King of Prussia"},
    "C-00079": {"Address 1": "Emi Bl O S 100", "Address 2": "", "City": "Brasilia", "Province/State": "Federal District"},
    "C-00087": {"City": "London", "Province/State": ""},
    "C-00090": {"Address 2": "Postfach", "City": "Zug", "Postal Code/Zip": "CH-6300"},
    "C-00095": {"Address 1": "89d Rue Pafebruch", "City": "Capallen", "Province/State": "District de Luxembourg", "Postal Code/Zip": "L-8308"},
    "C-00110": {"Province/State": ("VA", "rule")},
    "C-00016": {"Province/State": ("NY", "rule")},
    "C-00115": {"Address 1": ""},
    "C-00116": {"Address 1": "Prince Abdulrahman Bin Abdulaziz St", "Address 2": "", "City": "Riyadh", "Province/State": ""},
    "C-00118": {"Attention": "Ben Damery", "Address 1": "210Celebration Olace", "Province/State": ("FL", "rule")},
    "C-00120": {"Province/State": ("VA", "rule")},
    "C-00156": {"Province/State": ("AL", "rule")},
    "C-00161": {"Province/State": ("GA", "rule")},
    "C-00183": {"Province/State": ("CA", "rule")},
    "C-00194": {"Address 1": "Almas Tower Office 40D, JLT"},
    "C-00205": {"City": "Seoul", "Province/State": ""},
    "C-00222": {"Province/State": ("IN", "rule")},
    "C-00228": {"Address 2": "Yeongtong-gu", "City": "Suwon-si", "Province/State": "Gyeonggi-do"},
    "C-00237": {"City": "Basel", "Postal Code/Zip": "4002"},
    "C-00239": {"Address 1": "7 rue F. Roosevelt", "City": "Rabat"},
    "C-00241": {"City": "Riyadh", "Province/State": ""},
    "C-00243": {"City": ("Jakarta", "sfdc")},
    "C-00245": {"City": "Brussels", "Postal Code/Zip": "1000"},
    "C-00247": {"City": "London", "Province/State": ""},
    "C-00254": {"Address 1": "Anikó u. 4.", "City": "Budapest", "Postal Code/Zip": "1031"},
    "C-00272": {"City": "Jakarta", "Province/State": ""},
    "C-00281": {"Address 2": "", "City": "Vestavia Hills"},
    "C-00291": {"Province/State": ""},
    "C-00293": {"Address 1": "Av.EmbaixadorMacedoSoares 10001", "Address 2": "Predio 19 Esp 3 e 4 133", "City": "Sao Paulo"},
    "C-00296": {"City": "LUXEMBOURG", "Province/State": "", "Postal Code/Zip": "L-1150"},
    "C-00299": {"Address 2": "PO Box 712", "City": "Amsterdam", "Postal Code/Zip": "1000 AS"},
    "C-00300": {"City": "Hong Kong"},
    "C-00310": {"City": ("Berlin", "rule")},
    "C-00357": {"Address 1": "1701 East Mossy Oaks Road", "City": "Spring"},
    "C-00374": {"City": "Taipei", "Postal Code/Zip": "114"},
    "C-00382": {"Address 1": "Szechenyi Istvan ter 7-8. C. ep. 4. em", "City": "Budapest", "Postal Code/Zip": "1051"},
    "C-00391": {"City": "Riyadh", "Province/State": ""},
    "C-00392": {"Address 1": "2091 Gyeongchung-daero Bubal-eup", "City": "Icheon-si"},
    "C-00403": {"Address 2": "", "City": "Arroyo Grande"},
    "C-00404": {"Address 1": ("Werderstraße 36", "sfdc"), "Address 2": "ACHTUNG NEU: Zufahrt über Schloßstraße"},
    "C-00407": {"Address 2": "", "City": "LYON CEDEX 09", "Postal Code/Zip": "69279"},
    "C-00419": {"Address 1": "1 FREEDOM VALLEY DRIVE", "City": "OAKS"},
    "C-00425": {"Address 2": "", "City": "NORDEA", "Postal Code/Zip": "00020"},
    "C-00439": {"Address 1": "Al Thumama Road, Qurtubah"},
    "C-00444": {"Attention": "PO200412", "Address 1": "G126, Cody Tech Park", "Address 2": "", "City": "Farnborough"},
    "C-00447": {"City": "Staines", "Province/State": ""},
    "C-00560": {"Attention": "Kevin Darby", "Address 1": "5770 MISSILE WAY", "Address 2": "", "City": "Roy"},
}
ADDRESS_WHY = {
    "C-00115": "Sage street line was \"deilver digitally\", not an address",
    "C-00404": "Sage street line was a delivery note (\"ACHTUNG NEU: Zufahrt über Schloßstraße\"); street from Salesforce, note kept in Address 2",
    "C-00310": "State BE is Berlin; postal code 14195 is in Berlin",
    "C-00444": "PO200412 is a purchase order number, moved from Address 1 to Attention",
}
ADDRESS_CHECK = {
    "C-00020": "Postal code 55 0100000 is as Sage has it; Kazakhstan postal codes have 6 digits (Astana is 010000)",
    "C-00153": "ZIP 110018 is as Sage has it; New York ZIPs have 5 digits (West 40th Street is 10018)",
    "C-00326": "No ZIP code in Sage",
    "C-00238": "Sage address mixes Electronics City (Bangalore) and Hinjawadi (Pune); city left blank",
    "C-00604": "Sage address has garbled Turkish characters (CAMLYCA YÞ for ÇAMLICA İŞ), kept as Sage has them",
    "C-00546": "Salesforce has Doha, Qatar for the same P.O. Box; Sage has Dubai, kept",
}

# Second pass of address corrections (Anthony, 2026-10-28): contacts typed into the street line moved to Attention; city
# fields holding a state, county or district split into city and state, using the street and postal code to be sure of
# the city; Sage typos fixed only where the full address confirms the place; country prefixes stripped from postal codes
# and lost leading zeros restored; postal codes that cannot be worked out from the address removed. A ("value", "rule")
# tuple is a value not in the Sage text (a corrected spelling or a postal code read from the address).
ADDRESS_FIX2 = {
    "C-00291": {"Attention": "Cheick Diakite", "Address 1": "01 BP 3865, Abidjan 01", "Address 2": ""},
    "C-00312": {"Attention": "Sophia Choi", "Address 1": "425 West 6th Avenue, Unit 400", "Address 2": ""},
    "C-00413": {"Attention": "PHILIP HANKINS, Customer PO Number H86203", "Address 1": "7 Murray Rose Avenue", "Address 2": "",
                "City": "SYDNEY OLYMPIC PARK", "Province/State": "NSW"},
    "C-00125": {"Attention": "Johannes Weidacher", "Address 1": "Mühldorfstrasse 15", "Address 2": ""},
    "C-00129": {"Attention": "Maxi Schaefer", "Address 1": "Robert-Bosch-Straße 200", "Address 2": ""},
    "C-00150": {"Attention": "ASHISH MAHAJAN", "Address 1": "415 MISSION ST", "Address 2": ""},
    "C-00188": {"Attention": "Frau Brüner", "Address 1": "DVO Team IT-Einkauf", "Address 2": ""},
    "C-00227": {"Attention": "Jaap Albers (06-29677174)", "Address 1": "Prins Willem-Alexanderhof 20", "Address 2": "",
                "Province/State": "", "Postal Code/Zip": "2595 BE"},
    "C-00311": {"Attention": "Fabio Colombo", "Address 1": "Viale Restelli 1/A", "Address 2": "", "Postal Code/Zip": "20124"},
    "C-00320": {"Address 1": "Auf dem Steinbüchel 22", "Address 2": ""},
    "C-00386": {"Address 1": "Rue de la Fusée 96", "Address 2": ""},  # Luc Mortier is Atos's contact: Reseller Contact
    "C-00540": {"Attention": "Shil Bhattacharyya", "Address 1": "1003 W FM 193", "Address 2": ""},
    "C-00565": {"Attention": "Ms Jenny Parrish - Finance Department (L)", "Address 1": "PO Box 8000", "Address 2": ""},
    "C-00058": {"Address 1": "Rudolf-Breitscheid-Str 1-5", "Postal Code/Zip": "35037"},
    "C-00623": {"Address 2": "Clieveragh Road", "City": "Listowel", "Province/State": "Kerry"},
    "C-00051": {"Address 1": "Rakuten Crimson House, 1-14-1 Tamagawa", "City": "Setagaya-ku"},
    "C-00069": {"Address 1": "Eighty Eight Kasabkanka Lt 18 Jl., Casablanca Raya Kav. 88", "City": ("Jakarta Selatan", "rule")},
    "C-00075": {"City": ("Pittsburgh", "rule")},
    "C-00135": {"Country": "Russian Federation"},
    "C-00136": {"Address 1": "Miklukho-Maklaya ul, dom 40", "Address 2": "Podval Pomeshchenie I Kom 25", "City": ("Moscow", "rule"),
                "Postal Code/Zip": "117342"},
    "C-00139": {"City": ("Hangzhou", "rule"), "Province/State": "Zhejiang"},
    "C-00140": {"Address 2": "", "City": "Porto Velho", "Province/State": ("Rondônia", "rule"), "Postal Code/Zip": "76801-330"},
    "C-00148": {"City": ("San Francisco", "rule")},
    "C-00170": {"City": "Rende", "Province/State": "CS"},
    "C-00200": {"Address 2": "Enseada do Suá", "City": "Vitória"},
    "C-00212": {"City": "Milano", "Province/State": "MI"},
    "C-00213": {"City": ("Navi Mumbai", "rule"), "Province/State": "Maharashtra"},
    "C-00223": {"Address 2": "INFORMATION SYSTEMS CENTRE PLOT NO. 40 , HI- TECH CITY PHASE-II, MADHAPUR", "City": "HYDERABAD"},
    "C-00226": {"Address 2": "P.O. Box", "City": "Zürich"},
    "C-00233": {"City": "CASALECCHIO DI RENO", "Province/State": "BO"},
    "C-00257": {"Address 2": "", "City": "Cheltenham", "Province/State": "Gloucestershire"},
    "C-00276": {"Address 2": "NGALIEMA", "City": "KINSHASA"},
    "C-00288": {"City": ("Redwood City", "rule")},
    "C-00306": {"Address 2": "", "City": "Newbury", "Province/State": "Berkshire"},
    "C-00325": {"City": "Suzhou", "Province/State": "Jiangsu"},
    "C-00335": {"Address 1": "Av Cidade de Lisboa", "Address 2": "Várzea, CP.620", "City": "Praia", "Postal Code/Zip": ""},
    "C-00355": {"Address 2": "Marcigliana", "City": ("Roma", "rule")},
    "C-00361": {"Address 2": "", "City": "Ouro Preto do Oeste", "Province/State": ("Rondônia", "rule")},
    "C-00369": {"City": "New York"}, "C-00543": {"City": "New York"},
    "C-00376": {"City": ("Wiesbaden", "rule")},
    "C-00400": {"Address 1": "Rua Caetes, 13 – Piedade", "City": "Itaúna", "Province/State": "Minas Gerais"},
    "C-00401": {"Address 2": "", "City": "Koblenz", "Province/State": "Rheinland-Pfalz"},
    "C-00420": {"Address 2": "Wenyi West Road, Wuchang Street,Yuhang District", "City": "Hangzhou", "Province/State": "Zhejiang"},
    "C-00437": {"City": ("San Jose", "rule")},
    "C-00481": {"Address 2": "Westwells Rd", "City": "Corsham", "Province/State": ("Wiltshire", "rule")},
    "C-00569": {"City": ("Tbilisi", "rule")},
    "C-00588": {"Address 1": "HFM 4911; Channel Way", "City": "Preston", "Province/State": "Lancashire"},
    "C-00594": {"Address 2": "High-Tech Zone", "City": "Hefei", "Province/State": "Anhui", "Postal Code/Zip": ""},
    "C-00048": {"Postal Code/Zip": "EC2V 5DD"}, "C-00056": {"Postal Code/Zip": "1170"}, "C-00090": {"Postal Code/Zip": "6300"},
    "C-00095": {"Postal Code/Zip": "8308"}, "C-00111": {"Postal Code/Zip": ("600081", "rule")},
    "C-00117": {"Postal Code/Zip": "164 80"}, "C-00153": {"Postal Code/Zip": ("10018", "rule")},
    "C-00155": {"Postal Code/Zip": ("K1A 0Y7", "rule")}, "C-00198": {"Address 2": "", "Postal Code/Zip": "3372"},
    "C-00215": {"City": "Son", "Postal Code/Zip": "5692 ED"}, "C-00232": {"Postal Code/Zip": "852 29"},
    "C-00271": {"Postal Code/Zip": "60329"}, "C-00296": {"Postal Code/Zip": "1150"}, "C-00315": {"Postal Code/Zip": "93059"},
    "C-00317": {"Postal Code/Zip": ""}, "C-00327": {"Postal Code/Zip": "111 51"}, "C-00368": {"Postal Code/Zip": "8152"},
    "C-00427": {"Postal Code/Zip": "10709"}, "C-00440": {"Postal Code/Zip": "04289"}, "C-00441": {"Postal Code/Zip": "01510"},
    "C-00448": {"Postal Code/Zip": ("EC4N 6AE", "rule")}, "C-00492": {"Postal Code/Zip": ("08940", "sfdc")},
    "C-00518": {"Postal Code/Zip": "115 38"}, "C-00614": {"Postal Code/Zip": "63225"},
    "C-00566": {"Postal Code/Zip": ("20755", "rule")},
    "C-00180": {"Province/State": ""}, "C-00132": {"Province/State": "Guatemala"},
    "C-00177": {"Country": "Germany"},
    "C-00019": {"Address 1": "", "Address 2": "", "City": "", "Province/State": "", "Postal Code/Zip": "", "Country": ""},
    "C-00316": {"Country": "Monaco"}, "C-00256": {"Country": "Hong Kong"}, "C-00415": {"Country": "Hong Kong"},
    "C-00208": {"Address 1": ("No 14 Sarı Kanarya Sokak", "sfdc"), "City": ("Kozyataği", "sfdc")},
    # Customers with no address in Sage: high-confidence addresses approved by Anthony, 2026-10-28.
    "C-00097": {"Address 1": ("No 14 Sarı Kanarya Sokak", "sfdc"), "City": ("Kozyataği", "sfdc"),
                "Postal Code/Zip": ("34742", "sfdc"), "Country": ("Turkey", "sfdc")},
    "C-00530": {"Address 1": ("6 Rue Fructidor", "sfdc"), "City": ("Saint-Ouen-Sur-Seine", "sfdc"),
                "Postal Code/Zip": ("93400", "sfdc"), "Country": ("France", "sfdc")},
    "C-00536": {"Address 1": ("ul. Piecewska 34B", "sfdc"), "City": ("Gdańsk", "sfdc"), "Postal Code/Zip": ("80-288", "sfdc"),
                "Country": ("Poland", "sfdc")},
    "C-00532": {"Address 1": ("#22-24 Norodom Blvd", "rule"), "Address 2": ("Daun Penh", "rule"), "City": ("Phnom Penh", "rule"),
                "Country": ("Cambodia", "rule")},
}
for _cid, _fix in ADDRESS_FIX2.items():
    ADDRESS_FIX.setdefault(_cid, {}).update(_fix)
RESELLER_CONTACT = {"C-00386": "Luc Mortier"}  # Sage had the reseller's contact (Atos) in the customer's street line
ADDRESS_WHY.update({
    "C-00097": "No address in Sage; address from the Salesforce account Viennalife (formerly Aegon), Subnet 329, approved 2026-10-28",
    "C-00530": "No address in Sage; address from the Salesforce account Economie d'Energie, Subnet 947, approved 2026-10-28",
    "C-00536": "No address in Sage; address from the Salesforce account Nais.co, Subnet 964, approved 2026-10-28",
    "C-00532": "No address in Sage; head office address from public directories (#22-24 Norodom Blvd), approved 2026-10-28",
    "C-00208": "Sage street and city had garbled Turkish characters (Sar# Kanarya, Kozyata#i); Salesforce spelling used",
    "C-00136": "Sage city was the typo Moscoa; postal code 117342 from the Sage street line, which matches Miklukho-Maklaya ul (Sage postal field had 125373)",
    "C-00594": "Sage postal code 518057 is in Shenzhen, not Hefei; removed",
    "C-00177": "Sage country Georgia; the address is in Germany (Everswinkel 48351, a GmbH & Co. KG, phone +49 2582, email .de)",
    "C-00019": "Address left blank (2026-10-28): Sage has a London street (100 New Bridge Street) with city London, state CT and ZIP 06902 (Stamford, CT), which cannot be settled; Sage's bill-to is Kayak Software Corporation, 7 Market Street, Stamford, CT 06902",
    "C-00317": "Sage postal code 1153 is incomplete (Saudi codes have 5 digits); removed",
    "C-00335": "CP.620 is a P.O. box (Caixa Postal), not a postal code; moved to Address 2",
    "C-00448": "Sage postal code EC4N GAE is a typo; 66 Cannon Street is EC4N 6AE",
    "C-00155": "Sage postal code K1A OY7 has the letter O for zero",
    "C-00153": "Sage ZIP 110018 has an extra digit; West 40th Street, New York is 10018",
    "C-00566": "No ZIP code in Sage; Fort Meade, MD is 20755",
})
ADDRESS_CHECK.update({
    "C-00618": "City Yvelines (a French department) with postal code 75009 (Paris); left as Salesforce has it",
})
ADDRESS_CHECK.pop("C-00153", None)

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
INVESTOR = re.compile(r"C\d+$")  # C00001 to C00016: investors and note holders, not loaded
for x in sorted((x for x in sage if x["Status"] == "Active" and not re.match(r"C-\d{5}$", x["Customer ID"])
                 and not INVESTOR.match(x["Customer ID"])), key=lambda x: x["Customer ID"]):
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
ADDED = ["Question Categories", "Duplicate Action", "Merged Sage IDs", "Second Address", "Third Address", "Sage Customer ID", "Salesforce Account ID", "Parent Customer ID", "Additional Emails", "Other Tax ID", "Billed To (Reseller)",
         "Reseller Contact", "Reseller Address", "Reseller Invoice Email", "Salesforce Partners"]
REVIEW = ["Sage type", "Sage terms", "Last invoice", "Balance", "Salesforce match"]

# One-time-use customers are active in Sage but left out of the customer list report: only the list export has them.
report_ids = {x["Customer ID"] for x in sage}
ONETIME = [cid for cid in lst if cid not in report_ids]
blank = {k: "" for k in sage[0]}
onetime_rows = [dict(blank, **{"Customer ID": cid, "Customer name": lst[cid]["Customer name"], "Status": "Active",
                               "Customer type": lst[cid]["Customer type ID"]}) for cid in ONETIME]

out, new_terms, research, parents_dropped, excluded, parent_sf = [], {}, {}, {}, [], {}
for r in sage + onetime_rows:
    if r["Status"] != "Active":
        continue
    cid = r["Customer ID"]
    # One-time-use customers have no category and no invoices in the exports: left out (Anthony, 2026-10-27).
    if INVESTOR.match(cid) or cid in EXCLUDE or cid in ONETIME:
        excluded.append((cid, r["Customer name"]))
        continue
    c = {k: ["", ""] for k in COLS}
    def S(k, v, src="sage"):
        fixed = unmangle(v)
        if fixed != v:
            flags.append(f"Garbled characters repaired: {k}")
        c[k] = [fixed, src if fixed else ""]
    flags = []
    investor = False
    if cid in ONETIME:
        flags.append("One-time use in Sage: only the name is in the Sage exports, no address, contact or terms")
    last, bal = date(r["Last invoice date"]), float(r["Balance"] or 0)
    in_scope = True  # every customer not marked inactive in Sage
    m, how = match(r["Customer name"])
    if cid in NOT_MATCHED:
        m, how = None, ""
    elif how == "likely":
        how = "confirmed"

    if cid in renumber:
        S("Customer ID", renumber[cid], "rule")
        flags.append(f"Renumbered from Sage {cid}")
    else:
        S("Customer ID", cid)
    S("External ID", c["Customer ID"][0], "rule")
    S("Company Name", r["Customer name"])
    if m:
        S("Subnet ID", m["Subnet Account Id"], "sfdc")
        if m["Parent Account ID"]:
            # Parents that are not Sage customers have no billing history and are left out, so the link is dropped.
            par = by_id.get(m["Parent Account ID"])
            if par and any(norm(par["Account Name"]) == norm(x["Customer name"]) for x in sage):
                S("Parent Company", m["Parent Account"], "sfdc")
                parent_sf[cid] = m["Parent Account ID"]
            else:
                parents_dropped[m["Parent Account"]] = parents_dropped.get(m["Parent Account"], 0) + 1
    S("Subsidiary", "MinIO, Inc.", "rule")
    if r["Default currency"]:
        S("Primary Currency", r["Default currency"])
    else:
        S("Primary Currency", "USD", "prop")
    billto = r["billto_name"] and r["billto_name"] != r["display_name"]
    # Invoice email: the first AP or purchasing address, else the first address; the rest go to Additional Emails.
    emails = split_emails(r["display_email"], r["primary_email"], "" if billto else r["billto_email"])
    ap = [e for e in emails if AP.search(e.split("@")[0])]
    inv = (ap or emails or [""])[0]
    S("Customer Invoice Email", inv)
    more = [e for e in emails if e != inv]
    S("Status", "CUSTOMER-Closed Won", "rule")
    S("Individual (Type)", "FALSE", "rule")
    cat = CATEGORY.get(r["Customer type"], "")
    S("Customer Category", cat, "rule")
    if cid in NO_TYPE:
        cat = NO_TYPE[cid][0]
        S("Customer Category", cat, "rule")
        S("Subnet ID", NO_TYPE[cid][1], "rule")
        flags.append("No Sage type: category and Subnet ID confirmed by Nisha, 2026-10-27")
    S("Attention", r["display_attention"])
    S("Addressee", r["display_company"])
    S("Address 1", r["display_line1"].rstrip(","))
    S("Address 2", r["display_line2"].rstrip(","))
    l = lst.get(cid, {})
    S("City", l.get("City", "").rstrip(", ").strip())
    S("Province/State", l.get("State or territory", "").strip(" ,"))
    S("Postal Code/Zip", l.get("ZIP or postal code", "").strip(" ,"))
    S("Country", r["display_country"])
    if not r["display_line1"] and m and m["Billing Street"]:
        S("Address 1", m["Billing Street"], "sfdc")
        S("City", m["Billing City"], "sfdc")
        S("Province/State", m["Billing State/Province"], "sfdc")
        S("Postal Code/Zip", m["Billing Zip/Postal Code"], "sfdc")
        S("Country", m["Billing Country"], "sfdc")
    if c["Address 1"][0]:
        S("Default Billing", "TRUE", "rule")
        S("Default Shipping", "TRUE", "rule")
    else:
        flags.append("No street address")
    # US postal codes that lost their leading zero in Sage (7936 -> 07936).
    z = re.fullmatch(r"(\d{3,4})(-\d{4})?", c["Postal Code/Zip"][0])
    if z and c["Country"][0] == "United States" and c["Postal Code/Zip"][1] in ("sage", "sfdc"):
        flags.append(f"Postal code leading zero restored: was {c['Postal Code/Zip'][0]}")
        S("Postal Code/Zip", z.group(1).zfill(5) + (z.group(2) or ""), "rule")
    for k, v in CORRECT.get(cid, {}).items():
        flags.append(f"Corrected from Sage: {k} was {c[k][0] or 'blank'}")
        S(k, v, "rule")
    fix = ADDRESS_FIX.get(cid, {})
    if fix:
        moved = []
        for k, v in fix.items():
            v, how3 = v if isinstance(v, tuple) else (v, "sage")
            if c[k][0] != v:
                moved.append(f"{k} was {c[k][0]!r}" if c[k][0] else f"{k} was blank")
                S(k, v, how3 if how3 != "sage" else "rule")
        if moved:
            flags.append("Address fields corrected from the Sage text: " + "; ".join(moved))
        if cid in ADDRESS_WHY:
            flags.append(ADDRESS_WHY[cid])
        # an address moved into Address 1 becomes the default billing and shipping address, as Sage addresses do
        c["Default Billing"] = ["TRUE", "rule"] if c["Address 1"][0] else ["", ""]
        c["Default Shipping"] = list(c["Default Billing"])
    # Sage fills United States when no address is entered; with no address at all, that country is not data.
    if c["Country"] == ["United States", "sage"] and not any(c[k][0] for k in ("Address 1", "Address 2", "City", "Province/State", "Postal Code/Zip")):
        c["Country"] = ["", ""]
        flags.append("Country left blank: no address in Sage, and Sage's United States is its default when none is entered")
    if cid in ADDRESS_CHECK:
        flags.append("Address to check: " + ADDRESS_CHECK[cid])
    # Phone: Sage first, else Salesforce; a number that is not valid is left out and the source value kept in Flags.
    for raw_ph, src_ph in ((r["display_phone"], "sage"), ((m or {}).get("Phone", ""), "sfdc")):
        if not raw_ph:
            continue
        if cid in PHONE_BROKEN:
            flags.append(f"Phone left out: {raw_ph!r}, {PHONE_BROKEN[cid]}")
            continue
        num, note = phone(raw_ph, c["Country"][0])
        if note:
            flags.append(note + ("" if num else f" ({'Sage' if src_ph == 'sage' else 'Salesforce'})"))
        if num:
            S("Phone", num, src_ph)
            if num != raw_ph:
                flags.append(f"Phone formatted from {raw_ph!r}")
            break
    if m and m["Billing Country"] and c["Country"][0] and m["Billing Country"].lower() != c["Country"][0].lower():
        flags.append(f"Country differs in Salesforce: {m['Billing Country']}")
    if r["Term"]:
        t = term(r["Term"])
        if t:
            S("Terms", t, "rule" if t != r["Term"] else "sage")
            if t not in TERMS_LIST:
                new_terms[t] = new_terms.get(t, 0) + 1
                flags.append(f"New NetSuite term: {t}")
        else:
            research[r["Term"]] = research.get(r["Term"], 0) + 1  # Due per Contract: left blank (2026-10-27)
            flags.append(f"Terms left blank: Sage has {r['Term']}")
    raw_tax = r["Tax ID"] or (r["display_taxid"].split(": ", 1)[1] if r["display_taxid"] else "")
    other_tax = ""
    if raw_tax:
        vat, other_tax, why = tax_id(c["Country"][0] or r["display_country"], raw_tax)
        if vat:
            S("VAT ID", vat, "sage" if vat == raw_tax and r["Tax ID"] else "rule")
            S("International VAT ID", vat, "rule")  # same number in both columns; SOA to keep the one they use (2026-10-28)
        if why:
            flags.append(f"Tax ID: {why}")
        if not r["Tax ID"]:
            flags.append(f"Tax ID taken from Sage address: {r['display_taxid']}")
    for k in REQUIRED:
        if not c[k][0]:
            c[k][1] = "miss"

    if investor:
        flags.append("Investor or non-sales")
    dup = [x for x in names.get(r["Customer name"].strip().lower(), []) if x != cid]
    if dup:
        flags.append("Duplicate name: " + ", ".join(dup))
    else:
        nd = [x for x in near.get(norm(r["Customer name"]), []) if x != cid]
        if nd:
            flags.append("Similar name: " + ", ".join(nd))
    if not m:
        flags.append("No Salesforce match")
    elif how == "confirmed":
        flags.append("Salesforce match confirmed by name review")
    if not cat:
        flags.append("No customer type in Sage: Customer Category missing")
    if not last:
        flags.append("No invoice in Sage")

    a = {k: ["", ""] for k in ADDED}
    A = lambda k, v, src="sage": a.__setitem__(k, [v, src if v else ""])
    # Open items left after the 2026-10-27 decisions.
    qc = (["Category missing"] if not cat else []) + \
         (["New NetSuite term"] if c["Terms"][0] and c["Terms"][0] not in TERMS_LIST else [])
    A("Question Categories", "; ".join(qc), "rule")
    A("Sage Customer ID", cid)
    if m:
        A("Salesforce Account ID", id18(m["Account ID"]), "sfdc" if how in ("exact", "confirmed") else "prop")
    A("Other Tax ID", other_tax)
    reseller_emails = split_emails(r["billto_email"]) if billto else []
    if billto:
        # Sage writes the bill-to as "Contact, Company"; the company is the reseller, the person its contact (2026-10-28).
        company, contact = r["billto_company"].strip(), r["billto_attention"].strip()
        if re.match(r"(Inc|LLC|Ltd|Corp)\b\.?,\s+", company):  # "Click-Into, Inc., Click-Into Inc" split at the wrong comma
            company, contact = re.sub(r"^(Inc|LLC|Ltd|Corp)\b\.?,\s+", "", company), ""
        if norm(company).startswith(norm(contact)):
            contact = ""  # the contact line repeats the company name
        addr = ", ".join(x.strip(" ,") for x in [r["billto_line1"], r["billto_line2"], r["billto_citystatezip_country"]] if x.strip(" ,"))
        A("Billed To (Reseller)", company)
        A("Reseller Contact", contact or RESELLER_CONTACT.get(cid, ""))
        A("Reseller Address", re.sub(r"\s*,(\s*,)+", ",", addr))
        # Billed through a reseller (not the customer's own billing entity): the reseller's addresses Sage holds on the
        # customer move to Reseller Invoice Email, since invoices go to the reseller (2026-10-28).
        squashed = norm(r["Customer name"]).replace(" ", "")
        own_entity = bool(set(norm(company).split()) & set(norm(r["Customer name"]).split()))
        rdomains = {e.split("@")[1].lower() for e in reseller_emails}
        rwords = set(norm(company).split())
        def is_reseller(e):
            d = e.split("@")[1].lower()
            labels = [x for x in d.split(".")[:-1] if x not in ("com", "co", "gov", "org", "net", "ac", "edu", "email")]
            root = labels[-1] if labels else d
            mine_ = root in squashed or (len(squashed) > 3 and squashed in root)  # the customer's own domain
            return not own_entity and not mine_ and (d in rdomains or root in rwords)
        moved = [e for e in [inv] + more if e and is_reseller(e)]
        if moved:
            mine = [e for e in [inv] + more if e and e not in moved]
            ap_mine = [e for e in mine if AP.search(e.split("@")[0])]
            inv = (ap_mine or mine or [""])[0]
            more = [e for e in mine if e != inv]
            c["Customer Invoice Email"] = [inv, "sage" if inv else ""]
            reseller_emails += [e for e in moved if e.lower() not in {x.lower() for x in reseller_emails}]
            flags.append("Reseller's email moved from the customer's emails to Reseller Invoice Email: " + ", ".join(moved))
        A("Reseller Invoice Email", "; ".join(reseller_emails), "sage" if not moved else "rule")
    A("Additional Emails", "; ".join(more))
    p = partners.get(norm(r["Customer name"]))
    if not p and m:
        p = partners.get(norm(m["Account Name"]))
    if p:
        A("Salesforce Partners", "; ".join(sorted(p)), "sfdc")
    added = [a[k] for k in ADDED]
    review = [r["Customer type"], r["Term"], last.isoformat() if last else "", f"{bal:,.2f}" if bal else "",
              (m["Account Name"] + (" (likely)" if how == "likely" else " (confirmed)" if how == "confirmed" else "")) if m else ""]
    out.append({"scope": bool(in_scope), "cells": [c[k] for k in COLS] + added, "review": review, "flags": flags})

# Subnet IDs are a key identifier: one NetSuite customer per Subnet account. Where several Sage records matched the same
# Salesforce account and that company has several Subnet accounts in Salesforce, Sage cannot tell which record is which
# Subnet account, so Subnet ID and Salesforce Account ID are left to assign and the records are not merged.
EXTRA_SUBNET_GROUP = {"C-00333": "L3Harris Technologies, Inc."}  # L3 Technologies, L3Harris's name before 2019
SAI, SNI, QI0 = len(COLS) + ADDED.index("Salesforce Account ID"), COLS.index("Subnet ID"), len(COLS)
base = lambda n: re.sub(r"\s*(\(\d+\)|-\d+)$", "", n).strip().lower()
family = {}
for a in accounts:
    family.setdefault(base(a["Account Name"]), []).append(a)
hits = {}
for x in out:
    if x["cells"][SAI][0]:
        hits.setdefault(x["cells"][SAI][0][:15], []).append(x)
for x in out:
    sid = x["cells"][len(COLS) + ADDED.index("Sage Customer ID")][0]
    acct = by_id.get(x["cells"][SAI][0][:15]) if x["cells"][SAI][0] else None
    fam = family.get(base(acct["Account Name"])) if acct else family.get(base(EXTRA_SUBNET_GROUP.get(sid, "")))
    if not fam:
        continue
    subnets = [a for a in fam if a["Subnet Account Id"]]
    shared = acct and len(hits.get(acct["Account ID"], [])) > 1
    if len({a["Subnet Account Id"] for a in subnets}) > 1 and (shared or sid in EXTRA_SUBNET_GROUP):
        x["subnet_choices"] = "; ".join(f"{a['Subnet Account Id']} {a['Subnet Account Name']} ({id18(a['Account ID'])})" for a in subnets)
        x["cells"][SNI] = ["", "miss"]
        x["cells"][SAI] = ["", ""]
        q = [p for p in x["cells"][QI0][0].split("; ") if p] + ["Subnet ID to assign"]
        x["cells"][QI0] = ["; ".join(q), "rule"]
        x["flags"] = [f for f in x["flags"] if not f.startswith("Same Salesforce account")]
        x["cells"][len(COLS) + ADDED.index("Duplicate Action")] = ["Keep: separate Subnet accounts, Subnet ID to assign", "rule"]
    x["review"].append(x.get("subnet_choices", ""))
# Subnet assignments, chronological: the earlier Sage record goes with the earlier Subnet account (Anthony, 2026-10-26).
# L3Harris has three Sage records and five Subnet accounts; its assignment is proposed, not confirmed.
# L3Harris confirmed by Nisha from the Sage contracts (Slack, 2026-10-27): C-00333 holds three contracts, one per Subnet
# account, so it is split into three NetSuite customers to keep one Subnet ID per customer.
SUBNET_ASSIGN = {"C-00103": ("348", "rule"), "C-00462": ("879", "rule"), "C-00371": ("755", "rule"),
                 "C-00592": ("1067", "rule"), "C-00241": ("537", "rule"), "C-00542": ("998", "rule"),
                 "C-00333": ("695", "rule"), "C-00385": ("784", "rule"), "C-00562": ("1026", "rule")}
L3_CONTRACT = {"695": "CN-SO0548", "716": "CN-SO0565", "720": "CN-SO0603", "784": "CN-000160", "1026": "CN-000350"}
L3_SPLIT = [("716", "CN-SO0565"), ("720", "CN-SO0603")]  # new customers split from C-00333
by_subnet = {a["Subnet Account Id"]: a for a in accounts if a["Subnet Account Id"]}
for x in out:
    sid = x["cells"][len(COLS) + ADDED.index("Sage Customer ID")][0]
    if sid in SUBNET_ASSIGN:
        sn, how2 = SUBNET_ASSIGN[sid]
        x["cells"][SNI] = [sn, how2]
        x["cells"][SAI] = [id18(by_subnet[sn]["Account ID"]), how2]
        if how2 == "rule":
            q = [p for p in x["cells"][QI0][0].split("; ") if p and p != "Subnet ID to assign"]
            x["cells"][QI0] = ["; ".join(q), "rule" if q else ""]
            x["cells"][len(COLS) + ADDED.index("Duplicate Action")] = ["Keep: separate Subnet account", "rule"]
            x.pop("subnet_choices", None)
            if len(x["review"]) > len(REVIEW):
                x["review"][len(REVIEW)] = ""
        else:
            x["flags"].append("Subnet ID proposed by date, confirm")
        if sn in L3_CONTRACT:
            x["flags"].append(f"Subnet ID {sn} confirmed by Nisha from Sage contract {L3_CONTRACT[sn]}, 2026-10-27")
for x in out:
    if len(x["review"]) < len(REVIEW) + 1:
        x["review"].append("")
REVIEW.append("Possible Subnet accounts")

# L3Harris split: two new customers for the Subnet accounts billed on C-00333, with the same bill-to (TVAR Solutions),
# numbered after the highest Sage C-#####. Their contracts sit under C-00333 in Sage and move to them on load.
SCI0 = len(COLS) + ADDED.index("Sage Customer ID")
src333 = next(x for x in out if x["cells"][SCI0][0] == "C-00333")
for n_split, (sn, contract) in enumerate(L3_SPLIT, 1):
    x = json.loads(json.dumps(src333))
    new_id = f"C-{nxt:05d}"
    nxt += 1
    x["cells"][COLS.index("Customer ID")] = [new_id, "rule"]
    x["cells"][COLS.index("External ID")] = [new_id, "rule"]
    x["cells"][SNI] = [sn, "rule"]
    x["cells"][SAI] = [id18(by_subnet[sn]["Account ID"]), "rule"]
    x["cells"][COLS.index("Company Name")] = [f"{src333['cells'][COLS.index('Company Name')][0]} -{n_split:02d}", "rule"]
    x["cells"][SCI0] = ["", ""]
    x["cells"][len(COLS) + ADDED.index("Duplicate Action")] = [f"New: split from Sage C-00333 for Subnet {sn}", "rule"]
    x["review"] = [x["review"][0], x["review"][1], "", "", by_subnet[sn]["Account Name"]] + [""] * (len(x["review"]) - 5)
    x["flags"] = [f"New customer split from Sage C-00333 (Nisha, 2026-10-27): Subnet account {sn}, Sage contract {contract} "
                  f"to be assigned to this customer on load", "Company Name is C-00333's with a -01 or -02 suffix (Anthony, 2026-10-27)"]
    out.append(x)

# Order: open items (each by name), then everyone else by Customer ID.
QI = len(COLS)
RANK = ["Category missing", "New NetSuite term"]
def order(x):
    q = x["cells"][QI][0]
    r = min((RANK.index(p) for p in q.split("; ") if p in RANK), default=len(RANK))
    return (r, x["cells"][3][0].lower() if q else x["cells"][2][0])
out.sort(key=order)

# Flag Sage customers that matched the same Salesforce account.
SFI = len(COLS) + ADDED.index("Salesforce Account ID")
seen = {}
for x in out:
    e = x["cells"][SFI][0].lower()
    if e:
        seen.setdefault(e, []).append(x["cells"][2][0])
for x in out:
    ids = seen.get(x["cells"][SFI][0].lower(), [])
    if len(ids) > 1:
        x["flags"].append("Same Salesforce account as " + ", ".join(i for i in ids if i != x["cells"][2][0]))

# Duplicates (proposed): one customer per company. Keep the one invoiced most recently; if neither was invoiced,
# the one with more data, then the lower ID. Keep both when both were invoiced from different countries.
CI, CN, LI = COLS.index("Customer ID"), COLS.index("Country"), REVIEW.index("Last invoice")
DA = len(COLS) + ADDED.index("Duplicate Action")
byid = {x["cells"][CI][0]: x for x in out}
parent = {}
def find(i):
    while parent.get(i, i) != i:
        i = parent[i]
    return i
for x in out:
    for f in x["flags"]:
        mm = re.match(r"(?:Duplicate name|Similar name): (.*)|Same Salesforce account as (.*)", f)
        if mm:
            for o in (mm.group(1) or mm.group(2)).split(", "):
                if o in byid:
                    parent[find(o)] = find(x["cells"][CI][0])
# Duplicates found by shared email domain and confirmed by Anthony on 2026-10-26 (same company, different name).
for a, b in [("C-00575", "C-00640"), ("C-00039", "C-00405"), ("C-00049", "C-00405"), ("C-00465", "C-00204"), ("C-00629", "C-00481")]:
    parent[find(a)] = find(b)
groups = {}
for i in byid:
    groups.setdefault(find(i), []).append(i)
dup_groups = 0
for g in (g for g in groups.values() if len(g) > 1):
    xs = [byid[i] for i in g]
    if any("Subnet ID to assign" in x["cells"][QI][0] for x in xs):
        for x in xs:
            x["cells"][DA] = ["Keep: separate Subnet accounts, Subnet ID to assign", "rule"]
        continue
    if len({x["cells"][SNI][0] for x in xs if x["cells"][SNI][0]}) > 1:
        for x in xs:
            x["cells"][DA] = ["Keep: separate Subnet account", "rule"]
        continue
    if all(x["review"][LI] for x in xs) and len({x["cells"][CN][0] for x in xs}) > 1:
        for x in xs:
            x["cells"][DA] = ["Keep: separate entity, invoiced from different countries", "prop"]
        continue
    dup_groups += 1
    keep = max(xs, key=lambda x: (x["review"][LI], sum(bool(c[0]) for c in x["cells"]), -int(re.sub(r"\D", "", x["cells"][CI][0]))))
    kid = keep["cells"][CI][0]
    others = [x["cells"][CI][0] for x in xs if x is not keep]
    keep["cells"][DA] = ["Keep, merges " + ", ".join(others), "rule"]
    # Carry the merged records across: their Sage IDs, their addresses as second and third addresses, their emails.
    MI, A2, A3 = (len(COLS) + ADDED.index(k) for k in ("Merged Sage IDs", "Second Address", "Third Address"))
    SCI = len(COLS) + ADDED.index("Sage Customer ID")
    AE = len(COLS) + ADDED.index("Additional Emails")
    keep["cells"][MI] = [", ".join(x["cells"][SCI][0] for x in xs if x is not keep), "rule"]
    def one_line(x):
        parts = [x["cells"][COLS.index(k)][0] for k in ("Attention", "Address 1", "Address 2", "City", "Province/State", "Postal Code/Zip", "Country")]
        return ", ".join(p for p in parts if p)
    sq = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
    def parts(x):
        return {sq(x["cells"][COLS.index(k)][0]) for k in ("Address 1", "Address 2", "City", "Province/State", "Postal Code/Zip", "Country")} - {""}
    kept_parts = [parts(keep)]
    seen_addr = {sq(one_line(keep))}
    extra = []
    for x in sorted((x for x in xs if x is not keep), key=lambda x: x["review"][LI], reverse=True):
        line = one_line(x)
        if any(parts(x) <= p for p in kept_parts):
            continue  # same address, at most missing a field or the contact name
        kept_parts.append(parts(x))
        if line and sq(line) not in seen_addr:
            seen_addr.add(sq(line))
            via = ", address from Salesforce" if x["cells"][COLS.index("Address 1")][1] == "sfdc" else ""
            extra.append(f"{line} (from {x['cells'][SCI][0]}{via})")
    for col, v in zip((A2, A3), extra):
        keep["cells"][col] = [v, "rule"]
    if len(extra) > 2:
        keep["flags"].append("More than three addresses: " + " | ".join(extra[2:]))
    have = {e.lower() for e in [keep["cells"][COLS.index("Customer Invoice Email")][0]] + keep["cells"][AE][0].split("; ") if e}
    more = [e for x in xs if x is not keep for e in [x["cells"][COLS.index("Customer Invoice Email")][0]] + x["cells"][AE][0].split("; ")
            if e and e.lower() not in have and not have.add(e.lower())]
    if more:
        keep["cells"][AE] = ["; ".join(p for p in [keep["cells"][AE][0]] + more if p), keep["cells"][AE][1] or "rule"]
    if not keep["cells"][SNI][0]:
        donor = [x for x in xs if x is not keep and x["cells"][SNI][0]]
        if len(donor) == 1:
            keep["cells"][SNI] = [donor[0]["cells"][SNI][0], "rule"]
            keep["cells"][SAI] = [donor[0]["cells"][SAI][0], "rule"]
            keep["flags"].append(f"Subnet ID from merged {donor[0]['cells'][SCI][0]}")
    for x in xs:
        if x is not keep:
            x["cells"][DA] = ["Merge into " + kid, "rule"]

# Final pass over the loaded rows (2026-10-28).
CI_, NI_, DA_ = COLS.index("Customer ID"), COLS.index("Company Name"), len(COLS) + ADDED.index("Duplicate Action")
loaded = [x for x in out if not x["cells"][DA_][0].startswith("Merge into")]
# Customers with the same name and different Subnet IDs get -01, -02 in Customer ID order, as the L3Harris split did.
same_name = {}
for x in loaded:
    same_name.setdefault(x["cells"][NI_][0], []).append(x)
for name, xs in same_name.items():
    if len(xs) > 1 and len({x["cells"][SNI][0] for x in xs}) == len(xs) and all(x["cells"][SNI][0] for x in xs):
        for n_, x in enumerate(sorted(xs, key=lambda x: x["cells"][CI_][0]), 1):
            x["cells"][NI_] = [f"{name} -{n_:02d}", "rule"]
            x["flags"].append(f"Name suffix -{n_:02d}: {len(xs)} customers named {name}, each its own Subnet account")
# Attention that only repeats the company's own name is removed: the invoice would read "Attn: X / X" (2026-10-28).
ATI = COLS.index("Attention")
for x in out:
    att = x["cells"][ATI][0]
    if att and norm(att) == norm(re.sub(r" -0\d$", "", x["cells"][NI_][0])):
        x["cells"][ATI] = ["", ""]
        x["flags"].append(f"Attention removed: it repeated the company name ({att})")
# Parent Company names the parent as it is in this load, and Parent Customer ID gives its Customer ID.
PCI = len(COLS) + ADDED.index("Parent Customer ID")
for x in loaded:
    psf = parent_sf.get(x["cells"][SCI0][0])
    if not x["cells"][COLS.index("Parent Company")][0] or not psf:
        continue
    pname = norm(by_id[psf]["Account Name"]) if psf in by_id else ""
    par = [y for y in loaded if y["cells"][SAI][0][:15] == psf] or \
          [y for y in loaded if norm(re.sub(r" -0\d$", "", y["cells"][NI_][0])) == pname]
    if len(par) == 1:
        if par[0]["cells"][NI_][0] != x["cells"][COLS.index("Parent Company")][0]:
            x["flags"].append(f"Parent Company written as the parent's name in this load (Salesforce: {x['cells'][COLS.index('Parent Company')][0]})")
        x["cells"][COLS.index("Parent Company")] = [par[0]["cells"][NI_][0], "rule"]
        x["cells"][PCI] = [par[0]["cells"][CI_][0], "rule"]
    else:
        x["flags"].append("Parent Company not found in this load")
# US states as two-letter codes; Canadian provinces by full name (2026-10-28).
US_CODE = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
           "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
           "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
           "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
           "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
           "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
           "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
           "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
           "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}
CA_NAME = {"AB": "Alberta", "BC": "British Columbia", "MB": "Manitoba", "NB": "New Brunswick", "NL": "Newfoundland and Labrador",
           "NS": "Nova Scotia", "NT": "Northwest Territories", "NU": "Nunavut", "ON": "Ontario", "PE": "Prince Edward Island",
           "QC": "Quebec", "SK": "Saskatchewan", "YT": "Yukon"}
# Country names as NetSuite lists them for CSV import (Country enumeration, Oracle help, 2026-10-28).
NS_COUNTRY = {"Korea, Republic of": "Korea (the Republic of)", "Moldova, Republic of": "Moldova (the Republic of)",
              "Congo, Democratic Republic": "Congo (the Democratic Republic of the)", "Cape Verde": "Cabo Verde",
              "Czech Republic": "Czechia", "Curaçao": "Curacao", "Turkey": "Türkiye", "Vietnam": "Viet Nam",
              "Taiwan": "Taiwan (Province of China)", "Palestinian Territory, Occupied": "Palestine (State of)", "USA": "United States"}
STI, CTI = COLS.index("Province/State"), COLS.index("Country")
for x in out:
    st, ct = x["cells"][STI][0], x["cells"][CTI][0]
    if ct == "United States" and st in US_CODE:
        x["cells"][STI] = [US_CODE[st], "rule"]
    elif ct == "Canada" and st.upper() in CA_NAME:
        x["cells"][STI] = [CA_NAME[st.upper()], "rule"]
    if ct in NS_COUNTRY:
        x["cells"][CTI] = [NS_COUNTRY[ct], x["cells"][CTI][1]]
    pz = x["cells"][COLS.index("Postal Code/Zip")][0]
    if re.match(r"[A-Z]{1,2}\s?-\s?\d", pz):  # country prefix on a postal code (MD-2012, L-1748)
        x["cells"][COLS.index("Postal Code/Zip")] = [re.sub(r"^[A-Z]{1,2}\s?-\s?", "", pz), "rule"]
        x["flags"].append(f"Postal code country prefix removed: was {pz}")

# Bridge from the first Sage export (active customers) to the customers in the load.
onetime = [(i, lst[i]["Customer name"]) for i in ONETIME]
inactive = [(x["Customer ID"], x["Customer name"]) for x in sage if x["Status"] != "Active"]
merged_n = sum(1 for x in out if x["cells"][DA][0].startswith("Merge into"))
split_n = sum(1 for x in out if x["cells"][DA][0].startswith("New: split"))
bridge = {"first": len(lst), "onetime": onetime, "report": len(sage), "inactive": inactive, "excluded": excluded,
          "rows": len(out), "merged": merged_n, "kept": dup_groups, "split": split_n, "load": len(out) - merged_n}

data = {"cols": COLS + ADDED, "required": sorted(REQUIRED), "review": REVIEW, "rows": out, "built": TODAY.isoformat(),
        "renumber": renumber, "new_terms": sorted(new_terms.items(), key=lambda kv: int(kv[0].split()[1])),
        "research_terms": sorted(research.items(), key=lambda kv: -kv[1]),
        "dup_groups": dup_groups, "bridge": bridge, "parents_dropped": sum(parents_dropped.values()), "parents_dropped_n": len(parents_dropped), "last_std": f"C-{max(std):05d}", "next_id": f"C-{nxt:05d}"}
with open("data/customer-load-draft.csv", "w", newline="", encoding="utf-8-sig") as o:
    w = csv.writer(o)
    w.writerow(COLS + ADDED + ["_src:" + c for c in COLS + ADDED])
    for x in out:
        w.writerow([c[0] for c in x["cells"]] + [c[1] for c in x["cells"]])
with open("data/customer-load.csv", "w", newline="", encoding="utf-8-sig") as o:
    w = csv.writer(o)
    w.writerow(COLS + ADDED)
    for x in out:
        if not x["cells"][DA][0].startswith("Merge into"):
            w.writerow([c[0] for c in x["cells"]])
tpl = open("tools/review-template.html", encoding="utf-8").read()
open("data/customer-review.html", "w", encoding="utf-8").write(
    tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")))
SM = REVIEW.index("Salesforce match")
matched = {norm(re.sub(r" \((likely|confirmed)\)$", "", x["review"][SM])) for x in out if x["review"][SM]}
print(f"{len(out)} customers; Salesforce exact {sum(1 for x in out if x['review'][SM] and '(likely)' not in x['review'][SM])}, likely {sum('(likely)' in x['review'][SM] for x in out)}, none {sum(not x['review'][SM] for x in out)}")
print(f"Salesforce accounts with no Sage customer: {sum(1 for a in accounts if norm(a['Account Name']) not in matched)} of {len(accounts)}")
