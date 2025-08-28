#!/usr/bin/env python3
import os
import re
import sys

# Paths
GENUS_DIR = "../genus"
TREES_DIR = "."

# Function to extract scientific genus from scientific name
def extract_scientific_genus(scientific_name):
    # Extract the first word which should be the genus
    match = re.match(r'^(\w+)', scientific_name)
    if match:
        return match.group(1)
    return None

# Step 1: Extract genus information
def extract_genus_info():
    genus_info = {}
    genus_files = [f for f in os.listdir(GENUS_DIR) if f.endswith('.yml')]
    
    for genus_file in genus_files:
        file_path = os.path.join(GENUS_DIR, genus_file)
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            
            # Extract genus common name
            common_name_match = re.search(r'common_name:\s*"([^"]+)"', content)
            if not common_name_match:
                common_name_match = re.search(r"common_name:\s*'([^']+)'", content)
            
            # Extract genus scientific name
            scientific_name_match = re.search(r'scientific_name:\s*"([^"]+)"', content)
            if not scientific_name_match:
                scientific_name_match = re.search(r"scientific_name:\s*'([^']+)'", content)
            
            if common_name_match and scientific_name_match:
                common_name = common_name_match.group(1)
                scientific_name = scientific_name_match.group(1)
                
                # Extract scientific genus from genus scientific name
                scientific_genus = extract_scientific_genus(scientific_name)
                
                # Store mapping from scientific genus to common genus
                if scientific_genus:
                    genus_info[scientific_genus] = {'common_name': common_name}
                
                # Extract included species
                species_blocks = re.findall(r'- name:\s*"([^"]+)"\s+scientific_name:\s*"([^"]+)"', content)
                if not species_blocks:
                    species_blocks = re.findall(r"- name:\s*'([^']+)'\s+scientific_name:\s*'([^']+)'", content)
                
                for species_name, species_sci_name in species_blocks:
                    # Extract scientific genus for this species
                    species_scientific_genus = extract_scientific_genus(species_sci_name)
                    
                    # If extraction succeeded, store the mapping
                    if species_scientific_genus:
                        if species_scientific_genus not in genus_info:
                            genus_info[species_scientific_genus] = {'common_name': common_name}
                        
                        # Store an explicit mapping for this specific species
                        if 'species_mapping' not in genus_info[species_scientific_genus]:
                            genus_info[species_scientific_genus]['species_mapping'] = {}
                        
                        genus_info[species_scientific_genus]['species_mapping'][species_sci_name] = {
                            'common_name': species_name,
                            'genus_common_name': common_name
                        }
        except Exception as e:
            print(f"Error processing {genus_file}: {str(e)}")
    
    return genus_info

# Step 2: Update tree files with genus information
def update_tree_files(genus_info):
    updated_count = 0
    error_count = 0
    tree_files = [f for f in os.listdir(TREES_DIR) if f.endswith('.yml') and not f.startswith('update_genus')]
    
    for tree_file in tree_files:
        file_path = os.path.join(TREES_DIR, tree_file)
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            
            # Check if already has genus information
            if re.search(r'scientific_genus:', content):
                print(f"Skipping {tree_file}: already has genus information")
                continue
            
            # Extract scientific name
            scientific_name_match = re.search(r'scientific_name:\s*"([^"]+)"', content)
            if not scientific_name_match:
                scientific_name_match = re.search(r"scientific_name:\s*'([^']+)'", content)
            
            if not scientific_name_match:
                print(f"Error in {tree_file}: could not find scientific_name")
                error_count += 1
                continue
            
            scientific_name = scientific_name_match.group(1)
            
            # Extract scientific genus
            scientific_genus = extract_scientific_genus(scientific_name)
            
            # Skip if we can't extract the scientific genus
            if not scientific_genus:
                print(f"Error in {tree_file}: could not extract scientific genus from '{scientific_name}'")
                error_count += 1
                continue
            
            # Skip if we don't have info for this genus
            if scientific_genus not in genus_info:
                print(f"Error in {tree_file}: no genus info found for '{scientific_genus}'")
                error_count += 1
                continue
            
            # Get common genus name
            common_genus = genus_info[scientific_genus]['common_name']
            
            # Get more precise common genus name if available
            if ('species_mapping' in genus_info[scientific_genus] and 
                scientific_name in genus_info[scientific_genus]['species_mapping']):
                common_genus = genus_info[scientific_genus]['species_mapping'][scientific_name]['genus_common_name']
            
            # Find position to insert genus information (after family)
            family_match = re.search(r'(family:.*?\n)', content)
            if not family_match:
                print(f"Error in {tree_file}: could not find family field")
                error_count += 1
                continue
            
            # Find the indentation for tree fields
            tree_fields_pattern = re.search(r'(\s+)common_name:', content)
            if not tree_fields_pattern:
                print(f"Error in {tree_file}: could not determine indentation")
                error_count += 1
                continue
                
            indent = tree_fields_pattern.group(1)
            
            # Determine if we need to use single or double quotes
            quote_style = '"' if scientific_name_match.group(0).find('"') != -1 else "'"
            
            # Insert genus information after family line
            new_content = content.replace(
                family_match.group(0),
                family_match.group(0) +
                f"{indent}scientific_genus: {quote_style}{scientific_genus}{quote_style}\n" +
                f"{indent}common_genus: {quote_style}{common_genus}{quote_style}\n"
            )
            
            # Save the updated content
            with open(file_path, 'w') as file:
                file.write(new_content)
            
            print(f"Updated {tree_file}: {scientific_genus} ({common_genus})")
            updated_count += 1
            
        except Exception as e:
            print(f"Error processing {tree_file}: {str(e)}")
            error_count += 1
    
    return updated_count, error_count

# Main function
def main():
    print("Extracting genus information...")
    genus_info = extract_genus_info()
    print(f"Found information for {len(genus_info)} genera")
    
    print("\nUpdating tree files...")
    updated_count, error_count = update_tree_files(genus_info)
    
    print("\nSummary:")
    print(f"Updated {updated_count} tree files")
    print(f"Encountered {error_count} errors")

if __name__ == "__main__":
    main()