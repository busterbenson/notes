#!/usr/bin/env python3
"""
8-Bit Oracle - Ensure Left-to-Right Decimal Values

This script ensures that all compiled card files have a consistent
left-to-right decimal value field in both formats:
1. decimal_lr_value at the top level
2. lr_decimal_value within binary information

Usage:
    python ensure_decimal_lr.py
"""

import os
import yaml
import glob
import re

# Configuration
COMPILED_DIR = 'compiled'
BINARY_SORT_PATH = '../sorts/binary_sort.md'

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
            }
        
        return binary_data
    
    except Exception as e:
        print(f"Error extracting binary sort data: {e}")
        return {}

def calculate_lr_decimal(binary):
    """Calculate the left-to-right decimal value of a binary string."""
    values = [1, 2, 4, 8, 16, 32, 64, 128]  # Power of 2 values for each bit position
    decimal = 0
    
    for i, bit in enumerate(binary):
        if bit == "1":
            decimal += values[i]
    
    return decimal

def ensure_decimal_lr_value(file_path, binary_data):
    """Ensure the card file has correct decimal_lr_value and lr_decimal_value fields."""
    # Extract binary code from filename
    binary_code = os.path.basename(file_path).replace('.yml', '')
    
    # Calculate L->R decimal value
    lr_decimal = calculate_lr_decimal(binary_code)
    
    # Get value from binary_sort.md if available
    reference_value = None
    if binary_code in binary_data:
        reference_value = binary_data[binary_code]['decimal_lr']
    
    # Verify calculated value matches reference value
    if reference_value and str(lr_decimal) != reference_value:
        print(f"Warning: Calculated L->R decimal {lr_decimal} for {binary_code} doesn't match reference value {reference_value}")
    
    try:
        # Load YAML
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Use yaml to preserve formatting and comment
        data = yaml.safe_load(content)
        
        # Add decimal_lr_value if not present
        if 'decimal_lr_value' not in data:
            data['decimal_lr_value'] = str(lr_decimal)
        
        # Add or update lr_decimal_value
        if 'lr_decimal_value' in data and data['lr_decimal_value'] != lr_decimal:
            data['lr_decimal_value'] = lr_decimal
        
        # Ensure the values are consistent
        if 'decimal_lr_value' in data and 'lr_decimal_value' in data:
            if str(data['lr_decimal_value']) != data['decimal_lr_value']:
                data['lr_decimal_value'] = lr_decimal
                data['decimal_lr_value'] = str(lr_decimal)
        
        # Save the updated YAML
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False, sort_keys=False)
        
        return True
        
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def process_all_cards():
    """Process all cards in the compiled directory."""
    # Extract reference data
    binary_data = extract_binary_sort_data()
    
    # Get all card files
    all_files = glob.glob(f"{COMPILED_DIR}/*/*.yml")
    total_files = len(all_files)
    
    print(f"Found {total_files} card files to update")
    
    # Process each file
    success_count = 0
    for i, file_path in enumerate(all_files, 1):
        binary_code = os.path.basename(file_path).replace('.yml', '')
        print(f"[{i}/{total_files}] Updating {binary_code}...", end='')
        
        if ensure_decimal_lr_value(file_path, binary_data):
            success_count += 1
            print(" ✓")
        else:
            print(" ✗")
    
    print(f"\nUpdated {success_count}/{total_files} card files successfully")

if __name__ == "__main__":
    process_all_cards()