# Non-inventory items for sale

Load file: `MINIO_-_Noninventory_for_Sale.csv` (NetSuite template, headers only so far). Record type in the Import Assistant: Items > Non-inventory Item for Sale.

## Columns

| Column | What goes in it | Source / status |
|---|---|---|
| External ID | Unique key per item, used to update the item later instead of creating a duplicate | Convention TBC |
| Item Name | Item name/number. Must be unique | Item list TBC |
| Display Name/Code | Name shown on transactions | Item list TBC |
| Department | Existing NetSuite department, full name as shown in NetSuite | TBC |
| Class | Existing NetSuite class, full name as shown in NetSuite | TBC |
| Subsidiary | Existing NetSuite subsidiary | TBC |
| Include Children | Yes/No: item also available to child subsidiaries | TBC |
| Sales Description | Default description on sales transactions | Item list TBC |
| Base Price | Base Price price level | Price list TBC |
| Income account | Existing account, as shown in NetSuite | Chart of accounts TBC |
| Deferred Revenue account | Existing account, as shown in NetSuite | Chart of accounts TBC |
| Revenue Recogition Rule | Existing revenue recognition rule | Rev rec setup TBC |
| Rev Rec Forecast Rule | Existing revenue recognition rule used for forecasting | Rev rec setup TBC |
| Create Revenue Plans On | When revenue plans are created (for example Revenue Arrangement Creation, Billing, Fulfillment) | TBC |
| Direct Revenue Posting | Yes/No: post revenue directly, skipping revenue arrangements | TBC |
| Can be fulfilled/received | Yes/No | TBC |

Header wording is kept exactly as in the template, including `Revenue Recogition Rule`.

## Load log

| Date | File | Records | Errors | Outcome |
|---|---|---|---|---|
