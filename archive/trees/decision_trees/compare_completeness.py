#!/usr/bin/env python3
"""
Compare completeness of tree species between path files and mind map
"""

import os
import re
import glob
from collections import defaultdict

def extract_species_from_paths(path_files_dir):
    """Extract tree species names from path markdown files"""
    species_set = set()
    path_mentions = defaultdict(list)
    
    # Define patterns to match tree species
    species_pattern = r'├── ([^:]+?)(?:\s*\(([^)]+)\))?:'
    species_pattern2 = r'├── ([^:]+?)(?:\s*\(([^)]+)\))?\s*$'
    
    # Get all markdown files in the path
    md_files = glob.glob(os.path.join(path_files_dir, "*.md"))
    
    for file_path in md_files:
        file_name = os.path.basename(file_path)
        if file_name.startswith('_') or not file_name.endswith('.md'):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Find all species mention patterns
                matches = re.findall(species_pattern, content)
                matches.extend(re.findall(species_pattern2, content))
                
                for match in matches:
                    species_name = match[0].strip()
                    if species_name and not species_name.endswith("GROUP") and not species_name.startswith("What") and not species_name.startswith("All "):
                        # Standardize species name
                        if "Tree" not in species_name and "tree" not in species_name and ":" not in species_name:
                            species_name = f"{species_name} Tree"
                        
                        species_set.add(species_name)
                        path_mentions[species_name].append(file_name)
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    return species_set, path_mentions

def extract_species_from_mindmap(mind_map_path):
    """Extract tree species names from mind map file"""
    species_set = set()
    
    try:
        with open(mind_map_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find all node TEXT attributes
            text_nodes = re.findall(r'TEXT="([^"]+)"', content)
            
            for node_text in text_nodes:
                # Filter for species nodes (usually has genus in parentheses)
                if "(" in node_text and ")" in node_text and not node_text.endswith("GROUP") and not node_text.startswith("What"):
                    species_set.add(node_text)
                # Special case for simplified entries
                elif "Tree" in node_text and not node_text.endswith("GROUP") and not node_text.startswith("What"):
                    species_set.add(node_text)
    except Exception as e:
        print(f"Error processing {mind_map_path}: {str(e)}")
    
    return species_set

def main():
    # Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    paths_dir = os.path.join(script_dir, "paths")
    mind_map_path = os.path.join(paths_dir, "california_tree_guide_xmind_complete.mm")
    
    # Extract species from both sources
    path_species, path_mentions = extract_species_from_paths(paths_dir)
    mind_map_species = extract_species_from_mindmap(mind_map_path)
    
    print(f"Found {len(path_species)} species in path files")
    print(f"Found {len(mind_map_species)} species in mind map file")
    
    # Find missing species
    missing_species = path_species - mind_map_species
    
    if missing_species:
        print(f"\nMISSING SPECIES IN MIND MAP ({len(missing_species)}):")
        for species in sorted(missing_species):
            mentioned_in = ", ".join(path_mentions[species])
            print(f"- {species} (mentioned in: {mentioned_in})")
    else:
        print("\nNo missing species found!")
        
    # Check for species in mind map but not in paths (unexpected)
    extra_species = mind_map_species - path_species
    if extra_species:
        print(f"\nSPECIES IN MIND MAP BUT NOT IN PATHS ({len(extra_species)}):")
        for species in sorted(extra_species):
            print(f"- {species}")
    
if __name__ == "__main__":
    main()