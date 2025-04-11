#!/usr/bin/env python3
"""
8-Bit Oracle Card Generator

This script helps generate card YAML files for the 8-bit Oracle v3 system,
and also produces image generation prompts for ChatGPT. It now includes
support for narrative arcs and fables integration.

Usage:
    python card-generator.py <binary_code>
    
Example:
    python card-generator.py 00000000
"""

import sys
import os
import yaml
import math
from datetime import datetime

# Configuration
CORE_SYSTEMS_PATH = '../associations/core-systems.yml'
LUNAR_CYCLE_PATH = '../associations/lunar-cycle.yml'
COMPOSITE_ASSOCIATIONS_PATH = '../associations/composite-associations.yml'
ARCS_DIR = 'arcs/hexagram'
OUTPUT_DIR = 'v3'
STYLE_GUIDELINES_PATH = 'card-style-guidelines.md'

# Load core systems data
def load_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def load_markdown_file(file_path):
    """Load and parse a markdown file, returning it as text."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return None

def parse_narrative_arc(arc_text):
    """Parse a narrative arc markdown file and extract key sections."""
    if not arc_text:
        return {}
        
    sections = {}
    current_section = None
    current_content = []
    
    for line in arc_text.split('\n'):
        if line.startswith('## '):
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
                current_content = []
            current_section = line[3:].strip()
        elif line.startswith('### '):
            if current_section and current_content:
                # For subsections, add them as part of the current section
                current_content.append(line)
        else:
            if current_section:
                current_content.append(line)
    
    # Add the last section
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections

def extract_seasonal_card_info(arc_sections, binary_code, season):
    """Extract specific seasonal card information from the narrative arc."""
    if not arc_sections:
        return {}
        
    # Get the bits and determine which card in the narrative arc this is
    season_map = {
        "Winter": "00",
        "Spring": "10", 
        "Summer": "11",
        "Fall": "01"
    }
    
    hexagram = binary_code[0:6]
    season_bits = binary_code[6:8]
    
    # Extract the seasonal narrative for this specific card
    info = {}
    
    # Look for the specific section for this season
    narrative_structure = arc_sections.get("Narrative Arc Structure", "")
    season_specific_info = ""
    
    # Extract the season-specific section for this card (Fool, Hero, Monster, or Sage)
    for line in narrative_structure.split('\n'):
        if f"{season} ({hexagram}{season_map[season]})" in line:
            season_specific_info = line
            break
    
    info["season_specific"] = season_specific_info
    
    # Extract fable
    info["fable"] = arc_sections.get("Narrative Fable", "")
    
    # Extract visual continuity details
    visual_continuity = arc_sections.get("Visual Narrative Continuity", "")
    info["visual_continuity"] = visual_continuity
    
    return info

def count_bits(binary_str):
    """Count the number of '1's in a binary string."""
    return binary_str.count('1')

def generate_card(binary_code):
    """Generate a complete card YAML file based on the binary code."""
    # Validate binary code
    if not (len(binary_code) == 8 and all(bit in '01' for bit in binary_code)):
        print(f"Error: Invalid binary code '{binary_code}'. Must be 8 bits of 0s and 1s.")
        return None
    
    # Load data
    core_systems = load_yaml_file(CORE_SYSTEMS_PATH)
    lunar_cycle = load_yaml_file(LUNAR_CYCLE_PATH)
    try:
        composite_associations = load_yaml_file(COMPOSITE_ASSOCIATIONS_PATH)
    except:
        composite_associations = {}
    
    # Calculate basic values
    decimal_value = int(binary_code, 2)
    hexadecimal_value = hex(decimal_value)[2:].upper()
    
    # Split the binary code
    bits_1_3 = binary_code[0:3]
    bits_4_6 = binary_code[3:6]
    bits_7_8 = binary_code[6:8]
    
    # Calculate lunar phase
    lunar_phase_num = (decimal_value // 2) % 8
    phase_half = decimal_value % 2
    phase_half_name = "first_half" if phase_half == 0 else "second_half"
    
    # Get lunar cycle based on bit count
    bit_count_1_6 = count_bits(binary_code[0:6])
    lunar_cycle_num = (bit_count_1_6 % 4) + 1
    lunar_cycle_names = {
        1: "Inception Cycle",
        2: "Development Cycle",
        3: "Culmination Cycle",
        4: "Transition Cycle"
    }
    
    # Get lunar phase names
    luna_phase_name = lunar_cycle['lunar_cycle_system']['phases'][str(lunar_phase_num)]['name']
    luna_phase_half_name = lunar_cycle['lunar_cycle_system']['phases'][str(lunar_phase_num)][phase_half_name]['name']
    
    # Get season
    season_map = {
        "00": "Winter",
        "10": "Spring", 
        "11": "Summer",
        "01": "Fall"
    }
    season = season_map.get(bits_7_8, "Unknown")
    
    # Get inner world information
    inner_world_associations = composite_associations.get('inner_and_outer_worlds', {}).get('inner_world', {}).get('meanings', {}).get(bits_1_3, {})
    inner_world_color = inner_world_associations.get('color', "Unknown")
    inner_world_trigram = inner_world_associations.get('trigram', "Unknown")
    inner_world_meaning = inner_world_associations.get('desc', "Unknown")
    
    # Get outer world information
    outer_world_associations = composite_associations.get('inner_and_outer_worlds', {}).get('outer_world', {}).get('meanings', {}).get(bits_4_6, {})
    outer_world_color = outer_world_associations.get('color', "Unknown")
    outer_world_trigram = outer_world_associations.get('trigram', "Unknown")
    outer_world_meaning = outer_world_associations.get('desc', "Unknown")
    
    # Get hexagram information
    hexagram_key = bits_1_3 + bits_4_6
    i_ching = {}
    gene_key = {}
    
    # Try to get hexagram info from composite_associations if available
    if composite_associations and "hexagrams" in composite_associations:
        if hexagram_key in composite_associations["hexagrams"]:
            hex_data = composite_associations["hexagrams"][hexagram_key]
            gene_key_info = hex_data.get("gene_key", "")
            if gene_key_info:
                # Parse "NN: Shadow → Gift → Siddhi" format
                parts = gene_key_info.split(":")
                if len(parts) == 2:
                    number = parts[0].strip()
                    journey = parts[1].strip().split("→")
                    if len(journey) == 3:
                        gene_key = {
                            "number": number,
                            "shadow": journey[0].strip(),
                            "gift": journey[1].strip(),
                            "siddhi": journey[2].strip()
                        }
    
    # Determine archetype
    inner_world_active = count_bits(bits_1_3) >= 2
    outer_world_active = count_bits(bits_4_6) >= 2
    
    # Determine resonant season based on inner/outer world activity
    resonant_season_map = {
        "inner0-outer0": "Winter",
        "inner1-outer0": "Spring",
        "inner1-outer1": "Summer",
        "inner0-outer1": "Fall"
    }
    resonant_season_key = f"inner{'1' if inner_world_active else '0'}-outer{'1' if outer_world_active else '0'}"
    resonant_season = resonant_season_map.get(resonant_season_key, "Unknown")
    
    # Determine which cycle is the resonant one (Sage)
    seasons_order = ["Winter", "Spring", "Summer", "Fall"]
    resonant_idx = seasons_order.index(resonant_season)
    season_idx = seasons_order.index(season)
    
    cycle_diff = (season_idx - resonant_idx) % 4
    archetypes = ["Sage", "Fool", "Hero", "Monster"]
    archetype = archetypes[cycle_diff]
    
    # Get archetype color
    archetype_colors = {
        "Sage": "Purple",
        "Fool": "Turquoise",
        "Hero": "Gold",
        "Monster": "Iridescent"
    }
    archetype_color = archetype_colors.get(archetype, "Unknown")
    
    # Determine gender
    bit_count = count_bits(binary_code[0:6])
    if bit_count == 0 or bit_count == 6:
        gender = "neutral"
    elif bit_count == 3 or bit_count == 5:
        if archetype in ["Hero", "Monster"]:
            gender = "feminine"
        else:
            gender = "masculine"
    else:  # 2 or 4
        if archetype in ["Hero", "Monster"]:
            gender = "masculine"
        else:
            gender = "feminine"
    
    # Get tarot mapping
    tarot_card = "Unknown"  # This would need to be loaded from tarot mapping file
    
    # Default tarot suits mapping to seasons
    tarot_suits = {
        "00": "Pentacles", # Winter
        "10": "Wands",     # Spring
        "11": "Cups",      # Summer
        "01": "Swords"     # Fall
    }
    tarot_suit = tarot_suits.get(bits_7_8, "Unknown")
    
    # Default elements mapping to seasons
    elements = {
        "00": "Earth",  # Winter
        "10": "Fire",   # Spring
        "11": "Water",  # Summer
        "01": "Air"     # Fall
    }
    element = elements.get(bits_7_8, "Unknown")
    
    # Compile lunar designation
    lunar_designation = f"{luna_phase_half_name}, {lunar_cycle_names[lunar_cycle_num]} of {season}"
    
    # Load narrative arc if available
    arc_file_path = os.path.join(ARCS_DIR, f"{hexagram_key}.md")
    arc_text = load_markdown_file(arc_file_path)
    arc_sections = parse_narrative_arc(arc_text) if arc_text else {}
    
    # Extract seasonal info for this specific card
    arc_info = extract_seasonal_card_info(arc_sections, binary_code, season)
    
    # Get fable title
    fable_title = ""
    fable_section_name = "Narrative Fable"
    # Look for the section heading
    for section_name in arc_sections:
        if section_name.startswith("Narrative Fable"):
            fable_section_name = section_name
            if ":" in section_name:
                fable_title = section_name.split(":", 1)[1].strip()
                break
    
    # Get card name suggestions from composite associations if available
    suggested_name = ""
    if composite_associations and "hexagrams" in composite_associations:
        if hexagram_key in composite_associations["hexagrams"]:
            hex_data = composite_associations["hexagrams"][hexagram_key]
            if "seasonal_names" in hex_data and season in hex_data["seasonal_names"]:
                suggested_name = hex_data["seasonal_names"][season]
    
    # Build card data
    card_data = {
        "card": {
            "version": "3.0",
            "binary": binary_code,
            "decimal": decimal_value,
            "hexadecimal": hexadecimal_value,
            
            "basic_info": {
                "desc": f"[Description for {binary_code}]",
                "keywords": ["keyword1", "keyword2", "keyword3"],
                "symbols": ["symbol1", "symbol2", "symbol3"]
            },
            
            "direct_associations": {
                "archetype": archetype,
                "archetype_color": archetype_color,
                "gender": gender,
                
                "inner_world": {
                    "color": inner_world_color,
                    "trigram": inner_world_trigram,
                    "meaning": inner_world_meaning
                },
                
                "outer_world": {
                    "color": outer_world_color,
                    "trigram": outer_world_trigram,
                    "meaning": outer_world_meaning
                },
                
                "solar_cycle": {
                    "season": season,
                    "tarot_suit": tarot_suit,
                    "element": element
                },
                
                "lunar_cycle": {
                    "decimal_modulo": f"{decimal_value} % 8 = {lunar_phase_num}, {decimal_value} % 2 = {phase_half}",
                    "phase": luna_phase_name,
                    "phase_half": luna_phase_half_name.split('(')[0].strip() if '(' in luna_phase_half_name else luna_phase_half_name,
                    "cycle_number": str(lunar_cycle_num),
                    "cycle_name": lunar_cycle_names[lunar_cycle_num],
                    "complete_designation": lunar_designation
                },
                
                "tarot": {
                    "card": tarot_card,
                    "cycle_suit": tarot_suit,
                    "seasonal_expression": f"[Description of how this hexagram energy expresses in {season} as {archetype}]"
                },
                
                "hexagram": {
                    "i_ching": i_ching,
                    "gene_key": gene_key
                },
                
                "narrative_arc": {
                    "available": True if arc_text else False,
                    "fable_title": fable_title,
                    "core_theme": arc_sections.get("Core Theme", "") if arc_sections else "",
                    "evolutionary_journey": arc_sections.get("Evolutionary Journey", "") if arc_sections else ""
                }
            },
            
            "interpreted_meanings": {
                "basic": {
                    "name_6bit": f"[Name for {hexagram_key}]",
                    "name_8bit": suggested_name if suggested_name else f"[Name for {binary_code}]",
                    "gender": gender
                },
                
                "oracle_card": {
                    "card_name": f"[Name] ({luna_phase_half_name})",
                    "card_creature": f"[Description of a {gender} {archetype.lower()}]",
                    "question_posed": "[Question for querent]",
                    "card_scene": f"[Scene description incorporating {season}, {luna_phase_half_name}, {inner_world_color} and {outer_world_color} colors]",
                    "universal_symbol": "[Core symbol]",
                    "mood": "[Mood keywords]",
                    
                    "seasonal_narrative_coherence": """[Describe how this card connects to the other three cards in its hexagram (same bits 1-6, different bits 7-8). Include:
- How the central symbolic elements transform across seasons
- How the character/creature evolves through the four archetypes
- Specific visual connections to maintain across all four cards
- How this specific seasonal expression relates to the overall hexagram theme]""",
                    
                    "prompt_for_image_gen": f"""LIMITED COLOR RISOGRAPH-STYLE ILLUSTRATION FOR "{suggested_name if suggested_name else '[NAME]'}" ({binary_code})

