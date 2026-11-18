# Mid-life Asset Record

Template `MINIO_FAM_CSVTemplate_Mid-life Asset Record.xlsx`, tab **FAM_Mid-life Asset**. One row per asset.

| **Template column** | **Value** |
|----------------------|-------------------------------------------------------------|
| **Name** | Register Description |
| **Asset Description** | Register Vendor, then the register Comment when it differs from the Description |
| **Quantity** | 1 |
| **Subsidiary** | MinIO, Inc. |
| **Asset Type** | Computer Hardware to Equipment, Lease Improvement to Leasehold Improvements |
| **Asset Status** | Depreciating |
| **Asset Lifetime** | Register useful life in months. FA-076 and FA-082: months done plus months left (question 5) |
| **Asset Original Cost, Asset Current Cost** | Register cost. No write-downs |
| **Residual Value Percentage, Residual Value** | 0 |
| **Depreciation Start Date** | Register Dep Date when it falls in the first month depreciated, else the 1st of that month |
| **Last Depreciation Date** | 2026-10-31 |
| **Last Depreciation Period** | Months depreciated, first month to 2026-10 |
| **Last Depreciation Amount** | 2026-10 depreciation |
| **Current Net Book Value** | Register NBV at 2026-10-31 |

Ref is the row on the register's ALL FA tab (FA-069 is row 69). It is not in the load.

## Equipment

28 assets.

