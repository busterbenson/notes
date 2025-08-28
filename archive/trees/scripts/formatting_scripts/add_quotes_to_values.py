#!/usr/bin/env python3

import os
import re
import sys

def add_quotes_to_values(content):
    """Add quotes to string values if they're missing."""
    
    # Fields that should have quoted values at the top level
    top_level_fields = [
        "common_name",
        "scientific_name",
        "scientific_genus",
        "common_genus",
        "family",
        "summary",
    ]
    
    # Add quotes to top-level fields
    for field in top_level_fields:
        pattern = r'(\s+' + field + r': )([^"\n][^\n]*)'
        if re.search(pattern, content):
            content = re.sub(pattern, r'\1"\2"', content)
    
    # Add quotes to identification_path fields
    id_path_fields = [
        "primary_markers",
        "secondary_markers",
        "seasonal_markers",
        "similar_species_differentiation",
    ]
    
    for field in id_path_fields:
        pattern = r'(\s+' + field + r': )([^"\n][^\n]*)'
        if re.search(pattern, content):
            content = re.sub(pattern, r'\1"\2"', content)
    
    # Add quotes to kid_friendly_identification fields
    kid_fields = [
        "primary_identifier",
        "memorable_comparison",
        "touch_tip",
        "smell_tip",
        "fun_fact",
    ]
    
    for field in kid_fields:
        pattern = r'(\s+' + field + r': )([^"\n][^\n]*)'
        if re.search(pattern, content):
            content = re.sub(pattern, r'\1"\2"', content)
    
    # Add quotes to feature notes, exceptions, conditions
    feature_fields = [
        "notes",
        "exceptions",
        "conditions",
    ]
    
    for field in feature_fields:
        pattern = r'(\s+' + field + r': )([^"\n][^\n]*)'
        if re.search(pattern, content):
            content = re.sub(pattern, r'\1"\2"', content)
    
    # Add quotes to feature_id values
    pattern = r'(\s+feature_id: )([^"\n][^\n]*)'
    if re.search(pattern, content):
        content = re.sub(pattern, r'\1"\2"', content)
    
    # Add quotes to physical_characteristics fields
    phys_fields = [
        "height_range",
        "growth_rate",
        "crown_spread",
        "lifespan",
        "trunk_diameter",
        "root_system",
        "toxicity",
    ]
    
    for field in phys_fields:
        pattern = r'(\s+' + field + r': )([^"\n][^\n]*)'
        if re.search(pattern, content):
            content = re.sub(pattern, r'\1"\2"', content)
    
    # Add quotes to conservation_status fields
    pattern = r'(\s+status: )([^"\n][^\n]*)'
    if re.search(pattern, content):
        content = re.sub(pattern, r'\1"\2"', content)
    
    # Add quotes to list items
    # This is more complex because we need to be careful not to quote sublists
    # First, find all list items that start with a dash and don't have quotes
    list_pattern = r'(\s+- )([^"\n:][^\n:]*(?:\n\s+[^\n-:][^\n:]*)*)'
    
    # Find all matches
    matches = re.finditer(list_pattern, content)
    
    # Process each match
    for match in reversed(list(matches)):  # Reverse to avoid offsetting issues
        # Check if this is a list item with a subfield (has a colon)
        if ":" in match.group(2):
            continue
        
        # Add quotes to the content
        start = match.start(2)
        end = match.end(2)
        quoted_content = '"' + match.group(2) + '"'
        content = content[:start] + quoted_content + content[end:]
    
    return content

def add_quotes_to_tree_files():
    """Add quotes to values in all tree files."""
    trees_dir = os.path.join(os.getcwd(), "trees")
    
    if not os.path.exists(trees_dir):
        print(f"Directory {trees_dir} not found")
        return
    
    # Get a list of all .yml files in the trees directory
    tree_files = [f for f in os.listdir(trees_dir) if f.endswith('.yml')]
    
    print(f"Found {len(tree_files)} tree files to process")
    
    for filename in tree_files:
        filepath = os.path.join(trees_dir, filename)
        
        # Read the current content
        with open(filepath, 'r') as file:
            content = file.read()
        
        # Add quotes to values
        new_content = add_quotes_to_values(content)
        
        # Write the updated content back
        with open(filepath, 'w') as file:
            file.write(new_content)
    
    print(f"Added quotes to values in {len(tree_files)} tree files")

if __name__ == "__main__":
    add_quotes_to_tree_files()