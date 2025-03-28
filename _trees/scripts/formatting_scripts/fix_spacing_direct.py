#!/usr/bin/env python3

import os
import re
import sys

def fix_file_spacing(file_path):
    """Fix file spacing by directly modifying text patterns."""
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Replace section headers with properly spaced versions
    patterns = [
        (r'([^\n])\n  # Basic summary', r'\1\n\n  # Basic summary'),
        (r'([^\n])\n  # Identification path', r'\1\n\n  # Identification path'),
        (r'([^\n])\n  # Core features', r'\1\n\n  # Core features'),
        (r'([^\n])\n  # Kid-friendly identification', r'\1\n\n  # Kid-friendly identification'),
        (r'([^\n])\n  # Seasonal changes', r'\1\n\n  # Seasonal changes'),
        (r'([^\n])\n  # Additional required sections', r'\1\n\n  # Additional required sections'),
        (r'([^\n])\n  # Look-alike species', r'\1\n\n  # Look-alike species'),
        (r'([^\n])\n  # Cultural & ecological notes', r'\1\n\n  # Cultural & ecological notes'),
        (r'([^\n])\n  # Cultural significance', r'\1\n\n  # Cultural significance'),
        (r'([^\n])\n  # Range within California', r'\1\n\n  # Range within California'),
        (r'([^\n])\n  # Physical characteristics', r'\1\n\n  # Physical characteristics'),
        (r'([^\n])\n  # Conservation status', r'\1\n\n  # Conservation status'),
        (r'([^\n])\n  # Decision tree placement', r'\1\n\n  # Decision tree placement'),
        (r'([^\n])\n  # Wildlife value', r'\1\n\n  # Wildlife value'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    # Write the fixed content back to the file
    with open(file_path, 'w') as file:
        file.write(content)

def fix_all_files():
    """Fix spacing in all tree files."""
    tree_dir = os.path.join(os.getcwd(), "trees")
    
    if not os.path.exists(tree_dir):
        print(f"Directory {tree_dir} not found")
        return
    
    # Get all .yml files
    files = [f for f in os.listdir(tree_dir) if f.endswith('.yml')]
    print(f"Found {len(files)} tree files")
    
    for filename in files:
        file_path = os.path.join(tree_dir, filename)
        fix_file_spacing(file_path)
    
    print(f"Fixed spacing in {len(files)} tree files")

if __name__ == "__main__":
    fix_all_files()