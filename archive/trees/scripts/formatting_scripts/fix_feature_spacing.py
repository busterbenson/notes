#!/usr/bin/env python3

import os
import re
import sys

def fix_feature_spacing(content):
    """Fix spacing between feature items."""
    
    # Fix always_true section
    if "always_true:" in content:
        # Add spacing after "always_true:" if needed
        content = re.sub(r'(always_true:)\s*\n\s*-', r'\1\n\n    - ', content)
        
        # Add blank lines between feature items
        content = re.sub(r'(\n\s+- (?:feature_id|"feature_id"):[^\n]+\n\s+notes:[^\n]+(?:\n\s+[^-\n][^\n]*)*)', 
                         r'\1\n', content)
    
    # Fix usually_true section
    if "usually_true:" in content:
        # Add spacing after "usually_true:" if needed
        content = re.sub(r'(usually_true:)\s*\n\s*-', r'\1\n\n    - ', content)
        
        # Add blank lines between feature items
        content = re.sub(r'(\n\s+- (?:feature_id|"feature_id"):[^\n]+\n\s+(?:notes|exceptions):[^\n]+(?:\n\s+[^-\n][^\n]*)*)', 
                         r'\1\n', content)
    
    # Fix sometimes_true section
    if "sometimes_true:" in content:
        # Add spacing after "sometimes_true:" if needed
        content = re.sub(r'(sometimes_true:)\s*\n\s*-', r'\1\n\n    - ', content)
        
        # Add blank lines between feature items
        content = re.sub(r'(\n\s+- (?:feature_id|"feature_id"):[^\n]+\n\s+(?:notes|conditions):[^\n]+(?:\n\s+[^-\n][^\n]*)*)', 
                         r'\1\n', content)
    
    # Fix never_true section
    if "never_true:" in content:
        # Add spacing after "never_true:" if needed
        content = re.sub(r'(never_true:)\s*\n\s*-', r'\1\n\n    - ', content)
        
        # Add blank lines between feature items
        content = re.sub(r'(\n\s+- (?:feature_id|"feature_id"):[^\n]+\n\s+notes:[^\n]+(?:\n\s+[^-\n][^\n]*)*)', 
                         r'\1\n', content)
    
    return content

def fix_all_tree_files():
    """Fix feature spacing in all tree files."""
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
        
        # Apply the fix
        new_content = fix_feature_spacing(content)
        
        # Write the updated content back
        with open(filepath, 'w') as file:
            file.write(new_content)
    
    print(f"Fixed feature spacing in {len(tree_files)} tree files")

if __name__ == "__main__":
    fix_all_tree_files()