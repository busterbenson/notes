#!/usr/bin/env python3

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

def extract_tree_species_and_genera(content):
    """Extract tree species and genera from the shape-size-path.md file."""
    tree_species = []
    genera = []
    
    # Regular expression patterns
    # Look for lines with tree names in format "Common Name (Scientific Name)"
    tree_pattern = re.compile(r'([A-Z][a-z]+(?:[ \-](?:[A-Z][a-z]+|and))*) \(((?:[A-Z][a-z]+)(?: [a-z]+)?)\)')
    
    # Look for uppercase words ending with "GENUS" like "OAK GENUS"
    genus_pattern = re.compile(r'([A-Z]+ GENUS) \(([A-Z][a-z]+)\)')
    
    lines = content.split('\n')
    
    # Track seen items to avoid duplicates
    seen_trees = set()
    seen_genera = set()
    
    for line in lines:
        # Find tree species
        tree_matches = tree_pattern.findall(line)
        for match in tree_matches:
            common_name = match[0]
            scientific_name = match[1]
            # Remove any trailing characters like colons
            scientific_name = scientific_name.strip(':,.')
            
            # Only add if we haven't seen this scientific name before
            if scientific_name not in seen_trees:
                tree_species.append((common_name, scientific_name))
                seen_trees.add(scientific_name)
        
        # Find genera
        genus_matches = genus_pattern.findall(line)
        for match in genus_matches:
            genus_name = match[0].replace(" GENUS", "")
            scientific_genus = match[1]
            
            # Only add if we haven't seen this scientific genus before
            if scientific_genus not in seen_genera:
                genera.append((genus_name, scientific_genus))
                seen_genera.add(scientific_genus)
    
    return tree_species, genera

def normalize_name(name):
    """Convert a name to lowercase with hyphens instead of spaces for filename comparison."""
    return name.lower().replace(' ', '-')

def get_file_species_map(tree_files):
    """Create a mapping from species scientific names to file paths."""
    species_to_file = {}
    
    for file_path in tree_files:
        filename = os.path.basename(file_path)
        # Extract genus and species from filename
        if '.' in filename:
            parts = filename.split('.')
            if len(parts) >= 2:
                genus_species = parts[1].lower()
                # Handle both formats: genus-species.yml and genus.yml
                if '-' in genus_species:
                    genus, species = genus_species.split('-', 1)
                    species_name = f"{genus} {species.replace('-', ' ')}".replace('.yml', '')
                    species_to_file[species_name] = file_path
    
    return species_to_file

def get_file_genus_map(genus_files):
    """Create a mapping from genus scientific names to file paths."""
    genus_to_file = {}
    
    for file_path in genus_files:
        filename = os.path.basename(file_path)
        # Extract genus from filename
        if '.' in filename:
            parts = filename.split('.')
            if len(parts) >= 2:
                genus = parts[1].lower()
                # Handle genus.yml format
                genus_name = genus.replace('.yml', '')
                genus_to_file[genus_name] = file_path
    
    return genus_to_file

def check_existing_files(tree_species, genera, tree_files, genus_files):
    """Check which tree species and genera have existing files."""
    # Get the filename mappings
    species_to_file = get_file_species_map(tree_files)
    genus_to_file = get_file_genus_map(genus_files)
    
    # Track results
    existing_trees = []
    missing_trees = []
    existing_genera = []
    missing_genera = []
    
    # Also create simple lists of filename basenames for secondary checking
    tree_filenames = [os.path.basename(f).lower() for f in tree_files]
    genus_filenames = [os.path.basename(f).lower() for f in genus_files]
    
    # Check tree species
    for common_name, scientific_name in tree_species:
        parts = scientific_name.split()
        if len(parts) >= 2:
            genus = parts[0].lower()
            species = ' '.join(parts[1:]).lower()
            full_name = f"{genus} {species}"
            
            if full_name in species_to_file:
                existing_trees.append((common_name, scientific_name, os.path.basename(species_to_file[full_name])))
            else:
                # Try a more flexible search through filenames
                found = False
                species_hyphenated = species.replace(' ', '-')
                for filename in tree_filenames:
                    if genus in filename and species_hyphenated in filename:
                        existing_trees.append((common_name, scientific_name, filename))
                        found = True
                        break
                
                if not found:
                    missing_trees.append((common_name, scientific_name, f"[{genus}-{species_hyphenated}.yml]"))
    
    # Check genera
    for common_name, scientific_genus in genera:
        genus = scientific_genus.lower()
        
        if genus in genus_to_file:
            existing_genera.append((common_name, scientific_genus, os.path.basename(genus_to_file[genus])))
        else:
            # Try a more flexible search
            found = False
            common_normalized = normalize_name(common_name)
            for filename in genus_filenames:
                if genus in filename or common_normalized in filename:
                    existing_genera.append((common_name, scientific_genus, filename))
                    found = True
                    break
            
            if not found:
                missing_genera.append((common_name, scientific_genus, f"[{genus}.yml]"))
    
    return existing_trees, missing_trees, existing_genera, missing_genera

