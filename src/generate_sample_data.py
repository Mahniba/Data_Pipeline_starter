"""
generate_sample_data.py

Purpose:
    Generate a realistic but intentionally imperfect procurement dataset.

Why are we doing this?
    Real-world data is rarely clean. Before building our validation
    and cleaning pipelines, we need a dataset containing realistic
    data-quality problems.

Important business logic:
    A procurement project follows a simplified lifecycle:

        Programming
             ↓
        Published
             ↓
        Awarded

    A project can also end as:

        Published/Evaluation → Unsuccessful
        Programming/Published/Evaluation → Cancelled

    Therefore:

        Programming:
            - Has a budget
            - Does NOT have a publication date
            - Does NOT have an award amount
            - Does NOT have a contractor

        Published:
            - Has a budget
            - Has a publication date
            - Does NOT have an award amount
            - Does NOT have a contractor

        Awarded:
            - Has a budget
            - Has a publication date
            - Has an award amount
            - Has a contractor

        Unsuccessful:
            - Has a budget
            - Has a publication date
            - Does NOT have an award amount
            - Does NOT have a contractor

        Cancelled:
            - Has a budget
            - May have a publication date
            - Does NOT have an award amount
            - Does NOT have a contractor

Output:
    data/sample/procurement_raw_sample.csv
"""
# 1. IMPORT LIBRARIES

# csv allows us to write structured tabular data into a CSV file.
import csv

# random allows us to generate different realistic values.
import random

# datetime allows us to create realistic procurement dates.
from datetime import datetime, timedelta

# Path gives us a safer way to work with file/folder paths
# instead of manually writing Windows-specific paths.
from pathlib import Path
# 2. DEFINE THE OUTPUT LOCATION

# Path(__file__) gives us the location of this Python file.
#
# .parent
#     moves from generate_sample_data.py to the src folder.
#
# .parent.parent
#     moves from src to the main project directory.
#
# We therefore use the project root as our starting point.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define where our sample dataset will be stored.
OUTPUT_DIRECTORY = PROJECT_ROOT / "data" / "sample"

# Define the final CSV filename.
OUTPUT_FILE = OUTPUT_DIRECTORY / "procurement_raw_sample.csv"

# 3. CREATE THE OUTPUT DIRECTORY

# parents=True means Python can create missing parent folders.
# exist_ok=True means Python will not complain if the folder
# already exists.
OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

# 4. DEFINE REFERENCE VALUES

# These are realistic examples of organizations that might
# participate in public procurement.
organizations = [
    "MINMAP",
    "MINEPAT",
    "MINTP",
    "MINSANTE",
    "MINEDUB",
    "MINADER",
    "MINPOSTEL",
]


# Cameroon administrative regions.
regions = [
    "Centre",
    "Littoral",
    "North-West",
    "South-West",
    "West",
    "North",
    "Far-North",
    "Adamawa",
    "South",
    "East",
]


# Procurement categories.
procurement_types = [
    "Works",
    "Supplies",
    "Services",
]


# Procurement statuses.

# IMPORTANT:
# These statuses are not independent of the other columns.
# The status determines which fields should or should not
# contain values.
statuses = [
    "Programming",
    "Published",
    "Awarded",
    "Cancelled",
    "Unsuccessful",
]


# Example contractors.

# Contractors will only be assigned to projects whose status
# is "Awarded".
contractors = [
    "Cameroon Build Ltd",
    "Africa Infrastructure SARL",
    "Tech Solutions Cameroon",
    "Global Services Ltd",
    "Mountain Engineering",
    "Central Works SARL",
]

# 5. SET A RANDOM SEED
# A seed makes our random dataset reproducible.
#
# Without this, every time we run the program we would get
# different data.
#
# With a seed, another developer can run the same script and
# reproduce the same dataset.
random.seed(42)

# 6. GENERATE PROCUREMENT RECORDS

# We will generate 300 records.
NUMBER_OF_RECORDS = 300

