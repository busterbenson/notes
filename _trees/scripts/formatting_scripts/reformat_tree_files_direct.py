#!/usr/bin/env python3

import os
import re
import sys

def reformat_tree_file(content):
    """Reformat a tree file to match the Joshua Tree reference structure."""
    
    # First, extract all main components
    match = re.search(r'tree:\s*\n(.*?)(?=\s*# Basic summary)', content, re.DOTALL)
    if not match:
        return content  # Can't find header section
    
    header = match.group(1).strip()
    
    # Extract all sections
    sections = [
        ("# Basic summary", r'# Basic summary.*?(?=# Identification path|$)'),
        ("# Identification path", r'# Identification path.*?(?=# Core features|$)'),
        ("# Core features", r'# Core features.*?features:.*?(?=# Kid-friendly identification|$)'),
        ("features:", r'features:.*?(?=# Kid-friendly identification|$)'),
        ("# Kid-friendly identification", r'# Kid-friendly identification.*?(?=# Seasonal changes|# Seasonal timeline|$)'),
        ("# Seasonal changes", r'# Seasonal changes.*?(?=# Additional required sections|$)'),
        ("# Seasonal timeline", r'# Seasonal timeline.*?(?=# Additional required sections|$)'),
        ("# Additional required sections", r'# Additional required sections.*?(?=# Look-alike species|$)'),
        ("# Look-alike species", r'# Look-alike species.*?(?=# Cultural & ecological notes|$)'),
        ("# Cultural & ecological notes", r'# Cultural & ecological notes.*?(?=# Cultural significance|$)'),
        ("# Cultural significance", r'# Cultural significance.*?(?=# Range within California|$)'),
        ("# Range within California", r'# Range within California.*?(?=# Physical characteristics|$)'),
        ("# Physical characteristics", r'# Physical characteristics.*?(?=# Conservation status|$)'),
        ("# Conservation status", r'# Conservation status.*?(?=# Decision tree placement|$)'),
        ("# Decision tree placement", r'# Decision tree placement.*?(?=# Wildlife value|$)'),
        ("# Wildlife value", r'# Wildlife value.*?$'),
    ]
    
    # Extract content for each section
    section_contents = {}
    for section_name, pattern in sections:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            section_text = match.group(0).strip()
            # Remove the section header from the content
            if section_name != "features:":
                section_text = re.sub(r'^.*?\n', '', section_text, 1)
            section_contents[section_name] = section_text
    
    # Build the new content with proper spacing
    new_content = "tree:\n"
    new_content += header + "\n\n"
    
    # Add each section with proper spacing
    for section_name, pattern in sections:
        if section_name in section_contents:
            if section_name == "features:":
                # Skip the features section header here
                continue
                
            if section_name == "# Seasonal timeline":
                # Replace with Seasonal changes header
                new_content += "  # Seasonal changes\n" + section_contents[section_name] + "\n\n"
            else:
                new_content += f"  {section_name}\n" + section_contents[section_name] + "\n\n"
    
    # Fix formatting in features section
    if "# Core features" in section_contents and "features:" in section_contents:
        features_content = section_contents["features:"]
        
        # Fix always_true section
        if "always_true:" in features_content:
            features_content = re.sub(r'(always_true:)\s*\n\s*-', r'\1\n\n    - ', features_content)
            # Add blank lines between feature items
            features_content = re.sub(r'(\n\s+- feature_id:.*?)(\n\s+- feature_id:)', r'\1\n\n\2', features_content, flags=re.DOTALL)
        
        # Fix usually_true section
        if "usually_true:" in features_content:
            features_content = re.sub(r'(usually_true:)\s*\n\s*-', r'\1\n\n    - ', features_content)
            features_content = re.sub(r'(\n\s+- feature_id:.*?)(\n\s+- feature_id:)', r'\1\n\n\2', features_content, flags=re.DOTALL)
        
        # Fix sometimes_true section
        if "sometimes_true:" in features_content:
            features_content = re.sub(r'(sometimes_true:)\s*\n\s*-', r'\1\n\n    - ', features_content)
            features_content = re.sub(r'(\n\s+- feature_id:.*?)(\n\s+- feature_id:)', r'\1\n\n\2', features_content, flags=re.DOTALL)
        
        # Fix never_true section
        if "never_true:" in features_content:
            features_content = re.sub(r'(never_true:)\s*\n\s*-', r'\1\n\n    - ', features_content)
            features_content = re.sub(r'(\n\s+- feature_id:.*?)(\n\s+- feature_id:)', r'\1\n\n\2', features_content, flags=re.DOTALL)

        # Insert the features section after Core features section
        core_features_pos = new_content.find("  # Core features")
        if core_features_pos >= 0:
            core_features_end = new_content.find("\n\n", core_features_pos)
            if core_features_end >= 0:
                new_content = new_content[:core_features_end+2] + "  features:\n" + features_content + new_content[core_features_end+2:]
    
    return new_content.strip()

def reformat_all_tree_files():
    """Reformat all tree files in the trees directory."""
    trees_dir = os.path.join(os.getcwd(), "trees")
    
    if not os.path.exists(trees_dir):
        print(f"Directory {trees_dir} not found")
        return
    
    # Get a list of all .yml files in the trees directory
    tree_files = [f for f in os.listdir(trees_dir) if f.endswith('.yml')]
    
    print(f"Found {len(tree_files)} tree files to reformat")
    
    # Get the reference file content
    reference_file = os.path.join(trees_dir, "asparagaceae.joshua-tree.yml")
    if not os.path.exists(reference_file):
        print(f"Reference file {reference_file} not found")
        return
    
    # Skip the reference file
    if "asparagaceae.joshua-tree.yml" in tree_files:
        tree_files.remove("asparagaceae.joshua-tree.yml")
    
    for filename in tree_files:
        filepath = os.path.join(trees_dir, filename)
        
        # Read the file content
        with open(filepath, 'r') as file:
            content = file.read()
        
        # Apply the reformatting
        new_content = reformat_tree_file(content)
        
        # Write the reformatted content back
        with open(filepath, 'w') as file:
            file.write(new_content)
    
    print(f"Reformatted {len(tree_files)} tree files")

if __name__ == "__main__":
    reformat_all_tree_files()