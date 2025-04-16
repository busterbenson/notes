#!/usr/bin/env python3
"""
Convert Multiple Markdown Trees to a Single OPML for Workflowy

This script converts multiple markdown files with tree structures (using ├── and └── for branches)
to a single OPML file compatible with Workflowy, combining all trees under a main root.

Usage:
    python3 markdown_to_opml.py <output_opml_file> <input_markdown_file1> [<input_markdown_file2> ...]

Example:
    python3 markdown_to_opml.py california_tree_guide.opml shape-size-path.md leaf-needle-path.md bark-path.md
"""

import sys
import re
import os
import glob
import xml.dom.minidom
from xml.sax.saxutils import escape

def extract_content_section(markdown_text):
    """Extract the tree content section from the markdown file (within the code block)."""
    pattern = r'```\s*\n(.*?)\n```'
    match = re.search(pattern, markdown_text, re.DOTALL)
    if match:
        return match.group(1)
    else:
        raise ValueError("Could not find tree content within ``` code blocks")

def parse_tree_structure(tree_content):
    """Parse the tree content into a hierarchical structure."""
    lines = tree_content.split('\n')
    tree = []
    stack = [(tree, -1)]  # (parent_node, indent_level)
    
    for line in lines:
        if not line.strip() or '├──' not in line and '└──' not in line:
            continue
            
        # Calculate indent level
        if '├──' in line:
            indent = line.index('├──')
        elif '└──' not in line:
            continue
        else:
            indent = line.index('└──')
        
        # Normalize indent level (using pipe character spacing)
        level = indent // 4
        
        # Get the content of the line
        content = line[indent+4:].strip()
        
        # Create a new node
        node = {
            'text': content,
            'children': []
        }
        
        # Find the appropriate parent in the stack
        while stack[-1][1] >= level:
            stack.pop()
            
        # Add the node to its parent
        stack[-1][0].append(node)
        
        # Push the node to the stack
        stack.append((node['children'], level))
    
    return tree

def extract_title_from_markdown(markdown_content):
    """Extract the title from the markdown file (first level 1 heading)."""
    pattern = r'^#\s+(.*?)$'
    match = re.search(pattern, markdown_content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    else:
        return None

def get_path_title(file_path):
    """Get a clean title from the file path."""
    basename = os.path.basename(file_path).replace('.md', '')
    title = basename.replace('-', ' ').title()
    
    # Try to open the file and get the title from the content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
            content_title = extract_title_from_markdown(markdown_content)
            if content_title:
                return content_title
    except:
        pass
    
    return title

def create_opml_document(path_trees, title="California Tree Guide"):
    """Create an OPML document from multiple tree structures."""
    doc = xml.dom.minidom.getDOMImplementation().createDocument(None, "opml", None)
    opml = doc.documentElement
    opml.setAttribute("version", "2.0")
    
    head = doc.createElement("head")
    opml.appendChild(head)
    
    title_elem = doc.createElement("title")
    title_text = doc.createTextNode(title)
    title_elem.appendChild(title_text)
    head.appendChild(title_elem)
    
    body = doc.createElement("body")
    opml.appendChild(body)
    
    def add_outline(parent, items):
        for item in items:
            outline = doc.createElement("outline")
            # Clean the text and escape XML entities
            text = re.sub(r'\[.*?\]\(.*?\)', '', item['text'])  # Remove markdown links
            text = escape(text)
            outline.setAttribute("text", text)
            parent.appendChild(outline)
            
            if item['children']:
                add_outline(outline, item['children'])
    
    # Add main outline element for each tree
    for path_title, tree in path_trees:
        path_outline = doc.createElement("outline")
        path_outline.setAttribute("text", path_title)
        body.appendChild(path_outline)
        
        # Add the tree under this path outline
        add_outline(path_outline, tree)
    
    return doc

def process_markdown_file(file_path):
    """Process a single markdown file and return its tree structure."""
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    try:
        # Extract tree content from markdown
        tree_content = extract_content_section(markdown_content)
        
        # Parse the tree structure
        tree = parse_tree_structure(tree_content)
        
        return tree
    except ValueError as e:
        print(f"Error processing {file_path}: {e}")
        return []

def main():
    if len(sys.argv) < 3:
        print(f"Usage: python3 {sys.argv[0]} <output_opml_file> <input_markdown_file1> [<input_markdown_file2> ...]")
        print("Examples:")
        print(f"  Single path: python3 {sys.argv[0]} output.opml path.md")
        print(f"  Multiple paths: python3 {sys.argv[0]} combined.opml path1.md path2.md path3.md")
        sys.exit(1)
    
    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    
    # Check if wildcard patterns were used and expand them
    expanded_input_files = []
    for pattern in input_files:
        if '*' in pattern:
            expanded_input_files.extend(glob.glob(pattern))
        else:
            expanded_input_files.append(pattern)
    
    input_files = expanded_input_files
    
    if not input_files:
        print("No input files found.")
        sys.exit(1)
    
    # Process each markdown file
    path_trees = []
    for file_path in input_files:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
            
        # Get the title for this path
        path_title = get_path_title(file_path)
        
        # Process the file
        tree = process_markdown_file(file_path)
        
        # Add to the list of path trees
        if tree:
            path_trees.append((path_title, tree))
    
    if not path_trees:
        print("No valid tree structures found in the input files.")
        sys.exit(1)
    
    # Create the combined OPML document
    doc = create_opml_document(path_trees, "California Tree Guide")
    
    # Write OPML to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(doc.toprettyxml(indent="  "))
    
    print(f"Successfully combined {len(path_trees)} trees into OPML format at {output_file}")

if __name__ == "__main__":
    main()