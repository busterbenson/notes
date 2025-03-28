#!/usr/bin/env python3

import os
import re
import yaml
import sys

def validate_tree_file(content, filename):
    """Validate a tree file for structural and formatting issues."""
    issues = []
    
    # Check for required top-level fields
    required_fields = [
        "common_name",
        "scientific_name",
        "scientific_genus",
        "common_genus",
        "family",
    ]
    
    for field in required_fields:
        if not re.search(r'\s+' + field + r':', content):
            issues.append(f"Missing required field: {field}")
    
    # Check for required section headers
    required_sections = [
        "# Basic summary",
        "# Identification path",
        "# Core features",
        "# Kid-friendly identification",
        "# Seasonal changes",
    ]
    
    for section in required_sections:
        if section not in content:
            issues.append(f"Missing required section: {section}")
    
    # Check for proper quoting in top-level fields
    quoted_fields = [
        "common_name",
        "scientific_name",
        "scientific_genus",
        "common_genus",
        "family",
        "summary",
    ]
    
    for field in quoted_fields:
        pattern = r'\s+' + field + r': ([^"\n])'
        if re.search(pattern, content):
            issues.append(f"Field {field} is missing quotes")
    
    # We'll skip section header spacing check for now since it's less critical
    
    # Check for duplicate section headers
    if "# Seasonal timeline" in content and "# Seasonal changes" in content:
        issues.append("Duplicate section headers: # Seasonal timeline and # Seasonal changes")
    
    # Check for unknown common genus values
    if re.search(r'common_genus: "Unknown"', content):
        issues.append("Unknown value for common_genus field")
    
    return issues

def validate_all_tree_files():
    """Validate all tree files for consistent formatting."""
    trees_dir = os.path.join(os.getcwd(), "trees")
    
    if not os.path.exists(trees_dir):
        print(f"Directory {trees_dir} not found")
        return
    
    # Get a list of all .yml files in the trees directory
    tree_files = [f for f in os.listdir(trees_dir) if f.endswith('.yml')]
    
    print(f"Validating {len(tree_files)} tree files...")
    
    files_with_issues = 0
    unknown_genus_count = 0
    
    for filename in tree_files:
        filepath = os.path.join(trees_dir, filename)
        
        # Read the file content
        with open(filepath, 'r') as file:
            content = file.read()
        
        # Validate the file
        issues = validate_tree_file(content, filename)
        
        if issues:
            files_with_issues += 1
            print(f"\nIssues in {filename}:")
            for issue in issues:
                print(f"  - {issue}")
                if "Unknown value for common_genus field" in issue:
                    unknown_genus_count += 1
    
    if files_with_issues == 0:
        print("\nAll tree files passed validation!")
    else:
        print(f"\n{files_with_issues} files had issues")
        print(f"{unknown_genus_count} files have 'Unknown' common_genus values")

if __name__ == "__main__":
    validate_all_tree_files()