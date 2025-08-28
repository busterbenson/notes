# California Tree Guide OPML Exports

These OPML (Outline Processor Markup Language) files contain the California Tree Guide decision trees in a format compatible with [Workflowy](https://workflowy.com/) and other outlining tools.

## What is OPML?

OPML is an XML-based format that represents outlines. It's commonly used to exchange data between outlining applications, mind mapping software, and other tools that work with hierarchical data.

## Available OPML Files

The following OPML files are available:

- `california_tree_guide_combined.opml` - **All identification paths combined in one file** (recommended)
- `california_tree_guide_shape_size.opml` - Shape or Size identification path
- `california_tree_guide_leaf_needle.opml` - Leaf/Needle identification path
- `california_tree_guide_bark.opml` - Bark identification path
- `california_tree_guide_cone_fruit_seed.opml` - Cone/Fruit/Seed identification path

## How to Use with Workflowy

To import these files into Workflowy:

1. Log in to your Workflowy account
2. Click on your username or profile icon (top-right)
3. Select "Import/Export"
4. Choose "Import" and select the OPML file
5. The tree structure will be imported as a new node in your Workflowy account

## Recommended File

The `california_tree_guide_combined.opml` file is recommended for most users as it contains all identification paths in a single file. Each path is organized under its own top-level node, making navigation easier while keeping all the content together.

## How These Files Were Generated

These OPML files were automatically generated from the markdown tree structure files in the California Tree Guide project using a custom conversion script. The script preserves the hierarchical structure and relationships between all nodes in the tree.

Each outline entry in the OPML corresponds to a single item in the original tree structure.

## Using the Conversion Tool

The OPML export utility supports two modes:

1. Converting a single markdown file to OPML:
   ```
   python3 markdown_to_opml.py output_file.opml input_file.md
   ```

2. Combining multiple markdown files into a single OPML file:
   ```
   python3 markdown_to_opml.py output_file.opml input_file1.md input_file2.md input_file3.md
   ```

## Special Notes

- Markdown links in the original files have been removed in the OPML format
- Special characters have been properly escaped for XML compatibility
- The overall structure matches the original decision tree exactly