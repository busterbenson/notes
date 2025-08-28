#!/usr/bin/env python3

import os
import re
import sys

def add_blank_lines(content):
    """Add blank lines before section headers."""
    
    # Insert a blank line before each section header
    headers = [
        "  # Basic summary",
        "  # Identification path",
        "  # Core features",
        "  # Kid-friendly identification",
        "  # Seasonal changes",
        "  # Additional required sections",
        "  # Look-alike species",
        "  # Cultural & ecological notes",
        "  # Cultural significance",
        "  # Range within California",
        "  # Physical characteristics",
        "  # Conservation status",
        "  # Decision tree placement",
        "  # Wildlife value",
    ]
    
    # Extract the header part (common_name, scientific_name, etc.)
    header_match = re.search(r'tree:\s*\n(.*?)(?=\s*#)', content, re.DOTALL)
    header = header_match.group(1) if header_match else ""
    
    # Remove the header part from the content
    remaining = re.sub(r'tree:\s*\n.*?(?=\s*#)', '', content, flags=re.DOTALL)
    
    # Reconstruct the content with the header and blank lines before each section
    result = "tree:\n" + header + "\n"
    
    # Add each section with a blank line before it
    for i, header in enumerate(headers):
        pattern = r'(\s*)(' + re.escape(header) + r'.*?)(?=\s*(?:' + '|'.join(re.escape(h) for h in headers[i+1:]) + r'|\Z))'
        match = re.search(pattern, remaining, re.DOTALL)
        if match:
            indent, section = match.groups()
            result += "\n" + indent + section
    
    return result

def fix_all_tree_files():
    """Add blank lines before section headers in all tree files."""
    trees_dir = os.path.join(os.getcwd(), "trees")
    
    if not os.path.exists(trees_dir):
        print(f"Directory {trees_dir} not found")
        return
    
    # Get a list of all .yml files in the trees directory
    tree_files = [f for f in os.listdir(trees_dir) if f.endswith('.yml')]
    
    print(f"Found {len(tree_files)} tree files to process")
    
    for filename in tree_files:
        filepath = os.path.join(trees_dir, filename)
        
        # Read the file content
        with open(filepath, 'r') as file:
            content = file.read()
        
        # Add blank lines before section headers
        new_content = add_blank_lines(content)
        
        # Write the updated content back
        with open(filepath, 'w') as file:
            file.write(new_content)
    
    print(f"Added blank lines before section headers in {len(tree_files)} tree files")

if __name__ == "__main__":
    fix_all_tree_files()