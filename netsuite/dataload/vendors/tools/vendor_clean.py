# Formatting rules for the vendor load, the same as the customer load (decided 2026-10-27 and 2026-10-28):
# phones, NetSuite country names, US state codes, Canadian province names, postal codes, address cleanup.
# Used by build_review.py: clean(c, flags, sid) edits one vendor's template fields in place.
import re
import phonenumbers as pn

# Phone: US numbers as (999) 999-9999, all others in international format (+44 20 7885 8888).
# NetSuite phone fields hold 21 characters; extensions are written " x123".
REGION = {"United States": "US", "Canada": "CA", "Germany": "DE", "France": "FR", "Saudi Arabia": "SA",
          "United Kingdom": "GB", "India": "IN", "United Arab Emirates": "AE", "Turkey": "TR", "Sweden": "SE",
          "Singapore": "SG", "Poland": "PL", "Japan": "JP", "Indonesia": "ID", "Georgia": "GE", "Mexico": "MX",
          "Taiwan": "TW", "Vietnam": "VN", "Korea, Republic of": "KR", "Türkiye": "TR"}

def phone(raw, country):
    """Return (number, note). number is '' when the source value is not a valid phone number."""
    s = raw.strip().lstrip("'").strip()
    ext = ""
    m = re.search(r"\s*(?:x|ext\.?|extension)\s*:?\s*(\d+)$", s, re.I)
    if m:
        ext, s = m.group(1), s[:m.start()]
    s = re.sub(r"^\+\s+", "+", re.sub(r"\(0\)", "", s)).strip()
    s = re.sub(r"^\+{2,}", "+", s)
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
        n = p(s, "US")
    elif reg in ("US", "CA", None) and (len(digits) == 10 or len(digits) == 11 and digits[0] == "1"):
        n = p(digits, reg or "US")  # ten digits with no country: a North American number
    elif s[:1] in "0(":
        n = p(s, reg) if reg else None  # national format with a trunk prefix
    else:
        n = p("+" + digits) or (p(s, reg) if reg else None)  # digits that start with the country code
    if not n:
        return "", f"Phone left out: {raw!r} is not a valid phone number"
    nreg = pn.region_code_for_number(n)
    us = nreg == "US" and reg in ("US", None)  # a US number for a vendor outside the US is written internationally
    out = pn.format_number(n, pn.PhoneNumberFormat.NATIONAL if us else pn.PhoneNumberFormat.INTERNATIONAL)
    if ext:
        out += f" x{ext}"
        if len(out) > 21:
            out = pn.format_number(n, pn.PhoneNumberFormat.E164) + f" x{ext}"
    note = f"Phone is a {nreg} number (+{n.country_code}); the address is in {country}" if reg and nreg != reg else ""
    return out, note

# Country names as NetSuite lists them for CSV import.
NS_COUNTRY = {"Korea, Republic of": "Korea (the Republic of)", "Turkey": "Türkiye", "Taiwan": "Taiwan (Province of China)",
              "Vietnam": "Viet Nam", "Czech Republic": "Czechia", "Moldova, Republic of": "Moldova (the Republic of)"}
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

