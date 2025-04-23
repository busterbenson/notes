#!/usr/bin/env python3
"""
8-Bit Oracle Enhanced Card Description Generator

This script enhances the compiled card descriptions by adding additional information from:
- sorts/binary_sort.md
- associations/quick-reference-guide.md
- associations/archetype-guide.md

It updates the existing compiled YAML files with more comprehensive information.

Usage:
    python enhance_compiled_cards.py [options]
    
Options:
    --all             Process all cards (default)
    --card BINARY     Process a specific card by its 8-bit binary code (e.g., 00000000)
    --hexagram HEX    Process all cards for a specific hexagram (e.g., 000000)
"""

import os
import sys
import yaml
import glob
import re
import argparse

# Configuration
COMPILED_DIR = 'compiled'
BINARY_SORT_PATH = '../sorts/binary_sort.md'
QUICK_REFERENCE_PATH = '../associations/quick-reference-guide.md'
ARCHETYPE_GUIDE_PATH = '../associations/archetype-guide.md'

def load_yaml_file(file_path):
    """Load a YAML file and return its contents."""
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def save_yaml_file(file_path, data):
    """Save data to a YAML file."""
    try:
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False

def extract_binary_sort_data():
    """Extract card data from binary_sort.md."""
    try:
        with open(BINARY_SORT_PATH, 'r') as file:
            content = file.read()
        
        # Extract the table content
        table_pattern = r'\| Binary\s+\| Decimal.*?\n(.*?)(?:\n\n|\n#|$)'
        table_match = re.search(table_pattern, content, re.DOTALL)
        
        if not table_match:
            print("Error: Could not find binary sort table in binary_sort.md")
            return {}
        
        table_content = table_match.group(1).strip()
        
        # Parse each row
        binary_data = {}
        for line in table_content.split('\n'):
            if '|' not in line or line.strip().startswith('|-'):
                continue
            
            parts = [part.strip() for part in line.split('|')]
            if len(parts) < 7:  # Need at least binary, decimal, season, cycle, phase, half
                continue
            
            binary = parts[1].strip()
            if not binary or not all(bit in '01' for bit in binary):
                continue
            
            binary_data[binary] = {
                'decimal_lr': parts[2].strip(),
                'season': parts[3].strip(),
                'lunar_cycle': parts[4].strip(),
                'lunar_phase': parts[5].strip(),
                'phase_half': parts[6].strip()
            }
        
        return binary_data
    
    except Exception as e:
        print(f"Error extracting binary sort data: {e}")
        return {}

