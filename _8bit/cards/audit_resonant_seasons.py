#!/usr/bin/env python3
"""
8-Bit Oracle Resonant Seasons Audit

This script audits and fixes the resonant season assignments in the compiled card files.
It implements the correct resonant season logic:
- Inner state is determined by bits 1-3: inner=1 if 2+ bits are 1, inner=0 if 2+ bits are 0
- Outer state is determined by bits 4-6: outer=1 if 2+ bits are 1, outer=0 if 2+ bits are 0
- Resonant seasons:
  * inner0-outer0 → Winter
  * inner1-outer0 → Spring
  * inner1-outer1 → Summer
  * inner0-outer1 → Fall

The script will print a report of all cards with incorrect resonant seasons
and generate a command to fix them by regenerating the card files.

Usage:
    python audit_resonant_seasons.py
"""

import os
import yaml
import glob
import subprocess
import sys

# Configuration
COMPILED_DIR = 'compiled'

def analyze_bit_pattern(binary):
    """Analyze an 8-bit pattern and determine the correct resonant season."""
    # Extract inner and outer worlds
    inner_bits = binary[0:3]  # First 3 bits
    outer_bits = binary[3:6]  # Next 3 bits
    
    # Count 1s in each world
    inner_ones = inner_bits.count('1')
    outer_ones = outer_bits.count('1')
    
    # Determine inner/outer states
    inner_state = 1 if inner_ones >= 2 else 0
    outer_state = 1 if outer_ones >= 2 else 0
    
    # Map to resonant season
    if inner_state == 0 and outer_state == 0:
        return "Winter"
    elif inner_state == 1 and outer_state == 0:
        return "Spring"
    elif inner_state == 1 and outer_state == 1:
        return "Summer"
    elif inner_state == 0 and outer_state == 1:
        return "Fall"

def verify_and_count_seasons():
    """Verify resonant seasons in all compiled card files and count occurrences."""
    all_files = glob.glob(f"{COMPILED_DIR}/*/*.yml")
    
    incorrect_cards = []
    season_counts = {"Winter": 0, "Spring": 0, "Summer": 0, "Fall": 0}
    
    for file_path in all_files:
        # Extract binary code from filename
        binary_code = os.path.basename(file_path).replace('.yml', '')
        if len(binary_code) != 8 or not all(bit in '01' for bit in binary_code):
            print(f"Skipping {file_path}: Invalid binary code")
            continue
        
        # Calculate correct resonant season based on bit pattern
        correct_season = analyze_bit_pattern(binary_code)
        
        # Load the YAML file to check current resonant season
        try:
            with open(file_path, 'r') as file:
                card_data = yaml.safe_load(file)
            
            # Get current resonant season from the file
            current_season = None
            if "archetype" in card_data and "resonant_season" in card_data["archetype"]:
                current_season = card_data["archetype"]["resonant_season"]
            
            if current_season:
                # Count seasons
                season_counts[correct_season] += 1
                
                # Check if season is incorrect
                if current_season != correct_season:
                    incorrect_cards.append({
                        "binary": binary_code,
                        "file_path": file_path,
                        "current_season": current_season,
                        "correct_season": correct_season
                    })
            else:
                print(f"Warning: No resonant season found in {file_path}")
                
        except (yaml.YAMLError, FileNotFoundError) as e:
            print(f"Error processing {file_path}: {e}")
    
    return incorrect_cards, season_counts

def generate_fix_commands(incorrect_cards):
    """Generate commands to fix the incorrect card files."""
    # Group by hexagram to minimize commands
    hexagrams_to_fix = set()
    for card in incorrect_cards:
        hexagram = card["binary"][0:6]
        hexagrams_to_fix.add(hexagram)
    
    # Create single command to regenerate all affected hexagrams
    python_cmd = "python generate-all-associations.py"
    
    # Create command to regenerate specific hexagrams
    hexagram_cmds = []
    for hexagram in sorted(hexagrams_to_fix):
        hexagram_cmds.append(f"python association-generator.py {hexagram}")
    
    return python_cmd, hexagram_cmds

def main():
    """Main function to audit resonant seasons."""
    print("Auditing resonant seasons in compiled card files...")
    
    incorrect_cards, season_counts = verify_and_count_seasons()
    
    # Print season counts
    print("\nCurrent Resonant Season Distribution:")
    for season, count in season_counts.items():
        print(f"  {season}: {count} cards")
    
    # Check if we have a perfect balance (64 cards per season)
    total_cards = sum(season_counts.values())
    expected_per_season = total_cards // 4
    
    is_balanced = all(count == expected_per_season for count in season_counts.values())
    if is_balanced:
        print(f"\n✓ Perfect balance achieved: {expected_per_season} cards per season")
    else:
        print(f"\n✗ Imbalanced distribution (should be {expected_per_season} cards per season)")
    
    # Print incorrect cards
    if incorrect_cards:
        print(f"\nFound {len(incorrect_cards)} cards with incorrect resonant seasons:")
        for i, card in enumerate(incorrect_cards, 1):
            print(f"{i}. {card['binary']}: {card['current_season']} → {card['correct_season']}")
        
        # Generate fix commands
        regenerate_all_cmd, hexagram_cmds = generate_fix_commands(incorrect_cards)
        
        print("\nTo fix all cards at once, run:")
        print(f"  {regenerate_all_cmd}")
        
        print("\nOr to fix specific hexagrams, run:")
        for cmd in hexagram_cmds:
            print(f"  {cmd}")
    else:
        print("\n✓ All cards have correct resonant seasons")

if __name__ == "__main__":
    main()