# Genus Scripts

These scripts are used for adding and managing genus information in tree YAML files.

## Core Scripts

- `add_genus_info.py`: Core functions for extracting and mapping genus information
- `add_genus_to_all.py`: Main script that processes all tree files and generates a report
- `add_genus_to_single_file.py`: Processes a single tree file for testing
- `update_genus_info.py`: Advanced script that uses genus directory for information
- `test_genus_add.py`: Testing script for validating genus updates

## Support Scripts

- `add_missing_genus.py`: Adds genus info to files missing it
- `add_quotes_to_genus.py`: Ensures all genus values have proper quotes
- `check_missing_genus.py`: Identifies files with missing genus information
- `fix_newly_added_genus.py`: Fixes formatting issues with newly added genus fields
- `fix_tree_files.py`: Moves genus info to correct position in files

## Data Files

- `genus_update_report.csv`: Report of all genus updates with status

## Usage

The main script for adding genus information to all tree files is:

```bash
python add_genus_to_all.py
```

For testing on a single file:

```bash
python add_genus_to_single_file.py <filename>
```