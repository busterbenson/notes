#!/usr/bin/env python3

import os
import re

# Directory paths
TREES_DIR = "trees"

def add_quotes_to_genus():
    """Add quotation marks to genus fields in tree files."""
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
            
            # Check for unquoted scientific_genus
            scientific_genus_match = re.search(r'scientific_genus:\s*([^"\'\n]+)$', content, re.MULTILINE)
            if scientific_genus_match:
                unquoted_value = scientific_genus_match.group(1).strip()
                if not unquoted_value.startswith('"') and not unquoted_value.startswith("'"):
                    # Replace unquoted value with quoted value
                    content = re.sub(
                        r'(scientific_genus:\s*)([^"\'\n]+)$', 
                        r'\1"' + unquoted_value + r'"', 
                        content, 
                        flags=re.MULTILINE
                    )
                    print(f"Added quotes to scientific_genus in {filename}")
                    updated_count += 1
            
            # Check for unquoted common_genus
            common_genus_match = re.search(r'common_genus:\s*([^"\'\n]+)$', content, re.MULTILINE)
            if common_genus_match:
                unquoted_value = common_genus_match.group(1).strip()
                if not unquoted_value.startswith('"') and not unquoted_value.startswith("'"):
                    # Replace unquoted value with quoted value
                    content = re.sub(
                        r'(common_genus:\s*)([^"\'\n]+)$', 
                        r'\1"' + unquoted_value + r'"', 
                        content, 
                        flags=re.MULTILINE
                    )
                    print(f"Added quotes to common_genus in {filename}")
                    updated_count += 1
            
            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.write(content)
                
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            error_count += 1
    
    return updated_count, error_count

if __name__ == "__main__":
    updated, errors = add_quotes_to_genus()
    print(f"\nSummary: Updated {updated} files with {errors} errors")