# Create an empty list that will contain all procurement records.
records = []

# Define the earliest possible date used for publication.
BASE_DATE = datetime(2025, 1, 1)

# Generate each procurement record.
for number in range(1, NUMBER_OF_RECORDS + 1):

    # 6.1 CREATE PROJECT ID
    # :04d means the number will always contain four digits.    
    # Example:
    # 1   → PRJ-0001
    # 25  → PRJ-0025
    # 300 → PRJ-0300
    project_id = f"PRJ-{number:04d}"


    # 6.2 GENERATE BASIC PROJECT INFORMATION

    # Select an organization randomly from our reference list.
    organization = random.choice(organizations)

    # Select a region randomly.
    region = random.choice(regions)

    # Select a procurement category randomly.
    procurement_type = random.choice(procurement_types)

    # Select the procurement status.
    status = random.choice(statuses)

    # 6.3 GENERATE THE PROCUREMENT BUDGET
    # Every procurement project should have a planned budget.
    # The values are intentionally synthetic and are only
    # being used for this learning project.
    budget = random.randint(
        5_000_000,
        500_000_000
    )
    # 6.4 GENERATE PUBLICATION DATE BASED ON STATUS
    # We start with no publication date.
    # This is important because a project in Programming
    # has not yet been published.
    publication_date = None

    # A publication date is generated only for projects that
    # have reached or passed the publication stage.
    # Therefore:
    # Programming  → None
    # Published     → Date
    # Awarded       → Date
    # Cancelled     → Date or None
    # Unsuccessful  → Date
    if status in [
        "Published",
        "Awarded",
        "Unsuccessful",
    ]:

        publication_date = (
            BASE_DATE
            + timedelta(days=random.randint(0, 700))
        )

        publication_date = publication_date.strftime("%Y-%m-%d")


    elif status == "Cancelled":

        # A cancelled procurement may have been cancelled
        # before publication or after publication.
        #
        # To represent both possibilities, we randomly decide
        # whether it had already been published.
        was_published = random.choice([True, False])

        if was_published:

            publication_date = (
                BASE_DATE
                + timedelta(days=random.randint(0, 700))
            )

            publication_date = publication_date.strftime(
                "%Y-%m-%d"
            )

    # 6.5 GENERATE PROCESSING DURATION
    # We generate a normal positive processing duration.
    # Later, we intentionally introduce negative values as
    # data-quality problems.
    processing_days = random.randint(5, 180)
    # 6.6 GENERATE AWARD AMOUNT AND CONTRACTOR
    # Start with no award amount.
    # This is the important correction.
    # A project should NOT automatically receive an award
    # amount simply because we generated a budget.
    award_amount = None


    # Start with no contractor.
    contractor = None


    # Only an Awarded project receives an award amount and
    # contractor in our simplified procurement model.
    if status == "Awarded":

        # Generate an award amount between 70% and 100%
        # of the original budget.
        #
        # We use 1.00 as the normal upper limit here because
        # an award above the budget will be introduced later
        # deliberately as a data-quality anomaly.
        award_amount = round(
            budget * random.uniform(0.70, 1.00),
            2
        )

        # An awarded project must have a contractor.
        contractor = random.choice(contractors)

    record = {
        "project_id": project_id,
        "organization": organization,
        "region": region,
        "procurement_type": procurement_type,
        "budget_fcfa": budget,
        "status": status,
        "publication_date": publication_date,
        "award_amount_fcfa": award_amount,
        "contractor": contractor,
        "processing_days": processing_days,
    }


    # Add the record to our list.
    records.append(record)
# 7. INTRODUCE DATA-QUALITY PROBLEMS
# IMPORTANT:
# At this point, our BASE dataset follows the business logic.
# We now deliberately introduce some bad records.
# This allows our future validation pipeline to detect
# problems that should NOT exist in the original business data.

# Problem 1: Missing organization

