#!/usr/bin/env python3

import os
import re

# Directory paths
TREES_DIR = "trees"

def extract_genus_from_scientific_name(scientific_name):
    """Extract the genus from a scientific name."""
    # Remove any quotes
    scientific_name = scientific_name.strip('"\'')
    
    # Split by space and take the first part
    parts = scientific_name.split()
    if parts:
        return parts[0]
    return None

def add_missing_genus():
    """Add genus information to tree files that are missing it."""
    updated_count = 0
    error_count = 0
    
    # Get all tree files that have already been processed
    processed_genus_info = {}
    
    # First, collect genus information from processed files
    tree_files = [f for f in os.listdir(TREES_DIR) if f.endswith('.yml')]
    for filename in tree_files:
        file_path = os.path.join(TREES_DIR, filename)
        
        try:
            # Read the file content
            with open(file_path, 'r') as file:
                content = file.read()
            
            # Check if genus information is present
            scientific_genus_match = re.search(r'scientific_genus:\s*(.*?)$', content, re.MULTILINE)
            common_genus_match = re.search(r'common_genus:\s*(.*?)$', content, re.MULTILINE)
            scientific_name_match = re.search(r'scientific_name:\s*(.*?)$', content, re.MULTILINE)
            
            if scientific_genus_match and common_genus_match and scientific_name_match:
                scientific_genus = scientific_genus_match.group(1).strip('"\'').strip()
                common_genus = common_genus_match.group(1).strip('"\'').strip()
                scientific_name = scientific_name_match.group(1).strip('"\'').strip()
                
                # Extract genus part of scientific name
                extracted_genus = extract_genus_from_scientific_name(scientific_name)
                
                if extracted_genus and scientific_genus:
                    # Store mapping of scientific genus to common genus
                    processed_genus_info[extracted_genus] = {
                        'scientific_genus': scientific_genus,
                        'common_genus': common_genus
                    }
        except Exception as e:
            print(f"Error reading {filename}: {str(e)}")
    
    # Now process files with missing genus information
    for filename in tree_files:
        file_path = os.path.join(TREES_DIR, filename)
        
        try:
            # Read the file content
            with open(file_path, 'r') as file:
                content = file.read()
            
            # Skip if genus information is already present
            if re.search(r'scientific_genus:', content) and re.search(r'common_genus:', content):
                continue
            
            # Extract scientific name
            scientific_name_match = re.search(r'scientific_name:\s*(.*?)$', content, re.MULTILINE)
            if not scientific_name_match:
                print(f"Skipping {filename}: Could not find scientific_name")
                continue
            
            scientific_name = scientific_name_match.group(1).strip('"\'').strip()
            extracted_genus = extract_genus_from_scientific_name(scientific_name)
            
            if not extracted_genus:
                print(f"Skipping {filename}: Could not extract genus from {scientific_name}")
                continue
            
            # Look up genus information from processed files
            if extracted_genus in processed_genus_info:
                scientific_genus = processed_genus_info[extracted_genus]['scientific_genus']
                common_genus = processed_genus_info[extracted_genus]['common_genus']
            else:
                # Use the extracted genus as scientific_genus and "Unknown" as common_genus
                scientific_genus = extracted_genus
                common_genus = "Unknown"
                print(f"Warning: Using default genus information for {filename}: {scientific_genus}")
            
            # Add genus information after scientific_name and before family
            updated_content = re.sub(
                r'(scientific_name:\s*.*?\n)(\s+family:)',
                f'\\1  scientific_genus: {scientific_genus}\n  common_genus: {common_genus}\\2',
                content,
                flags=re.DOTALL
            )
            
            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.write(updated_content)
                
            print(f"Added genus information to {filename}")
            updated_count += 1
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            error_count += 1
    
    return updated_count, error_count

if __name__ == "__main__":
    updated, errors = add_missing_genus()
    print(f"\nSummary: Added genus information to {updated} files with {errors} errors")