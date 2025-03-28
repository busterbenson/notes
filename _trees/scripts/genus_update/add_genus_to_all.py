#!/usr/bin/env python3

import os
import re
import sys
import csv
from collections import defaultdict

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
        "Callitropsis": "Cedar",  # Alaska Cedar
        
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
        "Metasequoia": "Dawn Redwood",
        
        # Junipers
        "Juniperus": "Juniper",
        
        # Elms
        "Ulmus": "Elm",
        "Planera": "Water Elm",
        
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
        
        # Additional mappings
        "Yucca": "Joshua Tree",  # For Joshua Tree
        "Torreya": "California Nutmeg",
        "Lithocarpus": "Tanoak",
        "Notholithocarpus": "Tanoak",  # Scientific name changed from Lithocarpus
        "Cercis": "Redbud",
        "Parkinsonia": "Palo Verde",  # Previously listed as Cercidium
        "Chilopsis": "Desert Willow",
        "Liriodendron": "Tulip Tree",
        "Lagerstroemia": "Crape Myrtle",
        "Magnolia": "Magnolia",
        "Morella": "Bayberry",  # Updated from Myrica
        "Olea": "Olive",
        "Pyrus": "Pear",
        "Amelanchier": "Serviceberry",
        "Liquidambar": "Sweet Gum",
        "Ginkgo": "Ginkgo",
        "Pistacia": "Pistache",  # Chinese Pistache
        "Jacaranda": "Jacaranda",
        "Cunninghamia": "China-fir",
        "Cryptomeria": "Japanese Cedar",
        "Larix": "Larch",
        "Fagus": "Beech",
        "Tilia": "Basswood",
        "Lophostemon": "Brisbane Box",
        "Frangula": "Buckthorn",
        "Sorbus": "Whitebeam",
        "Cercocarpus": "Mountain Mahogany",
        "Prunus": "Cherry",  # Purple Leaf Plum
        "Sapindus": "Soapberry",
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
        return content, None, None
    
    scientific_name = scientific_name_match.group(1)
    scientific_genus = extract_genus(scientific_name)
    
    # Get common genus based on scientific genus
    common_genus = get_common_genus(scientific_genus, scientific_name)
    
    # Check if genus info already exists
    sg_match = re.search(r'scientific_genus:\s*"([^"]+)"', content)
    cg_match = re.search(r'common_genus:\s*"([^"]+)"', content)
    
    if sg_match and cg_match:
        sg = sg_match.group(1)
        cg = cg_match.group(1)
        
        # Update if common_genus is "Unknown" but we now have a mapping
        if cg == "Unknown" and common_genus != "Unknown":
            # Replace the "Unknown" common genus with new value
            updated_content = re.sub(
                r'(common_genus:\s*)"Unknown"', 
                r'\1"' + common_genus + '"', 
                content
            )
            return updated_content, scientific_genus, common_genus
        else:
            # No need to update
            return content, sg, cg
    
    # If no genus info exists, insert it after scientific_name
    insert_pos = scientific_name_match.end()
    indent_match = re.search(r'^(\s+)scientific_name:', content, re.MULTILINE)
    indent = indent_match.group(1) if indent_match else "  "
    
    genus_info = f'\n{indent}scientific_genus: "{scientific_genus}"\n{indent}common_genus: "{common_genus}"'
    updated_content = content[:insert_pos] + genus_info + content[insert_pos:]
    
    return updated_content, scientific_genus, common_genus

def process_all_files(dry_run=True):
    """Process all tree files and generate a report.
    
    Args:
        dry_run: If True, only simulates changes without writing files
    """
    trees_dir = "/Users/buster/projects/notes/_trees/trees"
    
    # Track changes and status
    updated_files = []
    unchanged_files = []
    unknown_common_genus = []
    genus_counts = defaultdict(int)
    
    # Get a list of all tree files
    tree_files = [f for f in os.listdir(trees_dir) if f.endswith('.yml')]
    tree_files.sort()
    
    print(f"Processing {len(tree_files)} tree files...")
    
    # Process each file
    for filename in tree_files:
        filepath = os.path.join(trees_dir, filename)
        
        # Read the current content
        with open(filepath, 'r') as file:
            content = file.read()
        
        # Add genus information
        updated_content, scientific_genus, common_genus = add_genus_info(content, filename)
        
        # Track results
        if scientific_genus:
            genus_counts[scientific_genus] += 1
            
            if common_genus == "Unknown":
                unknown_common_genus.append((filename, scientific_genus))
        
        # Write back only if changes were made
        if updated_content != content:
            with open(filepath, 'w') as file:
                file.write(updated_content)
            updated_files.append((filename, scientific_genus, common_genus))
            print(f"Updated {filename}")
        else:
            unchanged_files.append(filename)
    
    # Generate a report
    print("\n=== Genus Information Update Report ===")
    print(f"Total files processed: {len(tree_files)}")
    print(f"Files updated: {len(updated_files)}")
    print(f"Files unchanged: {len(unchanged_files)}")
    print(f"Files with unknown common genus: {len(unknown_common_genus)}")
    
    print("\nScientific genus distribution:")
    for genus, count in sorted(genus_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {genus}: {count}")
    
    print("\nFiles with unknown common genus:")
    for filename, genus in unknown_common_genus:
        print(f"  {filename} (Genus: {genus})")
    
    # Write a CSV report
    with open("/Users/buster/projects/notes/_trees/genus_update_report.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Scientific Genus", "Common Genus", "Status"])
        
        for filename, genus, common in updated_files:
            writer.writerow([filename, genus, common, "Updated"])
        
        for filename in unchanged_files:
            match = re.search(r'scientific_genus:\s*"([^"]+)"', open(os.path.join(trees_dir, filename)).read())
            cg_match = re.search(r'common_genus:\s*"([^"]+)"', open(os.path.join(trees_dir, filename)).read())
            
            sg = match.group(1) if match else "N/A"
            cg = cg_match.group(1) if cg_match else "N/A"
            
            writer.writerow([filename, sg, cg, "Unchanged"])
    
    print("\nDetailed report saved to genus_update_report.csv")

if __name__ == "__main__":
    process_all_files(dry_run=False)