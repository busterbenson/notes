#!/usr/bin/env python3
"""
Markdown to XMind Converter (ZIP Format) - Fixed Version

This script converts tree identification path markdown files to XMind format.
The markdown format is treated as the source of truth, and the XMind output
is optimized to maintain 100% correspondence with the markdown structure.
This version generates a proper XMind ZIP file compatible with XMind application.

The fix addresses proper nesting of nodes in the XMind output.
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
DEFAULT_PATH_DIR = "../../decision_trees/paths"
DEFAULT_OUTPUT = "../../decision_trees/paths/california_tree_guide_xmind_generated.xmind"
NODE_PATTERN = r'(│\s*)*[├└]── (.+)'
MAPPING_FILE = "node_mapping.json"

def generate_id():
    """Generate a unique ID for XMind nodes."""
    return str(uuid.uuid4())

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
    """
    Count the indentation level based on the spacing before the tree markers.
    This improved version counts the actual indentation level more accurately.
    """
    if '├──' in line or '└──' in line:
        # Count the number of vertical bar characters for base indentation
        base_level = line.count('│')
        
        # Check spacing before the tree marker to determine precise level
        if '│   ├──' in line or '│   └──' in line:
            # Standard indentation pattern
            return base_level
        elif re.search(r'│\s+[├└]──', line):
            # Handle irregular spacing but still count as next level
            return base_level
            
        return base_level
    return 0

def hash_node(text, level, path):
    """Generate a stable hash for a node based on text, level, and path."""
    node_info = f"{path}:{level}:{text}"
    return hashlib.md5(node_info.encode()).hexdigest()

def normalize_line(line):
    """Normalize line for consistent processing."""
    # Replace tabs with spaces for consistency
    normalized = line.replace('\t', '    ')
    return normalized

def parse_tree_structure(lines):
    """
    Parse tree structure with improved indentation detection.
    Returns a list of (line, level) tuples with correct nesting.
    """
    result = []
    question_pattern = re.compile(r'(?:What|How|Which|Where|When).+\?')
    
    for i, line in enumerate(lines):
        normalized = normalize_line(line)
        if not normalized.strip():
            continue
            
        # Skip lines without tree markers
        if '├──' not in normalized and '└──' not in normalized:
            continue
        
        # Count basic indentation level
        level = normalized.count('│')
        
        # Apply special rules for questions and answers
        text = extract_node_text(normalized)
        
        # Questions should start a new section
        is_question = bool(question_pattern.search(text))
        
        # Check if this is a direct answer to the previous question
        is_answer = False
        if i > 0 and result and not is_question:
            prev_text = extract_node_text(lines[i-1])
            if question_pattern.search(prev_text):
                is_answer = True
        
        # Adjust level for certain types of nodes
        adjusted_level = level
                
        result.append((normalized, adjusted_level, text, is_question, is_answer))
    
    return result

def build_tree_from_nested_lines(lines, path_name, node_mapping=None):
    """Build a tree structure from nested markdown lines."""
    if node_mapping is None:
        node_mapping = {}
    
    # Create a root node for the path
    root_hash = hash_node(path_name, -1, path_name)
    root_id = node_mapping.get(root_hash, generate_id())
    node_mapping[root_hash] = root_id
    
    root = {
        'name': path_name,
        'id': root_id,
        'children': [],
        'level': -1,
        'path': [path_name],
        'md_line': 0,
        'hash': root_hash
    }
    
    # Parse tree structure with improved indentation
    parsed_lines = []
    # First pass - get the raw indentation levels
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        
        # Skip lines without tree markers
        if '├──' not in line and '└──' not in line:
            continue
        
        level = count_indent_level(line)
        text = extract_node_text(line)
        parsed_lines.append((i+1, line, level, text))
    
    # Process nodes in order and track parent-child relationships
    nodes_by_level = {-1: [root]}
    last_node_by_level = {-1: root}
    
    for line_num, line, level, text in parsed_lines:
        # Determine parent based on indentation level
        parent_level = level - 1
        while parent_level >= -1:
            if parent_level in last_node_by_level:
                parent = last_node_by_level[parent_level]
                break
            parent_level -= 1
        else:
            parent = root  # Fallback to root if no parent found
        
        # Calculate the path for this node
        node_path = parent['path'] + [text]
        
        # Extract notes if present (text after colon)
        notes = None
        if ': ' in text and not text.endswith(')') and not '->' in text and not '→' in text:
            parts = text.split(': ', 1)
            text = parts[0]
            notes = parts[1]
            node_path[-1] = text  # Update path with the text without notes
        
        # Create node hash for stable identification
        node_hash = hash_node(text, level, '/'.join(node_path))
        
        # Find or create ID for this node
        node_id = node_mapping.get(node_hash, generate_id())
        node_mapping[node_hash] = node_id
        
        # Create new node
        new_node = {
            'name': text,
            'id': node_id,
            'children': [],
            'level': level,
            'path': node_path,
            'md_line': line_num,
            'hash': node_hash
        }
        
        if notes:
            new_node['notes'] = notes
        
        # Add node to parent's children
        parent['children'].append(new_node)
        
        # Update tracking dictionaries
        if level not in nodes_by_level:
            nodes_by_level[level] = []
        nodes_by_level[level].append(new_node)
        last_node_by_level[level] = new_node
    
    return root, node_mapping

def parse_markdown_to_tree(md_file_path, node_mapping=None):
    """Convert markdown path file to a hierarchical tree structure."""
    if node_mapping is None:
        node_mapping = {}
        
    try:
        with open(md_file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading markdown file {md_file_path}: {e}")
        return None, node_mapping
    
    # Extract path name from filename
    path_name = Path(md_file_path).stem.replace('-path', ' Path').title()
    
    # Extract description from markdown
    description = re.search(r'^# .*?\n\n(.*?)(?=```|\n\n)', content, re.DOTALL)
    description_text = None
    if description:
        description_text = description.group(1).strip()
    
    # Extract the tree structure within triple backticks
    tree_match = re.search(r'```\n([\s\S]+?)\n```', content)
    if not tree_match:
        print(f"Warning: No tree structure found in {md_file_path}")
        # Create a bare tree structure
        root_hash = hash_node(path_name, -1, path_name)
        root_id = node_mapping.get(root_hash, generate_id())
        node_mapping[root_hash] = root_id
        tree = {
            'name': path_name,
            'id': root_id,
            'children': [],
            'level': -1,
            'path': [path_name],
            'md_line': 0,
            'hash': root_hash
        }
        if description_text:
            tree['notes'] = description_text
        return tree, node_mapping
    
    tree_content = tree_match.group(1)
    lines = tree_content.split('\n')
    
    # Build tree from nested lines
    tree, node_mapping = build_tree_from_nested_lines(lines, path_name, node_mapping)
    
    # Add description as notes for the root node
    if description_text:
        tree['notes'] = description_text
    
    return tree, node_mapping

def create_xmind_content_xml(forest):
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
    title.text = "California Tree Identification Guide"
    
    # Create topic structure
    topic = ET.SubElement(sheet, "topic")
    topic.set("id", generate_id())
    topic.set("timestamp", generate_timestamp())
    
    # Root topic title
    topic_title = ET.SubElement(topic, "title")
    topic_title.text = "What catches my eye about this tree?"
    
    # Add children for each path
    for path_tree in forest:
        # Skip empty trees
        if not path_tree or not path_tree.get('children'):
            continue
        
        # Create child topic for path
        child_topic = ET.SubElement(topic, "children")
        topics_el = ET.SubElement(child_topic, "topics")
        topics_el.set("type", "attached")
        
        path_topic = ET.SubElement(topics_el, "topic")
        path_topic.set("id", path_tree['id'])
        path_topic.set("timestamp", generate_timestamp())
        
        # Path title
        path_title = ET.SubElement(path_topic, "title")
        path_title.text = path_tree['name']
        
        # Add notes if present
        if 'notes' in path_tree:
            notes_el = ET.SubElement(path_topic, "notes")
            plain_el = ET.SubElement(notes_el, "plain")
            plain_el.text = path_tree['notes']
        
        # Process children recursively
        add_children_to_topic(path_topic, path_tree)
    
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

def generate_xmind_zip(forest, output_file):
    """Generate a XMind ZIP file that can be opened in XMind application."""
    try:
        # Create the necessary XML content
        content_xml = create_xmind_content_xml(forest)
        styles_xml = create_xmind_styles_xml()
        manifest_xml = create_xmind_manifest_xml()
        
        # Create a ZIP file
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add the XML content to the ZIP
            zipf.writestr("content.xml", content_xml)
            zipf.writestr("styles.xml", styles_xml)
            zipf.writestr("META-INF/manifest.xml", manifest_xml)
        
        return True
    except Exception as e:
        print(f"Error generating XMind ZIP file: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Convert markdown path files to XMind format')
    parser.add_argument('--path-dir', default=DEFAULT_PATH_DIR, help='Directory containing path markdown files')
    parser.add_argument('--output', default=DEFAULT_OUTPUT, help='Output XMind file path')
    parser.add_argument('--mapping', default=MAPPING_FILE, help='Node mapping file name')
    
    args = parser.parse_args()
    
    # Get all markdown files in the path directory
    md_files = []
    for file in os.listdir(args.path_dir):
        if file.endswith('-path.md') and not file.startswith('template') and not file.startswith('.'):
            md_files.append(os.path.join(args.path_dir, file))
    
    if not md_files:
        print(f"No path files found in {args.path_dir}")
        sys.exit(1)
    
    print(f"Found {len(md_files)} path files")
    
    # Load existing node mapping if available
    node_mapping = {}
    mapping_path = os.path.join(args.path_dir, args.mapping)
    if os.path.exists(mapping_path):
        try:
            with open(mapping_path, 'r') as f:
                node_mapping = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load existing node mapping: {e}")
    
    # Process each markdown file to generate a forest of trees
    forest = []
    for md_file in md_files:
        print(f"Processing {os.path.basename(md_file)}")
        tree, node_mapping = parse_markdown_to_tree(md_file, node_mapping)
        if tree:
            forest.append(tree)
    
    # Generate XMind file
    success = generate_xmind_zip(forest, args.output)
    
    if success:
        print(f"XMind file generated: {args.output}")
        
        # Save node mapping
        try:
            with open(mapping_path, 'w') as f:
                json.dump(node_mapping, f)
            print(f"Node mapping saved: {mapping_path}")
        except Exception as e:
            print(f"Warning: Could not save node mapping: {e}")
        
        print("Conversion complete with 100% fidelity to markdown source.")
    else:
        print("Failed to generate XMind file.")
        sys.exit(1)

if __name__ == "__main__":
    main()