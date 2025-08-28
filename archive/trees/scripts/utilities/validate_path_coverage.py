#!/usr/bin/env python3

import os
import re
import xml.etree.ElementTree as ET
import glob
from collections import defaultdict, Counter

# Paths to analyze
PATHS_DIR = os.path.join(os.getcwd(), "decision_trees", "paths")
MINDMAP_FILE = os.path.join(PATHS_DIR, "california_tree_guide_xmind_complete.mm")

def extract_tree_genus_from_markdown(file_path):
    """Extract tree species and genus names from markdown path files."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find all tree/genus references in format: Name (Genus species)
    scientific_pattern = r'([A-Z][a-z]+\s+[a-z]+(?:(?:\s+var\.|)\s+[a-z]+)?)'
    common_genus_pattern = r'\b([A-Z][a-z]+ [A-Za-z]+|[A-Z][a-z]+)\s+\(([A-Z][a-z]+)'
    
    # Extract species
    species_matches = set()
    for match in re.finditer(r'([A-Z][a-z]+ [A-Za-z-]+)\s+\(' + scientific_pattern + r'\)', content):
        common_name = match.group(1).strip()
        scientific_name = match.group(2).strip()
        species_matches.add((common_name, scientific_name))
    
    # Extract genera
    genus_matches = set()
    for match in re.finditer(r'([A-Z][a-z]+ (GENUS|GROUP|FAMILY))\s+\(([A-Z][a-z]+)', content, re.IGNORECASE):
        genus_name = match.group(1).replace(" GENUS", "").replace(" GROUP", "").replace(" FAMILY", "").strip()
        scientific_genus = match.group(3).strip()
        genus_matches.add((genus_name, scientific_genus))
    
    # Extract other genus mentions
    for match in re.finditer(r'([A-Z][a-z]+) species', content):
        genus_name = match.group(1).strip()
        genus_matches.add((genus_name, genus_name))
    
    return species_matches, genus_matches

def extract_tree_genus_from_mindmap(file_path):
    """Extract tree species and genus names from FreeMind XML mind map."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    species_matches = set()
    genus_matches = set()
    
    # Search through all TEXT attributes in the XML
    for node in root.findall(".//node"):
        if 'TEXT' in node.attrib:
            text = node.attrib['TEXT']
            
            # Look for species: Common Name (Scientific name)
            species_match = re.search(r'([A-Z][a-z]+ [A-Za-z-]+)\s+\(([A-Z][a-z]+\s+[a-z]+(?:(?:\s+var\.|)\s+[a-z]+)?)\)', text)
            if species_match:
                common_name = species_match.group(1).strip()
                scientific_name = species_match.group(2).strip()
                species_matches.add((common_name, scientific_name))
            
            # Look for genera: GENUS (Scientific genus)
            genus_match = re.search(r'([A-Z][A-Z\s]+) (?:GENUS|GROUP|FAMILY)\s+\(([A-Z][a-z]+)', text, re.IGNORECASE)
            if genus_match:
                genus_name = genus_match.group(1).replace("GENUS", "").replace("GROUP", "").replace("FAMILY", "").strip()
                scientific_genus = genus_match.group(2).strip()
                genus_matches.add((genus_name, scientific_genus))
            
            # Check for genus references without scientific name
            genus_simple_match = re.search(r'([A-Z][a-z]+) (?:GENUS|species|spp\.)', text, re.IGNORECASE)
            if genus_simple_match and not genus_match:
                genus_name = genus_simple_match.group(1).strip()
                genus_matches.add((genus_name, genus_name))
    
    return species_matches, genus_matches

def analyze_coverage():
    """Analyze tree and genus coverage between markdown files and mindmap."""
    markdown_files = glob.glob(os.path.join(PATHS_DIR, "*-path.md"))
    
    # Extract data from markdown files
    md_species = set()
    md_genera = set()
    md_file_species = {}
    md_file_genera = {}
    
    for md_file in markdown_files:
        file_name = os.path.basename(md_file)
        species, genera = extract_tree_genus_from_markdown(md_file)
        md_file_species[file_name] = species
        md_file_genera[file_name] = genera
        md_species.update(species)
        md_genera.update(genera)
    
    # Extract data from mindmap
    mm_species, mm_genera = extract_tree_genus_from_mindmap(MINDMAP_FILE)
    
    # Find discrepancies
    missing_in_mindmap_species = md_species - mm_species
    missing_in_mindmap_genera = md_genera - mm_genera
    missing_in_markdown_species = mm_species - md_species
    missing_in_markdown_genera = mm_genera - md_genera
    
    # Generate report
    print("===== TREE AND GENUS COVERAGE ANALYSIS =====\n")
    
    print(f"Total trees in markdown paths: {len(md_species)}")
    print(f"Total trees in mindmap: {len(mm_species)}")
    print(f"Total genera in markdown paths: {len(md_genera)}")
    print(f"Total genera in mindmap: {len(mm_genera)}")
    
    print("\n--- TREES MISSING FROM MINDMAP ---")
    if missing_in_mindmap_species:
        for common, scientific in sorted(missing_in_mindmap_species):
            print(f"- {common} ({scientific})")
            # Find which files contain this species
            for file_name, species_set in md_file_species.items():
                if (common, scientific) in species_set:
                    print(f"  Found in: {file_name}")
    else:
        print("None - All trees in markdown files are covered in the mindmap!")
    
    print("\n--- GENERA MISSING FROM MINDMAP ---")
    if missing_in_mindmap_genera:
        for common, scientific in sorted(missing_in_mindmap_genera):
            print(f"- {common} Genus ({scientific})")
            # Find which files contain this genus
            for file_name, genera_set in md_file_genera.items():
                if (common, scientific) in genera_set:
                    print(f"  Found in: {file_name}")
    else:
        print("None - All genera in markdown files are covered in the mindmap!")
    
    print("\n--- TREES IN MINDMAP BUT MISSING FROM MARKDOWN ---")
    if missing_in_markdown_species:
        for common, scientific in sorted(missing_in_markdown_species):
            print(f"- {common} ({scientific})")
    else:
        print("None - All trees in mindmap are represented in markdown files!")
    
    print("\n--- GENERA IN MINDMAP BUT MISSING FROM MARKDOWN ---")
    if missing_in_markdown_genera:
        for common, scientific in sorted(missing_in_markdown_genera):
            print(f"- {common} Genus ({scientific})")
    else:
        print("None - All genera in mindmap are represented in markdown files!")
    
    # Analysis by path
    print("\n--- COVERAGE BY PATH ---")
    for file_name, species_set in sorted(md_file_species.items()):
        species_covered = sum(1 for sp in species_set if sp in mm_species)
        species_coverage = (species_covered / len(species_set)) * 100 if species_set else 100
        
        genera_set = md_file_genera[file_name]
        genera_covered = sum(1 for gen in genera_set if gen in mm_genera)
        genera_coverage = (genera_covered / len(genera_set)) * 100 if genera_set else 100
        
        print(f"{file_name}:")
        print(f"  - Trees: {species_covered}/{len(species_set)} ({species_coverage:.1f}%)")
        print(f"  - Genera: {genera_covered}/{len(genera_set)} ({genera_coverage:.1f}%)")

if __name__ == "__main__":
    analyze_coverage()