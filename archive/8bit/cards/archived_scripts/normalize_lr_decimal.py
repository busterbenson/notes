#!/usr/bin/env python3
"""
8-Bit Oracle - Normalize Left-to-Right Decimal Values

This script normalizes the format of left-to-right decimal values across all cards.
It ensures that:
1. All cards have lr_decimal_value field at the top level
2. Adds binary_code field if missing
3. Makes the field ordering consistent

Usage:
    python normalize_lr_decimal.py
"""

import os
import yaml
import glob

# Configuration
COMPILED_DIR = 'compiled'

def calculate_lr_decimal(binary):
    """Calculate the left-to-right decimal value of a binary string."""
    values = [1, 2, 4, 8, 16, 32, 64, 128]  # Power of 2 values for each bit position
    decimal = 0
    
    for i, bit in enumerate(binary):
        if bit == "1":
            decimal += values[i]
    
    return decimal

def normalize_card(file_path):
    """Normalize the card's YAML file format for left-to-right decimal values."""
    # Extract binary code from filename
    binary_code = os.path.basename(file_path).replace('.yml', '')
    
    # Calculate L->R decimal value
    lr_decimal = calculate_lr_decimal(binary_code)
    
    try:
        # Load the current card data
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        
        # Create normalized data structure
        normalized = {}
        
        # Ensure binary_code field exists
        if 'binary_code' not in data:
            normalized['binary_code'] = binary_code
        else:
            normalized['binary_code'] = data['binary_code']
        
        # Ensure decimal_value field exists (standard right-to-left)
        if 'decimal_value' not in data:
            normalized['decimal_value'] = int(binary_code, 2)
        else:
            normalized['decimal_value'] = data['decimal_value']
        
        # Ensure lr_decimal_value field exists
        normalized['lr_decimal_value'] = lr_decimal
        
        # Copy hexadecimal_value if it exists
        if 'hexadecimal_value' in data:
            normalized['hexadecimal_value'] = data['hexadecimal_value']
        
        # Copy the rest of the fields
        for key, value in data.items():
            if key not in ['binary_code', 'decimal_value', 'lr_decimal_value', 'hexadecimal_value', 'decimal_lr_value']:
                normalized[key] = value
        
        # Save the normalized data
        with open(file_path, 'w') as file:
            yaml.dump(normalized, file, default_flow_style=False, sort_keys=False)
        
        return True
        
    except Exception as e:
        print(f"Error normalizing {file_path}: {e}")
        return False

def process_all_cards():
    """Process all cards in the compiled directory."""
    # Get all card files
    all_files = glob.glob(f"{COMPILED_DIR}/*/*.yml")
    total_files = len(all_files)
    
    print(f"Found {total_files} card files to normalize")
    
    # Process each file
    success_count = 0
    for i, file_path in enumerate(all_files, 1):
        binary_code = os.path.basename(file_path).replace('.yml', '')
        print(f"[{i}/{total_files}] Normalizing {binary_code}...", end='')
        
        if normalize_card(file_path):
            success_count += 1
            print(" ✓")
        else:
            print(" ✗")
    
    print(f"\nNormalized {success_count}/{total_files} card files successfully")

if __name__ == "__main__":
    process_all_cards()