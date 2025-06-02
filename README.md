# 🧩 Domo ETL Column Lineage Tracker

## Overview

This project automates the tracking of column transformations in Domo ETL flows to establish full lineage from source to final output. It helps ensure traceability and consistency across your data pipelines by mapping transformed column names back to their original metadata descriptions.

## Key Features

- 🔐 Authenticates securely into Domo using session token.
- 🔄 Retrieves renaming metadata from a central Domo dataset.
- 📊 Updates ETL datasets with accurate column descriptions.
- 🔍 Tracks column name changes through a sequence-based method.
- 🧠 Maintains original and final column names even through passive transformation steps.

## Problem Statement

Domo ETL flows often include transformations that alter column names using tiles like:
- `Select Columns`
- `Alter Columns`
- `Join`

When multiple datasets are involved, tracking the lineage of columns becomes difficult. Some steps modify column names; others do not.

## Solution

We implemented a **sequence-based transformation tracker**:
- Parsed the JSON structure of Domo ETL dataflows.
- Assigned a numeric sequence to each transformation tile.
- Tracked when a column name change occurred (e.g., `1, 0, 0, 0, 0, 2`) where:
  - `1` = start of a transformation
  - `0` = passive tiles
  - `2` = actual renaming step
- Captured both the original and final names of each column.
- Remapped these values back into Domo datasets using Domo's Data API.

This approach ensures that even if a column goes through multiple tiles, its lineage from source to target is maintained accurately.

## Usage

1. **Set Domo Credentials**
   Update the `domo_instance`, `email`, and `password` variables.

2. **Prepare Metadata Mapping**
   Ensure your metadata table (e.g., `DIM_GoldMetadataRepository| Renamed`) has the following columns:
   - `Dataset_ID`
   - `rename`
   - `Column Description`

3. **Run the Script**
   ```bash
   python etl_column_remap.py