def extract_quick_reference_data():
    """Extract card data from quick-reference-guide.md."""
    reference_data = {
        'inner_world': {},
        'outer_world': {},
        'bit_definitions': {},
        'season_bits': {}
    }
    
    try:
        with open(QUICK_REFERENCE_PATH, 'r') as file:
            content = file.read()
        
        # Extract inner world data
        inner_pattern = r'### Inner World.*?\n\| Pattern.*?\n(.*?)(?:\n\n|\n###|$)'
        inner_match = re.search(inner_pattern, content, re.DOTALL)
        
        if inner_match:
            inner_content = inner_match.group(1).strip()
            for line in inner_content.split('\n'):
                if '|' not in line or line.strip().startswith('|-'):
                    continue
                
                parts = [part.strip() for part in line.split('|')]
                if len(parts) < 6:
                    continue
                
                pattern = parts[1].strip()
                reference_data['inner_world'][pattern] = {
                    'color': parts[2].strip(),
                    'trigram': parts[3].strip(),
                    'name': parts[4].strip(),
                    'description': parts[5].strip()
                }
        
        # Extract outer world data
        outer_pattern = r'### Outer World.*?\n\| Pattern.*?\n(.*?)(?:\n\n|\n###|$)'
        outer_match = re.search(outer_pattern, content, re.DOTALL)
        
        if outer_match:
            outer_content = outer_match.group(1).strip()
            for line in outer_content.split('\n'):
                if '|' not in line or line.strip().startswith('|-'):
                    continue
                
                parts = [part.strip() for part in line.split('|')]
                if len(parts) < 6:
                    continue
                
                pattern = parts[1].strip()
                reference_data['outer_world'][pattern] = {
                    'color': parts[2].strip(),
                    'trigram': parts[3].strip(),
                    'name': parts[4].strip(),
                    'description': parts[5].strip()
                }
        
        # Extract bit definitions
        bit_pattern = r'## Essential Bit Meanings.*?\n\| Bit.*?\n(.*?)(?:\n\n|\n##|$)'
        bit_match = re.search(bit_pattern, content, re.DOTALL)
        
        if bit_match:
            bit_content = bit_match.group(1).strip()
            for line in bit_content.split('\n'):
                if '|' not in line or line.strip().startswith('|-'):
                    continue
                
                parts = [part.strip() for part in line.split('|')]
                if len(parts) < 6:
                    continue
                
                bit = parts[1].strip()
                reference_data['bit_definitions'][bit] = {
                    'position': parts[2].strip(),
                    'resource': parts[3].strip(),
                    'question': parts[4].strip(),
                    'domain': parts[5].strip()
                }
        
        # Extract season bits
        season_pattern = r'## Season \(Bits 7-8\).*?\n\| Bits.*?\n(.*?)(?:\n\n|\n##|$)'
        season_match = re.search(season_pattern, content, re.DOTALL)
        
        if season_match:
            season_content = season_match.group(1).strip()
            for line in season_content.split('\n'):
                if '|' not in line or line.strip().startswith('|-'):
                    continue
                
                parts = [part.strip() for part in line.split('|')]
                if len(parts) < 3:
                    continue
                
                bits = parts[1].strip()
                reference_data['season_bits'][bits] = parts[2].strip()
        
        return reference_data
    
    except Exception as e:
        print(f"Error extracting quick reference data: {e}")
        return {
            'inner_world': {},
            'outer_world': {},
            'bit_definitions': {},
            'season_bits': {}
        }

def extract_archetype_guide_data():
    """Extract card data from archetype-guide.md."""
    try:
        with open(ARCHETYPE_GUIDE_PATH, 'r') as file:
            content = file.read()
        
        # Extract the lookup table
        table_pattern = r'## Lookup\n\| Binary.*?\n\|(.*?)(?:\n\n|\n#|$)'
        table_match = re.search(table_pattern, content, re.DOTALL)
        
        if not table_match:
            print("Error: Could not find lookup table in archetype-guide.md")
            return {}
        
        table_content = table_match.group(1).strip()
        
        # Extract archetype descriptions
        archetype_descriptions = {}
        for archetype in ["Fool", "Hero", "Monster", "Sage"]:
            desc_pattern = f"### {archetype}\n(.*?)(?:\n\n###|\n##|$)"
            desc_match = re.search(desc_pattern, content, re.DOTALL)
            if desc_match:
                archetype_descriptions[archetype] = desc_match.group(1).strip()
        
        # Parse each row in the lookup table
        archetype_data = {}
        for line in table_content.split('\n'):
            if '|' not in line:
                continue
            
            parts = [part.strip() for part in line.split('|')]
            if len(parts) < 6:  # Need binary, decimal, season, resonant season, archetype
                continue
            
            binary = parts[1].strip()
            if not binary or not all(bit in '01' for bit in binary):
                continue
            
            archetype_data[binary] = {
                'decimal': parts[2].strip(),
                'season': parts[3].strip(),
                'resonant_season': parts[4].strip(),
                'archetype': parts[5].strip(),
                'archetype_description': archetype_descriptions.get(parts[5].strip(), "")
            }
        
        return archetype_data
    
    except Exception as e:
        print(f"Error extracting archetype guide data: {e}")
        return {}

