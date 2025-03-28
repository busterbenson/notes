#!/usr/bin/env python3
import os
import re
import sys
import glob

# Directory containing tree files
TREES_DIR = "."

def fix_tree_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Check if the file has genus information
    scientific_genus_match = re.search(r'scientific_genus:\s*"([^"]+)"|scientific_genus:\s*\'([^\']+)\'|scientific_genus:\s*(\w+)', content)
    common_genus_match = re.search(r'common_genus:\s*"([^"]+)"|common_genus:\s*\'([^\']+)\'|common_genus:\s*(\w+)', content)
    
    # Check if the genus information is at the end of the file
    if scientific_genus_match and common_genus_match:
        # Check if the genus info is not in the header (first few lines)
        if scientific_genus_match.start() > 500:  # If it's more than 500 chars into the file, it's likely at the end
            print(f"Fixing incorrect format in {file_path}")
        else:
            header_match = re.search(r'common_name:.*?\n\s*scientific_name:.*?\n\s*scientific_genus:.*?\n\s*common_genus:.*?\n\s*family:', content, re.DOTALL)
            if header_match:
                print(f"File {file_path} already fixed - skipping")
                return False
            else:
                print(f"No issues found in {file_path} - genus info seems to be in correct position")
                return False
    else:
        print(f"Could not find genus information in {file_path}")
        return False
        
        # Get the genus values
        scientific_genus = scientific_genus_match.group(1) if scientific_genus_match.group(1) else scientific_genus_match.group(2)
        common_genus = common_genus_match.group(1) if common_genus_match.group(1) else common_genus_match.group(2)
        
        # Remove the genus information from the end
        content = re.sub(r'scientific_genus:.*?\n\s*common_genus:.*?\n', '', content)
        
        # Find where to insert the genus information (after scientific_name but before family)
        pattern = r'(scientific_name:\s*"[^"]+"|scientific_name:\s*\'[^\']+\')(\s*\n)'
        match = re.search(pattern, content)
        
        if not match:
            print(f"Could not find scientific_name in {file_path}")
            return
        
        # Determine quote style from scientific_name
        quote_style = '"' if '"' in match.group(1) else "'"
        
        # Extract indentation
        indent_match = re.search(r'(\s+)common_name:', content)
        if not indent_match:
            print(f"Could not determine indentation in {file_path}")
            return
        
        indent = indent_match.group(1)
        
        # Insert genus information
        replacement = (
            f'{match.group(1)}{match.group(2)}'
            f'{indent}scientific_genus: {quote_style}{scientific_genus}{quote_style}{match.group(2)}'
            f'{indent}common_genus: {quote_style}{common_genus}{quote_style}{match.group(2)}'
        )
        
        new_content = re.sub(pattern, replacement, content, count=1)
        
        # Fix double quotes within quotes
        new_content = re.sub(r'"([^"]*)"([^"]*)"', r'"$1\'$2\'"', new_content)
        
        # Write the fixed content
        with open(file_path, 'w') as file:
            file.write(new_content)
        
        print(f"Fixed {file_path}")
        return True
    
    # Check if the file has already been fixed
    header_match = re.search(r'common_name:.*?\n\s*scientific_name:.*?\n\s*scientific_genus:.*?\n\s*common_genus:.*?\n\s*family:', content, re.DOTALL)
    
    if header_match:
        print(f"File {file_path} already fixed - skipping")
        return False
    
    # Otherwise, no fix needed because it's either not processed by the script or already fixed manually
    print(f"No issues found in {file_path}")
    return False

def main():
    # Find all tree files
    tree_files = glob.glob(os.path.join(TREES_DIR, "*.yml"))
    
    # Skip our script files
    tree_files = [f for f in tree_files if not f.endswith(('update_genus_info.py', 'add_genus_info.py', 'fix_tree_files.py'))]
    
    fixed_count = 0
    for file_path in tree_files:
        if fix_tree_file(file_path):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    main()