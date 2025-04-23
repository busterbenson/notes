#!/usr/bin/env python3
"""
8-Bit Oracle Card Generator

This script generates a complete card YAML file for a given 8-bit binary code.
It calculates all necessary attributes and follows the template structure.

Usage:
    python generate-card.py <binary_code>
    
Example:
    python generate-card.py 10101010
"""

import sys
import os
import yaml
import re
import argparse
from pathlib import Path

# Configuration
CORE_SYSTEMS_PATH = '../associations/core-systems.yml'
COMPOSITE_ASSOCIATIONS_PATH = '../associations/composite-associations.yml'
LUNAR_CYCLE_PATH = '../associations/lunar-cycle.yml'
TEMPLATE_PATH = 'card-template.yml'
OUTPUT_DIR = 'generated'

def load_yaml_file(file_path):
    """Load a YAML file and return its contents."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def count_bits(binary_str):
    """Count the number of '1's in a binary string."""
    return binary_str.count('1')

def convert_to_decimal(binary_code):
    """Convert binary code to decimal using left-to-right bit significance."""
    values = [1, 2, 4, 8, 16, 32, 64, 128]  # Power of 2 values for each bit position
    decimal = 0
    
    for i, bit in enumerate(binary_code):
        if bit == "1":
            decimal += values[i]
    
    return decimal

def determine_archetype(inner_bits, outer_bits, season_bits):
    """Determine the archetype based on inner world, outer world, and season bits."""
    # Calculate inner and outer world states
    inner_active = count_bits(inner_bits) >= 2
    outer_active = count_bits(outer_bits) >= 2
    
    inner_state = 1 if inner_active else 0
    outer_state = 1 if outer_active else 0
    
    # Map inner-outer to resonant season
    resonant_season_map = {
        (0, 0): "00",  # Winter
        (1, 0): "10",  # Spring
        (1, 1): "11",  # Summer
        (0, 1): "01"   # Fall
    }
    
    resonant_season = resonant_season_map[(inner_state, outer_state)]
    
    # Determine archetype based on actual season vs resonant season
    seasons_order = ["00", "10", "11", "01"]  # Winter, Spring, Summer, Fall
    resonant_idx = seasons_order.index(resonant_season)
    actual_idx = seasons_order.index(season_bits)
    
    # Calculate the difference to determine archetype
    diff = (actual_idx - resonant_idx) % 4
    
    archetypes = ["Sage", "Fool", "Hero", "Monster"]
    archetype = archetypes[diff]
    
    return archetype, resonant_season

def determine_gender(bit_count, archetype):
    """Determine gender based on bit count and archetype."""
    if bit_count == 0 or bit_count == 6:
        return "neutral"
    elif bit_count in [3, 5]:
        if archetype in ["Hero", "Monster"]:
            return "feminine"
        else:
            return "masculine"
    else:  # 2 or 4 bits
        if archetype in ["Hero", "Monster"]:
            return "masculine"
        else:
            return "feminine"

def calculate_lunar_phase(decimal_value, lunar_cycle_data):
    """Calculate lunar phase information based on decimal value."""
    lunar_phase_num = (decimal_value // 2) % 8
    phase_half = decimal_value % 2
    
    phase_data = lunar_cycle_data["lunar_cycle_system"]["phases"][str(lunar_phase_num)]
    phase_name = phase_data["name"]
    
    if phase_half == 0:
        half_name = phase_data["first_half"]["name"]
        half_desc = phase_data["first_half"]["half_phase_desc"]
    else:
        half_name = phase_data["second_half"]["name"]
        half_desc = phase_data["second_half"]["half_phase_desc"]
    
    return {
        "phase": phase_name,
        "half_name": half_name,
        "half_desc": half_desc,
        "decimal_modulo": f"{decimal_value} % 8 = {lunar_phase_num}, {decimal_value} % 2 = {phase_half}"
    }

def get_trigram_data(trigram, core_systems):
    """Get trigram data from core systems."""
    trigram_data = core_systems["core_associations"]["i_ching_trigrams"].get(trigram, {})
    color_data = core_systems["core_associations"]["rgb_colors"].get(trigram, {})
    
    return {
        "trigram": trigram_data.get("traditional_name", ""),
        "symbol": trigram_data.get("trigram_symbol", ""),
        "color": color_data.get("name", "")
    }

def get_inner_outer_world_data(bits, composite_associations, position):
    """Get inner or outer world data from composite associations."""
    frameworks = composite_associations["composite_associations"].get("inner_and_outer_worlds", {})
    component = frameworks.get(position, {})
    meanings = component.get("meanings", {})
    
    if bits in meanings:
        return meanings[bits]
    
    return {}

def get_hexagram_data(hexagram, core_systems):
    """Get hexagram data from core systems."""
    if hexagram in core_systems["core_associations"]["hexagrams"]:
        return core_systems["core_associations"]["hexagrams"][hexagram]
    
    return {}

def get_tarot_correspondence(inner_outer_bits, season_bits, core_systems):
    """Get tarot correspondence based on inner+outer bits and season."""
    # This is a placeholder - actual implementation would depend on the tarot mapping
    season_to_suit = {
        "00": "Swords",
        "10": "Wands",
        "11": "Cups",
        "01": "Pentacles"
    }
    
    suit = season_to_suit.get(season_bits, "")
    # In a real implementation, you would map the inner+outer bits to a specific card
    
    return {
        "card": f"[Card for {inner_outer_bits}]",
        "cycle_suit": suit,
        "seasonal_expression": f"[Description of how this hexagram energy expresses in this season]"
    }

def generate_card(binary_code):
    """Generate a card for the given binary code."""
    # Validate binary code format
    if not re.match(r'^[01]{8}$', binary_code):
        raise ValueError("Binary code must be exactly 8 bits (0s and 1s)")
    
    # Load necessary data
    core_systems = load_yaml_file(CORE_SYSTEMS_PATH)
    composite_associations = load_yaml_file(COMPOSITE_ASSOCIATIONS_PATH)
    lunar_cycle_data = load_yaml_file(LUNAR_CYCLE_PATH)
    card_template = load_yaml_file(TEMPLATE_PATH)
    
    # Prepare basic card information
    inner_bits = binary_code[0:3]
    outer_bits = binary_code[3:6]
    season_bits = binary_code[6:8]
    
    # Calculate decimal and hexadecimal values
    decimal = convert_to_decimal(binary_code)
    hexadecimal = format(int(binary_code, 2), '02x')
    
    # Determine season
    season_map = {"00": "Winter", "10": "Spring", "11": "Summer", "01": "Fall"}
    season = season_map.get(season_bits, "Unknown")
    
    # Determine archetype and resonant season
    archetype, resonant_season = determine_archetype(inner_bits, outer_bits, season_bits)
    resonant_season_name = season_map.get(resonant_season, "Unknown")
    
    # Determine archetype color
    archetype_colors = {
        "Sage": "Iridescent",
        "Fool": "Turquoise",
        "Hero": "Gold",
        "Monster": "Purple"
    }
    archetype_color = archetype_colors.get(archetype, "")
    
    # Count bits for gender determination
    bit_count_1_6 = count_bits(binary_code[0:6])
    gender = determine_gender(bit_count_1_6, archetype)
    
    # Get inner and outer world data
    inner_trigram_data = get_trigram_data(inner_bits, core_systems)
    outer_trigram_data = get_trigram_data(outer_bits, core_systems)
    
    inner_world_meaning = get_inner_outer_world_data(inner_bits, composite_associations, "inner_world")
    outer_world_meaning = get_inner_outer_world_data(outer_bits, composite_associations, "outer_world")
    
    # Get hexagram data
    hexagram = binary_code[0:6]
    hexagram_data = get_hexagram_data(hexagram, core_systems)
    
    # Calculate lunar cycle
    lunar_info = calculate_lunar_phase(decimal, lunar_cycle_data)
    cycle_number = (bit_count_1_6 % 4) + 1
    cycle_names = {
        1: "Inception Cycle",
        2: "Development Cycle",
        3: "Culmination Cycle",
        4: "Transition Cycle"
    }
    cycle_name = cycle_names.get(cycle_number, "")
    
    # Construct the card data
    card_data = {
        "card": {
            # Summary
            "version": "1.0",
            "binary": binary_code,
            "decimal": str(decimal),
            "hexadecimal": hexadecimal,
            
            # Basic Info
            "basic_info": {
                "desc": f"[A paragraph describing the card's core energy and meaning - focus on the combination of hexagram energy with the {season}/{archetype} expression. Include how the bit pattern reflects resources present/absent and how this connects to the card's overall meaning.]",
                "keywords": ["[keyword 1]", "[keyword 2]", "[keyword 3]", "[keyword 4]", "[keyword 5]", "[keyword 6]"],
                "symbols": ["[symbol 1]", "[symbol 2]", "[symbol 3]", "[symbol 4]", "[symbol 5]", "[symbol 6]"]
            },
            
            # Direct Associations
            "direct_associations": {
                "archetype": archetype,
                "archetype_color": archetype_color,
                "gender": gender,
                
                # Inner World
                "inner_world": {
                    "color": inner_trigram_data["color"],
                    "trigram": inner_trigram_data["trigram"],
                    "meaning": inner_world_meaning.get("desc", "[Inner world meaning]")
                },
                
                # Outer World
                "outer_world": {
                    "color": outer_trigram_data["color"],
                    "trigram": outer_trigram_data["trigram"],
                    "meaning": outer_world_meaning.get("desc", "[Outer world meaning]")
                },
                
                # Solar Season
                "solar_cycle": {
                    "season": season,
                    "tarot_suit": {"Winter": "Swords", "Spring": "Wands", "Summer": "Cups", "Fall": "Pentacles"}.get(season, ""),
                    "element": {"Winter": "Air", "Spring": "Fire", "Summer": "Water", "Fall": "Earth"}.get(season, "")
                },
                
                # Lunar cycle
                "lunar_cycle": {
                    "decimal_modulo": lunar_info["decimal_modulo"],
                    "phase": lunar_info["phase"],
                    "phase_half": lunar_info["half_desc"],
                    "cycle_number": str(cycle_number),
                    "cycle_name": cycle_name,
                    "complete_designation": f"{lunar_info['half_name']}, {cycle_name} of {season}"
                },
                
                # Tarot
                "tarot": get_tarot_correspondence(hexagram, season_bits, core_systems),
                
                # Hexagram-related
                "hexagram": {
                    "i_ching": {
                        "number": hexagram_data.get("i_ching", {}).get("number", "[N]"),
                        "name": hexagram_data.get("i_ching", {}).get("traditional_name", "[Name]"),
                        "label": hexagram_data.get("i_ching", {}).get("label", "[Label]"),
                        "description": hexagram_data.get("i_ching", {}).get("description", "[Description]")
                    },
                    "gene_key": {
                        "number": hexagram_data.get("gene_key", {}).get("number", "[N]"),
                        "shadow": hexagram_data.get("gene_key", {}).get("shadow", "[Shadow]"),
                        "gift": hexagram_data.get("gene_key", {}).get("gift", "[Gift]"),
                        "siddhi": hexagram_data.get("gene_key", {}).get("siddhi", "[Siddhi]"),
                        "meaning": hexagram_data.get("gene_key", {}).get("description", "[Meaning]")
                    }
                }
            },
            
            # Interpreted Meanings
            "interpreted_meanings": {
                "basic": {
                    "name_6bit": f"[Name based on hexagram {hexagram}]",
                    "name_8bit": f"[Name incorporating {season}]",
                    "gender": gender
                },
                
                # Oracle card creation
                "oracle_card": {
                    "card_name": f"[Evocative name for card {binary_code}]",
                    "card_creature": f"[Description of the mythological figure or character that embodies this card's energy, with {gender} terms]",
                    "question_posed": "[Question this card asks the querent - should prompt reflection about the core themes]",
                    "card_scene": "[Detailed description of the card's imagery, incorporating all symbolic elements, colors, and archetype]",
                    "universal_symbol": "[Core symbol that captures the essence of this card]",
                    "mood": "[Emotional/energetic quality of the card]",
                    
                    # Image generation prompt
                    "prompt_for_image_gen": f"""Limited color risograph-style illustration of [short scene description].