def california_native_or_common(common_name, scientific_name):
    """Determine if a tree is native to California or commonly cultivated, based on name and common knowledge."""
    california_natives = {
        'Coast Redwood', 'Giant Sequoia', 'Sugar Pine', 'Ponderosa Pine', 'Jeffrey Pine',
        'Sierra Juniper', 'Western Juniper', 'Sitka Spruce', 'Noble Fir', 'Lodgepole Pine',
        'Bishop Pine', 'Monterey Pine', 'Valley Oak', 'Coast Live Oak', 'Blue Oak',
        'California Black Oak', 'Oregon White Oak', 'Canyon Live Oak', 'Torrey Pine',
        'Gray Pine', 'Knobcone Pine', 'California Red Fir', 'White Fir', 'Douglas-fir',
        'Pacific Dogwood', 'Western Redbud', 'Joshua Tree', 'California Fan Palm',
        'Pacific Madrone', 'Manzanita', 'California Buckeye'
    }
    
    commonly_cultivated = {
        'Dawn Redwood', 'Deodar Cedar', 'Atlas Cedar', 'Italian Cypress', 'Tulip Tree',
        'London Plane Tree', 'American Sycamore', 'Ginkgo', 'Japanese Maple', 'Silver Maple',
        'Red Maple', 'Norway Maple', 'English Oak', 'Southern Magnolia', 'Bradford Pear',
        'Flowering Dogwood', 'American Elm', 'Chinese Elm', 'Mexican Fan Palm',
        'Date Palm', 'Crape Myrtle', 'Jacaranda', 'Blue Spruce', 'Lombardy Poplar',
        'Weeping Willow', 'Birch', 'European Beech', 'Honey Locust', 'Olive'
    }
    
    # Check if common name matches a known native
    for native in california_natives:
        if native.lower() in common_name.lower():
            return "Native to California"
    
    # Check if common name matches a commonly cultivated tree
    for cultivated in commonly_cultivated:
        if cultivated.lower() in common_name.lower():
            return "Commonly cultivated"
    
    # Default to unknown status
    return "Status unknown"

def main():
    # Base directories
    base_dir = Path("/Users/buster/projects/notes/_trees")
    shape_size_path = base_dir / "decision_trees/paths/shape-size-path.md"
    trees_dir = base_dir / "trees"
    genus_dir = base_dir / "genus"
    
    # Check if the file exists
    if not shape_size_path.exists():
        print(f"Error: File not found: {shape_size_path}")
        sys.exit(1)
    
    # Read the content of the file
    with open(shape_size_path, "r") as file:
        content = file.read()
    
    # Extract tree species and genera from the file
    tree_species, genera = extract_tree_species_and_genera(content)
    
    # Get lists of existing tree and genus files
    tree_files = list(trees_dir.glob("*.yml"))
    genus_files = list(genus_dir.glob("*.yml"))
    
    # Check which tree species and genera have existing files
    existing_trees, missing_trees, existing_genera, missing_genera = check_existing_files(
        tree_species, genera, tree_files, genus_files
    )
    
    # Print summary
    print(f"Total tree species mentioned in shape-size-path.md: {len(tree_species)}")
    print(f"Total genera mentioned in shape-size-path.md: {len(genera)}")
    print(f"Tree species with existing files: {len(existing_trees)}")
    print(f"Tree species without files: {len(missing_trees)}")
    print(f"Genera with existing files: {len(existing_genera)}")
    print(f"Genera without files: {len(missing_genera)}")
    
    # Print detailed reports
    if existing_trees:
        print("\n=== EXISTING TREE SPECIES ===")
        for common_name, scientific_name, filename in existing_trees:
            print(f"- {common_name} ({scientific_name}) -> {filename}")
    
    if missing_trees:
        print("\n=== MISSING TREE SPECIES ===")
        for common_name, scientific_name, expected_filename in missing_trees:
            status = california_native_or_common(common_name, scientific_name)
            print(f"- {common_name} ({scientific_name}) -> {expected_filename} - {status}")
    
    if existing_genera:
        print("\n=== EXISTING GENERA ===")
        for common_name, scientific_genus, filename in existing_genera:
            print(f"- {common_name} GENUS ({scientific_genus}) -> {filename}")
    
    if missing_genera:
        print("\n=== MISSING GENERA ===")
        for common_name, scientific_genus, expected_filename in missing_genera:
            print(f"- {common_name} GENUS ({scientific_genus}) -> {expected_filename}")
    
    # Print recommendations
    print("\n=== RECOMMENDATIONS ===")
    print("1. Consider creating files for California native trees that are missing")
    print("2. Consider creating files for commonly cultivated trees in California")
    print("3. For trees that are neither native nor commonly cultivated, consider removing them from the shape-size-path.md file")
    print("4. Ensure all mentioned genera have corresponding genus files")
    print("5. Consider adding specific pattern matches in the script to identify more tree files")

if __name__ == "__main__":
    main()