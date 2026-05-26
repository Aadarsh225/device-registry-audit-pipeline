import os

print("=" * 60)
print("STARTING COMPLETE DATA PIPELINE")
print("=" * 60)

print("\nRunning ETL...")
os.system("python scripts/ETL.py")

print("\nRunning Manual Validation...")
os.system("python scripts/validate.py")

print("\nRunning Great Expectations...")
os.system("python scripts/great_expectation_check.py")

print("\nPIPELINE EXECUTED SUCCESSFULLY")
print("=" * 60)