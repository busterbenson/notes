#!/usr/bin/env python3
"""
Tree Identification Sync Tool

A bidirectional converter between markdown path files and XMind mind maps.
This tool enables editing in either format and synchronizing changes.
"""

import os
import sys
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET
import re
import time
import shutil

# Constants
DEFAULT_PATH_DIR = "../../decision_trees/paths"
DEFAULT_XMIND_FILE = "../../decision_trees/paths/california_tree_guide_xmind_complete.xmind"
DEFAULT_OUTPUT_DIR = "../../decision_trees/paths/generated"
NODE_PATTERN = r'(│\s*)*[├└]── (.+)'

def generate_id():
    """Generate a unique ID for XMind nodes."""
    return f"ID_{int(time.time() * 1000)}_{int(1000 * (time.time() % 1))}"

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
    try:
        with open(md_file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading markdown file {md_file_path}: {e}")
        return None
    
    # Extract path name from filename
    path_name = Path(md_file_path).stem.replace('-path', ' Path').title()
    tree = {'name': path_name, 'children': []}
    
    # Extract description from markdown
    description = re.search(r'^# .*?\n\n(.*?)(?=```|\n\n)', content, re.DOTALL)
    if description:
        tree['notes'] = description.group(1).strip()
    
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
        
        # Check for descriptions (text after colon)
        if ': ' in text and not text.startswith('→'):
            parts = text.split(': ', 1)
            new_node['name'] = parts[0]
            new_node['notes'] = parts[1]
        
        # Add node to parent
        if not current_nodes[-1].get('children'):
            current_nodes[-1]['children'] = []
        current_nodes[-1]['children'].append(new_node)
        
        # Update for next iteration
        if level == prev_level:
            # Same level, replace last node in current_nodes
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
        return parts[0].strip(), parts[1].strip()
    return node_text, None

def create_richcontent_element(text):
    """Create richcontent XML element for node notes."""
    richcontent = ET.Element('richcontent', {'TYPE': 'NOTE'})
    html = ET.SubElement(richcontent, 'html')
    head = ET.SubElement(html, 'head')
    body = ET.SubElement(html, 'body')
    
    # Split text into paragraphs
    paragraphs = text.split('\n')
    for para in paragraphs:
        p = ET.SubElement(body, 'p')
        p.text = para.strip()
    
    return richcontent

def convert_tree_to_xmind_nodes(parent_element, tree_node, level=0):
    """Recursively convert tree structure to XMind XML nodes."""
    timestamp = generate_timestamp()
    
    # Create XML node
    node_attrs = {
        'CREATED': timestamp,
        'ID': generate_id(),
        'MODIFIED': timestamp,
        'TEXT': tree_node['name']
    }
    
    # Add styling for root nodes
    if level == 0:
        node_attrs.update({
            'COLOR': '#333333',
            'BACKGROUND_COLOR': '#F2F2F2',
            'STYLE': 'bubble'
        })
    
    node = ET.SubElement(parent_element, 'node', node_attrs)
    
    # Add richcontent if available
    if tree_node.get('notes'):
        node.append(create_richcontent_element(tree_node['notes']))
    
    # Process children
    for child in tree_node.get('children', []):
        convert_tree_to_xmind_nodes(node, child, level + 1)
    
    return node

def generate_xmind_from_trees(trees, output_path):
    """Generate XMind XML from multiple tree structures."""
    # Create XML structure
    xmind_map = ET.Element('map', {'version': '1.0.1'})
    
    # Create root node
    root_timestamp = generate_timestamp()
    root_node = ET.SubElement(xmind_map, 'node', {
        'CREATED': root_timestamp,
        'ID': generate_id(),
        'MODIFIED': root_timestamp,
        'TEXT': 'California Tree Identification Guide',
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
    p1.text = "This mind map represents the California Tree Identification Guide."
    p2 = ET.SubElement(body, 'p')
    p2.text = "It allows you to identify trees by observable features rather than technical botanical knowledge."
    p3 = ET.SubElement(body, 'p')
    p3.text = "The guide covers trees commonly found in California."
    
    # Process each path tree
    for tree in trees:
        convert_tree_to_xmind_nodes(root_node, tree)
    
    # Write to file
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(xmind_map, encoding='utf-8').decode()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    print(f"XMind file generated: {output_path}")

def extract_node_text_from_xml(node):
    """Extract text from a node element."""
    return node.attrib.get('TEXT', '').strip()

def extract_node_notes_from_xml(node):
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

def parse_xmind_to_trees(xmind_file):
    """Parse XMind XML to extract multiple tree structures."""
    try:
        tree = ET.parse(xmind_file)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing XMind file: {e}")
        return []
    
    # Find the main node (first node of the map)
    main_node = root.find('.//node')
    if main_node is None:
        print("No main node found in XMind file")
        return []
    
    # Find all path nodes (children of the main node)
    path_nodes = main_node.findall('./node')
    if not path_nodes:
        print("No path nodes found in XMind file")
        return []
    
    # Extract tree structures for each path
    trees = []
    for path_node in path_nodes:
        path_tree = extract_node_tree_from_xml(path_node)
        if path_tree:
            trees.append(path_tree)
    
    return trees

def extract_node_tree_from_xml(node):
    """Recursively extract node tree from XMind XML."""
    text = extract_node_text_from_xml(node)
    notes = extract_node_notes_from_xml(node)
    
    tree_node = {
        'name': text,
        'children': []
    }
    
    if notes:
        tree_node['notes'] = notes
    
    # Process child nodes
    for child in node.findall('./node'):
        tree_node['children'].append(extract_node_tree_from_xml(child))
    
    return tree_node

def format_markdown_tree_line(node_name, level):
    """Format a markdown line for tree structure."""
    indent = '│   ' * level
    marker = '├── '
    return f"{indent}{marker}{node_name}"

def node_tree_to_markdown_lines(node, level=0, lines=None):
    """Convert a node tree to markdown lines."""
    if lines is None:
        lines = []
    
    # Skip the root node
    if level > 0:
        node_text = node['name']
        if node.get('notes') and not node_text.endswith(')'):
            node_text = f"{node_text}: {node['notes']}"
        
        lines.append(format_markdown_tree_line(node_text, level - 1))
    
    # Process children
    for child in node.get('children', []):
        node_tree_to_markdown_lines(child, level + 1, lines)
    
    return lines

def generate_markdown_from_tree(tree):
    """Generate markdown content from a tree structure."""
    path_name = tree['name']
    
    # Create markdown header
    header = f"# {path_name}\n\n"
    
    # Add description
    if tree.get('notes'):
        header += f"{tree['notes']}\n\n"
    else:
        header += "Look at the features of your tree.\n\n"
    
    # Generate the tree structure
    tree_lines = node_tree_to_markdown_lines(tree)
    
    # Format as code block
    tree_content = "```\n" + "\n".join(tree_lines) + "\n```\n\n"
    
    # Add footer with links to other paths
    footer = "## What Else Can You See?\n"
    paths = [
        "leaf-needle-path.md",
        "bark-path.md",
        "flower-path.md",
        "smell-path.md",
        "cone-fruit-seed-path.md",
        "shape-size-path.md",
        "winter-detective-path.md"
    ]
    
    # Get the current path
    current_path = path_name.lower().replace(' path', '-path.md')
    
    # Create links to other paths
    for path in paths:
        if path != current_path:
            path_title = path.replace('-path.md', '').replace('-', '/')
            path_title = ' '.join(word.capitalize() for word in path_title.split('/'))
            footer += f"* If the {path_title} is distinctive: [{path_title} Path]({path})\n"
    
    return header + tree_content + footer

def markdown_to_xmind(path_dir, output_file):
    """Convert markdown path files to XMind format."""
    path_dir = Path(path_dir)
    output_file = Path(output_file)
    
    # Create output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Find all *-path.md files
    path_files = list(path_dir.glob('*-path.md'))
    
    if not path_files:
        print(f"No path files found in {path_dir}")
        return False
    
    print(f"Found {len(path_files)} path files")
    
    # Parse each markdown file to a tree structure
    trees = []
    for path_file in sorted(path_files):
        print(f"Processing {path_file.name}")
        tree = parse_markdown_to_tree(path_file)
        if tree:
            trees.append(tree)
    
    if not trees:
        print("No valid trees extracted from markdown files")
        return False
    
    # Generate XMind file
    generate_xmind_from_trees(trees, output_file)
    return True

def xmind_to_markdown(xmind_file, output_dir):
    """Convert XMind format to markdown path files."""
    xmind_file = Path(xmind_file)
    output_dir = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Parse XMind file to tree structures
    trees = parse_xmind_to_trees(xmind_file)
    
    if not trees:
        print("No valid trees extracted from XMind file")
        return False
    
    print(f"Found {len(trees)} trees in XMind file")
    
    # Generate markdown files
    for tree in trees:
        path_name = tree['name'].lower().replace(' path', '-path')
        file_name = f"{path_name}.md"
        output_file = output_dir / file_name
        
        print(f"Generating {file_name}")
        
        markdown_content = generate_markdown_from_tree(tree)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"  Generated: {output_file}")
    
    return True

def sync_markdown_to_xmind(path_dir, xmind_file):
    """Sync markdown files to XMind file."""
    # Create a backup of the XMind file if it exists
    xmind_path = Path(xmind_file)
    if xmind_path.exists():
        backup_path = xmind_path.with_suffix('.bak')
        shutil.copy2(xmind_path, backup_path)
        print(f"Created backup: {backup_path}")
    
    # Convert markdown to XMind
    success = markdown_to_xmind(path_dir, xmind_file)
    
    if success:
        print(f"Successfully synced markdown files to XMind: {xmind_file}")
    else:
        print("Failed to sync markdown files to XMind")
    
    return success

def sync_xmind_to_markdown(xmind_file, output_dir):
    """Sync XMind file to markdown files."""
    # Create backups of existing markdown files
    output_path = Path(output_dir)
    if output_path.exists():
        for md_file in output_path.glob('*-path.md'):
            backup_path = md_file.with_suffix('.md.bak')
            shutil.copy2(md_file, backup_path)
            print(f"Created backup: {backup_path}")
    
    # Convert XMind to markdown
    success = xmind_to_markdown(xmind_file, output_dir)
    
    if success:
        print(f"Successfully synced XMind to markdown files in: {output_dir}")
    else:
        print("Failed to sync XMind to markdown files")
    
    return success

def bidirectional_sync(path_dir, xmind_file, output_dir=None):
    """Perform bidirectional sync based on modification times."""
    path_dir = Path(path_dir)
    xmind_file = Path(xmind_file)
    
    if output_dir is None:
        output_dir = path_dir
    else:
        output_dir = Path(output_dir)
    
    # Check if XMind file exists
    if not xmind_file.exists():
        print(f"XMind file does not exist: {xmind_file}")
        print("Generating XMind file from markdown files...")
        return sync_markdown_to_xmind(path_dir, xmind_file)
    
    # Check modification times
    xmind_mtime = xmind_file.stat().st_mtime
    
    # Find the most recently modified markdown file
    markdown_files = list(path_dir.glob('*-path.md'))
    if not markdown_files:
        print(f"No markdown files found in {path_dir}")
        print("Generating markdown files from XMind file...")
        return sync_xmind_to_markdown(xmind_file, output_dir)
    
    latest_md_mtime = max(f.stat().st_mtime for f in markdown_files)
    
    if latest_md_mtime > xmind_mtime:
        print("Markdown files are more recent than XMind file")
        print("Syncing markdown to XMind...")
        return sync_markdown_to_xmind(path_dir, xmind_file)
    else:
        print("XMind file is more recent than markdown files")
        print("Syncing XMind to markdown...")
        return sync_xmind_to_markdown(xmind_file, output_dir)

def main():
    parser = argparse.ArgumentParser(description='Bidirectional converter between markdown path files and XMind mind maps')
    parser.add_argument('--action', choices=['md2xmind', 'xmind2md', 'sync'], default='sync',
                        help='Action to perform (default: sync)')
    parser.add_argument('--path-dir', default=DEFAULT_PATH_DIR,
                        help=f'Directory containing path markdown files (default: {DEFAULT_PATH_DIR})')
    parser.add_argument('--xmind', default=DEFAULT_XMIND_FILE,
                        help=f'Path to XMind file (default: {DEFAULT_XMIND_FILE})')
    parser.add_argument('--output-dir', default=None,
                        help=f'Output directory for generated files (default: same as input)')
    
    args = parser.parse_args()
    
    if args.action == 'md2xmind':
        sync_markdown_to_xmind(args.path_dir, args.xmind)
    elif args.action == 'xmind2md':
        output_dir = args.output_dir if args.output_dir else args.path_dir
        sync_xmind_to_markdown(args.xmind, output_dir)
    else:  # sync
        output_dir = args.output_dir if args.output_dir else args.path_dir
        bidirectional_sync(args.path_dir, args.xmind, output_dir)

if __name__ == "__main__":
    main()