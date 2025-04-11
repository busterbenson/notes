# Archived Scripts

This directory contains scripts that are no longer used in the current 8-Bit Oracle card generation workflow but are preserved for reference.

## Scripts

### card-generator.py
- **Purpose**: Generated YAML files for cards in the v3/ directory
- **Reason for archiving**: The workflow now uses markdown files directly in the completed/ directory instead of YAML files
- **Replacement**: `create-description.py` and `create-enhanced-card.py` together generate markdown files directly

### convert_yaml_to_md.py
- **Purpose**: Migration utility to convert YAML files from v3/ to markdown files in completed/
- **Reason for archiving**: One-time migration is complete, no longer needed for ongoing work
- **Replacement**: Not needed; all new cards are generated directly as markdown

### generate-card-description.py
- **Purpose**: An earlier version of card description generation
- **Reason for archiving**: Appears to be superseded by `create-description.py`
- **Replacement**: `create-description.py` provides this functionality

## Current Workflow

The current workflow uses these primary scripts:

1. `association-generator.py` - Generates raw associations in YAML format in compiled/
2. `create-description.py` - Creates initial markdown card template
3. `create-enhanced-card.py` - Enhances markdown cards with system data and image prompt
4. `generate-card.sh` - Main orchestration script that ties everything together

All card data is now stored in markdown format in the completed/ directory.