def enhance_card(card_path, binary_data, reference_data, archetype_data):
    """Enhance a card's YAML file with additional information."""
    # Extract binary code from filename
    binary_code = os.path.basename(card_path).replace('.yml', '')
    
    # Load the current card data
    card_data = load_yaml_file(card_path)
    if not card_data:
        return False
    
    # Add information from binary sort
    if binary_code in binary_data:
        sort_info = binary_data[binary_code]
        
        # Add to lunar_cycle section if it exists
        if 'lunar_cycle' in card_data:
            card_data['lunar_cycle']['cycle_number'] = sort_info['lunar_cycle']
            card_data['lunar_cycle']['lunar_phase_detailed'] = sort_info['lunar_phase']
            card_data['lunar_cycle']['phase_half'] = sort_info['phase_half']
        else:
            card_data['lunar_cycle'] = {
                'cycle_number': sort_info['lunar_cycle'],
                'lunar_phase_detailed': sort_info['lunar_phase'],
                'phase_half': sort_info['phase_half'],
                'season': sort_info['season']
            }
        
        # Add decimal_lr value
        card_data['decimal_lr_value'] = sort_info['decimal_lr']
    
    # Add information from quick reference guide
    inner_bits = binary_code[0:3]
    outer_bits = binary_code[3:6]
    
    # Add enhanced inner world descriptions
    if inner_bits in reference_data['inner_world']:
        inner_info = reference_data['inner_world'][inner_bits]
        
        if 'inner_world' in card_data:
            card_data['inner_world']['detailed_name'] = inner_info['name']
            card_data['inner_world']['detailed_description'] = inner_info['description']
            if 'color' not in card_data['inner_world'] and 'color' in inner_info:
                card_data['inner_world']['color'] = inner_info['color']
        else:
            card_data['inner_world'] = {
                'bits': inner_bits,
                'detailed_name': inner_info['name'],
                'detailed_description': inner_info['description'],
                'color': inner_info['color']
            }
    
    # Add enhanced outer world descriptions
    if outer_bits in reference_data['outer_world']:
        outer_info = reference_data['outer_world'][outer_bits]
        
        if 'outer_world' in card_data:
            card_data['outer_world']['detailed_name'] = outer_info['name']
            card_data['outer_world']['detailed_description'] = outer_info['description']
            if 'color' not in card_data['outer_world'] and 'color' in outer_info:
                card_data['outer_world']['color'] = outer_info['color']
        else:
            card_data['outer_world'] = {
                'bits': outer_bits,
                'detailed_name': outer_info['name'],
                'detailed_description': outer_info['description'],
                'color': outer_info['color']
            }
    
    # Add enhanced bit definitions
    if 'bit_associations' not in card_data:
        card_data['bit_associations'] = {}
    
    for bit_num in range(1, 9):
        bit_key = str(bit_num)
        if bit_key in reference_data['bit_definitions']:
            bit_info = reference_data['bit_definitions'][bit_key]
            
            if f'bit{bit_num}' not in card_data['bit_associations']:
                card_data['bit_associations'][f'bit{bit_num}'] = {}
            
            bit_obj = card_data['bit_associations'][f'bit{bit_num}']
            bit_obj['resource'] = bit_info['resource']
            bit_obj['question'] = bit_info['question']
            bit_obj['domain'] = bit_info['domain']
            bit_obj['value'] = binary_code[bit_num-1]
    
    # Add archetype guide information
    if binary_code in archetype_data:
        arch_info = archetype_data[binary_code]
        
        if 'archetype' in card_data:
            card_data['archetype']['detailed_description'] = arch_info['archetype_description']
        else:
            card_data['archetype'] = {
                'name': arch_info['archetype'],
                'resonant_season': arch_info['resonant_season'],
                'detailed_description': arch_info['archetype_description']
            }
    
    # Save the enhanced card data
    return save_yaml_file(card_path, card_data)

