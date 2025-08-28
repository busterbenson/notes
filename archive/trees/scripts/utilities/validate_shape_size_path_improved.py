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

def find_tree_file(scientific_name, tree_files):
    """Find a tree file matching the scientific name, return None if not found."""
    genus, *species_parts = scientific_name.lower().split()
    species = " ".join(species_parts)
    species_hyphenated = species.replace(" ", "-")
    
    # Strategy 1: Look for direct match in filename
    for file_path in tree_files:
        filename = os.path.basename(file_path).lower()
        if genus in filename and species_hyphenated in filename:
            return file_path
    
    # Strategy 2: Look for common name in files
    common_name_pattern = scientific_name.split()[0].lower()
    for file_path in tree_files:
        filename = os.path.basename(file_path).lower()
        if genus in filename and (species_hyphenated in filename or any(part in filename for part in species.split())):
            return file_path
    
    # Strategy 3: Check file contents for scientific name or common name terms
    genus_species = f"{genus} {species}"
    for file_path in tree_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read().lower()
                if genus_species in content or species_hyphenated in content:
                    return file_path
        except Exception:
            continue
            
    return None

def find_genus_file(scientific_genus, common_genus, genus_files):
    """Find a genus file matching the scientific or common genus name."""
    scientific_genus = scientific_genus.lower()
    common_genus = common_genus.lower()
    
    # Strategy 1: Look for direct match in filename
    for file_path in genus_files:
        filename = os.path.basename(file_path).lower()
        if scientific_genus in filename:
            return file_path
        
        # Try to match the common name
        common_words = common_genus.split()
        for word in common_words:
            if word in filename and len(word) > 3:  # Avoid short words like "oak"
                return file_path
    
    # Strategy 2: Check file contents for genus name
    for file_path in genus_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read().lower()
                if scientific_genus in content:
                    return file_path
        except Exception:
            continue
    
    return None

