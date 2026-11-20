# Depreciation history (DHR)

Template `MINIO_ FAM_DHR.xlsx`, tab **DHR Import Template**, filled as SOA's **FAM_DHR_lumpsum** example: one Depreciation row per asset for the depreciation taken to 2026-10-31.

| **Template column** | **Value** |
|----------------------|-------------------------------------------------------------|
| **DHR Name** | Ref and date, such as FA-069 Depreciation to 2026-10-31 |
| **Asset Name** | Name from the mid-life load. NetSuite's format is the asset ID plus the name (FAM00001 Chairs), so the ID is added once the assets are imported |
| **Subsidiary, Quantity, Asset Type, Asset Lifetime** | As in the mid-life load |
| **Transaction Type** | Depreciation |
| **Transaction Date** | 2026-10-31 |
| **Transaction Amount** | Accumulated depreciation at 2026-10-31 |
| **Net Book Value (NBV)** | Original Cost less Transaction Amount |
| **Depreciation Period, Period-1** | The asset's Last Depreciation Period, and that less 1 |
| **Purchase Date** | Register Purchase Date |
| **Original Cost** | Register cost |

32 assets, in the order of the load file.

| **Ref** | **DHR Name** | **Asset Name** | **Subsidiary** | **Quantity** | **Asset Type** | **Transaction Type** | **Transaction Date** | **Transaction Amount** | **Net Book Value (NBV)** | **Depreciation Period** | **Period-1** | **Asset Lifetime** | **Purchase Date** | **Original Cost** |
|------|-----|----------------------|-------|----:|---------|---------|--------|---------:|---------:|-----:|----:|-----:|--------|---------:|
| **FA-069** | FA-069 Depreciation to 2026-10-31 | AMAX AceleMax NVIDIA GPU server | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 311,002.78 | 8,885.79 | 35 | 34 | 36 | 2023-12-04 | 319,888.57 |
| **FA-070** | FA-070 Depreciation to 2026-10-31 | Laptop - Petr Kobalicek | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 3,243.00 | 294.82 | 33 | 32 | 36 | 2024-01-30 | 3,537.82 |
| **FA-071** | FA-071 Depreciation to 2026-10-31 | Laptop - Piotr Wyderski | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 3,386.18 | 307.84 | 33 | 32 | 36 | 2024-01-11 | 3,694.02 |
| **FA-072** | FA-072 Depreciation to 2026-10-31 | SuperMicro X13SET-G servers (2) | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 106,137.10 | 9,648.83 | 33 | 32 | 36 | 2024-02-23 | 115,785.93 |
| **FA-073** | FA-073 Depreciation to 2026-10-31 | Additional power, 275 Shoreline Ste 100 | MinIO, Inc. | 1 | Leasehold Improvements | Depreciation | 2026-10-31 | 15,465.38 | 14,467.62 | 31 | 30 | 60 | 2024-04-15 | 29,933.00 |
| **FA-074** | FA-074 Depreciation to 2026-10-31 | Computers & equipment - MIRAPATH | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 5,235.89 | 1,745.30 | 27 | 26 | 36 | 2024-08-20 | 6,981.19 |
| **FA-075** | FA-075 Depreciation to 2026-10-31 | NVIDIA Spectrum-3 SN4700 switch | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 27,292.29 | 10,497.03 | 26 | 25 | 36 | 2024-08-07 | 37,789.32 |
| **FA-076** | FA-076 Depreciation to 2026-10-31 | Suite 100 tenant overage (TWA 1) | MinIO, Inc. | 1 | Leasehold Improvements | Depreciation | 2026-10-31 | 11,877.33 | 10,392.67 | 24 | 23 | 44 | 2024-11-20 | 22,270.00 |
| **FA-077** | FA-077 Depreciation to 2026-10-31 | Dell PowerEdge R7615 server 2024-12-06 | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 75,502.04 | 42,675.06 | 23 | 22 | 36 | 2024-12-06 | 118,177.10 |
| **FA-078** | FA-078 Depreciation to 2026-10-31 | Dell PowerEdge R7615 server 2024-12-10 | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 134,307.58 | 75,912.98 | 23 | 22 | 36 | 2024-12-10 | 210,220.56 |
| **FA-079** | FA-079 Depreciation to 2026-10-31 | Dell PowerEdge XE968 server | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 162,937.41 | 92,095.06 | 23 | 22 | 36 | 2024-12-12 | 255,032.47 |
| **FA-080** | FA-080 Depreciation to 2026-10-31 | Dell hardware - Center of Excellence | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 3,889.73 | 2,198.54 | 23 | 22 | 36 | 2024-12-20 | 6,088.27 |
| **FA-081** | FA-081 Depreciation to 2026-10-31 | 100GB Switch with 28 cables | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 5,490.39 | 3,493.89 | 22 | 21 | 36 | 2025-01-11 | 8,984.28 |
| **FA-082** | FA-082 Depreciation to 2026-10-31 | Suite 100 blinds (TWA 2) | MinIO, Inc. | 1 | Leasehold Improvements | Depreciation | 2026-10-31 | 5,297.38 | 4,955.62 | 22 | 21 | 42 | 2025-01-14 | 10,253.00 |
| **FA-083** | FA-083 Depreciation to 2026-10-31 | Server Technology Smart PRO3X with PIPS | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 3,370.34 | 2,407.38 | 21 | 20 | 36 | 2025-01-20 | 5,777.72 |
| **FA-084** | FA-084 Depreciation to 2026-10-31 | NVIDIA CX-7 400Gb NIC cards (18) | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 70,088.80 | 44,601.97 | 22 | 21 | 36 | 2025-01-22 | 114,690.77 |
| **FA-085** | FA-085 Depreciation to 2026-10-31 | Mellanox CX-7 support and warranty, 3 yrs | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 7,388.68 | 4,701.89 | 22 | 21 | 36 | 2025-01-23 | 12,090.57 |
| **FA-086** | FA-086 Depreciation to 2026-10-31 | NVIDIA 400GbE transceivers and cables | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 5,176.45 | 3,697.47 | 21 | 20 | 36 | 2025-02-24 | 8,873.92 |
| **FA-087** | FA-087 Depreciation to 2026-10-31 | Rahi data center hardware, March 2025 | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 5,908.69 | 4,726.96 | 20 | 19 | 36 | 2025-03-10 | 10,635.65 |
| **FA-088** | FA-088 Depreciation to 2026-10-31 | Suite 100 doors (TWA 3) | MinIO, Inc. | 1 | Leasehold Improvements | Depreciation | 2026-10-31 | 6,366.00 | 6,366.00 | 20 | 19 | 40 | 2025-03-25 | 12,732.00 |
| **FA-089** | FA-089 Depreciation to 2026-10-31 | Laptop - Ali Yaldaz | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 1,795.32 | 1,606.34 | 19 | 18 | 36 | 2025-04-02 | 3,401.66 |
| **FA-090** | FA-090 Depreciation to 2026-10-31 | FS.COM transceiver | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 1,159.10 | 1,037.08 | 19 | 18 | 36 | 2025-04-24 | 2,196.18 |
| **FA-091** | FA-091 Depreciation to 2026-10-31 | Fiber optic jumper cables | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 432.92 | 387.34 | 19 | 18 | 36 | 2025-04-30 | 820.26 |
| **FA-092** | FA-092 Depreciation to 2026-10-31 | SanDisk storage cards (192) | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 91,022.40 | 91,022.40 | 18 | 17 | 36 | 2025-05-15 | 182,044.80 |
| **FA-093** | FA-093 Depreciation to 2026-10-31 | Supermicro CUST 2XX550 480GB | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 6,055.61 | 21,194.64 | 8 | 7 | 36 | 2025-03-05 | 27,250.25 |
| **FA-094** | FA-094 Depreciation to 2026-10-31 | NVIDIA Spectrum-4 switch and networking | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 10,665.83 | 53,329.17 | 6 | 5 | 36 | 2026-05-07 | 63,995.00 |
| **FA-095** | FA-095 Depreciation to 2026-10-31 | NVIDIA CX-7 NIC card with warranty | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 2,499.66 | 19,997.24 | 4 | 3 | 36 | 2026-07-06 | 22,496.90 |
| **FA-096** | FA-096 Depreciation to 2026-10-31 | NADDOD purchase, September 2026 | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 325.26 | 11,383.97 | 1 | 0 | 36 | 2026-09-22 | 11,709.23 |
| **FA-097** | FA-097 Depreciation to 2026-10-31 | MacBooks for new hires (5) | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 366.65 | 12,832.86 | 1 | 0 | 36 | 2026-09-28 | 13,199.51 |
| **FA-098** | FA-098 Depreciation to 2026-10-31 | AMAX purchase (Sage V-00545) | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 1,777.64 | 62,217.36 | 1 | 0 | 36 | 2022-10-19 | 63,995.00 |
| **FA-099** | FA-099 Depreciation to 2026-10-31 | Amazon purchase (Sage V00021) | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 441.99 | 15,469.53 | 1 | 0 | 36 | 2022-10-19 | 15,911.52 |
| **FA-100** | FA-100 Depreciation to 2026-10-31 | Ramp users - other expenses | MinIO, Inc. | 1 | Equipment | Depreciation | 2026-10-31 | 102.08 | 3,572.65 | 1 | 0 | 36 | 2022-10-20 | 3,674.73 |
| **Total** |  |  |  |  |  |  |  | **1,086,007.90** | **638,123.30** |  |  |  |  | **1,724,131.20** |
