# Tree Project Scripts

This directory contains scripts used for managing and formatting the California trees collection.

## Directory Structure

- **genus_update/**: Scripts and documentation for the genus update project (completed)
- **genus_scripts/**: Scripts for adding and managing genus information in tree files
- **formatting_scripts/**: Scripts for formatting and standardizing tree file structure
- **utilities/**: Utility scripts for validating and checking tree files
- **data/**: Data files used by the scripts, including reference CSV files
- **reformat_yaml.py**: General-purpose YAML reformatting script

## Main Projects

### 1. Genus Update Project (Complete)

Located in `genus_update/`, this project added structured genus information to all tree files:
- Added scientific_genus and common_genus fields
- Created mappings for 57 different genera
- Generated detailed reports of all changes

### 2. File Formatting

Located in `formatting_scripts/`, these scripts were used to standardize the format of all tree files:
- Ensured consistent indentation and field positioning
- Added proper section headers and spacing
- Standardized quoting of string values

### 3. Validation and Utilities

Located in `utilities/`, these scripts help validate the tree files:
- Check for formatting consistency
- Validate required fields
- Ensure structural compliance

### 4. Data Files

Located in `data/`, these files provide reference data:
- `all-trees-in-california-2025-03-23.csv`: Original dataset of California trees

## Usage Notes

Most scripts are preservation artifacts from completed projects. The most useful ongoing scripts are:

1. Validation: `utilities/validate_tree_files.py`
2. General formatting: `reformat_yaml.py`

If you need to add new genus information to any new tree files, refer to the scripts in `genus_scripts/`. Each directory contains its own README with more detailed information.