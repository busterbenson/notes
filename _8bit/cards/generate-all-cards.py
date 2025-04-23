#!/usr/bin/env python3
"""
Generate all 256 possible 8-bit Oracle cards.

This script generates every possible 8-bit binary combination (00000000 through 11111111)
and creates a card YAML file for each one using the generate-card.py script.

Usage:
    python generate-all-cards.py
"""

import os
import sys
import subprocess
import itertools

def generate_binary_strings():
    """Generate all possible 8-bit binary strings."""
    return [''.join(bits) for bits in itertools.product('01', repeat=8)]

def generate_cards(binary_strings):
    """Generate card YAML files for all binary strings."""
    # Create the output directory if it doesn't exist
    os.makedirs('generated', exist_ok=True)
    
    total = len(binary_strings)
    # Process each binary string
    for i, binary in enumerate(binary_strings):
        try:
            # Progress update every 16 cards
            if i % 16 == 0:
                print(f"Generating cards: {i}/{total} ({i/total:.1%})")
            
            # Run the generate-card.py script for this binary
            subprocess.run(['python', 'generate-card.py', binary], check=True, stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(f"Error generating card for {binary}: {e}")
            continue

def main():
    """Main function."""
    print("Generating all 256 possible 8-bit Oracle cards...")
    
    # Generate all binary strings
    binary_strings = generate_binary_strings()
    print(f"Found {len(binary_strings)} possible binary combinations.")
    
    # Generate cards for all binary strings
    generate_cards(binary_strings)
    
    print("\nCard generation complete!")
    print(f"All card YAML files have been saved to the 'generated/' directory.")

if __name__ == "__main__":
    main()