| **Ref** | **Name** | **Lifetime** | **Original Cost** | **Start Date** | **Last Period** | **Last Amount** | **Current NBV** |
|---------|------------------------------|---------:|-------------:|------------|--------:|-----------:|------------:|
| **FA-069** | Ordered Server - 1 Qty S/N: 311625572 - AceleMax NVIDIA GPU HPC | 36 | 319,888.57 | 2023-12-04 | 35 | 8,885.80 | 8,885.79 |
| **FA-070** | Petr Kobalicek: Petr Kobalicek - report \#R004ZpgHK6WQ - Laptop purchase | 36 | 3,537.82 | 2024-02-01 | 33 | 98.27 | 294.82 |
| **FA-071** | Piotr Wyderski: Laptop purchase and 3 Yr Pro Support - DELL Precision 7680 16inch | 36 | 3,694.02 | 2024-02-01 | 33 | 102.61 | 307.84 |
| **FA-072** | 2 Servers for MinIO OPTIMIZED X13SET-G | 36 | 115,785.93 | 2024-02-23 | 33 | 3,216.27 | 9,648.83 |
| **FA-074** | Computers & Equipment | 36 | 6,981.19 | 2024-08-20 | 27 | 193.92 | 1,745.30 |
| **FA-075** | Ordered Server - 1 Qty S/N: MT2413XZ089P - NVIDIA Spectrum-3 SN4700 switch | 36 | 37,789.32 | 2024-09-01 | 26 | 1,049.71 | 10,497.03 |
| **FA-077** | PowerEdge R7615 server | 36 | 118,177.10 | 2024-12-06 | 23 | 3,282.70 | 42,675.06 |
| **FA-078** | PowerEdge R7615 server | 36 | 210,220.56 | 2024-12-10 | 23 | 5,839.46 | 75,912.98 |
| **FA-079** | PowerEdge XE968 server | 36 | 255,032.47 | 2024-12-12 | 23 | 7,084.23 | 92,095.06 |
| **FA-080** | ENGINEERING CC 0349 - December 2024 - Center of Excellence Project | 36 | 6,088.27 | 2024-12-20 | 23 | 169.12 | 2,198.54 |
| **FA-081** | 100GB Switch with 28 cables | 36 | 8,984.28 | 2025-01-01 | 22 | 249.56 | 3,493.89 |
| **FA-083** | Server Technology Smart PRO3X with PIPS | 36 | 5,777.72 | 2025-02-01 | 21 | 160.50 | 2,407.38 |
| **FA-084** | Ordered Server - 18 qty-Nvidia CX-7 NIC Card PCIe 5.0x16 400Gb OSFP 18 qty | 36 | 114,690.77 | 2025-01-22 | 22 | 3,185.85 | 44,601.97 |
| **FA-085** | Ordered Server - 18 qty-Mellanox Support and Warranty 3 yrs for ADPTR-CX7 36 qty | 36 | 12,090.57 | 2025-01-23 | 22 | 335.85 | 4,701.89 |
| **FA-086** | 2- Nvidia Transceiver 400GBE 2- Nvidia Passive Fiber Cable SMF | 36 | 8,873.92 | 2025-02-24 | 21 | 246.49 | 3,697.47 |
| **FA-087** | Hardware order for data center March 2025 | 36 | 10,635.65 | 2025-03-10 | 20 | 295.43 | 4,726.96 |
| **FA-089** | Ali Yaldaz. Macbook Pro M4 Pro 14" 48 GB | 36 | 3,401.66 | 2025-04-02 | 19 | 94.49 | 1,606.34 |
| **FA-090** | Transceiver | 36 | 2,196.18 | 2025-04-24 | 19 | 61.01 | 1,037.08 |
| **FA-091** | Fiber optic jumper cables | 36 | 820.26 | 2025-04-30 | 19 | 22.79 | 387.34 |
| **FA-092** | 192 Storage Cards | 36 | 182,044.80 | 2025-05-01 | 18 | 5,056.80 | 91,022.40 |
| **FA-093** | SUPERMICRO CUST 2XX550 480GB | 36 | 27,250.25 | 2026-03-01 | 8 | 756.95 | 21,194.64 |
| **FA-094** | NVIDIA Spectrum-4 Switch and networking equipment | 36 | 63,995.00 | 2026-05-01 | 6 | 1,777.64 | 53,329.17 |
| **FA-095** | Nvidia CX-7 NIC Card PCIe 5.0x16 400Gb OSFP- warrantly and shipping | 36 | 22,496.90 | 2026-07-01 | 4 | 624.92 | 19,997.24 |
| **FA-096** | NADDOD Technology Inc - September 2026 | 36 | 11,709.23 | 2026-10-01 | 1 | 325.26 | 11,383.97 |
| **FA-097** | Ramp: Kiel Michael Mercado - Laptops are for new hires. 5x MacBooks | 36 | 13,199.51 | 2026-10-01 | 1 | 366.65 | 12,832.86 |
| **FA-098** | V-00545--AMAX Information Technologies | 36 | 63,995.00 | 2026-10-01 | 1 | 1,777.64 | 62,217.36 |
| **FA-099** | V00021--Amazon | 36 | 15,911.52 | 2026-10-01 | 1 | 441.99 | 15,469.53 |
| **FA-100** | Other Expenses--Other Expenses for Ramp Users | 36 | 3,674.73 | 2026-10-01 | 1 | 102.08 | 3,572.65 |
| **Total** | | | **1,648,943.20** | | | | **601,941.39** |

## Leasehold Improvements

4 assets.

| **Ref** | **Name** | **Lifetime** | **Original Cost** | **Start Date** | **Last Period** | **Last Amount** | **Current NBV** |
|---------|------------------------------|---------:|-------------:|------------|--------:|-----------:|------------:|
| **FA-073** | Contract: 241100 - 275 Shoreline/100/Minio Additional Power | 60 | 29,933.00 | 2024-04-30 | 31 | 498.88 | 14,467.62 |
| **FA-076** | MinIO-Ste 100- TWA 1 - Tenant Overage | 44 | 22,270.00 | 2024-11-20 | 24 | 519.63 | 10,392.67 |
| **FA-082** | TWA2\_275 MinIO Suite 100\_10220-24-t001 AST - Blinds | 42 | 10,253.00 | 2025-01-14 | 22 | 247.78 | 4,955.62 |
| **FA-088** | TWA\#3\_MinIO\_10220-24- t001 AST - Doors | 40 | 12,732.00 | 2025-03-25 | 20 | 318.30 | 6,366.00 |
| **Total** | | | **75,188.00** | | | | **36,181.91** |
