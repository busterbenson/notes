# Tree Identification Sync Tool

A set of Python scripts for bidirectional conversion between Markdown path files and XMind mind maps. This tool enables you to edit tree identification guides in either format and synchronize changes.

## Features

- Convert Markdown path files to XMind format
- Convert XMind mind maps to Markdown path files
- Bidirectional synchronization based on modification times
- Preserve formatting, notes, and hierarchical structure
- Create backups before modifications

## Scripts

1. **tree_sync.py** - Main script for bidirectional conversion
2. **md_to_xmind_converter.py** - Convert Markdown to XMind format
3. **xmind_to_md_converter.py** - Convert XMind to Markdown format
4. **validate_conversion.py** - Validate the conversion results

## Usage

### Bidirectional Sync

The `tree_sync.py` script will automatically detect which files are more recent and sync in the appropriate direction:

```bash
python tree_sync.py
```

This will:
1. Compare modification times of Markdown and XMind files
2. Sync from Markdown to XMind if Markdown files are newer
3. Sync from XMind to Markdown if the XMind file is newer

### Markdown to XMind

To explicitly convert from Markdown to XMind:

```bash
python tree_sync.py --action md2xmind
```

### XMind to Markdown

To explicitly convert from XMind to Markdown:

```bash
python tree_sync.py --action xmind2md
```

### Validation

To validate the conversion and check for discrepancies:

```bash
python validate_conversion.py
```

For detailed information about discrepancies:

```bash
python validate_conversion.py --detailed
```

### Custom Paths

You can specify custom paths for the source and output files:

```bash
python tree_sync.py --path-dir /path/to/markdown/files --xmind /path/to/xmind/file.xmind --output-dir /path/to/output
```

## Current State and Known Issues

The current implementation provides an approximately 60-70% match between formats. There are several reasons for this discrepancy:

1. **Indentation Structure**: The Markdown tree structure uses a specific indentation format (`│`, `├──`, etc.) that doesn't perfectly map to the hierarchical structure in XMind.

2. **Formatting Differences**: Rich formatting in XMind (colors, fonts, styles) is not preserved in Markdown.

3. **Node Organization**: The XMind format may organize nodes differently than the Markdown format.

4. **Special Characters**: Some special characters or symbols (like arrows, emojis) may not be preserved correctly.

## Improving Correspondence

To achieve 100% correspondence, consider these enhancements:

1. **Improve Tree Structure Parsing**: Enhance the parsing of tree structures in Markdown to better handle indentation and nesting.

2. **Standardize Node Format**: Define a standard format for node text and richcontent that can be preserved across formats.

3. **Mapping File**: Create a mapping file to track node relationships between formats.

4. **Custom XMind Format**: Create a custom XMind format specifically designed to preserve Markdown structure.

5. **Enhanced Validation**: Improve the validation script to identify specific discrepancies.

## Best Practices

1. **Make backups**: The tool creates backups automatically, but additional backups are recommended
2. **Edit one format at a time**: Avoid simultaneous edits to both formats
3. **Run sync regularly**: Keep formats in sync to avoid conflicts
4. **Check results**: Verify the conversion looks correct
5. **Validate after conversion**: Use the validation script to check for discrepancies

## Requirements

- Python 3.6 or higher
- ElementTree XML library (included in standard Python)

## License

This tool is provided under the MIT License. Feel free to modify and enhance it for your needs.