def process_all_cards():
    """Process all cards in the compiled directory."""
    # Extract data from reference files
    binary_data = extract_binary_sort_data()
    reference_data = extract_quick_reference_data()
    archetype_data = extract_archetype_guide_data()
    
    # Get all card files
    all_files = glob.glob(f"{COMPILED_DIR}/*/*.yml")
    total_files = len(all_files)
    
    print(f"Found {total_files} card files to enhance")
    
    # Process each file
    success_count = 0
    for i, file_path in enumerate(all_files, 1):
        binary_code = os.path.basename(file_path).replace('.yml', '')
        print(f"[{i}/{total_files}] Enhancing {binary_code}...", end='')
        
        if enhance_card(file_path, binary_data, reference_data, archetype_data):
            success_count += 1
            print(" ✓")
        else:
            print(" ✗")
    
    print(f"\nEnhanced {success_count}/{total_files} card files successfully")

def process_specific_card(binary_code):
    """Process a specific card by its binary code."""
    # Extract data from reference files
    binary_data = extract_binary_sort_data()
    reference_data = extract_quick_reference_data()
    archetype_data = extract_archetype_guide_data()
    
    # Validate binary code
    if len(binary_code) != 8 or not all(bit in '01' for bit in binary_code):
        print(f"Error: Invalid binary code '{binary_code}'. Must be 8 bits of 0s and 1s.")
        return False
    
    # Construct the file path
    hexagram = binary_code[0:6]
    file_path = os.path.join(COMPILED_DIR, hexagram, f"{binary_code}.yml")
    
    if not os.path.exists(file_path):
        print(f"Error: Card file for {binary_code} not found at {file_path}")
        return False
    
    print(f"Enhancing card {binary_code}...", end='')
    
    if enhance_card(file_path, binary_data, reference_data, archetype_data):
        print(" ✓")
        return True
    else:
        print(" ✗")
        return False

def process_hexagram(hexagram):
    """Process all cards for a specific hexagram."""
    # Extract data from reference files
    binary_data = extract_binary_sort_data()
    reference_data = extract_quick_reference_data()
    archetype_data = extract_archetype_guide_data()
    
    # Validate hexagram
    if len(hexagram) != 6 or not all(bit in '01' for bit in hexagram):
        print(f"Error: Invalid hexagram '{hexagram}'. Must be 6 bits of 0s and 1s.")
        return False
    
    # Get all card files for this hexagram
    hexagram_dir = os.path.join(COMPILED_DIR, hexagram)
    if not os.path.exists(hexagram_dir):
        print(f"Error: Hexagram directory {hexagram_dir} not found")
        return False
    
    card_files = glob.glob(f"{hexagram_dir}/*.yml")
    total_files = len(card_files)
    
    if total_files == 0:
        print(f"Error: No card files found for hexagram {hexagram}")
        return False
    
    print(f"Found {total_files} card files for hexagram {hexagram}")
    
    # Process each file
    success_count = 0
    for i, file_path in enumerate(card_files, 1):
        binary_code = os.path.basename(file_path).replace('.yml', '')
        print(f"[{i}/{total_files}] Enhancing {binary_code}...", end='')
        
        if enhance_card(file_path, binary_data, reference_data, archetype_data):
            success_count += 1
            print(" ✓")
        else:
            print(" ✗")
    
    print(f"\nEnhanced {success_count}/{total_files} card files for hexagram {hexagram} successfully")
    return success_count > 0

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Enhance 8-Bit Oracle compiled card descriptions.')
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--all', action='store_true', help='Process all cards (default)')
    group.add_argument('--card', metavar='BINARY', help='Process a specific card by its 8-bit binary code')
    group.add_argument('--hexagram', metavar='HEX', help='Process all cards for a specific hexagram')
    
    args = parser.parse_args()
    
    # If no arguments are provided, default to --all
    if not (args.all or args.card or args.hexagram):
        args.all = True
    
    return args

def main():
    """Main function to enhance compiled cards."""
    args = parse_arguments()
    
    print("8-Bit Oracle Enhanced Card Description Generator")
    print("-----------------------------------------------")
    
    if args.all:
        process_all_cards()
    elif args.card:
        process_specific_card(args.card)
    elif args.hexagram:
        process_hexagram(args.hexagram)

if __name__ == "__main__":
    main()