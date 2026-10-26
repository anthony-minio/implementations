# Open questions

1. **Deferred Revenue account.** COA Draft v1 has 23100 Deferred Revenue - ST, 23200 Deferred Revenue - LT, and under 23200: 23210 Deferred Revenue Unbilled, 23220 Deferred Revenue Billed, 23230 Deferred Revenue Paid. Which one do the items post to? An item takes one account, so NetSuite does not split short and long term on the transaction. Proposed: post to 23100 and reclass the part beyond 12 months to 23200 with a period-end journal entry. Unbilled, Billed and Paid look carried over from Sage's contract revenue setup; confirm whether they are still needed.
2. **Account format.** The CSV uses number and name, such as `41100 License Revenue`. Confirm on a test import that NetSuite matches it; child accounts may need the full path.
3. **OEM license.** Does AIStor OEM License use the same accounts and rule as the direct licenses?
4. **Platform training subscription.** Is it recognized like the live trainings or like a subscription?
5. **Base Price.** Do these items have list prices?
6. **Classes in production.** License, Support, Training and Professional Services must exist in production before this load.
7. **Not in this load.** The Items tab lists Surcharge Fee for Marketplace and Reseller Margin (presented as a discount) as TBD. No Professional Services SKUs yet; 42100 Professional Services Revenue is ready when there are.
8. **Template header.** The template spells `Revenue Recogition Rule`. Kept as is; it only needs to match when mapping the import.
