# Genus Update Scripts

This directory contains scripts used to add genus information to the tree YAML files.

## Key Files

- `add_genus_info.py`: Core functions for extracting and mapping genus information
- `add_genus_to_all.py`: Main script that processes all tree files and generates a report
- `test_genus_add.py`: Testing script used to validate the genus update functions
- `genus_update_report.csv`: Final report showing all genus updates
- `final_summary.md`: Summary of the genus update process

## Usage

To add genus information to tree files:

```bash
python add_genus_to_all.py
```

This script:
1. Extracts scientific genus from the scientific name
2. Maps scientific genus to common genus using a comprehensive dictionary
3. Adds both scientific_genus and common_genus fields to each tree file
4. Generates a report of all updates

## Genus Mapping System

The scripts use a sophisticated mapping system to handle different genus classifications:

1. Simple mappings (e.g., "Pinus" → "Pine")
2. Complex mappings for genera with subgroups (e.g., Quercus/Oak species are mapped to "White Oak", "Live Oak", or "Black Oak" based on their species)

## Report Format

The genus_update_report.csv contains:
- Filename
- Scientific Genus
- Common Genus
- Update Status

## Workflow

The genus update process was completed in these steps:

1. Extract scientific genus from scientific name
2. Create mapping of scientific to common genus names
3. Test the update on a subset of files
4. Apply changes to all tree files
5. Verify success with the generated report