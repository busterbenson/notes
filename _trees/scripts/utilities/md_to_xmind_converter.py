#!/usr/bin/env python3
"""
Markdown to XMind Converter

This script converts tree identification path markdown files to XMind format.
It enables bidirectional editing between markdown files and XMind mind maps.
"""

import re
import os
import sys
import time
import xml.etree.ElementTree as ET
import argparse
from pathlib import Path

# Constants
DEFAULT_PATH_DIR = "../../decision_trees/paths"
DEFAULT_OUTPUT = "../../decision_trees/paths/california_tree_guide_xmind_generated.xmind"
NODE_PATTERN = r'(│\s*)*[├└]── (.+)'

def generate_id():
    """Generate a unique ID for XMind nodes."""
    return f"ID_{int(time.time() * 1000)}"

def generate_timestamp():
    """Generate a timestamp for XMind nodes."""
    return str(int(time.time() * 1000))

def extract_node_text(line):
    """Extract node text from a markdown line."""
    match = re.search(NODE_PATTERN, line)
    if match:
        return match.group(2).strip()
    return line.strip()

def count_indent_level(line):
    """Count the indentation level of a markdown line."""
    # Count the number of '│' characters to determine level
    if '├──' in line or '└──' in line:
        return line.count('│')
    return 0

def parse_markdown_to_tree(md_file_path):
    """Convert markdown path file to a hierarchical tree structure."""
    with open(md_file_path, 'r') as f:
        content = f.read()
    
    tree = {'name': os.path.basename(md_file_path).replace('-path.md', '').title(), 'children': []}
    
    # Extract the content between the triple backticks
    markdown_content = re.search(r'```\n([\s\S]+?)\n```', content)
    if not markdown_content:
        print(f"Warning: No tree structure found in {md_file_path}")
        return tree
    
    markdown_content = markdown_content.group(1)
    lines = markdown_content.split('\n')
    
    # Process each line
    current_nodes = [tree]
    prev_level = -1
    
    for line in lines:
        if not line.strip():
            continue
            
        level = count_indent_level(line)
        text = extract_node_text(line)
        
        # Skip continuation lines (no tree markers)
        if '├──' not in line and '└──' not in line:
            continue
        
        # Adjust current path based on indentation
        if level > prev_level:
            # Going deeper
            pass
        elif level < prev_level:
            # Going back up
            current_nodes = current_nodes[:level+1]
        
        # Create new node
        new_node = {'name': text, 'children': []}
        
        # Add node to parent
        if not current_nodes[-1].get('children'):
            current_nodes[-1]['children'] = []
        current_nodes[-1]['children'].append(new_node)
        
        # Update for next iteration
        if level == prev_level:
            # Same level, replace last node
            current_nodes[-1] = new_node
        else:
            # Different level, append
            current_nodes.append(new_node)
        
        prev_level = level
    
    return tree

def extract_richcontent(node_text):
    """Extract rich content from node text if available."""
    # Check for descriptions in format: Text: Description
    parts = node_text.split(':', 1)
    if len(parts) > 1 and not parts[0].endswith(')'):
        return parts[0], parts[1].strip()
    return node_text, None

def create_richcontent_element(text):
    """Create richcontent XML element for node notes."""
    richcontent = ET.Element('richcontent', {'TYPE': 'NOTE'})
    html = ET.SubElement(richcontent, 'html')
    head = ET.SubElement(html, 'head')
    body = ET.SubElement(html, 'body')
    p = ET.SubElement(body, 'p')
    p.text = text
    return richcontent

def convert_tree_to_xmind_nodes(parent_element, tree_node, level=0):
    """Recursively convert tree structure to XMind XML nodes."""
    timestamp = generate_timestamp()
    
    # Extract node text and richcontent
    node_text, note_text = extract_richcontent(tree_node['name'])
    
    # Create XML node
    node = ET.SubElement(parent_element, 'node', {
        'CREATED': timestamp,
        'ID': generate_id(),
        'MODIFIED': timestamp,
        'TEXT': node_text
    })
    
    # Add richcontent if available
    if note_text:
        node.append(create_richcontent_element(note_text))
    
    # Process children
    for child in tree_node.get('children', []):
        convert_tree_to_xmind_nodes(node, child, level + 1)
    
    return node

def generate_xmind_from_tree(tree, output_path):
    """Generate XMind XML from the tree structure."""
    # Create XML structure
    xmind_map = ET.Element('map', {'version': '1.0.1'})
    
    # Create root node
    root_timestamp = generate_timestamp()
    root_node = ET.SubElement(xmind_map, 'node', {
        'CREATED': root_timestamp,
        'ID': generate_id(),
        'MODIFIED': root_timestamp,
        'TEXT': tree['name'],
        'FOLDED': 'false',
        'COLOR': '#333333',
        'BACKGROUND_COLOR': '#F2F2F2',
        'STYLE': 'bubble'
    })
    
    # Add description for the root node
    richcontent = ET.SubElement(root_node, 'richcontent', {'TYPE': 'NOTE'})
    html = ET.SubElement(richcontent, 'html')
    head = ET.SubElement(html, 'head')
    body = ET.SubElement(html, 'body')
    p1 = ET.SubElement(body, 'p')
    p1.text = f"This mind map represents the {tree['name']} path for tree identification."
    p2 = ET.SubElement(body, 'p')
    p2.text = "It allows you to identify trees by observable features rather than technical botanical knowledge."
    
    # Process children
    for child in tree.get('children', []):
        convert_tree_to_xmind_nodes(root_node, child)
    
    # Write to file
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(xmind_map, encoding='utf-8').decode()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    print(f"XMind file generated: {output_path}")

def process_path_files(path_dir, output_file):
    """Process all path markdown files and combine them into a single XMind."""
    path_dir = Path(path_dir)
    
    # Find all *-path.md files
    path_files = list(path_dir.glob('*-path.md'))
    
    if not path_files:
        print(f"No path files found in {path_dir}")
        return
    
    print(f"Found {len(path_files)} path files")
    
    # Create root tree
    main_tree = {
        'name': 'California Tree Identification Guide',
        'children': []
    }
    
    # Process each path file
    for path_file in path_files:
        print(f"Processing {path_file.name}")
        tree = parse_markdown_to_tree(path_file)
        main_tree['children'].append(tree)
    
    # Generate XMind file
    generate_xmind_from_tree(main_tree, output_file)

def main():
    parser = argparse.ArgumentParser(description='Convert markdown path files to XMind format')
    parser.add_argument('--path-dir', help='Directory containing path markdown files', default=DEFAULT_PATH_DIR)
    parser.add_argument('--output', help='Output XMind file path', default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    
    process_path_files(args.path_dir, args.output)

if __name__ == "__main__":
    main()