def check_existing_files(tree_species, genera, tree_files, genus_files):
    """Check which tree species and genera have existing files."""
    # Track results
    existing_trees = []
    missing_trees = []
    existing_genera = []
    missing_genera = []
    
    # Create sets of filenames for faster lookups
    tree_filenames = {os.path.basename(f).lower() for f in tree_files}
    genus_filenames = {os.path.basename(f).lower() for f in genus_files}
    
    # Special case mappings for known species
    special_case_map = {
        "Sequoia sempervirens": "cupressaceae.coast-redwood.yml",
        "Sequoiadendron giganteum": "cupressaceae.giant-sequoia.yml",
        "Metasequoia glyptostroboides": "cupressaceae.dawn-redwood.yml",
        "Pinus lambertiana": "pinaceae.sugar-pine.yml",
        "Pinus ponderosa": "pinaceae.ponderosa-pine.yml",
        "Picea sitchensis": "pinaceae.sitka-spruce.yml",
        "Abies procera": "pinaceae.noble-fir.yml",
        "Quercus lobata": "fagaceae.valley-oak.yml",
        "Quercus agrifolia": "fagaceae.coast-live-oak.yml",
        "Cornus nuttallii": "cornaceae.pacific-dogwood.yml",
        "Cercis occidentalis": "fabaceae.california-redbud.yml",
        "Juniperus occidentalis": "cupressaceae.western-juniper.yml",
        "Acer palmatum": "sapindaceae.japanese-maple.yml",
        "Chamaecyparis lawsoniana": "cupressaceae.port-orford-cedar.yml",
        "Thuja plicata": "cupressaceae.western-redcedar.yml",
    }
    
    # Special case mappings for known genera
    special_genus_map = {
        "Salix": "salicaceae.aspen.yml",  # Close enough, needs a proper willow genus file
        "Populus": "salicaceae.aspen.yml", 
        "Sequoiadendron": "cupressaceae.redwood.yml",
        "Metasequoia": "cupressaceae.redwood.yml",
        "Liriodendron": None,  # No corresponding genus
        "Sciadopitys": None,   # No corresponding genus
        "Washingtonia": "arecaceae.palm.yml",
        "Phoenix": "arecaceae.palm.yml",
        "Fouquieria": None,    # No corresponding genus
        "Yucca": "asparagaceae.joshua-tree.yml",  # Close mapping
        "Cedrus": "pinaceae.true-cedar.yml",
        "Tsuga": "pinaceae.hemlock.yml",
        "Pseudotsuga": "pinaceae.douglas-fir.yml",
    }
    
    # Check tree species
    for common_name, scientific_name in tree_species:
        # Check special case mapping first
        if scientific_name in special_case_map and special_case_map[scientific_name] is not None:
            filename = special_case_map[scientific_name]
            if any(os.path.basename(f).lower() == filename.lower() for f in tree_files):
                existing_trees.append((common_name, scientific_name, filename))
                continue
        
        # Try to find a matching file
        file_path = find_tree_file(scientific_name, tree_files)
        if file_path:
            filename = os.path.basename(file_path)
            existing_trees.append((common_name, scientific_name, filename))
        else:
            missing_trees.append((common_name, scientific_name, f"[{scientific_name.lower().replace(' ', '-')}.yml]"))
    
    # Check genera
    for common_name, scientific_genus in genera:
        # Check special case mapping first
        if scientific_genus in special_genus_map and special_genus_map[scientific_genus] is not None:
            filename = special_genus_map[scientific_genus]
            if any(os.path.basename(f).lower() == filename.lower() for f in genus_files):
                existing_genera.append((common_name, scientific_genus, filename))
                continue
            
        # Try to find a matching file
        file_path = find_genus_file(scientific_genus, common_name, genus_files)
        if file_path:
            filename = os.path.basename(file_path)
            existing_genera.append((common_name, scientific_genus, filename))
        else:
            missing_genera.append((common_name, scientific_genus, f"[{scientific_genus.lower()}.yml]"))
    
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
        'Pacific Madrone', 'Manzanita', 'California Buckeye', 'Port Orford Cedar', 
        'Western Hemlock', 'Brewer Spruce', 'Mountain Hemlock', 'Incense-cedar',
        'Alaska-cedar', 'Western White Pine', 'Bristlecone Pine', 'Whitebark Pine',
        'Limber Pine', 'Engelmann Spruce', 'Pinyon Pine', 'Desert Willow'
    }
    
    commonly_cultivated = {
        'Dawn Redwood', 'Deodar Cedar', 'Atlas Cedar', 'Italian Cypress', 'Tulip Tree',
        'London Plane Tree', 'American Sycamore', 'Ginkgo', 'Japanese Maple', 'Silver Maple',
        'Red Maple', 'Norway Maple', 'English Oak', 'Southern Magnolia', 'Bradford Pear',
        'Flowering Dogwood', 'American Elm', 'Chinese Elm', 'Mexican Fan Palm',
        'Date Palm', 'Crape Myrtle', 'Jacaranda', 'Blue Spruce', 'Lombardy Poplar',
        'Weeping Willow', 'Birch', 'European Beech', 'Honey Locust', 'Olive',
        'Norway Spruce', 'Serbian Spruce', 'Umbrella Pine', 'Japanese Black Pine',
        'Lebanese Cedar', 'True Cedar', 'European Hornbeam', 'Chinese Pistache',
        'Camphor Tree', 'Corkscrew Willow', 'Sweet Gum', 'Saucer Magnolia',
        'Golden Rain Tree', 'Eastern Redbud', 'Bald Cypress', 'Weeping Cherry'
    }
    
    # Check if common name matches a known native
    for native in california_natives:
        if native.lower() in common_name.lower():
            return "Native to California"
    
    # Check if common name matches a commonly cultivated tree
    for cultivated in commonly_cultivated:
        if cultivated.lower() in common_name.lower():
            return "Commonly cultivated"
    
    # Check scientific name for clues
    scientific_parts = scientific_name.split()
    if len(scientific_parts) >= 2:
        # Common California native genera
        calif_native_genera = {'pinus', 'quercus', 'abies', 'picea', 'sequoia', 'calocedrus', 'tsuga', 'chamaecyparis', 'juniperus'}
        genus = scientific_parts[0].lower()
        if genus in calif_native_genera:
            return "Likely native (genus typical to California)"
        
        # Check for species names that suggest California nativity
        calif_species = {'californica', 'californicus', 'californicum', 'pacifica', 'occidentalis', 'nevadensis', 'sierrae'}
        species = scientific_parts[1].lower()
        if species in calif_species:
            return "Likely native (species name suggests California)"
    
    # Default to unknown status
    return "Status unknown - recommend research"

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
    
    # Organize missing trees by priority
    native_trees = []
    cultivated_trees = []
    other_trees = []
    
    for common_name, scientific_name, expected_filename in missing_trees:
        status = california_native_or_common(common_name, scientific_name)
        if "Native" in status:
            native_trees.append((common_name, scientific_name, expected_filename, status))
        elif "cultivated" in status:
            cultivated_trees.append((common_name, scientific_name, expected_filename, status))
        else:
            other_trees.append((common_name, scientific_name, expected_filename, status))
    
    if missing_trees:
        print("\n=== MISSING CALIFORNIA NATIVE TREES ===")
        for common_name, scientific_name, expected_filename, status in native_trees:
            print(f"- {common_name} ({scientific_name}) -> {expected_filename} - {status}")
        
        print("\n=== MISSING COMMONLY CULTIVATED TREES ===")
        for common_name, scientific_name, expected_filename, status in cultivated_trees:
            print(f"- {common_name} ({scientific_name}) -> {expected_filename} - {status}")
        
        print("\n=== OTHER MISSING TREES ===")
        for common_name, scientific_name, expected_filename, status in other_trees:
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
    if missing_trees:
        print("1. Create files for these missing California native trees (HIGH PRIORITY):")
        for common_name, scientific_name, expected_filename, _ in native_trees[:min(5, len(native_trees))]:
            print(f"   - {common_name} ({scientific_name})")
    
        print("\n2. Create files for these missing commonly cultivated trees (MEDIUM PRIORITY):")
        for common_name, scientific_name, expected_filename, _ in cultivated_trees[:min(5, len(cultivated_trees))]:
            print(f"   - {common_name} ({scientific_name})")
    
    if missing_genera:
        print("\n3. Create these missing genus files (HIGH PRIORITY):")
        for common_name, scientific_genus, expected_filename in missing_genera:
            print(f"   - {common_name} GENUS ({scientific_genus})")
    
    if other_trees:
        print("\n4. Consider removing or replacing these trees from shape-size-path.md (LOW PRIORITY):")
        for common_name, scientific_name, _, _ in other_trees[:min(10, len(other_trees))]:
            print(f"   - {common_name} ({scientific_name})")
    
    print("\n5. File naming recommendation:")
    print("   - For tree species: familyname.genus-species.yml")
    print("   - For genera: familyname.genus.yml")

if __name__ == "__main__":
    main()