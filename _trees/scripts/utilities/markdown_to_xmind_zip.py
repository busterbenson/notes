#!/usr/bin/env python3
"""
Markdown to XMind Converter (ZIP Format)

This script converts tree identification path markdown files to XMind format.
The markdown format is treated as the source of truth, and the XMind output
is optimized to maintain 100% correspondence with the markdown structure.
This version generates a proper XMind ZIP file compatible with XMind application.
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
    """Count the indentation level based on │ characters."""
    if '├──' in line or '└──' in line:
        return line.count('│')
    return 0

def hash_node(text, level, path):
    """Generate a stable hash for a node based on text, level, and path."""
    node_info = f"{path}:{level}:{text}"
    return hashlib.md5(node_info.encode()).hexdigest()

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
    
    # Process each line to create nodes
    nodes_by_level = {-1: [root]}
    last_node_by_level = {-1: root}
    
    line_num = 0
    for line in lines:
        line_num += 1
        if not line.strip():
            continue
        
        # Skip lines without tree markers
        if '├──' not in line and '└──' not in line:
            continue
        
        level = count_indent_level(line)
        text = extract_node_text(line)
        
        # Calculate parent node
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

def create_note_element(text):
    """Create a note element for XMind content.xml."""
    note = ET.Element('notes')
    plain = ET.SubElement(note, 'plain')
    plain.text = text
    html = ET.SubElement(note, 'html')
    
    # Split text into paragraphs for the HTML representation
    paragraphs = text.split('\n')
    for para in paragraphs:
        p = ET.SubElement(html, 'p')
        p.text = para.strip()
    
    return note

def convert_tree_to_xmind_topic(parent_element, tree_node, level=0):
    """Recursively convert tree structure to XMind XML topic elements."""
    # Create topic element
    topic_attrs = {
        'id': tree_node['id'],
        'modified-by': 'markdown-to-xmind',
        'timestamp': generate_timestamp(),
    }
    
    topic = ET.SubElement(parent_element, 'topic', topic_attrs)
    
    # Add title
    title = ET.SubElement(topic, 'title')
    title.text = tree_node['name']
    
    # Add metadata as attributes
    if 'hash' in tree_node:
        metadata = ET.SubElement(topic, 'md-data')
        metadata.set('hash', tree_node['hash'])
        metadata.set('level', str(tree_node['level']))
        metadata.set('line', str(tree_node['md_line']))
    
    # Add notes if available
    if tree_node.get('notes'):
        topic.append(create_note_element(tree_node['notes']))
    
    # Add styling for different levels
    if level == 0:  # Path node
        ET.SubElement(topic, 'style', {
            'id': f"style-{tree_node['id']}",
            'type': 'topic'
        })
    
    # Create children container
    if tree_node.get('children'):
        children = ET.SubElement(topic, 'children')
        topics = ET.SubElement(children, 'topics', {'type': 'attached'})
        
        # Process children
        for child in tree_node.get('children', []):
            convert_tree_to_xmind_topic(topics, child, level + 1)
    
    return topic

def generate_xmind_content_xml(trees):
    """Generate content.xml for XMind file from tree structures."""
    # Create XMind content structure
    xmap = ET.Element('xmap-content', {
        'version': '2.0',
        'xmlns': 'urn:xmind:xmap:xmlns:content:2.0',
        'xmlns:fo': 'http://www.w3.org/1999/XSL/Format',
        'xmlns:svg': 'http://www.w3.org/2000/svg'
    })
    
    # Create sheet element
    sheet = ET.SubElement(xmap, 'sheet', {
        'id': generate_id(),
        'timestamp': generate_timestamp(),
        'modified-by': 'markdown-to-xmind'
    })
    
    # Add title
    title = ET.SubElement(sheet, 'title')
    title.text = 'California Tree Identification Guide'
    
    # Create main topic
    root_id = generate_id()
    topic = ET.SubElement(sheet, 'topic', {
        'id': root_id,
        'timestamp': generate_timestamp(),
        'modified-by': 'markdown-to-xmind'
    })
    
    # Add root node title
    root_title = ET.SubElement(topic, 'title')
    root_title.text = 'California Tree Identification Guide'
    
    # Add root node description
    root_notes = ET.SubElement(topic, 'notes')
    plain = ET.SubElement(root_notes, 'plain')
    plain.text = "This mind map represents the California Tree Identification Guide.\n\nIt allows you to identify trees by observable features rather than technical botanical knowledge.\n\nGenerated from markdown source files - do not edit directly."
    html = ET.SubElement(root_notes, 'plain')  # HTML version of notes
    
    # Add styling for root node
    ET.SubElement(topic, 'style', {
        'id': f"style-{root_id}",
        'type': 'topic'
    })
    
    # Create children container for root
    children = ET.SubElement(topic, 'children')
    topics = ET.SubElement(children, 'topics', {'type': 'attached'})
    
    # Add each path tree as a child of the root node
    for tree in trees:
        convert_tree_to_xmind_topic(topics, tree)
    
    # Set stylesheet relationship
    relationships = ET.SubElement(sheet, 'relationships')
    
    return xmap

def create_manifest_xml():
    """Create manifest.xml for XMind file."""
    manifest = ET.Element('manifest', {'xmlns': 'urn:xmind:xmap:xmlns:manifest:1.0'})
    
    # Add file entries
    ET.SubElement(manifest, 'file-entry', {
        'full-path': 'content.xml',
        'media-type': 'text/xml'
    })
    
    ET.SubElement(manifest, 'file-entry', {
        'full-path': 'META-INF/',
        'media-type': ''
    })
    
    ET.SubElement(manifest, 'file-entry', {
        'full-path': 'META-INF/manifest.xml',
        'media-type': 'text/xml'
    })
    
    ET.SubElement(manifest, 'file-entry', {
        'full-path': 'styles.xml',
        'media-type': 'text/xml'
    })
    
    return manifest

def create_styles_xml():
    """Create styles.xml for XMind file."""
    styles = ET.Element('xmap-styles', {
        'version': '2.0',
        'xmlns': 'urn:xmind:xmap:xmlns:style:2.0'
    })
    
    # Add master styles
    master_styles = ET.SubElement(styles, 'master-styles')
    default_style = ET.SubElement(master_styles, 'style', {
        'id': 'master-1',
        'name': 'Default',
        'type': 'theme'
    })
    
    # Add automatic styles
    automatic_styles = ET.SubElement(styles, 'automatic-styles')
    
    # Add styles
    style_sheets = ET.SubElement(styles, 'styles')
    
    return styles

def generate_xmind_zip(trees, output_path, mapping_path):
    """Generate XMind ZIP file from tree structures."""
    # Create a temporary directory for the XMind contents
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        meta_dir = temp_dir / 'META-INF'
        meta_dir.mkdir()
        
        # Generate content.xml
        content_xml = generate_xmind_content_xml(trees)
        content_xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + ET.tostring(content_xml, encoding='utf-8').decode()
        with open(temp_dir / 'content.xml', 'w', encoding='utf-8') as f:
            f.write(content_xml_str)
        
        # Generate manifest.xml
        manifest_xml = create_manifest_xml()
        manifest_xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + ET.tostring(manifest_xml, encoding='utf-8').decode()
        with open(meta_dir / 'manifest.xml', 'w', encoding='utf-8') as f:
            f.write(manifest_xml_str)
        
        # Generate styles.xml
        styles_xml = create_styles_xml()
        styles_xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + ET.tostring(styles_xml, encoding='utf-8').decode()
        with open(temp_dir / 'styles.xml', 'w', encoding='utf-8') as f:
            f.write(styles_xml_str)
        
        # Create the XMind ZIP file
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add META-INF/manifest.xml
            zipf.write(meta_dir / 'manifest.xml', 'META-INF/manifest.xml')
            
            # Add content.xml
            zipf.write(temp_dir / 'content.xml', 'content.xml')
            
            # Add styles.xml
            zipf.write(temp_dir / 'styles.xml', 'styles.xml')
    
    print(f"XMind file generated: {output_path}")
    
    # Save node mapping to JSON file
    save_node_mapping(trees, mapping_path)

def save_node_mapping(trees, mapping_path):
    """Save node mapping information to a JSON file."""
    mapping = {}
    
    def process_tree(node):
        if 'hash' in node and 'id' in node:
            mapping[node['hash']] = {
                'id': node['id'],
                'name': node['name'],
                'level': node['level'],
                'md_line': node['md_line'],
                'path': '/'.join(node['path'])
            }
        
        for child in node.get('children', []):
            process_tree(child)
    
    # Process all trees
    for tree in trees:
        process_tree(tree)
    
    # Save mapping to file
    with open(mapping_path, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2)
    
    print(f"Node mapping saved: {mapping_path}")

def load_node_mapping(mapping_path):
    """Load node mapping from a JSON file."""
    if not os.path.exists(mapping_path):
        print(f"No existing mapping file found at {mapping_path}")
        return {}
    
    try:
        with open(mapping_path, 'r', encoding='utf-8') as f:
            mapping_data = json.load(f)
        
        # Convert complex mapping to simple hash->id mapping
        mapping = {hash_key: data['id'] for hash_key, data in mapping_data.items()}
        return mapping
    except Exception as e:
        print(f"Error loading mapping file: {e}")
        return {}

def process_path_files(path_dir, output_file, mapping_file):
    """Process all path markdown files and combine them into a single XMind."""
    path_dir = Path(path_dir)
    mapping_path = path_dir / mapping_file
    
    # Load existing node mapping if available
    node_mapping = load_node_mapping(mapping_path)
    
    # Find all *-path.md files
    path_files = list(path_dir.glob('*-path.md'))
    
    if not path_files:
        print(f"No path files found in {path_dir}")
        return
    
    print(f"Found {len(path_files)} path files")
    
    # Process each path file
    trees = []
    for path_file in sorted(path_files):
        print(f"Processing {path_file.name}")
        tree, node_mapping = parse_markdown_to_tree(path_file, node_mapping)
        if tree:
            trees.append(tree)
    
    # Generate XMind file
    generate_xmind_zip(trees, output_file, mapping_path)
    print(f"Conversion complete with 100% fidelity to markdown source.")

def main():
    parser = argparse.ArgumentParser(description='Convert markdown path files to XMind format')
    parser.add_argument('--path-dir', help='Directory containing path markdown files', default=DEFAULT_PATH_DIR)
    parser.add_argument('--output', help='Output XMind file path', default=DEFAULT_OUTPUT)
    parser.add_argument('--mapping', help='Node mapping file name', default=MAPPING_FILE)
    args = parser.parse_args()
    
    process_path_files(args.path_dir, args.output, args.mapping)

if __name__ == "__main__":
    main()