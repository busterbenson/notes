#!/usr/bin/env python3

import os
import re
import yaml
import sys

def add_section_headers_and_spacing(content):
    """Add section headers and proper spacing between sections."""
    
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
    
    # Add spacing before section headers
    for _, header in sections:
        if header in content:
            # Add blank line before section headers if not already present
            content = re.sub(r'([^\n])\n' + re.escape(header), r'\1\n\n' + header, content)
    
    # Ensure consistent spacing in features section
    if "  # Core features" in content:
        # Fix spacing between feature categories
        feature_categories = ["always_true:", "usually_true:", "sometimes_true:", "never_true:"]
        for category in feature_categories:
            if category in content:
                # Add spacing after category and between feature items
                content = re.sub(r'(' + re.escape(category) + r')\s*\n\s*-', r'\1\n\n    - ', content)
                content = re.sub(r'(\n\s+- feature_id:.*?)(\n\s+- feature_id:)', r'\1\n\n\2', content)
    
    # Ensure consistent spacing in "kid_friendly_identification"
    if "  # Kid-friendly identification" in content:
        content = re.sub(r'(detective_steps:)\s*\n\s*-', r'\1\n    - ', content)
        content = re.sub(r'(\n\s+- step:.*?)(\n\s+- step:)', r'\1\n\n\2', content)

    # Ensure consistent spacing in seasonal timeline
    if "  # Seasonal changes" in content:
        content = re.sub(r'(seasonal_timeline:)\s*\n\s*-', r'\1\n  - ', content)
        content = re.sub(r'(\n\s+- season:.*?)(\n\s+- season:)', r'\1\n\n\2', content)
    
    # Ensure consistent spacing in confirmation checklist
    if "confirmation_checklist:" in content:
        content = re.sub(r'(confirmation_checklist:)\s*\n\s*-', r'\1\n  - ', content)
        content = re.sub(r'(\n\s+- feature:.*?)(\n\s+- feature:)', r'\1\n\n\2', content)
    
    # Ensure consistent spacing in look_alikes
    if "look_alikes:" in content:
        content = re.sub(r'(look_alikes:)\s*\n\s*-', r'\1\n  - ', content)
        content = re.sub(r'(\n\s+- species:.*?)(\n\s+- species:)', r'\1\n\n\2', content)
    
    # Ensure consistent spacing in cultural_significance
    if "cultural_significance:" in content:
        content = re.sub(r'(cultural_significance:)\s*\n\s*-', r'\1\n\n  - ', content)
        content = re.sub(r'(\n\s+- culture:.*?)(\n\s+- culture:)', r'\1\n\n\2', content)
        
    # Ensure proper indentation for cultural_significance's physical_uses and symbolic_meaning
    if "physical_uses:" in content:
        content = re.sub(r'physical_uses:\s*\n\s*-', r'physical_uses:\n    - ', content)
    
    if "symbolic_meaning:" in content:
        content = re.sub(r'symbolic_meaning:\s*\n\s*-', r'symbolic_meaning:\n    - ', content)
    
    # Add quotes to summary, primary_markers, and other string values if missing
    if "summary:" in content and not 'summary: "' in content:
        content = re.sub(r'summary: ([^\n"]+)', r'summary: "\1"', content)
    
    # Fix indentation for family, scientific_genus, and common_genus
    for field in ["family:", "scientific_genus:", "common_genus:"]:
        if field in content:
            content = re.sub(r'(\n\s+)' + field + r'([^\n]+)', r'\1' + field + r'\2', content)
    
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
    
    # Skip the reference file
    if "asparagaceae.joshua-tree.yml" in tree_files:
        tree_files.remove("asparagaceae.joshua-tree.yml")
    
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