Use {inner_trigram_data['color']} for foreground elements (inner world) and {outer_trigram_data['color']} for background/environment (outer world), with {archetype_color} highlights.
Maintain risograph/woodblock print texture with strong contrast, 3-4 colors max, and minimalistic geometric forms.
Include a clean, full-width title bar at the bottom, centered, with a card title '[CARD TITLE]' in bold and a more subtle subtitle below that with the 8-bit code '{binary_code}', without corner decorations or symbols.
Feature [card_creature in the card_scene, key symbolic elements, e.g., moon phase, animal companions, symbolic object].
The scene should evoke the mood of [MOOD KEYWORDS] and incorporate subtle seasonal/elemental references appropriate for {season}.
Style should blend Rider-Waite simplicity with modern symbolic abstraction, emotionally resonant but compositionally clean."""
                }
            },
            
            # Related Cards
            "related_cards": {
                # Season variations of the same card
                "same_card_winter": f"{hexagram}00",
                "same_card_spring": f"{hexagram}10",
                "same_card_summer": f"{hexagram}11",
                "same_card_fall": f"{hexagram}01",
                
                # Opposites
                "opposite": ''.join('1' if bit == '0' else '0' for bit in binary_code),
                
                # Related thematically
                "thematic_pair": "[Related binary]",
                
                # Complete cycle
                "full_cycle": [f"{hexagram}00", f"{hexagram}10", f"{hexagram}11", f"{hexagram}01"]
            },
            
            # Bit Values
            "bit_values": {
                "bit1": binary_code[0],
                "bit2": binary_code[1],
                "bit3": binary_code[2],
                "bit4": binary_code[3],
                "bit5": binary_code[4],
                "bit6": binary_code[5],
                "bit78": binary_code[6:8]
            },
            
            # Fractal Manifestations
            "fractal_meanings": {
                "quantum": {
                    "pattern": "[How this card's energy pattern manifests at quantum level]",
                    "insight": "[The wisdom this reveals about reality's fundamental nature]"
                },
                "biological": {
                    "pattern": "[How this card's energy pattern appears in living systems]",
                    "insight": "[The wisdom this reveals about life and evolution]"
                },
                "psychological": {
                    "pattern": "[How this card's energy pattern manifests in human mind]",
                    "insight": "[The wisdom this reveals about consciousness and thought]"
                },
                "social": {
                    "pattern": "[How this card's energy pattern appears in communities]",
                    "insight": "[The wisdom this reveals about human connection]"
                },
                "ecological": {
                    "pattern": "[How this card's energy pattern manifests in ecosystems]",
                    "insight": "[The wisdom this reveals about natural systems]"
                },
                "cosmic": {
                    "pattern": "[How this card's energy pattern appears at universal scale]",
                    "insight": "[The wisdom this reveals about the nature of existence]"
                }
            }
        }
    }
    
    return card_data

def save_card_file(binary_code, card_data):
    """Save the card to a YAML file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_path = os.path.join(OUTPUT_DIR, f"{binary_code}.yml")
    
    with open(file_path, 'w') as file:
        yaml.dump(card_data, file, default_flow_style=False, sort_keys=False)
    
    return file_path

def main():
    """Main function to create a card from a binary code."""
    parser = argparse.ArgumentParser(description='Generate an 8-Bit Oracle card from a binary code.')
    parser.add_argument('binary_code', help='8-bit binary code (e.g., 10101010)')
    args = parser.parse_args()
    
    try:
        binary_code = args.binary_code
        
        # Generate the card
        card_data = generate_card(binary_code)
        
        # Save the card to a file
        output_path = save_card_file(binary_code, card_data)
        
        print(f"Card for {binary_code} generated and saved to: {output_path}")
        print("\nNext steps:")
        print("1. Open the file and fill in the placeholder fields with meaningful content")
        print("2. Add keywords, symbols, and other specific details")
        print("3. Craft a compelling card description")
        print("4. Develop the imagery concept for the card")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()