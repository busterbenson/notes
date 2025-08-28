#!/usr/bin/env python3

import os
import re
import sys

def add_section_headers_and_spacing(content):
    """Add section headers and proper spacing between sections."""
    
    # First, ensure tree: is at the beginning
    if not content.startswith("tree:"):
        content = "tree:" + content.split("tree:", 1)[1]
    
    # Replace existing section headers with standardized format
    sections = [
        (r"# Basic summary", "  # Basic summary"),
        (r"# Identification path", "  # Identification path"),
        (r"# Core features", "  # Core features"),
        (r"# Kid-friendly identification", "  # Kid-friendly identification"),
        (r"# Seasonal changes", "  # Seasonal changes"),
        (r"# Seasonal timeline", "  # Seasonal changes"),
        (r"# Additional required sections", "  # Additional required sections"),
        (r"# Look-alike species", "  # Look-alike species"),
        (r"# Cultural & ecological notes", "  # Cultural & ecological notes"),
        (r"# Cultural significance", "  # Cultural significance"),
        (r"# Range within California", "  # Range within California"),
        (r"# Physical characteristics", "  # Physical characteristics"),
        (r"# Conservation status", "  # Conservation status"),
        (r"# Decision tree placement", "  # Decision tree placement"),
        (r"# Wildlife value", "  # Wildlife value"),
    ]
    
    # First ensure all section headers are properly formatted
    for old_header, new_header in sections:
        if old_header in content:
            content = content.replace(old_header, new_header)
    
    # Add white space before top level fields
    top_level_fields = [
        "common_name:", 
        "scientific_name:", 
        "scientific_genus:", 
        "common_genus:", 
        "family:"
    ]
    
    for i, field in enumerate(top_level_fields):
        if i > 0 and field in content:  # Skip the first field
            prev_field = top_level_fields[i-1]
            pattern = f'({prev_field}.*?\n)({field})'
            content = re.sub(pattern, r'\1\n\2', content, flags=re.DOTALL)
    
    # Add spacing before section headers
    for _, header in sections:
        if header in content:
            # Add blank line before section headers
            content = re.sub(r'([^\n])\n' + re.escape(header), r'\1\n\n' + header, content)
    
    # Ensure consistent spacing in features section
    if "  # Core features" in content:
        # Add blank line after features: line
        content = re.sub(r'(features:)\s*\n', r'\1\n\n', content)
        
        # Fix spacing between feature categories
        feature_categories = ["always_true:", "usually_true:", "sometimes_true:", "never_true:"]
        for category in feature_categories:
            if category in content:
                # Ensure proper indentation of category
                content = re.sub(r'([^\n])\n(\s*)' + category, r'\1\n\n\2' + category, content)
                
                # Add spacing after category header and between feature items
                content = re.sub(r'(' + re.escape(category) + r')\s*\n\s*-', r'\1\n\n    - ', content)
                
                # Add blank lines between feature items
                content = re.sub(r'(\n\s+- feature_id: "[^"]+?".*?)(\n\s+- feature_id:)', 
                                r'\1\n\n\2', content, flags=re.DOTALL)
    
    # Ensure consistent spacing in "kid_friendly_identification"
    if "  # Kid-friendly identification" in content:
        # Add proper spacing for detective_steps
        content = re.sub(r'(detective_steps:)\s*\n\s*-', r'\1\n    - ', content)
        
        # Add blank lines between steps
        content = re.sub(r'(\n\s+- step: \d+.*?)(\n\s+- step:)', 
                        r'\1\n\n\2', content, flags=re.DOTALL)

    # Ensure consistent spacing in seasonal timeline
    if "seasonal_timeline:" in content:
        # Add proper indentation
        content = re.sub(r'(seasonal_timeline:)\s*\n\s*-', r'\1\n  - ', content)
        
        # Add blank lines between seasons
        content = re.sub(r'(\n\s+- season: "[^"]+?".*?)(\n\s+- season:)', 
                        r'\1\n\n\2', content, flags=re.DOTALL)
    
    # Ensure consistent spacing in confirmation checklist
    if "confirmation_checklist:" in content:
        # Add proper indentation
        content = re.sub(r'(confirmation_checklist:)\s*\n\s*-', r'\1\n  - ', content)
        
        # Add blank lines between items
        content = re.sub(r'(\n\s+- feature: "[^"]+?".*?)(\n\s+- feature:)', 
                        r'\1\n\n\2', content, flags=re.DOTALL)
    
    # Ensure consistent spacing in look_alikes
    if "look_alikes:" in content:
        # Add proper indentation
        content = re.sub(r'(look_alikes:)\s*\n\s*-', r'\1\n  - ', content)
        
        # Add blank lines between species
        content = re.sub(r'(\n\s+- species: "[^"]+?".*?)(\n\s+- species:)', 
                        r'\1\n\n\2', content, flags=re.DOTALL)
    
    # Ensure consistent spacing in cultural_significance
    if "cultural_significance:" in content:
        # Add proper indentation and spacing
        content = re.sub(r'(cultural_significance:)\s*\n\s*-', r'\1\n\n  - ', content)
        
        # Add blank lines between cultures
        content = re.sub(r'(\n\s+- culture: "[^"]+?".*?)(\n\s+- culture:)', 
                        r'\1\n\n\2', content, flags=re.DOTALL)
        
    # Ensure proper indentation for cultural_significance's physical_uses and symbolic_meaning
    if "physical_uses:" in content:
        content = re.sub(r'(physical_uses:)\s*\n\s*-', r'\1\n    - ', content)
    
    if "symbolic_meaning:" in content:
        content = re.sub(r'(symbolic_meaning:)\s*\n\s*-', r'\1\n    - ', content)
    
    # Add quotes to summary, primary_markers, and other string values if missing
    if "summary:" in content and not 'summary: "' in content:
        content = re.sub(r'summary: ([^\n"]+)', r'summary: "\1"', content)
    
    return content

def reformat_tree_files():
    """Reformat all tree files to match the style of the Joshua Tree file."""
    trees_dir = os.path.join(os.getcwd(), "trees")
    
    if not os.path.exists(trees_dir):
        print(f"Directory {trees_dir} not found")
        return
    
    reference_file = os.path.join(trees_dir, "asparagaceae.joshua-tree.yml")
    if not os.path.exists(reference_file):
        print(f"Reference file {reference_file} not found")
        return
        
    # Get a list of all .yml files in the trees directory
    tree_files = [f for f in os.listdir(trees_dir) if f.endswith('.yml')]
    
    print(f"Found {len(tree_files)} tree files to reformat")
    
    for filename in tree_files:
        filepath = os.path.join(trees_dir, filename)
        
        # Read the current content
        with open(filepath, 'r') as file:
            content = file.read()
        
        # Apply the formatting
        new_content = add_section_headers_and_spacing(content)
        
        # Write the reformatted content back
        with open(filepath, 'w') as file:
            file.write(new_content)
    
    print(f"Reformatted {len(tree_files)} tree files")

if __name__ == "__main__":
    reformat_tree_files()