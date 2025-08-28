#!/usr/bin/env python3
"""
Validation Script for Tree Sync

This script validates the conversion between markdown files and XMind mind maps,
ensuring 100% correspondence in content and structure.
"""

import os
import sys
import re
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

def extract_tree_structure_from_markdown(md_file):
    """Extract tree structure from a markdown file."""
    with open(md_file, 'r') as f:
        content = f.read()
    
    # Extract the tree structure within code blocks
    tree_match = re.search(r'```\n([\s\S]+?)\n```', content)
    if not tree_match:
        return None
    
    tree_content = tree_match.group(1)
    
    # Normalize the tree content
    lines = [line.strip() for line in tree_content.split('\n') if line.strip()]
    
    # Extract node texts (strip decoration characters)
    nodes = []
    for line in lines:
        # Skip lines without tree markers
        if '├──' not in line and '└──' not in line:
            continue
        
        # Extract the node text after the tree marker
        match = re.search(r'[├└]── (.+)', line)
        if match:
            node_text = match.group(1).strip()
            nodes.append(node_text)
    
    return nodes

def extract_tree_structure_from_xmind(xmind_file, path_name):
    """Extract tree structure for a specific path from an XMind file."""
    try:
        tree = ET.parse(xmind_file)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing XMind file: {e}")
        return None
    
    # Normalize path name for comparison
    path_name = path_name.replace('-path', ' Path').title()
    
    # Find the path node
    path_node = None
    for node in root.findall('.//node'):
        node_text = node.attrib.get('TEXT', '')
        if node_text == path_name:
            path_node = node
            break
    
    if not path_node:
        print(f"Path '{path_name}' not found in XMind file")
        return None
    
    # Extract all node texts recursively
    nodes = []
    extract_nodes_recursively(path_node, nodes)
    
    return nodes

def extract_nodes_recursively(node, nodes_list):
    """Recursively extract node texts from XMind XML."""
    # Skip the root node itself
    if node.attrib.get('TEXT') not in nodes_list:
        nodes_list.append(node.attrib.get('TEXT', '').strip())
    
    # Process child nodes
    for child in node.findall('./node'):
        extract_nodes_recursively(child, nodes_list)

def normalize_text(text):
    """Normalize text for comparison."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove special characters that might differ between formats
    text = re.sub(r'[→→]', '', text)
    # Lowercase for case-insensitive comparison
    return text.lower()

def compare_tree_structures(md_nodes, xmind_nodes):
    """Compare tree structures between markdown and XMind."""
    if not md_nodes or not xmind_nodes:
        return False, None, None
    
    # Normalize nodes for comparison
    md_nodes_norm = [normalize_text(node) for node in md_nodes]
    xmind_nodes_norm = [normalize_text(node) for node in xmind_nodes]
    
    # Check for nodes in markdown but not in XMind
    missing_in_xmind = []
    for i, node in enumerate(md_nodes_norm):
        if node and node not in xmind_nodes_norm:
            missing_in_xmind.append(md_nodes[i])
    
    # Check for nodes in XMind but not in markdown
    missing_in_md = []
    for i, node in enumerate(xmind_nodes_norm):
        if node and node not in md_nodes_norm:
            missing_in_md.append(xmind_nodes[i])
    
    # Calculate coverage percentage
    md_coverage = 100 - (len(missing_in_xmind) / len(md_nodes) * 100 if md_nodes else 0)
    xmind_coverage = 100 - (len(missing_in_md) / len(xmind_nodes) * 100 if xmind_nodes else 0)
    
    is_perfect = len(missing_in_xmind) == 0 and len(missing_in_md) == 0
    
    return is_perfect, md_coverage, xmind_coverage, missing_in_xmind, missing_in_md

def validate_conversion(md_dir, xmind_file, detailed=False):
    """Validate conversion between markdown files and XMind mind map."""
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
    
    # Validate each path file
    all_perfect = True
    results = []
    
    for path_file in sorted(path_files):
        path_name = path_file.stem
        print(f"Validating {path_name}...")
        
        # Extract tree structures
        md_nodes = extract_tree_structure_from_markdown(path_file)
        xmind_nodes = extract_tree_structure_from_xmind(xmind_file, path_name)
        
        # Compare structures
        is_perfect, md_coverage, xmind_coverage, missing_in_xmind, missing_in_md = compare_tree_structures(
            md_nodes, xmind_nodes
        )
        
        if is_perfect:
            print(f"  ✅ Perfect match: {path_name}")
        else:
            print(f"  ❌ Discrepancies found: {path_name}")
            print(f"    - Markdown coverage in XMind: {md_coverage:.1f}%")
            print(f"    - XMind coverage in Markdown: {xmind_coverage:.1f}%")
            
            if detailed:
                if missing_in_xmind:
                    print(f"    - Items in Markdown but missing in XMind ({len(missing_in_xmind)}):")
                    for item in missing_in_xmind[:5]:  # Show only first 5
                        print(f"      * {item}")
                    if len(missing_in_xmind) > 5:
                        print(f"      * ... and {len(missing_in_xmind) - 5} more")
                
                if missing_in_md:
                    print(f"    - Items in XMind but missing in Markdown ({len(missing_in_md)}):")
                    for item in missing_in_md[:5]:  # Show only first 5
                        print(f"      * {item}")
                    if len(missing_in_md) > 5:
                        print(f"      * ... and {len(missing_in_md) - 5} more")
        
        all_perfect = all_perfect and is_perfect
        results.append({
            'path': path_name,
            'perfect': is_perfect,
            'md_coverage': md_coverage,
            'xmind_coverage': xmind_coverage,
            'missing_in_xmind': missing_in_xmind,
            'missing_in_md': missing_in_md
        })
    
    # Summary
    print("\n=== VALIDATION SUMMARY ===")
    perfect_count = sum(1 for r in results if r['perfect'])
    print(f"Paths with perfect match: {perfect_count}/{len(results)} ({perfect_count/len(results)*100:.1f}%)")
    
    avg_md_coverage = sum(r['md_coverage'] for r in results) / len(results)
    avg_xmind_coverage = sum(r['xmind_coverage'] for r in results) / len(results)
    print(f"Average Markdown coverage in XMind: {avg_md_coverage:.1f}%")
    print(f"Average XMind coverage in Markdown: {avg_xmind_coverage:.1f}%")
    
    # Overall result
    if all_perfect:
        print("\n✅ VALIDATION SUCCESSFUL: 100% correspondence between Markdown and XMind!")
    else:
        print("\n❌ VALIDATION FAILED: Discrepancies found between Markdown and XMind.")
        print("Run with --detailed for more information about discrepancies.")
    
    return all_perfect

def main():
    parser = argparse.ArgumentParser(description='Validate conversion between markdown files and XMind mind map')
    parser.add_argument('--md-dir', default='../../decision_trees/paths',
                      help='Directory containing markdown path files')
    parser.add_argument('--xmind', default='../../decision_trees/paths/california_tree_guide_generated.xmind',
                      help='XMind file path')
    parser.add_argument('--detailed', action='store_true',
                      help='Show detailed information about discrepancies')
    
    args = parser.parse_args()
    
    success = validate_conversion(args.md_dir, args.xmind, args.detailed)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()