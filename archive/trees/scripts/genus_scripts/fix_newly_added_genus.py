#!/usr/bin/env python3

import os
import re

# Directory paths
TREES_DIR = "trees"

def fix_newly_added_genus():
    """Fix the formatting issues with newly added genus information."""
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
            
            # Check for the common formatting issue with genus and family on the same line
            if re.search(r'common_genus: Unknown\s+family:', content):
                print(f"Fixing {filename}: Found genus info and family on the same line")
                
                # Fix format: "common_genus: Unknown  family:" -> "common_genus: Unknown\n  family:"
                content = re.sub(
                    r'(common_genus: Unknown)\s+(family:)',
                    r'\1\n  \2',
                    content
                )
                
                # Write the fixed content back to the file
                with open(file_path, 'w') as file:
                    file.write(content)
                    
                updated_count += 1
                
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            error_count += 1
    
    return updated_count, error_count

if __name__ == "__main__":
    updated, errors = fix_newly_added_genus()
    print(f"\nSummary: Updated {updated} files with {errors} errors")