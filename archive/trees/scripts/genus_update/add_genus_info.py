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

def get_common_genus(scientific_genus, scientific_name):
    """Get the common genus name based on scientific genus."""
    # Define mappings for common genuses
    genus_mappings = {
        # Pines
        "Pinus": "Pine",
        
        # Firs
        "Abies": "Fir",
        
        # Spruces
        "Picea": "Spruce",
        
        # Cedars
        "Cedrus": "True Cedar",
        "Calocedrus": "Incense Cedar",
        "Thuja": "Cedar",
        "Chamaecyparis": "Cedar",
        
        # Cypress
        "Cupressus": "Cypress",
        
        # Oaks
        "Quercus": {
            "white_oak": ["lobata", "garryana", "douglasii", "engelmannii"],  # White Oak species
            "live_oak": ["agrifolia", "wislizeni", "chrysolepis", "tomentella"],  # Live Oak species
            "black_oak": ["kelloggii", "velutina"]  # Black Oak species
        },
        
        # Maples
        "Acer": "Maple",
        
        # Dogwoods
        "Cornus": "Dogwood",
        
        # Alders
        "Alnus": "Alder",
        
        # Birches
        "Betula": "Birch",
        
        # Ash
        "Fraxinus": "Ash",
        
        # Redwoods
        "Sequoia": "Redwood",
        "Sequoiadendron": "Giant Sequoia",
        
        # Junipers
        "Juniperus": "Juniper",
        
        # Elms
        "Ulmus": "Elm",
        
        # Walnuts
        "Juglans": "Walnut",
        
        # Eucalyptus
        "Eucalyptus": "Eucalyptus",
        
        # Madrone
        "Arbutus": "Madrone",
        
        # Bay
        "Umbellularia": "Bay Laurel",
        
        # Sycamore
        "Platanus": "Sycamore",
        
        # Aspen/Cottonwood
        "Populus": {
            "aspen": ["tremuloides", "grandidentata"],  # Aspen species
            "cottonwood": ["fremontii", "deltoides", "trichocarpa"]  # Cottonwood species
        },
        
        # Laurel
        "Laurus": "Laurel",
        
        # Palms
        "Washingtonia": "Fan Palm",
        
        # Douglas Fir
        "Pseudotsuga": "Douglas-fir",
        
        # Hemlock
        "Tsuga": "Hemlock",
        
        # Yew
        "Taxus": "Yew",
        
        # Buckeye
        "Aesculus": "Buckeye",
        
        # Locust
        "Robinia": "Locust",
        "Gleditsia": "Locust",
    }
    
    # Check if we have a mapping for this genus
    if scientific_genus in genus_mappings:
        mapping = genus_mappings[scientific_genus]
        
        # For simple mappings
        if isinstance(mapping, str):
            return mapping
        
        # For complex mappings like oaks and poplars
        if isinstance(mapping, dict):
            species_part = scientific_name.split()[1] if len(scientific_name.split()) > 1 else ""
            
            for common_type, species_list in mapping.items():
                if any(sp in species_part for sp in species_list):
                    if common_type == "white_oak":
                        return "White Oak"
                    elif common_type == "live_oak":
                        return "Live Oak"
                    elif common_type == "black_oak":
                        return "Black Oak"
                    elif common_type == "aspen":
                        return "Aspen"
                    elif common_type == "cottonwood":
                        return "Cottonwood"
            
            # Default for complex mappings
            if scientific_genus == "Quercus":
                return "Oak"
            elif scientific_genus == "Populus":
                return "Poplar"
    
    # If we don't have a specific mapping, use "Unknown"
    return "Unknown"

def add_genus_info(content, filename):
    """Add genus information to a tree file while preserving structure."""
    # Extract the scientific name
    scientific_name_match = re.search(r'scientific_name:\s*"([^"]+)"', content)
    if not scientific_name_match:
        return content
    
    scientific_name = scientific_name_match.group(1)
    scientific_genus = extract_genus(scientific_name)
    
    # Get common genus based on scientific genus
    common_genus = get_common_genus(scientific_genus, scientific_name)
    
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
    if len(sys.argv) > 1:
        # Process a specific file
        process_single_file(sys.argv[1])
    else:
        # Process the Joshua Tree file as a test
        process_single_file("asparagaceae.joshua-tree.yml")