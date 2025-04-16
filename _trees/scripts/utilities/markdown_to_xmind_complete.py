#!/usr/bin/env python3
"""
Markdown to XMind Converter (Complete Version)

This completely redesigned script properly converts the tree identification 
markdown files to XMind format, with full fix for nesting issues.
"""

import re
import os
import sys
import time
import json
import hashlib
import xml.etree.ElementTree as ET
import argparse
from pathlib import Path
import zipfile
import io
import uuid
import shutil
import tempfile

# Constants
DEFAULT_PATH_DIR = "/Users/buster/projects/notes/_trees/decision_trees/paths"
DEFAULT_OUTPUT = "/Users/buster/projects/notes/_trees/decision_trees/paths/export/california_tree_guide.xmind"
MAPPING_FILE = "node_mapping.json"

def generate_id():
    """Generate a unique ID for XMind nodes."""
    return str(uuid.uuid4())

def generate_timestamp():
    """Generate a timestamp for XMind nodes."""
    return str(int(time.time() * 1000))

def extract_node_text(line):
    """Extract node text from a markdown line."""
    # Match tree structure: ├── or └── followed by text
    match = re.search(r'[├└]── (.*)', line)
    if match:
        return match.group(1).strip()
    return line.strip()

def hash_node(text, level, path):
    """Generate a stable hash for a node based on text, level, and path."""
    node_info = f"{path}:{level}:{text}"
    return hashlib.md5(node_info.encode()).hexdigest()

def get_indent_level(line):
    """
    Get indent level based on the number of leading pipe (│) characters
    and spaces, more accurate than just counting pipes.
    """
    indent = line.index('├──') if '├──' in line else line.index('└──') if '└──' in line else 0
    # Normalize indent to logical levels (each level is 4 characters: "│   ")
    level = indent // 4 if indent else 0
    return level

def parse_markdown_structure(md_content):
    """Parse markdown path file to extract tree structure."""
    # Extract the title
    title_match = re.search(r'^# (.*)', md_content)
    title = title_match.group(1) if title_match else "Untitled Path"
    
    # Extract the description (text between title and first code block)
    description = re.search(r'^# .*?\n\n(.*?)(?=```|\n\n)', md_content, re.DOTALL)
    description_text = description.group(1).strip() if description else None
    
    # Extract the tree structure (text between triple backticks)
    tree_match = re.search(r'```\n([\s\S]+?)\n```', md_content)
    tree_text = tree_match.group(1) if tree_match else None
    
    return title, description_text, tree_text

def build_tree_structure(tree_text, node_mapping=None):
    """
    Build a complete tree structure from markdown text with proper nesting.
    """
    if node_mapping is None:
        node_mapping = {}
    
    if not tree_text:
        return None, node_mapping
    
    # Split into lines
    lines = tree_text.split('\n')
    
    # Create a root node
    root = {
        'name': "Root",
        'id': generate_id(),
        'children': [],
        'level': -1,
        'hash': hash_node("Root", -1, "Root")
    }
    
    # Keep track of the last node at each level
    nodes_by_level = {-1: root}
    
    # Process each line
    line_number = 0
    for line in lines:
        line_number += 1
        if not line.strip() or ('├──' not in line and '└──' not in line):
            continue
        
        # Get indent level
        level = get_indent_level(line)
        
        # Extract node text
        text = extract_node_text(line)
        
        # Extract notes if present (after a colon, not inside parentheses)
        notes = None
        if ': ' in text and not text.endswith(')') and not '->' in text and not '→' in text:
            parts = text.split(': ', 1)
            text = parts[0]
            notes = parts[1]
        
        # Find the parent node (one level up)
        parent_level = level - 1
        while parent_level not in nodes_by_level and parent_level >= -1:
            parent_level -= 1
        
        parent = nodes_by_level.get(parent_level, root)
        
        # Calculate path for node
        if parent == root:
            path = [text]
        else:
            path = parent.get('path', []) + [text]
        
        # Create node hash
        node_hash = hash_node(text, level, '/'.join(path))
        
        # Create new node
        node = {
            'name': text,
            'id': node_mapping.get(node_hash, generate_id()),
            'children': [],
            'level': level,
            'path': path,
            'line': line_number,
            'hash': node_hash
        }
        
        # Store node ID in mapping
        node_mapping[node_hash] = node['id']
        
        # Add notes if present
        if notes:
            node['notes'] = notes
        
        # Add node to parent's children
        parent['children'].append(node)
        
        # Update last node at this level
        nodes_by_level[level] = node
        
        # Clear out any deeper levels as they're no longer valid parents
        deeper_levels = [l for l in nodes_by_level.keys() if l > level]
        for l in deeper_levels:
            if l in nodes_by_level:
                del nodes_by_level[l]
    
    return root, node_mapping

