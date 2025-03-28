#!/usr/bin/env python3

import os
import re
import sys

def extract_features(content):
    """Extract the features data from the content."""
    features_match = re.search(r'features:.*?(?=\n\s*# Kid-friendly identification|\Z)', content, re.DOTALL)
    if not features_match:
        return None
    
    features_content = features_match.group(0)
    
    # Extract feature categories
    categories = ["always_true", "usually_true", "sometimes_true", "never_true"]
    extracted_data = {}
    
    for category in categories:
        category_match = re.search(r'' + category + r':.*?(?=\n\s*(?:always_true|usually_true|sometimes_true|never_true):|$)', features_content, re.DOTALL)
        if category_match:
            category_content = category_match.group(0)
            # Extract feature items
            feature_items = []
            feature_matches = re.finditer(r'\n\s*- (?:feature_id|"feature_id"):(.*?)(?=\n\s*- (?:feature_id|"feature_id"):|$)', category_content, re.DOTALL)
            for match in feature_matches:
                feature_item = match.group(1).strip()
                feature_items.append(feature_item)
            extracted_data[category] = feature_items
    
    return extracted_data

def format_features(features_data):
    """Format the features data into a properly structured string."""
    result = "  features:\n\n"
    
    categories = ["always_true", "usually_true", "sometimes_true", "never_true"]
    for category in categories:
        if category in features_data and features_data[category]:
            result += f"    {category}:\n\n"
            for item in features_data[category]:
                # Extract feature_id and any other attributes
                feature_id_match = re.search(r'("[^"]+"|\S+)', item)
                feature_id = feature_id_match.group(1) if feature_id_match else ""
                
                # Format the feature item with proper indentation and spacing
                result += f"      - feature_id: {feature_id}\n"
                
                # Add notes, conditions, exceptions
                notes_match = re.search(r'notes:(?:\s*)("[^"]+"|\S+[^\n]*)', item)
                if notes_match:
                    notes = notes_match.group(1)
                    result += f"        notes: {notes}\n"
                
                conditions_match = re.search(r'conditions:(?:\s*)("[^"]+"|\S+[^\n]*)', item)
                if conditions_match:
                    conditions = conditions_match.group(1)
                    result += f"        conditions: {conditions}\n"
                
                exceptions_match = re.search(r'exceptions:(?:\s*)("[^"]+"|\S+[^\n]*)', item)
                if exceptions_match:
                    exceptions = exceptions_match.group(1)
                    result += f"        exceptions: {exceptions}\n"
                
                result += "\n"
            
            result += "\n"
    
    return result

def fix_features_in_file(content):
    """Extract and reformat the features section in the content."""
    features_data = extract_features(content)
    if not features_data:
        return content
    
    # Format the features data
    formatted_features = format_features(features_data)
    
    # Replace the old features section with the new one
    pattern = r'features:.*?(?=\n\s*# Kid-friendly identification|\Z)'
    return re.sub(pattern, formatted_features.strip(), content, flags=re.DOTALL)

def fix_all_tree_files():
    """Fix the features section in all tree files."""
    trees_dir = os.path.join(os.getcwd(), "trees")
    
    if not os.path.exists(trees_dir):
        print(f"Directory {trees_dir} not found")
        return
    
    # Get a list of all .yml files in the trees directory
    tree_files = [f for f in os.listdir(trees_dir) if f.endswith('.yml')]
    
    # Skip the reference file
    if "asparagaceae.joshua-tree.yml" in tree_files:
        tree_files.remove("asparagaceae.joshua-tree.yml")
    
    print(f"Found {len(tree_files)} tree files to process")
    
    for filename in tree_files:
        filepath = os.path.join(trees_dir, filename)
        
        # Read the file content
        with open(filepath, 'r') as file:
            content = file.read()
        
        # Apply the fix
        new_content = fix_features_in_file(content)
        
        # Write the updated content back
        with open(filepath, 'w') as file:
            file.write(new_content)
    
    print(f"Fixed features section in {len(tree_files)} tree files")

if __name__ == "__main__":
    fix_all_tree_files()