# XMind Conversion Process

This document explains how to convert the markdown-based decision tree paths to XMind format.

## Overview

The decision trees for the California Tree Guide are maintained in markdown format, which serves as the source of truth. We generate XMind files for visualization and interactive exploration of these decision trees.

## Using the Conversion Script

The `markdown_to_xmind_complete.py` script converts all path files to a single XMind file that maintains the proper hierarchical structure.

### Basic Usage

```bash
python3 /Users/buster/projects/notes/_trees/scripts/utilities/markdown_to_xmind_complete.py
```

This will use the default settings to:
1. Process all path files in `/Users/buster/projects/notes/_trees/decision_trees/paths/`
2. Generate the XMind file at `/Users/buster/projects/notes/_trees/decision_trees/paths/export/california_tree_guide.xmind`
3. Save node mapping information to maintain consistency between runs

### Custom Usage

You can customize the directories and filenames:

```bash
python3 /Users/buster/projects/notes/_trees/scripts/utilities/markdown_to_xmind_complete.py \
  --path-dir /path/to/markdown/files \
  --output /path/to/output/file.xmind \
  --mapping custom_mapping_file.json
```

## Maintaining Consistency

The script uses a node mapping file to ensure consistency between runs. This means that node positions and relationships will remain stable even if you regenerate the XMind file after changes to the markdown files.

## Troubleshooting

If you encounter issues with the XMind file:

1. **Missing Paths**: Make sure all path files end with `-path.md`
2. **Improper Nesting**: Check the indentation in your markdown files
3. **XMind Won't Open File**: Verify the file format by checking that it contains the expected XML files

## Key Improvements in the Latest Version

The current version of the script (`markdown_to_xmind_complete.py`) includes these important improvements:

1. **Proper Node Nesting**: Questions and their answers are correctly nested
2. **Full Path Coverage**: All path files are included in the output
3. **Consistent Node Relationships**: Hierarchical structure is maintained
4. **Robust Parsing**: Better handling of various markdown formatting patterns

## Generating the XMind File After Updates

Always regenerate the XMind file after making changes to any of the markdown path files:

1. Make your changes to the markdown files
2. Run the conversion script
3. Verify that the XMind file opens correctly and displays the expected structure
4. Check that questions and their answers are properly nested

## XMind File Location

The generated XMind file is stored in:
`/Users/buster/projects/notes/_trees/decision_trees/paths/export/california_tree_guide.xmind`