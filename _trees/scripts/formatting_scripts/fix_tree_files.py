#!/usr/bin/env python3

import os
import re
import sys

# Directory paths
TREES_DIR = "trees"

def fix_tree_files():
    """Fix the position of genus information in tree files."""
    updated_count = 0
    error_count = 0
    
    # Get all tree files
    tree_files = [f for f in os.listdir(TREES_DIR) if f.endswith('.yml')]
    
    for filename in tree_files:
        file_path = os.path.join(TREES_DIR, filename)
        
        try:
            # Read the original file content
            with open(file_path, 'r') as file:
                content = file.read()
            
            # Fix indentation of family field
            if re.search(r'common_genus:.*?\n\s+family:', content):
                print(f"Fixing {filename}: Correcting indentation of family field")
                content = re.sub(
                    r'(common_genus:.*?\n)\s+(family:)',
                    r'\1  \2',
                    content
                )
                # Write the fixed content back to the file
                with open(file_path, 'w') as file:
                    file.write(content)
                updated_count += 1
                continue
                
            # Check if the file already has genus info near the family field (and properly formatted)
            if re.search(r'scientific_name:[^\n]*\n\s+scientific_genus:', content) or \
               re.search(r'scientific_name:[^\n]*\n\s+common_genus:', content):
                print(f"Skipping {filename}: Genus info already in the correct position")
                continue
            
            # Extract genus information from the end of the file
            scientific_genus_match = re.search(r'scientific_genus:\s*(.*?)$', content, re.MULTILINE)
            common_genus_match = re.search(r'common_genus:\s*(.*?)$', content, re.MULTILINE)
            
            if not scientific_genus_match or not common_genus_match:
                print(f"Skipping {filename}: Missing genus information")
                continue
            
            scientific_genus = scientific_genus_match.group(1).strip()
            common_genus = common_genus_match.group(1).strip()
            
            # Remove the genus information from the end of the file
            content = re.sub(r'\n\s+scientific_genus:.*$', '', content, flags=re.MULTILINE)
            content = re.sub(r'\n\s+common_genus:.*$', '', content, flags=re.MULTILINE)
            
            # Find the position to insert the genus information (after scientific_name and before family)
            updated_content = re.sub(
                r'(scientific_name:\s*.*?\n)(\s+family:)',
                f'\\1  scientific_genus: {scientific_genus}\n  common_genus: {common_genus}\\2',
                content,
                flags=re.DOTALL
            )
            
            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.write(updated_content)
                
            print(f"Updated {filename}")
            updated_count += 1
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            error_count += 1
    
    return updated_count, error_count

if __name__ == "__main__":
    updated, errors = fix_tree_files()
    print(f"\nSummary: Updated {updated} files with {errors} errors")