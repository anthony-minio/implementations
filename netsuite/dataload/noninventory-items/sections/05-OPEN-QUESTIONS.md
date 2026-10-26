# Open questions

1. **Department.** 4000 Cost of Revenue (COR) is a cost department and a parent with no people. Coding revenue to it puts revenue and cost of revenue in one department on department reports. Options: leave Department blank on the items (Class already carries the revenue type), use 4000, or use 2000 Sales.
2. **Deferred Revenue account.** COA Draft v1 has 23100 Deferred Revenue - ST, 23200 Deferred Revenue - LT, and under 23200: 23210 Deferred Revenue Unbilled, 23220 Deferred Revenue Billed, 23230 Deferred Revenue Paid. Which one do the items post to?
3. **Account format.** The CSV uses number and name, such as `41100 License Revenue`. Confirm on a test import that NetSuite matches it; child accounts may need the full path.
4. **OEM license.** Does AIStor OEM License use the same accounts and rule as the direct licenses?
5. **Platform training subscription.** Is it recognized like the live trainings or like a subscription?
6. **Base Price.** Do these items have list prices?
7. **Classes in production.** License, Support, Training and Professional Services must exist in production before this load.
8. **Not in this load.** The Items tab lists Surcharge Fee for Marketplace and Reseller Margin (presented as a discount) as TBD. No Professional Services SKUs yet; 42100 Professional Services Revenue is ready when there are.
9. **Template header.** The template spells `Revenue Recogition Rule`. Kept as is; it only needs to match when mapping the import.
