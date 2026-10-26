# Non-inventory items for sale

Load file: `MINIO_-_Noninventory_for_Sale.csv`. 11 items. External ID, Item Name and Display Name/Code are filled from the item list Anthony provided on 2026-10-26; the other columns are open. Record type in the Import Assistant: Items > Non-inventory Item for Sale.

## Columns

| Column | What goes in it | Source / status |
|---|---|---|
| External ID | Unique key per item, used to update the item later instead of creating a duplicate | Item ID (proposed) |
| Item Name | Item name/number. Must be unique | Item ID (proposed) |
| Display Name/Code | Name shown on transactions | Item name |
| Department | Existing NetSuite department, full name as shown in NetSuite | TBC |
| Class | Existing NetSuite class, full name as shown in NetSuite | TBC |
| Subsidiary | Existing NetSuite subsidiary | TBC |
| Include Children | Yes/No: item also available to child subsidiaries | TBC |
| Sales Description | Default description on sales transactions | TBC. Could repeat the item name |
| Base Price | Base Price price level | Price list TBC |
| Income account | Existing account, as shown in NetSuite | Chart of accounts TBC |
| Deferred Revenue account | Existing account, as shown in NetSuite | Chart of accounts TBC |
| Revenue Recogition Rule | Existing revenue recognition rule | Rev rec setup TBC |
| Rev Rec Forecast Rule | Existing revenue recognition rule used for forecasting | Rev rec setup TBC |
| Create Revenue Plans On | When revenue plans are created (for example Revenue Arrangement Creation, Billing, Fulfillment) | TBC |
| Direct Revenue Posting | Yes/No: post revenue directly, skipping revenue arrangements | TBC |
| Can be fulfilled/received | Yes/No | TBC |

Header wording is kept exactly as in the template, including `Revenue Recogition Rule`.

## Values by item group

The accounting columns are usually the same for every item in a group. Proposed groups, from the item ID prefixes:

| Group | Items | Department | Class | Income account | Deferred Revenue account | Rev rec rule | Base Price |
|---|---|---|---|---|---|---|---|
| Support (`NS-SUPT-`) | 5 SLA tiers | TBC | TBC | TBC | TBC | TBC | TBC |
| Training (`NS-TRAIN-`) | 2 live virtual, 1 platform subscription | TBC | TBC | TBC | TBC | TBC | TBC |
| License (`NS-LIC-`, `NS-OEM-LIC-`) | AIStor, AIStor OEM, MemKV | TBC | TBC | TBC | TBC | TBC | TBC |

Open questions:

- Does the OEM license use the same accounts and rule as the direct licenses?
- Does the platform training subscription follow the live training items or behave like a subscription?
- Base Price: list prices, or leave blank and price on each order?

## Load log

| Date | File | Records | Errors | Outcome |
|---|---|---|---|---|