def parse_path_file(file_path, node_mapping=None):
    """Parse a path file and build its tree structure."""
    if node_mapping is None:
        node_mapping = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None, node_mapping
    
    # Extract path name from filename
    path_name = Path(file_path).stem.replace('-path', ' Path').title()
    
    # Parse markdown structure
    title, description, tree_text = parse_markdown_structure(content)
    
    # If title extracted, use it instead of filename
    if title:
        path_name = title
    
    # Build tree structure
    root, node_mapping = build_tree_structure(tree_text, node_mapping)
    
    if not root:
        print(f"Warning: Could not build tree for {file_path}")
        return None, node_mapping
    
    # Update root node with path information
    root['name'] = path_name
    if description:
        root['notes'] = description
    
    return root, node_mapping

def create_xmind_content_xml(forest, root_title="California Tree Identification Guide"):
    """Create XMind content XML from tree structure."""
    # Root element
    root = ET.Element("xmap-content")
    root.set("version", "1.0")
    
    # Create sheet element
    sheet = ET.SubElement(root, "sheet")
    sheet.set("id", generate_id())
    sheet.set("timestamp", generate_timestamp())
    
    # Sheet title
    title = ET.SubElement(sheet, "title")
    title.text = root_title
    
    # Create topic structure
    topic = ET.SubElement(sheet, "topic")
    topic.set("id", generate_id())
    topic.set("timestamp", generate_timestamp())
    
    # Root topic title
    topic_title = ET.SubElement(topic, "title")
    topic_title.text = "What catches my eye about this tree?"
    
    # Add children for each path
    child_topic = ET.SubElement(topic, "children")
    topics_el = ET.SubElement(child_topic, "topics")
    topics_el.set("type", "attached")
    
    # Process each path tree
    for tree in forest:
        if not tree or 'children' not in tree or not tree['children']:
            continue
        
        # Extract the first level of the tree (the path itself)
        path_node = tree
        
        # Create the path topic
        path_topic = ET.SubElement(topics_el, "topic")
        path_topic.set("id", path_node.get('id', generate_id()))
        path_topic.set("timestamp", generate_timestamp())
        
        # Path title
        path_title = ET.SubElement(path_topic, "title")
        path_title.text = path_node['name']
        
        # Add notes if present
        if 'notes' in path_node:
            notes_el = ET.SubElement(path_topic, "notes")
            plain_el = ET.SubElement(notes_el, "plain")
            plain_el.text = path_node['notes']
        
        # Process all children
        add_children_to_topic(path_topic, path_node)
    
    return ET.tostring(root, encoding='utf-8', xml_declaration=True)

def add_children_to_topic(parent_el, node):
    """Recursively add children to a topic element."""
    if not node.get('children'):
        return
    
    # Create children element
    children_el = ET.SubElement(parent_el, "children")
    topics_el = ET.SubElement(children_el, "topics")
    topics_el.set("type", "attached")
    
    # Add each child
    for child in node['children']:
        topic_el = ET.SubElement(topics_el, "topic")
        topic_el.set("id", child['id'])
        topic_el.set("timestamp", generate_timestamp())
        
        # Title
        title_el = ET.SubElement(topic_el, "title")
        title_el.text = child['name']
        
        # Add notes if present
        if 'notes' in child:
            notes_el = ET.SubElement(topic_el, "notes")
            plain_el = ET.SubElement(notes_el, "plain")
            plain_el.text = child['notes']
        
        # Process children recursively
        add_children_to_topic(topic_el, child)

