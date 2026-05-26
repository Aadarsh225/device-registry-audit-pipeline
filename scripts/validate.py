import pandas as pd

print("=" * 60)
print("MANUAL DATA VALIDATION")
print("=" * 60)

# Load master table
master = pd.read_json(
    "data/processed/master_device_audit.json"
)

print("\nMaster Shape :", master.shape)


# =====================================================
# NULL CHECKS
# =====================================================

print("\nNULL VALUE CHECK")
print(master.isnull().sum())


# =====================================================
# DUPLICATE CHECKS
# =====================================================

print("\nDUPLICATE CHECKS")

print("Duplicate machine_identifier :",
      master["machine_identifier"].duplicated().sum())

print("Duplicate audit id :",
      master["_id_audit"].duplicated().sum())

print("Duplicate serial_number :",
      master["serial_number"].duplicated().sum())


# =====================================================
# AMOUNT CHECKS
# =====================================================

print("\nAMOUNT CHECKS")

print("Negative Amount :",
      (master["amount"] < 0).sum())

print("Zero Amount :",
      (master["amount"] == 0).sum())


# =====================================================
# SCHEME CHECKS
# =====================================================

print("\nSCHEME CHECKS")

print(master["scheme"].value_counts())


# =====================================================
# STATUS CHECKS
# =====================================================

print("\nSTATUS CHECKS")

print(master["status"].value_counts())


# =====================================================
# DEVICE CHECKS
# =====================================================

print("\nDEVICE CHECKS")

print("Inactive Devices :",
      (master["is_active"] == False).sum())

print("Unmatched Devices :",
      (master["owner"] == "UNMATCHED_DEVICE").sum())


# =====================================================
# FINAL SUMMARY
# =====================================================

print("\nVALIDATION COMPLETED")
print("=" * 60)