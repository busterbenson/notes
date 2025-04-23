# Archived Scripts

This directory contains scripts that are no longer used in the current 8-Bit Oracle card generation workflow but are preserved for reference.

## Scripts from Previous Workflow

### Scripts That Referenced the Compiled Directory
These scripts were used in the previous workflow that relied on the compiled/ directory, which has been replaced by the new generate-card.py system:

- **association-generator.py** - Generated association data files in the compiled/ directory
- **generate-all-associations.py** - Generated all association files for all hexagrams
- **audit_resonant_seasons.py** - Audited resonant season calculations in compiled cards
- **fix_compiled_cards.py** - Fixed issues in compiled card files
- **enhance_compiled_cards.py** - Enhanced compiled card files with additional data
- **ensure_decimal_lr.py** - Ensured decimal values used left-to-right bit priority
- **normalize_lr_decimal.py** - Normalized decimal values to use left-to-right bit priority

### Card Description Generation Scripts
These scripts were related to generating card descriptions, now replaced by the more comprehensive generation process:

- **create-description.py** - Created structured card descriptions in markdown format
- **create-enhanced-card.py** - Enhanced markdown cards with system data and image prompts
- **generate-card-description.py** - An earlier version of card description generation

## Current Workflow

The current workflow uses these primary scripts (in the parent directory):

1. **generate-card.py** - Creates complete card YAML files with all sections from the template
2. **generate-card.sh** - Shell wrapper for the Python script with validation and instructions
3. **generate-hexagram.sh** - Generates all four seasonal cards for a hexagram at once
4. **generate-all-cards.py** - Generates all 256 possible 8-bit Oracle cards

All card data is now stored in YAML format in the generated/ directory, ready to be filled with meaningful content.