def create_xmind_styles_xml():
    """Create a minimal styles.xml for XMind."""
    styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<xmap-styles version="2.0">
    <automatic-styles>
    </automatic-styles>
</xmap-styles>"""
    return styles_xml.encode('utf-8')

def create_xmind_manifest_xml():
    """Create manifest.xml for XMind."""
    manifest_xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<manifest xmlns="urn:xmind:xmap:xmlns:manifest:1.0">
  <file-entry full-path="content.xml" media-type="text/xml"/>
  <file-entry full-path="styles.xml" media-type="text/xml"/>
</manifest>"""
    return manifest_xml.encode('utf-8')

def generate_xmind_zip(forest, output_file, root_title="California Tree Identification Guide"):
    """Generate a XMind ZIP file that can be opened in XMind application."""
    try:
        # Create the necessary XML content
        content_xml = create_xmind_content_xml(forest, root_title)
        styles_xml = create_xmind_styles_xml()
        manifest_xml = create_xmind_manifest_xml()
        
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Create a ZIP file
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add the XML content to the ZIP
            zipf.writestr("content.xml", content_xml)
            zipf.writestr("styles.xml", styles_xml)
            zipf.writestr("META-INF/manifest.xml", manifest_xml)
        
        print(f"Generated XMind file: {output_file}")
        return True
    except Exception as e:
        print(f"Error generating XMind ZIP file: {e}")
        return False

def main():
    """Main function to process command line arguments and generate XMind file."""
    parser = argparse.ArgumentParser(description='Convert markdown tree files to XMind format')
    parser.add_argument('--path-dir', default=DEFAULT_PATH_DIR, help='Directory containing path markdown files')
    parser.add_argument('--output', default=DEFAULT_OUTPUT, help='Output XMind file path')
    parser.add_argument('--mapping', default=MAPPING_FILE, help='Node mapping file name')
    
    args = parser.parse_args()
    
    # Validate input directory
    if not os.path.isdir(args.path_dir):
        print(f"Error: Path directory '{args.path_dir}' does not exist or is not a directory")
        sys.exit(1)
    
    # Find all path files
    path_files = []
    for file in os.listdir(args.path_dir):
        if file.endswith('-path.md') and not file.startswith('template') and not file.startswith('.'):
            path_files.append(os.path.join(args.path_dir, file))
    
    # Check if we found any files
    if not path_files:
        print(f"No path files found in {args.path_dir}")
        sys.exit(1)
    
    print(f"Found {len(path_files)} path files")
    
    # Load existing node mapping if available
    node_mapping = {}
    mapping_path = os.path.join(args.path_dir, args.mapping)
    if os.path.exists(mapping_path):
        try:
            with open(mapping_path, 'r') as f:
                node_mapping = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load existing node mapping: {e}")
    
    # Process all path files
    forest = []
    for file_path in path_files:
        print(f"Processing {os.path.basename(file_path)}")
        tree, node_mapping = parse_path_file(file_path, node_mapping)
        if tree:
            forest.append(tree)
    
    # Check if we successfully parsed any trees
    if not forest:
        print("No trees parsed successfully")
        sys.exit(1)
    
    # Generate XMind file
    success = generate_xmind_zip(forest, args.output)
    
    # Save node mapping
    if success:
        try:
            with open(mapping_path, 'w') as f:
                json.dump(node_mapping, f)
            print(f"Node mapping saved: {mapping_path}")
            print("Conversion complete!")
        except Exception as e:
            print(f"Warning: Could not save node mapping: {e}")
    else:
        print("Failed to generate XMind file")
        sys.exit(1)

if __name__ == "__main__":
    main()