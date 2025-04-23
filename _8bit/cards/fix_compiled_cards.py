#!/usr/bin/env python3
"""
8-Bit Oracle Compiled Cards Fixer

This script:
1. Fixes the resonant season assignment in card 00000000.yml
2. Regenerates any cards with missing fields or incorrect resonant seasons
3. Ensures all compiled cards follow the correct format

Usage:
    python fix_compiled_cards.py
"""

import os
import yaml
import glob
import subprocess

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

def fix_card_00000000():
    """Fix the 00000000.yml card by adding the missing resonant season."""
    file_path = os.path.join(COMPILED_DIR, '000000', '00000000.yml')
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return False
    
    try:
        with open(file_path, 'r') as file:
            card_data = yaml.safe_load(file)
        
        # Check if resonant_season is missing
        if "archetype" in card_data and "resonant_season" not in card_data["archetype"]:
            # Add resonant_season (which should be Winter for 00000000)
            card_data["archetype"]["resonant_season"] = "Winter"
            card_data["archetype"]["resonant_season_key"] = "inner0-outer0"
            
            # Add any other missing fields based on the expected structure
            if "cycle_position" not in card_data["archetype"]:
                card_data["archetype"]["cycle_position"] = "Resonant Season"
            
            if "cycle_description" not in card_data["archetype"]:
                card_data["archetype"]["cycle_description"] = "A Winter expression of a Winter-resonant pattern"
            
            # Write back the updated data
            with open(file_path, 'w') as file:
                yaml.dump(card_data, file, default_flow_style=False, sort_keys=False)
            
            print(f"✓ Updated {file_path} with resonant season: Winter")
            return True
        else:
            print(f"✓ {file_path} already has resonant season information")
            return False
            
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def find_cards_with_missing_fields():
    """Find all cards with missing required fields."""
    all_files = glob.glob(f"{COMPILED_DIR}/*/*.yml")
    cards_to_fix = []
    
    required_fields = {
        "archetype": ["name", "color", "resonant_season", "resonant_season_key", "cycle_position"],
        "inner_world": ["name", "color"],
        "outer_world": ["name", "color"],
        "bit_associations.bit78": ["season", "element"],
        "lunar_cycle": ["phase"]
    }
    
    for file_path in all_files:
        # Extract binary code from filename
        binary_code = os.path.basename(file_path).replace('.yml', '')
        hexagram = binary_code[0:6]
        
        try:
            with open(file_path, 'r') as file:
                card_data = yaml.safe_load(file)
            
            missing_fields = []
            
            # Check all required fields
            for section, fields in required_fields.items():
                if "." in section:
                    parent, child = section.split(".")
                    if parent not in card_data or child not in card_data[parent]:
                        missing_fields.append(f"{section}")
                        continue
                    
                    for field in fields:
                        if field not in card_data[parent][child]:
                            missing_fields.append(f"{section}.{field}")
                else:
                    if section not in card_data:
                        missing_fields.append(section)
                        continue
                        
                    for field in fields:
                        if field not in card_data[section]:
                            missing_fields.append(f"{section}.{field}")
            
            # Check resonant season accuracy
            if ("archetype" in card_data and 
                "resonant_season" in card_data["archetype"]):
                current_season = card_data["archetype"]["resonant_season"]
                correct_season = analyze_bit_pattern(binary_code)
                
                if current_season != correct_season:
                    missing_fields.append(f"Incorrect resonant season: {current_season} → {correct_season}")
            
            if missing_fields:
                cards_to_fix.append({
                    "binary": binary_code,
                    "hexagram": hexagram,
                    "file_path": file_path,
                    "missing_fields": missing_fields
                })
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            cards_to_fix.append({
                "binary": binary_code,
                "hexagram": hexagram,
                "file_path": file_path,
                "missing_fields": ["Error reading file"]
            })
    
    return cards_to_fix

def regenerate_cards(cards_to_fix):
    """Regenerate the cards that need fixing."""
    # Group by hexagram to minimize regeneration commands
    hexagrams_to_fix = set()
    for card in cards_to_fix:
        hexagrams_to_fix.add(card["hexagram"])
    
    print(f"\nRegenerating {len(hexagrams_to_fix)} hexagrams ({len(cards_to_fix)} cards)...")
    
    # Regenerate each hexagram
    success_count = 0
    for hexagram in sorted(hexagrams_to_fix):
        cmd = f"python association-generator.py {hexagram}"
        print(f"Running: {cmd}")
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(f"Error regenerating hexagram {hexagram}: {e}")
    
    print(f"\n✓ Successfully regenerated {success_count}/{len(hexagrams_to_fix)} hexagrams")

def verify_resonant_seasons():
    """Verify the distribution of resonant seasons after fixes."""
    all_files = glob.glob(f"{COMPILED_DIR}/*/*.yml")
    season_counts = {"Winter": 0, "Spring": 0, "Summer": 0, "Fall": 0}
    
    for file_path in all_files:
        # Extract binary code from filename
        binary_code = os.path.basename(file_path).replace('.yml', '')
        
        try:
            with open(file_path, 'r') as file:
                card_data = yaml.safe_load(file)
            
            # Get current resonant season from the file
            if "archetype" in card_data and "resonant_season" in card_data["archetype"]:
                current_season = card_data["archetype"]["resonant_season"]
                season_counts[current_season] += 1
                
        except Exception as e:
            print(f"Error verifying {file_path}: {e}")
    
    print("\nFinal Resonant Season Distribution:")
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

def main():
    """Main function to fix compiled cards."""
    print("Fixing compiled card files...")
    
    # Fix the special case of 00000000.yml
    fix_card_00000000()
    
    # Find cards with missing fields
    cards_to_fix = find_cards_with_missing_fields()
    
    if cards_to_fix:
        print(f"\nFound {len(cards_to_fix)} cards with missing or incorrect fields:")
        for i, card in enumerate(cards_to_fix, 1):
            print(f"\n{i}. {card['binary']}:")
            for field in card['missing_fields']:
                print(f"   - Missing/incorrect: {field}")
        
        # Ask user if they want to regenerate these cards
        regenerate = input("\nRegenerate these cards? (y/n): ")
        if regenerate.lower() == 'y':
            regenerate_cards(cards_to_fix)
    else:
        print("\n✓ All cards have the required fields")
    
    # Verify final distribution
    verify_resonant_seasons()

if __name__ == "__main__":
    main()