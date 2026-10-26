# Open questions

1. **Account format.** The CSV uses number and name, such as `41100 License Revenue`. Confirm on a test import that NetSuite matches it; child accounts may need the full path.
2. **OEM license.** Does AIStor OEM License use the same accounts and rule as the direct licenses?
3. **Platform training subscription.** Is it recognized like the live trainings or like a subscription?
4. **Base Price.** Do these items have list prices? How AIStor and MemKV licenses are measured (for example per TiB) is not known or may not be standard; the license descriptions leave the unit out for now.
5. **Classes in production.** License, Support, Training and Professional Services must exist in production before this load.
6. **Not in this load.** The Items tab lists Surcharge Fee for Marketplace and Reseller Margin (presented as a discount) as TBD. No Professional Services SKUs yet; 42100 Professional Services Revenue is ready when there are.
7. **Template header.** The template spells `Revenue Recogition Rule`. Kept as is; it only needs to match when mapping the import.
8. **Long-term deferred revenue.** Items post to 23100 Deferred Revenue - ST. The part earned more than 12 months out is reclassed to 23200 Deferred Revenue - LT by a period-end journal entry. Confirm the Unbilled, Billed and Paid accounts under 23200 are still needed.
9. **Show Display Name with Item Codes.** Setup > Company > General Preferences. Shows code and name together in item fields. If turned on, later CSV imports that reference items need the display name too, or fail with Invalid Parent Reference Key. Decide before the sales order and invoice loads.
