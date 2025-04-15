#!/usr/bin/env python3
"""
XMind to Markdown Converter

This script converts XMind mind maps to tree identification path markdown files.
It enables bidirectional editing between markdown files and XMind mind maps.
"""

import re
import os
import sys
import xml.etree.ElementTree as ET
import argparse
from pathlib import Path

# Constants
DEFAULT_XMIND_FILE = "../../decision_trees/paths/california_tree_guide_xmind_complete.xmind"
DEFAULT_OUTPUT_DIR = "../../decision_trees/paths/generated"

def extract_node_text(node):
    """Extract text from a node element."""
    return node.attrib.get('TEXT', '').strip()

def extract_node_notes(node):
    """Extract notes from a node element's richcontent."""
    richcontent = node.find('./richcontent[@TYPE="NOTE"]')
    if richcontent is not None:
        # Extract text from all paragraphs in the note
        paragraphs = []
        for p in richcontent.findall('.//p'):
            if p.text:
                paragraphs.append(p.text.strip())
        return '\n'.join(paragraphs)
    return None

def parse_xmind_to_tree(xmind_file):
    """Parse XMind XML to a tree structure."""
    try:
        tree = ET.parse(xmind_file)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing XMind file: {e}")
        return None
    
    # Find the main node (first node of the map)
    main_node = root.find('.//node')
    if main_node is None:
        print("No main node found in XMind file")
        return None
    
    # Extract the tree structure
    return extract_node_tree(main_node)

def extract_node_tree(node):
    """Recursively extract node tree from XMind XML."""
    text = extract_node_text(node)
    notes = extract_node_notes(node)
    
    tree_node = {
        'name': text,
        'notes': notes,
        'children': []
    }
    
    # Process child nodes
    for child in node.findall('./node'):
        tree_node['children'].append(extract_node_tree(child))
    
    return tree_node

def find_path_trees(main_tree):
    """Find all path trees in the main tree."""
    path_trees = []
    
    # Look for path trees in the children of the main tree
    for child in main_tree.get('children', []):
        name = child.get('name', '').lower()
        if 'path' in name:
            path_trees.append(child)
    
    return path_trees

def generate_markdown_line(node, level):
    """Generate a markdown line for a node at given level."""
    # Create proper indentation
    indent = '│   ' * level
    prefix = '├── ' if level > 0 else ''
    
    # Combine indentation, marker, and text
    line = f"{indent}{prefix}{node['name']}"
    
    return line

def node_tree_to_markdown(node, level=0):
    """Convert a node tree to markdown lines."""
    lines = []
    
    # Add current node
    if level > 0:  # Skip the root node
        lines.append(generate_markdown_line(node, level))
    
    # Process children
    for i, child in enumerate(node.get('children', [])):
        child_lines = node_tree_to_markdown(child, level + 1)
        lines.extend(child_lines)
    
    return lines

def generate_markdown_from_tree(tree, path_name):
    """Generate markdown content from a tree structure."""
    # Create markdown header
    header = f"# {path_name}\n\n"
    header += "Look at the features of your tree.\n\n"
    
    # Add notes from the tree if available
    if tree.get('notes'):
        header += f"{tree['notes']}\n\n"
    
    # Generate the tree structure
    tree_lines = node_tree_to_markdown(tree)
    
    # Format as code block
    tree_content = "```\n" + "\n".join(tree_lines) + "\n```\n\n"
    
    # Add footer
    footer = "## What Else Can You See?\n"
    footer += "* If the leaves or needles are distinctive: [Leaf/Needle Path](leaf-needle-path.md)\n"
    footer += "* If the bark has interesting texture or color: [Bark Path](bark-path.md)\n"
    footer += "* If the flowers are visible: [Flower Path](flower-path.md)\n"
    footer += "* If the leaves or needles have a smell when crushed: [Smell Path](smell-path.md)\n"
    footer += "* If you can see fruits, berries, or seeds: [Cone/Fruit/Seed Path](cone-fruit-seed-path.md)\n"
    footer += "* If the tree has a distinctive overall shape: [Shape/Size Path](shape-size-path.md)\n"
    
    return header + tree_content + footer

def process_xmind_file(xmind_file, output_dir):
    """Process an XMind file and generate markdown files."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Processing XMind file: {xmind_file}")
    main_tree = parse_xmind_to_tree(xmind_file)
    
    if not main_tree:
        print("Failed to parse XMind file")
        return
    
    # Find path trees
    path_trees = main_tree.get('children', [])
    
    if not path_trees:
        print("No path trees found in XMind file")
        return
    
    print(f"Found {len(path_trees)} path trees")
    
    # Generate markdown file for each path
    for path_tree in path_trees:
        path_name = path_tree.get('name', 'Unknown').replace(' Path', '').lower()
        file_name = f"{path_name}-path.md"
        output_file = output_dir / file_name
        
        print(f"Generating {file_name}")
        
        markdown_content = generate_markdown_from_tree(path_tree, path_tree.get('name', 'Unknown'))
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"  Generated: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Convert XMind mind maps to markdown path files')
    parser.add_argument('--xmind', help='Input XMind file path', default=DEFAULT_XMIND_FILE)
    parser.add_argument('--output-dir', help='Output directory for markdown files', default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    
    process_xmind_file(args.xmind, args.output_dir)

if __name__ == "__main__":
    main()