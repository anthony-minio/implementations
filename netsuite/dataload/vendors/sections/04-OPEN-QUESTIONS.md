# Open questions

1. **Scope.** Load all 1,770 active vendors as with customers, or only vendors with activity since 2024-10-26 (563) plus any with an open balance?
2. **Ramp as the vendor master.** If Ramp syncs vendors to NetSuite, vendors paid through Ramp may be created by the sync. Does the load cover all vendors, or only those outside Ramp?
3. **Credit card merchants.** 427 vendors of type Credit Cards, 418 never billed. Load or leave out?
4. **MinIO employees.** 136 vendors of type MinIO employee, used for reimbursements. NetSuite usually reimburses through employee records. Load as vendors or leave out?
5. **AR resellers.** 127 resellers set up as vendors, 125 never billed. Load only those MinIO pays?
6. **Ramp-only vendors.** 27 Ramp vendors have no Sage vendor. Add them to the load?
7. **Tax IDs.** Sage and Ramp hold tax IDs and Ramp holds W-9 classification. Put Tax ID in the load file, or have it entered separately to keep it out of circulated files?
8. **Subsidiary.** Vendors with INR or SGD currency: MinIO Pvt. Ltd. or MinIO Singapore Pte. Ltd.?
9. **Vendor ID numbering and duplicates.** Apply the customer rules: keep V-#####, renumber V##### and RMP_#, merge duplicates into the most recently used record, NetSuite auto-numbers new vendors from the next number.
10. **Default Payables Account.** 20100 Accounts Payable - Trade for every vendor?
