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

### create-description.py
- **Purpose**: Creates a structured card description in markdown format
- **Reason for archiving**: Functionality now integrated into `generate-card.py`
- **Replacement**: `generate-card.py` and `generate-card.sh` provide this functionality in a more comprehensive way

## Current Workflow

The current workflow uses these primary scripts:

1. `generate-card.py` - Creates complete card YAML files with all sections from the template
2. `generate-card.sh` - Shell wrapper for the Python script with validation and instructions
3. `generate-hexagram.sh` - Generates all four seasonal cards for a hexagram at once

All card data is now stored in YAML format in the generated/ directory, ready to be filled with meaningful content.
EOL < /dev/null