Create a limited-color risograph-style illustration that captures the essence of the {suggested_name if suggested_name else '[NAME]'} card - representing {arc_sections.get("Core Theme", "")[0:100] + "..." if arc_sections.get("Core Theme", "") else "[brief description of card's core meaning]"}.

CARD DIMENSIONS AND STYLE:
- 1200 x 2000 pixels (3:5 ratio)
- NO decorative borders or frames around the illustration
- Allow natural margins (5-8% of width) between content and card edges
- Content should NOT touch the very edges - leave appropriate breathing room
- The illustration should use traditional tarot card-style layout with natural margins
- Bottom 15% contains the title bar area with a clean horizontal line separation
- Woodblock print/risograph aesthetic with bold lines and limited colors
- Visible texture and grain throughout all elements
- Strong contrast between elements with minimalist composition

COLOR PALETTE:
- Primary: {inner_world_color} (for inner world character)
- Secondary: {outer_world_color} (for outer world environment)
- Accent: {archetype_color} (representing the {archetype} archetype)
- White/off-white background with subtle texture
- Use black for all outlines and details with varying line weights
- Some graduated values to create depth and dimension

CHARACTER DESCRIPTION (INNER WORLD):
- A {gender} {archetype.lower()} whose form [describe physical appearance and presence]
- [If gender-neutral] Neither masculine nor feminine, but [describe gender-neutral quality]
- [Describe stance, posture, gesture] 
- [Describe facial expression, eyes, gaze]
- [Describe what they might be holding or doing]
- [Describe how they embody the archetype's energy]
- [Describe any unique features that relate to the card's meaning]

SCENE DESCRIPTION (OUTER WORLD):
- [Describe environment that reflects {season} qualities]
- [Describe how the environment relates to the lunar phase {luna_phase_half_name}]
- [Describe background elements that reinforce the card's meaning]
- [Describe any weather, light, or atmospheric conditions]
- [Describe how the character interacts with or relates to the environment]
- [Describe any boundary or threshold elements in the scene]

LUNAR PHASE REPRESENTATION:
- Small, discrete {luna_phase_name} icon in upper right corner - [describe visual appearance]
- This represents the {luna_phase_half_name} phase - [describe meaning of this lunar phase]
- [Describe how the lunar phase icon might echo other elements in the image]

SYMBOLIC ELEMENTS:
- [Symbol 1]: [Describe visual appearance and meaning]
- [Symbol 2]: [Describe visual appearance and meaning]
- [Symbol 3]: [Describe visual appearance and meaning]
- [Symbol 4]: [Describe visual appearance and meaning]

NARRATIVE ARC ELEMENTS:
- This card is part of the hexagram {hexagram_key} narrative: "{fable_title if fable_title else '[Narrative name]'}"
- As the {season}/{archetype} expression, it should incorporate key narrative elements appropriate for this stage
- Important motifs from the narrative arc:
  * Primary Symbol: Look for descriptions of any central motif and how it appears in this season
  * Character Development: How the character/creature appears in the {archetype} archetype
  * Environment: How the setting manifests in {season}
  * Symbolic Elements: Include items or symbols mentioned for this specific season/archetype
- Include visual motifs that connect to the other three seasonal cards in this hexagram

MOOD AND ATMOSPHERE:
- [Mood quality 1] - [describe feeling or emotional tone]
- [Mood quality 2] - [describe feeling or emotional tone]
- [Mood quality 3] - [describe feeling or emotional tone]
- [Mood quality 4] - [describe feeling or emotional tone]

LAYOUT SPECIFICATIONS:
- Full width title bar at bottom (15% of card height)
- "[NAME]" in bold, centered, all caps
- "{luna_phase_half_name} • {binary_code}" in smaller text below
- Main illustration filling the space above the title bar
- Strong composition with [describe focal point placement]

ARTISTIC DIRECTION:
- [Artistic direction 1]
- [Artistic direction 2]
- [Artistic direction 3]
- [Artistic direction 4]
- [Artistic direction 5]

SYMBOLIC MEANINGS TO CONVEY:
- [Symbolic meaning 1]
- [Symbolic meaning 2]
- [Symbolic meaning 3]
- [Symbolic meaning 4]
- [Symbolic meaning 5]

This card represents [summary of card's primary meaning]. The image should evoke [primary emotional/psychological response]."""
                }
            },
            
            "related_cards": {
                "same_card_winter": f"{hexagram_key}00",
                "same_card_spring": f"{hexagram_key}10",
                "same_card_summer": f"{hexagram_key}11",
                "same_card_fall": f"{hexagram_key}01",
                "opposite": "{:08b}".format(decimal_value ^ 0xFF),
                "thematic_pair": "[Related binary]",
                "full_cycle": [f"{hexagram_key}{bits}" for bits in ["11", "01", "00", "10"]]
            },
            
            "bit_values": {
                "bit1": binary_code[0],
                "bit2": binary_code[1],
                "bit3": binary_code[2],
                "bit4": binary_code[3],
                "bit5": binary_code[4],
                "bit6": binary_code[5],
                "bit78": binary_code[6:8]
            },
            
            "fractal_meanings": {
                "quantum": {
                    "pattern": "[Quantum level pattern]",
                    "insight": "[Quantum insight]"
                },
                "biological": {
                    "pattern": "[Biological pattern]",
                    "insight": "[Biological insight]"
                },
                "psychological": {
                    "pattern": "[Psychological pattern]",
                    "insight": "[Psychological insight]"
                },
                "social": {
                    "pattern": "[Social pattern]",
                    "insight": "[Social insight]"
                },
                "ecological": {
                    "pattern": "[Ecological pattern]",
                    "insight": "[Ecological insight]"
                },
                "cosmic": {
                    "pattern": "[Cosmic pattern]",
                    "insight": "[Cosmic insight]"
                }
            }
        }
    }
    
    return card_data

