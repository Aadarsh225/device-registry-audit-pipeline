import pandas as pd
import great_expectations as gx

print("=" * 60)
print("GREAT EXPECTATIONS DATA QUALITY CHECK")
print("=" * 60)

# =====================================================
# LOAD MASTER TABLE
# =====================================================

master = pd.read_json(
    "data/processed/master_device_audit.json"
)

print("\nMaster Shape :", master.shape)


# =====================================================
# CREATE CONTEXT
# =====================================================

context = gx.get_context()

# Create datasource
datasource = context.data_sources.add_pandas(
    name="master_source"
)

# Create dataframe asset
data_asset = datasource.add_dataframe_asset(
    name="master_asset"
)

# Create batch definition
batch_definition = data_asset.add_batch_definition_whole_dataframe(
    "master_batch"
)

# Build batch request
batch_request = batch_definition.build_batch_request(
    {"dataframe": master}
)

# Create / Update expectation suite
suite = context.suites.add_or_update(
    gx.ExpectationSuite(
        name="master_validation_suite"
    )
)

# Create validator
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite=suite
)


# =====================================================
# EXPECTATIONS
# =====================================================

print("\nRUNNING EXPECTATIONS...\n")

# 1. machine_identifier should not be null
validator.expect_column_values_to_not_be_null(
    "machine_identifier"
)

# 2. amount must be >= 0
validator.expect_column_values_to_be_between(
    "amount",
    min_value=0
)

# 3. valid status
validator.expect_column_values_to_be_in_set(
    "status",
    ["SUCCESS", "FAILED", "PENDING", "FIRED", "UNKNOWN"]
)

# 4. valid scheme
validator.expect_column_values_to_be_in_set(
    "scheme",
    ["gpay", "phonepe", "paytm", "bhim", "fonepay", "UNKNOWN"]
)

# 5. owner not null
validator.expect_column_values_to_not_be_null(
    "owner"
)

# 6. serial_number not null
validator.expect_column_values_to_not_be_null(
    "serial_number"
)

# 7. model not null
validator.expect_column_values_to_not_be_null(
    "model"
)

# 8. no duplicate audit id
validator.expect_column_values_to_be_unique(
    "_id_audit"
)

# 9. boolean active flag
validator.expect_column_values_to_be_in_set(
    "is_active",
    [True, False]
)

# 10. valid device type
validator.expect_column_values_to_be_in_set(
    "type",
    ["static", "dynamic", "unknown"]
)


# =====================================================
# VALIDATE
# =====================================================

results = validator.validate()

print("\nValidation Success :", results["success"])

print("\nExpectation Results:")
for result in results["results"]:
    print(
        result["expectation_config"]["type"],
        "->",
        result["success"]
    )


# =====================================================
# EXTRA NULL CHECKS (helpful debug)
# =====================================================

print("\nNULL VALUE SUMMARY")
print(master.isnull().sum())


# =====================================================
# SAVE / UPDATE SUITE
# =====================================================

context.suites.add_or_update(
    validator.expectation_suite
)

print("\nGreat Expectations Check Completed")
print("=" * 60)