#!/usr/bin/env python3
"""
Verification Script for Markdown to XMind Correspondence

This script verifies that the XMind file perfectly corresponds to the
source markdown files. It checks node structure, content, and ordering.
"""

import re
import os
import sys
import json
import xml.etree.ElementTree as ET
import argparse
from pathlib import Path
import hashlib

# Constants
DEFAULT_PATH_DIR = "../../decision_trees/paths"
DEFAULT_XMIND_FILE = "../../decision_trees/paths/california_tree_guide_xmind_generated.xmind"
MAPPING_FILE = "node_mapping.json"
NODE_PATTERN = r'(│\s*)*[├└]── (.+)'

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

def extract_tree_structure_from_markdown(md_file):
    """Extract tree structure from a markdown file with line numbers."""
    try:
        with open(md_file, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading markdown file {md_file}: {e}")
        return None
    
    # Extract the tree structure within triple backticks
    tree_match = re.search(r'```\n([\s\S]+?)\n```', content)
    if not tree_match:
        print(f"Warning: No tree structure found in {md_file}")
        return None
    
    tree_content = tree_match.group(1)
    lines = tree_content.split('\n')
    
    # Create a root node for the path itself
    path_name = Path(md_file).stem.replace('-path', ' Path').title()
    root_hash = hash_node(path_name, -1, path_name)
    
    nodes = [{
        'text': path_name,
        'level': -1,
        'path': [path_name],
        'line': 0,
        'hash': root_hash,
        'notes': None
    }]
    
    # Process the tree structure
    pending_lines = []
    
    # First, collect all lines with tree markers
    for i, line in enumerate(lines):
        if '├──' in line or '└──' in line:
            pending_lines.append((i + 1, line))
    
    # Then process the lines
    for line_num, line in pending_lines:
        level = count_indent_level(line)
        text = extract_node_text(line)
        
        # Calculate parent path
        parent_nodes = [n for n in nodes if n['level'] == level - 1]
        if not parent_nodes:
            # If no direct parent, find the closest ancestor
            ancestors = [n for n in nodes if n['level'] < level]
            if ancestors:
                # Sort by level in descending order to find the closest ancestor
                ancestors.sort(key=lambda x: x['level'], reverse=True)
                parent = ancestors[0]
            else:
                # Fall back to the root node
                parent = nodes[0]
        else:
            # Multiple potential parents at the right level, choose the most recent one
            parent = parent_nodes[-1]
        
        # Calculate full path
        full_path = parent['path'] + [text]
        
        # Extract notes if present (text after colon)
        notes = None
        if ': ' in text and not text.endswith(')') and not '->' in text and not '→' in text:
            parts = text.split(': ', 1)
            text = parts[0]
            notes = parts[1]
            full_path[-1] = text  # Update path with the text without notes
        
        # Create node hash for stable identification
        node_hash = hash_node(text, level, '/'.join(full_path))
        
        # Add node to list
        nodes.append({
            'text': text,
            'level': level,
            'path': full_path,
            'line': line_num,
            'hash': node_hash,
            'notes': notes
        })
    
    return nodes

def extract_tree_structure_from_xmind(xmind_file):
    """Extract tree structure from an XMind file with metadata."""
    try:
        tree = ET.parse(xmind_file)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing XMind file: {e}")
        return None
    
    # Check if this is a properly generated XMind file
    if root.get('source') != 'MARKDOWN':
        print("Warning: XMind file was not generated with the enhanced markdown_to_xmind.py script")
    
    # Extract all nodes with their metadata
    nodes = []
    
    def extract_nodes_recursively(elem, path=[]):
        # Skip the root California Tree Guide node
        if elem.get('TEXT') == 'California Tree Identification Guide':
            for child in elem.findall('./node'):
                extract_nodes_recursively(child, path)
            return
        
        text = elem.get('TEXT', '')
        node_hash = elem.get('MD_HASH', '')
        level = int(elem.get('MD_LEVEL', '-1'))
        line = int(elem.get('MD_LINE', '0'))
        
        # Extract notes if present
        notes = None
        richcontent = elem.find('./richcontent[@TYPE="NOTE"]')
        if richcontent is not None:
            paragraphs = []
            for p in richcontent.findall('.//p'):
                if p.text:
                    paragraphs.append(p.text.strip())
            if paragraphs:
                notes = '\n'.join(paragraphs)
        
        # Calculate path for this node
        current_path = path + [text]
        
        # Add node to list
        nodes.append({
            'text': text,
            'level': level,
            'path': current_path,
            'line': line,
            'hash': node_hash,
            'notes': notes
        })
        
        # Process child nodes
        for child in elem.findall('./node'):
            extract_nodes_recursively(child, current_path)
    
    # Start extraction from the root node
    main_node = root.find('.//node')
    if main_node is None:
        print("No main node found in XMind file")
        return None
    
    extract_nodes_recursively(main_node)
    return nodes

def compare_structures(md_nodes, xmind_nodes):
    """Compare tree structures between markdown and XMind for a single path."""
    if not md_nodes or not xmind_nodes:
        return False, {'missing_in_xmind': len(md_nodes) if md_nodes else 0, 
                       'extra_in_xmind': len(xmind_nodes) if xmind_nodes else 0}
    
    # Create hash-based lookups
    md_by_hash = {node['hash']: node for node in md_nodes if 'hash' in node}
    xmind_by_hash = {node['hash']: node for node in xmind_nodes if 'hash' in node}
    
    # Compare node sets
    md_hashes = set(md_by_hash.keys())
    xmind_hashes = set(xmind_by_hash.keys())
    
    missing_in_xmind = md_hashes - xmind_hashes
    extra_in_xmind = xmind_hashes - md_hashes
    common_hashes = md_hashes.intersection(xmind_hashes)
    
    # Compare node content for common nodes
    content_mismatches = []
    for hash_val in common_hashes:
        md_node = md_by_hash[hash_val]
        xmind_node = xmind_by_hash[hash_val]
        
        if md_node['text'] != xmind_node['text']:
            content_mismatches.append({
                'hash': hash_val,
                'md_text': md_node['text'],
                'xmind_text': xmind_node['text']
            })
    
    # Compare notes for common nodes
    note_mismatches = []
    for hash_val in common_hashes:
        md_node = md_by_hash[hash_val]
        xmind_node = xmind_by_hash[hash_val]
        
        md_notes = md_node.get('notes')
        xmind_notes = xmind_node.get('notes')
        
        # Skip root node notes comparison for now
        # Root nodes often have description text in markdown that's not strictly part of the tree
        if md_node['level'] == -1 and md_node['line'] == 0:
            continue
        
        # Normalize for comparison
        if md_notes is not None:
            md_notes = md_notes.strip()
        if xmind_notes is not None:
            xmind_notes = xmind_notes.strip()
        
        if md_notes != xmind_notes:
            note_mismatches.append({
                'hash': hash_val,
                'md_notes': md_notes,
                'xmind_notes': xmind_notes
            })
    
    # Compare node order
    md_line_by_hash = {node['hash']: node['line'] for node in md_nodes if 'hash' in node}
    xmind_line_by_hash = {node['hash']: node['line'] for node in xmind_nodes if 'hash' in node}
    
    order_mismatches = []
    for hash1 in common_hashes:
        for hash2 in common_hashes:
            if hash1 != hash2:
                md_order = (md_line_by_hash[hash1] < md_line_by_hash[hash2])
                xmind_order = (xmind_line_by_hash[hash1] < xmind_line_by_hash[hash2])
                
                if md_order != xmind_order:
                    order_mismatches.append({
                        'hash1': hash1,
                        'hash2': hash2,
                        'md_order': 'before' if md_order else 'after',
                        'xmind_order': 'before' if xmind_order else 'after',
                        'node1': md_by_hash[hash1]['text'],
                        'node2': md_by_hash[hash2]['text']
                    })
    
    # Prepare result
    is_perfect = (len(missing_in_xmind) == 0 and 
                  len(extra_in_xmind) == 0 and 
                  len(content_mismatches) == 0 and 
                  len(note_mismatches) == 0 and 
                  len(order_mismatches) == 0)
    
    results = {
        'missing_in_xmind': [md_by_hash[h]['text'] for h in missing_in_xmind],
        'extra_in_xmind': [xmind_by_hash[h]['text'] for h in extra_in_xmind],
        'content_mismatches': content_mismatches,
        'note_mismatches': note_mismatches,
        'order_mismatches': order_mismatches,
        'md_node_count': len(md_nodes),
        'xmind_node_count': len(xmind_nodes),
        'common_node_count': len(common_hashes)
    }
    
    return is_perfect, results

def verify_correspondence(md_dir, xmind_file, detailed=False):
    """Verify correspondence between markdown files and XMind mind map."""
    md_dir = Path(md_dir)
    xmind_file = Path(xmind_file)
    
    # Check if files exist
    if not md_dir.exists() or not md_dir.is_dir():
        print(f"Markdown directory not found: {md_dir}")
        return False
    
    if not xmind_file.exists():
        print(f"XMind file not found: {xmind_file}")
        return False
    
    # Find all *-path.md files
    path_files = list(md_dir.glob('*-path.md'))
    
    if not path_files:
        print(f"No path files found in {md_dir}")
        return False
    
    print(f"Found {len(path_files)} path files")
    
    # Extract XMind structure once
    xmind_nodes = extract_tree_structure_from_xmind(xmind_file)
    if not xmind_nodes:
        print("Failed to extract nodes from XMind file")
        return False
    
    # Group XMind nodes by path
    xmind_nodes_by_path = {}
    for node in xmind_nodes:
        if len(node['path']) > 0:
            path_name = node['path'][0]
            if path_name not in xmind_nodes_by_path:
                xmind_nodes_by_path[path_name] = []
            xmind_nodes_by_path[path_name].append(node)
    
    # Validate each path file
    all_perfect = True
    results = []
    
    for path_file in sorted(path_files):
        path_name = path_file.stem.replace('-path', ' Path').title()
        print(f"Validating {path_name}...")
        
        # Extract tree structures
        md_nodes = extract_tree_structure_from_markdown(path_file)
        path_xmind_nodes = xmind_nodes_by_path.get(path_name, [])
        
        if not md_nodes:
            print(f"  ❌ Failed to extract nodes from {path_file}")
            all_perfect = False
            continue
        
        if not path_xmind_nodes:
            print(f"  ❌ No nodes found in XMind for {path_name}")
            all_perfect = False
            continue
        
        # Compare structures
        is_perfect, comparison = compare_structures(md_nodes, path_xmind_nodes)
        
        if is_perfect:
            print(f"  ✅ Perfect match: {path_name} ({comparison['md_node_count']} nodes)")
        else:
            print(f"  ❌ Discrepancies found: {path_name}")
            print(f"    - Markdown nodes: {comparison['md_node_count']}")
            print(f"    - XMind nodes: {comparison['xmind_node_count']}")
            print(f"    - Common nodes: {comparison['common_node_count']}")
            
            if detailed:
                if comparison['missing_in_xmind']:
                    print(f"    - Items in Markdown but missing in XMind ({len(comparison['missing_in_xmind'])}):")
                    for item in comparison['missing_in_xmind'][:5]:  # Show only first 5
                        print(f"      * {item}")
                    if len(comparison['missing_in_xmind']) > 5:
                        print(f"      * ... and {len(comparison['missing_in_xmind']) - 5} more")
                
                if comparison['extra_in_xmind']:
                    print(f"    - Items in XMind but missing in Markdown ({len(comparison['extra_in_xmind'])}):")
                    for item in comparison['extra_in_xmind'][:5]:  # Show only first 5
                        print(f"      * {item}")
                    if len(comparison['extra_in_xmind']) > 5:
                        print(f"      * ... and {len(comparison['extra_in_xmind']) - 5} more")
                
                if comparison['content_mismatches']:
                    print(f"    - Content mismatches ({len(comparison['content_mismatches'])}):")
                    for mismatch in comparison['content_mismatches'][:3]:  # Show only first 3
                        print(f"      * MD: {mismatch['md_text']}")
                        print(f"        XM: {mismatch['xmind_text']}")
                    if len(comparison['content_mismatches']) > 3:
                        print(f"      * ... and {len(comparison['content_mismatches']) - 3} more")
                
                if comparison['note_mismatches']:
                    print(f"    - Note mismatches ({len(comparison['note_mismatches'])}):")
                    for mismatch in comparison['note_mismatches'][:3]:  # Show only first 3
                        print(f"      * {mismatch['md_notes']} vs {mismatch['xmind_notes']}")
                    if len(comparison['note_mismatches']) > 3:
                        print(f"      * ... and {len(comparison['note_mismatches']) - 3} more")
        
        all_perfect = all_perfect and is_perfect
        results.append({
            'path': path_name,
            'perfect': is_perfect,
            'comparison': comparison
        })
    
    # Summary
    print("\n=== VALIDATION SUMMARY ===")
    perfect_count = sum(1 for r in results if r['perfect'])
    print(f"Paths with perfect match: {perfect_count}/{len(results)} ({perfect_count/len(results)*100:.1f}%)")
    
    total_md_nodes = sum(r['comparison']['md_node_count'] for r in results)
    total_xmind_nodes = sum(r['comparison']['xmind_node_count'] for r in results)
    total_common_nodes = sum(r['comparison']['common_node_count'] for r in results)
    
    md_coverage = (total_common_nodes / total_md_nodes * 100) if total_md_nodes > 0 else 0
    xmind_coverage = (total_common_nodes / total_xmind_nodes * 100) if total_xmind_nodes > 0 else 0
    
    print(f"Total nodes in Markdown: {total_md_nodes}")
    print(f"Total nodes in XMind: {total_xmind_nodes}")
    print(f"Total common nodes: {total_common_nodes}")
    print(f"Markdown coverage in XMind: {md_coverage:.2f}%")
    print(f"XMind coverage in Markdown: {xmind_coverage:.2f}%")
    
    # Overall result
    if all_perfect:
        print("\n✅ VALIDATION SUCCESSFUL: 100% correspondence between Markdown and XMind!")
    else:
        print("\n❌ VALIDATION FAILED: Discrepancies found between Markdown and XMind.")
        print("Run with --detailed for more information about discrepancies.")
    
    return all_perfect

def main():
    parser = argparse.ArgumentParser(description='Verify correspondence between markdown files and XMind mind map')
    parser.add_argument('--md-dir', default=DEFAULT_PATH_DIR,
                      help='Directory containing markdown path files')
    parser.add_argument('--xmind', default=DEFAULT_XMIND_FILE,
                      help='XMind file path')
    parser.add_argument('--detailed', action='store_true',
                      help='Show detailed information about discrepancies')
    
    args = parser.parse_args()
    
    success = verify_correspondence(args.md_dir, args.xmind, args.detailed)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()