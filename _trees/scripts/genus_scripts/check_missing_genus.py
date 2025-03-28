#!/usr/bin/env python3

import os
import re

# Directory paths
TREES_DIR = "trees"

def check_missing_genus():
    """Check which tree files are missing genus information."""
    missing_count = 0
    total_count = 0
    missing_files = []
    
    # Get all tree files
    tree_files = [f for f in os.listdir(TREES_DIR) if f.endswith('.yml')]
    total_count = len(tree_files)
    
    for filename in tree_files:
        file_path = os.path.join(TREES_DIR, filename)
        
        try:
            # Read the file content
            with open(file_path, 'r') as file:
                content = file.read()
            
            # Check if genus information is missing
            if not re.search(r'scientific_genus:', content) or not re.search(r'common_genus:', content):
                missing_files.append(filename)
                missing_count += 1
                
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    print("\nFiles missing genus information:")
    for filename in sorted(missing_files):
        print(filename)
    
    print(f"\nSummary: {missing_count}/{total_count} files missing genus information, {total_count - missing_count} complete")
    
    return missing_files

if __name__ == "__main__":
    check_missing_genus()