#!/usr/bin/env python3

import os
import re
import sys

def extract_genus(scientific_name):
    """Extract genus from scientific name."""
    parts = scientific_name.strip('"\'').split()
    if len(parts) >= 1:
        return parts[0]
    return "Unknown"

def add_genus_info(content, filename):
    """Add genus information to a tree file while preserving structure."""
    # Extract the scientific name
    scientific_name_match = re.search(r'scientific_name:\s*"([^"]+)"', content)
    if not scientific_name_match:
        return content
    
    scientific_name = scientific_name_match.group(1)
    scientific_genus = extract_genus(scientific_name)
    
    # Set common genus based on known mapping or use "Unknown"
    common_genus = "Unknown"
    
    # Extract family name to look for a genus mapping
    family_match = re.search(r'family:\s*"([^"]+)"', content)
    if family_match:
        family = family_match.group(1).lower()
        
        # Handle special case for Quercus (oak) species
        if scientific_genus == "Quercus":
            # For Blue Oak, oregona, garrayana: White Oak group
            if 'douglasii' in scientific_name or 'garryana' in scientific_name or 'lobata' in scientific_name:
                common_genus = "White Oak"
            # For most other oaks: Live Oak or Black Oak group
            elif 'agrifolia' in scientific_name or 'wislizeni' in scientific_name:
                common_genus = "Live Oak"
            elif 'kelloggii' in scientific_name or 'velutina' in scientific_name:
                common_genus = "Black Oak"
            else:
                common_genus = "Oak"  # Default for other oaks
        else:
            # Look for a matching genus file
            genus_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "genus")
            
            if os.path.exists(genus_folder):
                genus_files = [f for f in os.listdir(genus_folder) if f.endswith(".yml")]
                for genus_file in genus_files:
                    if scientific_genus.lower() in genus_file.lower():
                        # Read the genus file to extract common genus
                        with open(os.path.join(genus_folder, genus_file), 'r') as f:
                            genus_content = f.read()
                            common_genus_match = re.search(r'common_name:\s*"([^"]+)"', genus_content)
                            if common_genus_match:
                                common_genus = common_genus_match.group(1)
                                break
    
    # If genus info already exists, don't modify
    if re.search(r'scientific_genus:', content):
        return content
    
    # Insert genus information after scientific_name, preserving indentation
    insert_pos = scientific_name_match.end()
    indent_match = re.search(r'^(\s+)scientific_name:', content, re.MULTILINE)
    indent = indent_match.group(1) if indent_match else "  "
    
    genus_info = f'\n{indent}scientific_genus: "{scientific_genus}"\n{indent}common_genus: "{common_genus}"'
    updated_content = content[:insert_pos] + genus_info + content[insert_pos:]
    
    return updated_content

def process_single_file(filename):
    """Process a single tree file."""
    trees_dir = "/Users/buster/projects/notes/_trees/trees"
    filepath = os.path.join(trees_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist")
        return
    
    # Read the current content
    with open(filepath, 'r') as file:
        content = file.read()
    
    # Add genus information
    updated_content = add_genus_info(content, filename)
    
    # Write back only if changes were made
    if updated_content != content:
        with open(filepath, 'w') as file:
            file.write(updated_content)
        print(f"Updated {filename}")
    else:
        print(f"No changes needed for {filename}")
    
    # Display the updated content
    print("\nUpdated content:")
    print("-" * 40)
    print(updated_content[:500] + "..." if len(updated_content) > 500 else updated_content)
    print("-" * 40)

if __name__ == "__main__":
    # Test with the Joshua Tree file
    process_single_file("asparagaceae.joshua-tree.yml")