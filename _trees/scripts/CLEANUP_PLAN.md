# Script Cleanup Plan

This document outlines a plan for safely removing duplicate script files from the project root once all scripts have been properly organized.

## Current Organization

All script files have been copied to the following directories:
- `scripts/genus_update/`: Completed genus update project scripts and documentation
- `scripts/genus_scripts/`: All scripts related to genus information management
- `scripts/formatting_scripts/`: All scripts related to tree file formatting
- `scripts/utilities/`: Scripts for validation and checking
- `scripts/data/`: Data files used by the scripts

## Files to Remove

Once you confirm the script organization is complete and all scripts are functioning properly in their new locations, the following files can be safely removed:

### Python Scripts in Root Directory
- add_blank_lines.py
- add_genus_info.py
- add_genus_to_all.py
- add_genus_to_single_file.py
- add_missing_genus.py
- add_quotes_to_genus.py
- add_quotes_to_values.py
- check_missing_genus.py
- fix_feature_spacing.py
- fix_features_complete.py
- fix_newly_added_genus.py
- fix_spacing_direct.py
- fix_tree_files.py
- normalize_tree_files.py
- reformat_tree_files.py
- reformat_tree_files_direct.py
- reformat_tree_files_v2.py
- test_genus_add.py
- validate_tree_files.py

### Data Files in Root Directory
- genus_update_report.csv
- final_summary.md

### Python Scripts in trees/ Directory
- trees/add_genus_info.py
- trees/fix_tree_files.py
- trees/update_genus_info.py

## Verification Steps Before Removal

1. Verify all scripts in their new locations by running test cases
2. Check that all documentation is accurate and complete
3. Ensure no references to the root directory paths in any of the scripts
4. Create a backup of the entire directory structure before deletion (if desired)

## Cleanup Command

After verification, you can use the following command to move all scripts to an archive folder or delete them:

```bash
# Option 1: Move to archive
mkdir -p archive
mv *.py genus_update_report.csv final_summary.md archive/

# Option 2: Delete files
rm *.py genus_update_report.csv final_summary.md
```

## Post-Cleanup

After cleanup, update any documentation or README files that might reference the root directory scripts to point to their new locations.