def extract_image_prompt(card_data):
    """Extract just the image generation prompt from a card data structure."""
    return card_data["card"]["interpreted_meanings"]["oracle_card"]["prompt_for_image_gen"]

def save_card_file(binary_code, card_data):
    """Save the card data to a YAML file in the correct directory."""
    # Create directory structure
    hexagram = binary_code[0:6]
    directory = os.path.join(OUTPUT_DIR, hexagram)
    os.makedirs(directory, exist_ok=True)
    
    # Save YAML file
    file_path = os.path.join(directory, f"{binary_code}.yml")
    with open(file_path, 'w') as file:
        yaml.dump(card_data, file, default_flow_style=False, sort_keys=False)
    
    return file_path

def save_image_prompt(binary_code, prompt):
    """Save the image generation prompt to a text file."""
    # Create directory structure
    hexagram = binary_code[0:6]
    directory = os.path.join(OUTPUT_DIR, hexagram)
    os.makedirs(directory, exist_ok=True)
    
    # Save prompt file
    file_path = os.path.join(directory, f"{binary_code}_image_prompt.txt")
    with open(file_path, 'w') as file:
        file.write(prompt)
    
    return file_path

def main():
    """Main function to generate a card based on command line arguments."""
    if len(sys.argv) != 2:
        print("Usage: python card-generator.py <binary_code>")
        sys.exit(1)
    
    binary_code = sys.argv[1]
    
    print(f"Generating card for binary code: {binary_code}")
    
    # Generate card data
    card_data = generate_card(binary_code)
    if not card_data:
        sys.exit(1)
    
    # Save card file
    card_file = save_card_file(binary_code, card_data)
    print(f"Card YAML file saved to: {card_file}")
    
    # Extract and save image prompt
    prompt = extract_image_prompt(card_data)
    prompt_file = save_image_prompt(binary_code, prompt)
    print(f"Image prompt saved to: {prompt_file}")
    
    # Print the prompt for easy copying
    print("\n=== IMAGE GENERATION PROMPT ===\n")
    print(prompt)
    print("\n==============================\n")
    
    print("Done!")

if __name__ == "__main__":
    main()