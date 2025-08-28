# Tree Utility Scripts

This directory contains utility scripts for managing and validating the California Tree Guide data files.

## Available Scripts

- `validate_tree_files.py` - Validates the format and structure of tree and genus YAML files
- `validate_shape_size_path_improved.py` - Checks if all trees mentioned in the shape-size path have corresponding files
- `markdown_to_xmind_complete.py` - Converts markdown decision trees to XMind format
- `generate_xmind.sh` - Shell script to easily regenerate the XMind file

## Tree File Validation

The `validate_tree_files.py` script validates all tree and genus YAML files to ensure they meet the required structure and formatting guidelines:

- Checks for all required sections and subsections
- Validates feature ID formatting
- Ensures seasonal data includes all seasons
- Verifies the structure of identification paths and detective steps

### Usage

To run the validation script:

```bash
# Create virtual environment (first time only)
python3 -m venv venv
source venv/bin/activate
pip install PyYAML

# Run the validation
python validate_tree_files.py [path_to_base_directory]
```

If no path is provided, it will use the default tree and genus directories.

### Validation Results

The script will produce a detailed report of any issues found, including:
- Missing required sections
- Invalid feature ID formats
- Missing seasonal information
- YAML parsing errors

## Shape-Size Path Tree Coverage Analysis

The shape-size-path.md file mentions many tree species and genera. We analyzed this file to determine which mentioned trees have corresponding YML files and which are missing.

### Summary

- **37** tree species mentioned in shape-size-path.md
- **25** genera mentioned in shape-size-path.md
- **29** tree species have existing files
- **8** tree species are missing files
- **25** genera have existing files (All genera are covered!)
- **0** genera are missing files

### Missing Items by Priority

#### High Priority (California Native Trees)
Only one California native tree is missing a file:

1. Bristlecone Pine (Pinus longaeva)

#### Medium Priority (Commonly Cultivated Trees)
These commonly cultivated trees are mentioned but missing files:

1. Tulip Tree (Liriodendron tulipifera)
2. Umbrella Pine (Sciadopitys verticillata)
3. Japanese Black Pine (Pinus thunbergii)
4. Date Palm (Phoenix dactylifera)

#### Low Priority (Trees to Consider Removing)
These trees are neither California natives nor commonly cultivated, so they could be removed from the path file:

1. Gum (Corymbia citriodora)
2. Ocotillo (Fouquieria splendens)
3. Black Mangrove (Avicennia germinans)

### Usage

To run the shape-size path validation script:

```bash
python3 validate_shape_size_path_improved.py
```

This will analyze the shape-size-path.md file and generate a report of missing trees and genera.