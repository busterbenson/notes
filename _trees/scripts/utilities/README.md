# Utility Scripts

These scripts provide utility functions for working with the tree files and path coverage.

## Markdown to XMind Sync Tool

The primary tool is `sync_tree_docs.py`, which provides a unified interface for converting markdown files to XMind format and ensuring 100% correspondence.

### Key Features

- **100% correspondence** between markdown and XMind files
- **Markdown as source of truth** - edit markdown files, generate XMind for visualization
- **Node-level tracking** with persistent IDs and hashes
- **Proper XMind format** compatible with XMind application
- **Verification tools** to ensure perfect conversion

### Usage

#### Sync Markdown to XMind

```bash
./sync_tree_docs.py sync
```

This will:
1. Generate an XMind file from markdown files
2. Verify 100% correspondence between formats

#### Generate XMind Only

```bash
./sync_tree_docs.py generate
```

#### Verify Correspondence

```bash
./sync_tree_docs.py verify
```

For detailed verification results:

```bash
./sync_tree_docs.py verify --detailed
```

#### Open XMind File

```bash
./sync_tree_docs.py view
```

### Custom Paths

You can specify custom paths for the markdown directory and XMind file:

```bash
./sync_tree_docs.py sync --path-dir /path/to/markdown/files --xmind /path/to/output.xmind
```

## Validation Scripts

### `validate_tree_files.py`

Validates the structure and formatting of tree YAML files in the `/trees` directory.

**Usage:**
```bash
cd _trees  # Make sure you're in the _trees directory
python scripts/utilities/validate_tree_files.py
```

**Functionality:**
- Checks for required fields (common_name, scientific_name, etc.)
- Checks for required sections (Basic summary, Identification path, etc.)
- Validates proper quoting in fields
- Reports on files with "Unknown" genus values

### `validate_path_coverage.py`

Analyzes and validates tree and genus coverage across all path files and the mind map.

**Usage:**
```bash
cd _trees  # Make sure you're in the _trees directory
python scripts/utilities/validate_path_coverage.py
```

**Functionality:**
- Extracts tree species and genus references from all markdown path files
- Extracts tree species and genus references from the mind map XML
- Identifies species and genera missing from the mind map
- Identifies species and genera in the mind map but missing from path files
- Reports coverage percentages for each path file
- Helps ensure complete coverage across the identification guide

### `verify_correspondence.py`

Verifies the correspondence between markdown files and XMind mind map.

**Usage:**
```bash
python verify_correspondence.py --md-dir /path/to/markdown --xmind /path/to/xmind.xmind
```

**Functionality:**
- Checks for 100% node-level correspondence between formats
- Verifies text, notes, and structure match exactly
- Reports detailed discrepancies when found

## Workflow

1. **Edit markdown files** as the source of truth
2. **Run sync tool**: `./sync_tree_docs.py sync`
3. **View in XMind**: `./sync_tree_docs.py view`
4. **Repeat** when markdown files are updated

## Additional Documentation

- [Detailed Documentation](README_MARKDOWN_SOURCE.md) - In-depth explanation of the conversion process

## Adding New Utility Scripts

When adding new utility scripts:
1. Include comprehensive docstrings
2. Add a description to this README
3. Make the script executable (`chmod +x script_name.py`)
4. Test thoroughly before committing