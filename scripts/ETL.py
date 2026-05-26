import pandas as pd

# ==========================================================
# ETL PIPELINE
# Device Registry + Registry Audit
# Extract → Transform → Load
# ==========================================================

print("=" * 60)
print("STARTING ETL PIPELINE")
print("=" * 60)

# ==========================================================
# 1. EXTRACT
# Load raw data
# ==========================================================

print("\n[1] EXTRACTING SOURCE FILES...")

device_registry = pd.read_json(
    "data/mongo_source/device_registry.json"
)

registry_audit = pd.read_json(
    "data/audit_source/registry_audit.json"
)

print("Device Registry Shape :", device_registry.shape)
print("Registry Audit Shape  :", registry_audit.shape)

print("\nDevice Registry Columns:")
print(device_registry.columns.tolist())

print("\nRegistry Audit Columns:")
print(registry_audit.columns.tolist())


# ==========================================================
# 2. TRANSFORM / DATA QUALITY CHECK
# ==========================================================

print("\n" + "=" * 60)
print("TRANSFORM + VALIDATION")
print("=" * 60)

# ----------------------------------------------------------
# REMOVE DUPLICATES
# ----------------------------------------------------------

print("\nREMOVING DUPLICATES...")

device_registry = device_registry.drop_duplicates(
    subset=["machine_identifier"]
)

registry_audit = registry_audit.drop_duplicates(
    subset=["_id"]
)

print("Device Registry Shape After Dedupe :", device_registry.shape)
print("Registry Audit Shape After Dedupe  :", registry_audit.shape)


# ----------------------------------------------------------
# DEVICE REGISTRY CHECKS
# ----------------------------------------------------------

print("\nDEVICE REGISTRY CHECKS")

print("Duplicate machine_identifier :",
      device_registry["machine_identifier"].duplicated().sum())

print("Null serial_number :",
      device_registry["serial_number"].isnull().sum())

print("Null model :",
      device_registry["model"].isnull().sum())

print("Null owner :",
      device_registry["owner"].isnull().sum())


# Convert is_active safely to boolean
device_registry["is_active"] = (
    device_registry["is_active"]
    .fillna(False)
    .astype(bool)
)

print("Inactive Devices :",
      (device_registry["is_active"] == False).sum())


# Convert date columns
device_registry["created_at"] = pd.to_datetime(
    device_registry["created_at"],
    errors="coerce"
)

device_registry["updated_at"] = pd.to_datetime(
    device_registry["updated_at"],
    errors="coerce"
)

print("Invalid created_at :",
      device_registry["created_at"].isnull().sum())

print("Invalid updated_at :",
      device_registry["updated_at"].isnull().sum())


# ----------------------------------------------------------
# REGISTRY AUDIT CHECKS
# ----------------------------------------------------------

print("\nREGISTRY AUDIT CHECKS")

# Convert amount to numeric
registry_audit["amount"] = pd.to_numeric(
    registry_audit["amount"],
    errors="coerce"
)

print("Null Amount :",
      registry_audit["amount"].isnull().sum())

print("Negative Amount :",
      (registry_audit["amount"] < 0).sum())

print("Null Status :",
      registry_audit["status"].isnull().sum())

print("Duplicate machine_identifier :",
      registry_audit["machine_identifier"].duplicated().sum())


# Valid scheme check
valid_scheme = [
    "gpay",
    "phonepe",
    "paytm",
    "bhim",
    "fonepay"
]

invalid_scheme = registry_audit[
    ~registry_audit["scheme"].isin(valid_scheme)
]

print("Invalid Scheme Count :",
      len(invalid_scheme))


# Convert audit date
registry_audit["created_at"] = pd.to_datetime(
    registry_audit["created_at"],
    errors="coerce"
)

print("Invalid Audit Dates :",
      registry_audit["created_at"].isnull().sum())


# ----------------------------------------------------------
# BASIC CLEANING
# ----------------------------------------------------------

print("\nAPPLYING BASIC CLEANING...")

# Fill missing values
device_registry["model"] = (
    device_registry["model"]
    .fillna("UNKNOWN_MODEL")
)

device_registry["owner"] = (
    device_registry["owner"]
    .fillna("UNKNOWN_OWNER")
)

device_registry["serial_number"] = (
    device_registry["serial_number"]
    .fillna("UNKNOWN_SERIAL")
)

registry_audit["amount"] = (
    registry_audit["amount"]
    .fillna(0)
)

registry_audit["amount"] = (
    registry_audit["amount"].abs()
)

registry_audit["status"] = (
    registry_audit["status"]
    .fillna("UNKNOWN")
)

# Invalid scheme → UNKNOWN
registry_audit.loc[
    ~registry_audit["scheme"].isin(valid_scheme),
    "scheme"
] = "UNKNOWN"

print("Cleaning Completed")


# ----------------------------------------------------------
# DATE QUALITY AFTER CLEANING
# ----------------------------------------------------------

print("\nDATE QUALITY")

print("Valid Device Dates :",
      device_registry["created_at"].notnull().sum())

print("Valid Audit Dates :",
      registry_audit["created_at"].notnull().sum())


# ----------------------------------------------------------
# CREATE MASTER TABLE
# ----------------------------------------------------------

print("\nCREATING MASTER TABLE...")

master = registry_audit.merge(
    device_registry,
    on="machine_identifier",
    how="left",
    suffixes=("_audit", "_device")
)

# Unmatched devices
master["owner"] = (
    master["owner"]
    .fillna("UNMATCHED_DEVICE")
)

print("Master Shape :", master.shape)

print("Unmatched Devices :",
      (master["owner"] == "UNMATCHED_DEVICE").sum())

print("Duplicate machine_identifier in Master :",
      master["machine_identifier"].duplicated().sum())


# ----------------------------------------------------------
# DATA PROFILING / ANALYTICS
# ----------------------------------------------------------

print("\nDATA PROFILING")

print("\nTransaction Status Count:")
print(master["status"].value_counts())

print("\nScheme Count:")
print(master["scheme"].value_counts())

print("\nTop Device Models:")
print(master["model"].value_counts().head())

print("\nActive vs Inactive Devices:")
print(master["is_active"].value_counts())

print("\nTotal Amount Processed:")
print(master["amount"].sum())

print("\nAverage Transaction Amount:")
print(master["amount"].mean())


# ==========================================================
# 3. LOAD
# Save processed data
# ==========================================================

print("\n" + "=" * 60)
print("LOADING CLEAN DATA")
print("=" * 60)

# CSV output
device_registry.to_csv(
    "data/processed/device_registry_clean.csv",
    index=False
)

registry_audit.to_csv(
    "data/processed/registry_audit_clean.csv",
    index=False
)

master.to_csv(
    "data/processed/master_device_audit.csv",
    index=False
)

# JSON output (Best for MongoDB)
master.to_json(
    "data/processed/master_device_audit.json",
    orient="records",
    indent=4
)

print("device_registry_clean.csv saved")
print("registry_audit_clean.csv saved")
print("master_device_audit.csv saved")
print("master_device_audit.json saved")


# ==========================================================
# FINAL SUMMARY
# ==========================================================

print("\n" + "=" * 60)
print("ETL PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)