# Markdown to XMind Conversion Tools

This package contains tools for converting tree identification markdown files to XMind format with 100% correspondence. The markdown files are treated as the source of truth, and the XMind file is generated to maintain perfect fidelity to the markdown structure.

## Tools

1. **markdown_to_xmind_zip.py**: Converts markdown path files to XMind format with perfect fidelity (creates a proper XMind zip file)
2. **verify_correspondence.py**: Verifies that the XMind file perfectly corresponds to the markdown files
3. **markdown_to_xmind.py**: (Legacy) Generates XML format that may not be directly compatible with XMind application

## Key Features

- **100% correspondence** between markdown and XMind files
- **Node-level tracking** with persistent IDs and hashes
- **Structural preservation** including node order and hierarchy
- **Content fidelity** for text and notes
- **Verification tools** to ensure perfect conversion

## How It Works

### Enhanced XMind Generation

The `markdown_to_xmind.py` script uses several techniques to ensure perfect correspondence:

1. **Unique Node Identification**:
   - Each node is assigned a stable hash based on its content, level, and path
   - This hash is stored as metadata in the XMind file
   - A mapping file tracks the relationship between node hashes and IDs

2. **Exact Structure Preservation**:
   - Indentation levels in markdown map directly to XMind hierarchy
   - Node order is preserved exactly as in the markdown
   - Line numbers from markdown are stored as metadata

3. **Content Fidelity**:
   - Node text is preserved exactly
   - Notes and descriptions are stored in richcontent elements
   - Special formatting is handled consistently

4. **Source Tracking**:
   - The XMind file includes metadata indicating it was generated from markdown
   - Path information is preserved to track which markdown file each node came from

### Verification

The `verify_correspondence.py` script checks that the XMind file perfectly corresponds to the markdown files by:

1. Extracting the tree structure from both formats
2. Comparing node sets using hash-based identification
3. Checking for missing or extra nodes
4. Verifying node content and notes match exactly
5. Confirming node order is preserved
6. Providing detailed reports on any discrepancies

## Usage

### Generate XMind from Markdown

```bash
python markdown_to_xmind_zip.py --path-dir /path/to/markdown/files --output /path/to/output.xmind
```

Default paths:
- Markdown files: `../../decision_trees/paths/*.md`
- Output XMind: `../../decision_trees/paths/california_tree_guide_xmind_generated.xmind`
- Mapping file: `../../decision_trees/paths/node_mapping.json`

### Verify Correspondence

```bash
python verify_correspondence.py --md-dir /path/to/markdown/files --xmind /path/to/xmind/file.xmind
```

For detailed information about any discrepancies:

```bash
python verify_correspondence.py --detailed
```

## Workflow

1. **Edit markdown files** as the source of truth
2. **Generate XMind** using the `markdown_to_xmind.py` script
3. **Verify correspondence** using the `verify_correspondence.py` script
4. **View in XMind** to visualize the tree structure
5. **Repeat** when markdown files are updated

## Limitations

- The XMind file is read-only from a workflow perspective
- Changes should only be made to the markdown files
- Custom styling in XMind will be lost when regenerating from markdown

## Requirements

- Python 3.6 or higher
- ElementTree XML library (included in standard Python)