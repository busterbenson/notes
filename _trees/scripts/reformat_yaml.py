#!/usr/bin/env python3
import os
import sys
import re
import yaml

"""
Script to reformat tree YAML files that don't have the top-level 'tree:' element.
This script will:
1. Check if a file has a top-level 'tree:' element
2. If not, add it and reindent all content
3. Save the transformed content back to the file
"""

def process_file(file_path):
    print(f"Processing {file_path}...")
    
    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the file already has a top-level tree: element
    if content.lstrip().startswith('tree:'):
        print(f"  - Already has top-level tree: element")
        return False
    
    # Create the new content with top-level tree: and indented content
    lines = content.split('\n')
    new_lines = ['tree:']
    
    for line in lines:
        if line.strip():  # Skip empty lines at the beginning
            new_lines.append('  ' + line)
        else:
            new_lines.append(line)
    
    new_content = '\n'.join(new_lines)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  - Reformatted with top-level tree: element")
    return True

def main():
    trees_dir = '/Users/buster/projects/notes/_trees/trees'
    
    # Get list of files to process
    files_to_process = []
    for filename in os.listdir(trees_dir):
        if not filename.endswith('.yml'):
            continue
        
        file_path = os.path.join(trees_dir, filename)
        
        # Check if file has tree: top-level element
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line != 'tree:':
                files_to_process.append(file_path)
    
    print(f"Found {len(files_to_process)} files to process")
    
    # Process each file
    processed_count = 0
    for file_path in files_to_process:
        if process_file(file_path):
            processed_count += 1
    
    print(f"Reformatted {processed_count} files")

if __name__ == "__main__":
    main()