# Remove the organization from a few records.
# An organization should normally exist, so these records
# will later be considered invalid.
for record in random.sample(records, 8):
    record["organization"] = ""


# Problem 2: Missing region

# Remove the region from a few records.
# This creates another missing-value problem.
for record in random.sample(records, 6):
    record["region"] = ""

# Problem 3: Inconsistent spelling

# Some regions may be entered differently by different users.
# "North West" and "North-West" refer to the same region
# conceptually, but our database should eventually use one
# standardized representation.
for record in random.sample(records, 8):
    record["region"] = "North West"


# Correct standardized form:
# North-West

# Problem 4: Extra spaces

# Add unnecessary spaces around some organization names.
# Example:
# "MINMAP"
# becomes:
# "  MINMAP  "
# Our cleaning pipeline will eventually remove these spaces.
for record in random.sample(records, 6):

    # Only add spaces if the organization is not already
    # missing.
    #
    # This prevents us from transforming "" into "    ".
    if record["organization"]:
        record["organization"] = (
            "  "
            + record["organization"]
            + "  "
        )

# Problem 5: Invalid processing duration
# Processing days cannot logically be negative.
# We deliberately create four invalid records so that
# our validation pipeline has something to detect.
for record in random.sample(records, 4):
    record["processing_days"] = -10

# Problem 6: Suspicious award amount
# We deliberately create award amounts greater than the
# original budget.
# IMPORTANT:
# We ONLY do this to records that are actually Awarded.
# This preserves our main business rule:
# Programming / Published / Cancelled / Unsuccessful
# should NOT suddenly receive an award amount.
# At the same time, Awarded records with an award greater
# than their budget become suspicious records that our
# validation system can detect.
awarded_records = [
    record
    for record in records
    if record["status"] == "Awarded"
]

# Make sure we have enough Awarded records before sampling.
if len(awarded_records) >= 5:

    for record in random.sample(awarded_records, 5):

        record["award_amount_fcfa"] = (
            record["budget_fcfa"] * 1.50
        )
# Problem 7: Missing contractor
# A contractor should exist for an Awarded project.
#
# Therefore, we deliberately remove the contractor from
# some Awarded projects.
awarded_records_with_contractors = [
    record
    for record in records
    if (
        record["status"] == "Awarded"
        and record["contractor"] is not None
    )
]


if len(awarded_records_with_contractors) >= 5:

    for record in random.sample(
        awarded_records_with_contractors,
        5
    ):

        record["contractor"] = ""

# 8. CREATE DUPLICATES
# Duplicate records are extremely common in real datasets.
# We take several existing records and append copies of them.
# This gives our validation pipeline something to detect later.

duplicates = random.sample(records, 10)


for record in duplicates:

    # copy() is used so that we create a separate dictionary
    # rather than another reference to the same dictionary.
    records.append(record.copy())

# 9. DEFINE CSV COLUMNS
# These are the columns that will appear in our CSV file.
fieldnames = [
    "project_id",
    "organization",
    "region",
    "procurement_type",
    "budget_fcfa",
    "status",
    "publication_date",
    "award_amount_fcfa",
    "contractor",
    "processing_days",
]

# 10. WRITE DATA TO CSV
# Open the output CSV file.
#
# newline=""
#     prevents unwanted blank lines on Windows.
#
# encoding="utf-8"
#     ensures that text is stored correctly.
with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:

    # DictWriter allows us to write dictionaries directly
    # into CSV rows.
    writer = csv.DictWriter(
        csv_file,
        fieldnames=fieldnames
    )

    # Write the header row.
    writer.writeheader()

    # Write all records.
    writer.writerows(records)

# 11. PRINT A SUMMARY
print("=" * 60)

print("SAMPLE DATASET GENERATED")

print("=" * 60)

print(f"Output file: {OUTPUT_FILE}")

print(f"Number of records: {len(records)}")

print(f"Number of columns: {len(fieldnames)}")

print("Status: SUCCESS")

print("=" * 60)