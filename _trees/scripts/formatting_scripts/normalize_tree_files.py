#!/usr/bin/env python3

import os
import re
import yaml

# Directory paths
TREES_DIR = "trees"

def normalize_tree_files():
    """Normalize formatting in tree files and add quotes to all string values."""
    updated_count = 0
    error_count = 0
    
    # Get all tree files
    tree_files = [f for f in os.listdir(TREES_DIR) if f.endswith('.yml')]
    
    for filename in tree_files:
        file_path = os.path.join(TREES_DIR, filename)
        
        try:
            # Read the original file content to preserve formatting and comments
            with open(file_path, 'r') as file:
                original_content = file.read()
            
            # Check if the common_name, scientific_name, and family fields are quoted
            common_name_match = re.search(r'common_name:\s*([^"\'\n]+)$', original_content, re.MULTILINE)
            if common_name_match and not (common_name_match.group(1).startswith('"') or common_name_match.group(1).startswith("'")):
                unquoted_value = common_name_match.group(1).strip()
                original_content = re.sub(
                    r'(common_name:\s*)([^"\'\n]+)$', 
                    r'\1"' + unquoted_value + r'"', 
                    original_content, 
                    flags=re.MULTILINE
                )
                print(f"Added quotes to common_name in {filename}")
                updated_count += 1
                
            scientific_name_match = re.search(r'scientific_name:\s*([^"\'\n]+)$', original_content, re.MULTILINE)
            if scientific_name_match and not (scientific_name_match.group(1).startswith('"') or scientific_name_match.group(1).startswith("'")):
                unquoted_value = scientific_name_match.group(1).strip()
                original_content = re.sub(
                    r'(scientific_name:\s*)([^"\'\n]+)$', 
                    r'\1"' + unquoted_value + r'"', 
                    original_content, 
                    flags=re.MULTILINE
                )
                print(f"Added quotes to scientific_name in {filename}")
                updated_count += 1
                
            family_match = re.search(r'family:\s*([^"\'\n]+)$', original_content, re.MULTILINE)
            if family_match and not (family_match.group(1).startswith('"') or family_match.group(1).startswith("'")):
                unquoted_value = family_match.group(1).strip()
                original_content = re.sub(
                    r'(family:\s*)([^"\'\n]+)$', 
                    r'\1"' + unquoted_value + r'"', 
                    original_content, 
                    flags=re.MULTILINE
                )
                print(f"Added quotes to family in {filename}")
                updated_count += 1
            
            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.write(original_content)
                
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            error_count += 1
    
    return updated_count, error_count

if __name__ == "__main__":
    updated, errors = normalize_tree_files()
    print(f"\nSummary: Updated {updated} files with {errors} errors")