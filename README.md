# Cost-Optimization-Challenge-Managing-Billing-Records-in-Azure-Serverless-Architecture
Solution for an Azure cost optimization challenge using serverless architecture. Implements data archival from Cosmos DB to Blob Storage for billing records older than 3 months, with zero downtime and no API changes.
## Overview

This solution addresses a cost optimization challenge using Azure serverless components. The system stores over 2 million billing records in Azure Cosmos DB, and records older than 3 months are rarely accessed.

### Goals:
- Reduce Cosmos DB cost
- Retain access to all records with low latency
- No API contract changes
- Zero downtime and no data loss

## Solution Architecture

- Active (< 3 months): Stored in Azure Cosmos DB
- Archived (> 3 months): Moved to Azure Blob Storage
- Azure Functions:
  - One for archival (timer trigger)
  - One for read access with fallback to Blob

## Files Included

- `archive_function.py` – Moves old records to Blob
- `read_function.py` – Dual-read logic (Cosmos DB → Blob fallback)
- `diagram.png` – Architecture overview
- `chatgpt_conversation.txt` – AI-assisted design conversation
- `README.md` – Solution explanation (this file)

## Technologies Used

- Azure Functions
- Azure Cosmos DB
- Azure Blob Storage
- Python SDKs


