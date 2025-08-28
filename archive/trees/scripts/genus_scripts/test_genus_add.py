#!/usr/bin/env python3

import os
import re
import sys
import importlib.util

# Dynamically import the add_genus_info module from add_genus_to_all.py
spec = importlib.util.spec_from_file_location("add_genus_to_all", "/Users/buster/projects/notes/_trees/add_genus_to_all.py")
add_genus_to_all = importlib.util.module_from_spec(spec)
spec.loader.exec_module(add_genus_to_all)

# Import the specific function
add_genus_info = add_genus_to_all.add_genus_info

def process_test_files():
    """Process a small set of test files."""
    trees_dir = "/Users/buster/projects/notes/_trees/trees"
    
    # Test files representing different families and cases
    test_files = [
        "fagaceae.blue-oak.yml",        # Oak (already has genus info)
        "asparagaceae.joshua-tree.yml", # Joshua Tree (already has genus info)
        "pinaceae.ponderosa-pine.yml",  # Pine
        "juglandaceae.california-black-walnut.yml",  # Walnut
        "salicaceae.quaking-aspen.yml"  # Aspen
    ]
    
    for filename in test_files:
        filepath = os.path.join(trees_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"File {filepath} not found")
            continue
        
        # Read the current content
        with open(filepath, 'r') as file:
            content = file.read()
        
        # Add genus information without writing to file
        updated_content, scientific_genus, common_genus = add_genus_info(content, filename)
        
        # Display results
        print(f"File: {filename}")
        print(f"  Scientific Genus: {scientific_genus}")
        print(f"  Common Genus: {common_genus}")
        print(f"  Modified: {'Yes' if updated_content != content else 'No'}")
        print()

if __name__ == "__main__":
    process_test_files()