# Address fields corrected by hand, each from the Sage address itself (2026-10-28). Tax numbers written in the
# address move to Tax ID, which is blank for each of these vendors.
ADDRESS_FIX = {
    "V-00747": ({"address1_line2": "", "address1_city": "Little Silver", "address1_state": "NJ"},
                "City was in Address 2 and the state in City (New Jersey, with TX as the state); ZIP 07739 is Little Silver, NJ"),
    "V00073": ({"address2_line2": "", "address2_city": "St. Louis"}, "Remit-to city was in Address 2"),
    "V-01420": ({"address1_state": "VA"}, "Falls Church and ZIP 22046 are in Virginia; Sage had VT"),
    "V-01476": ({"address1_city": "Singapore", "address1_zipCode": "018983"}, "Postal code was 018983 SGP; city added"),
    "V-01555": ({"address1_line2": "", "address1_city": "Sinsheim", "address1_zipCode": "74889"},
                "Postal code and city were in Address 2 (74889 Sinsheim)"),
    "V-01031": ({"address1_line1": "10F, No.516, Sec. 1", "address1_line2": "Neihu Rd.", "address1_city": "Taipei",
                 "taxIdNum": "16428796"},
                "Address 1 started with the Taiwan business number (Unified No: 16428796), moved to Tax ID"),
    "V-01515": ({"address1_line1": "İSMETPAŞA", "address1_line2": "BAYRAMPAŞA", "address1_city": "İSTANBUL",
                 "address1_zipCode": "34040", "address1_country": "Turkey"},
                "The whole Istanbul address was in Address 1 and the country was United States"),
    "V-01310": ({"address1_line1": "ul. Zeusa 41", "address1_line2": "", "address1_city": "Warsaw", "address1_zipCode": "01-497"},
                "Address 1 began with a garbled title and the company name (Prezes Zarz#du -- OSEC Sp. z o.o.), removed; "
                "the street number 41 had run into the postal code (4101-497 is ul. Zeusa 41, 01-497); Warszawa repeated in Address 2"),
    "V-00737": ({"address1_line2": "Jl. Casablanca Raya Kav. 88", "taxIdNum": "81.483.842.1-015.000"},
                "Address 2 held the Indonesian tax number (NPWP 81.483.842.1-015.000), moved to Tax ID"),
    "V-01077": ({"address1_city": "Menlo Park"}, "City repeated the street; ZIP 94025 is Menlo Park"),
    "V-01444": ({"address1_zipCode": ""}, "Postal code held the city (Manhattan Beach); left blank"),
    "V-01084": ({"address1_city": "Hamamatsu", "address1_state": "Shizuoka"},
                "City held the prefecture and State held it in Japanese (静岡県); the street (浜松市...) is in Hamamatsu"),
    "V-01514": ({"address1_city": "Dubai", "address1_state": ""}, "City was in State"),
    "V-01513": ({"address1_city": "Dubai", "address1_state": ""}, "City was in State"),
    "V-00727": ({"address1_line1": "1000 Toa Payoh North, Level 2", "address1_line2": "News Centre", "address1_city": "Singapore",
                 "taxIdNum": "197400503M"},
                "Address 1 held the Singapore company registration number (Co. Reg. 197400503M), moved to Tax ID; the street moved up"),
    "V-00544": ({"address1_city": "New York"}, "City blank; ZIP 10036 is New York, NY"),
    "V-00453": ({"address1_line1": "PO Box 101822", "address1_line2": ""}, "Address 1 repeated the company name"),
    "V-01055": ({"address1_attention": "Accounts Payable", "address1_line1": "1 WORLD WIDE WAY", "address1_line2": ""},
                "Address 1 held the attention line (Attn: Accounts Payable)"),
    "V00143": ({"address1_line2": "", "address1_city": "FT. Myers"}, "City was in Address 2"),
}

ADDR = [f"address{n}_{k}" for n in (1, 2) for k in ("attention", "line1", "line2", "city", "state", "zipCode", "country")]

def clean(c, flags, sid):
    """Apply the formatting rules to one vendor's fields ({field: [value, source]}) and note each change in flags."""
    # The country only says where a phone number is from when the vendor has an address; Sage defaults it to United States.
    country0 = c["address1_country"][0] if c["address1_line1"][0] or sid in ADDRESS_FIX else None
    for f in ("phone", "fax"):
        v = c[f][0]
        if v:
            out, note = phone(v, country0)
            if out != v:
                c[f] = [out, "rule" if out else ""]
                flags.append(note if not out else f"{f.title()} formatted from {v!r}" + (f"; {note}" if note else ""))
            elif note:
                flags.append(note)
    if sid in ADDRESS_FIX:
        fix, why = ADDRESS_FIX[sid]
        for f, v in fix.items():
            c[f] = [v, "rule" if v else ""]
        flags.append(f"Address fields corrected: {why}")
    for f in ADDR:  # stray commas and spaces from Sage's print layout
        v = c[f][0]
        t = re.sub(r"\s+", " ", v).strip(" ,")
        if t != v:
            c[f] = [t, c[f][1] if t else ""]
    for n in (1, 2):
        a = lambda k: f"address{n}_{k}"
        ct, st, zp = c[a("country")][0], c[a("state")][0], c[a("zipCode")][0]
        if ct in NS_COUNTRY:
            c[a("country")] = [NS_COUNTRY[ct], c[a("country")][1]]
        if not c[a("line1")][0] and not c[a("city")][0]:
            if ct == "United States":  # Sage's default country, not an address
                c[a("country")] = ["", ""]
                if n == 1:
                    flags.append("Country left blank: no address in Sage, which defaults the country to United States")
            continue
        if ct == "United States" and st in US_CODE:
            c[a("state")] = [US_CODE[st], "rule"]
        if ct == "Canada" and st.upper() in CA_NAME:
            c[a("state")] = [CA_NAME[st.upper()], "rule"]
        if ct == "United States" and re.fullmatch(r"\d{9}", zp):
            c[a("zipCode")] = [f"{zp[:5]}-{zp[5:]}", "rule"]
        if ct == "United States" and re.fullmatch(r"\d{3,4}", zp):
            c[a("zipCode")] = [zp.zfill(5), "rule"]
            flags.append(f"ZIP code leading zero restored: was {zp}")
        if re.match(r"[A-Z]{1,2}\s?-\s?\d", zp):
            c[a("zipCode")] = [re.sub(r"^[A-Z]{1,2}\s?-\s?", "", zp), "rule"]
            flags.append(f"Postal code country prefix removed: was {zp}")
        if ct == "Singapore" and not c[a("city")][0]:
            c[a("city")] = ["Singapore", "rule"]
