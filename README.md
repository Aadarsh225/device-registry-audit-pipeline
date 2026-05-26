# Device Registry Audit Pipeline

## Project Overview
This project is an ETL (Extract, Transform, Load) and Data Quality Pipeline built using Python, Pandas, MongoDB Atlas, and Great Expectations.

The goal of this project is to combine **Device Registry Data** and **Registry Audit Data** into a single **Master Table / Master Collection** and validate whether the data is clean, consistent, and reliable.

This simulates a real-world banking/payment device system where QR devices support multiple payment methods like GPay, PhonePe, Paytm, BHIM, and Fonepay.

---

## Tech Stack
- Python
- Pandas
- MongoDB Atlas
- Great Expectations
- JSON
- CSV
- Git / GitHub

---

## Project Workflow

### 1. Extract
Raw messy JSON data is loaded from:
- `device_registry.json`
- `registry_audit.json`

---

### 2. Transform
Performed multiple cleaning and validation steps:
- Duplicate removal
- Null value check
- Missing owner handling
- Missing serial number handling
- Invalid date conversion
- Negative amount handling
- Invalid scheme validation
- Type correction
- Boolean conversion
- Data standardization

---

### 3. Master Table Creation
Merged both datasets using:

`machine_identifier`

This created a unified master dataset containing:
- Device information
- Audit / transaction details
- Payment schemes
- Device owner
- Status
- Model
- Active/Inactive state
- Timestamps

---

### 4. Load
Saved processed output as:
- `device_registry_clean.csv`
- `registry_audit_clean.csv`
- `master_device_audit.csv`
- `master_device_audit.json`

---

### 5. Validation
Performed manual data quality validation:
- Null checks
- Duplicate checks
- Invalid scheme checks
- Unmatched device records
- Date quality checks
- Negative amount checks

---

### 6. Great Expectations
Used Great Expectations to validate:
- Required columns
- Non-null values
- Valid payment schemes
- Positive transaction amount
- Data consistency

---

## Folder Structure

```bash
device-registry-audit-pipeline/
┣ data/
┃ ┣ mongo_source/
┃ ┃ ┗ device_registry.json
┃ ┣ audit_source/
┃ ┃ ┗ registry_audit.json
┃ ┗ processed/
┃   ┣ device_registry_clean.csv
┃   ┣ registry_audit_clean.csv
┃   ┣ master_device_audit.csv
┃   ┗ master_device_audit.json
┣ scripts/
┃ ┣ ETL.py
┃ ┣ validate.py
┃ ┗ great_expectation_check.py
┣ README.md
┣ requirements.txt
┗ .gitignore