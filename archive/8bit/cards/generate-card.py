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
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
CORE_SYSTEMS_PATH = os.path.join(PROJECT_DIR, 'associations', 'core-systems.yml')
COMPOSITE_ASSOCIATIONS_PATH = os.path.join(PROJECT_DIR, 'associations', 'composite-associations.yml')
LUNAR_CYCLE_PATH = os.path.join(PROJECT_DIR, 'associations', 'lunar-cycle.yml')
ARCHETYPE_GUIDE_PATH = os.path.join(PROJECT_DIR, 'associations', 'archetype-guide.md')
QUICK_REFERENCE_PATH = os.path.join(PROJECT_DIR, 'associations', 'quick-reference-guide.md')
BINARY_SORT_PATH = os.path.join(PROJECT_DIR, 'sorts', 'binary_sort.md')
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, 'card-template.yml')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'generated')

def load_yaml_file(file_path):
    """Load a YAML file and return its contents."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def load_markdown_file(file_path):
    """Load a markdown file and return its contents as a string."""
    with open(file_path, 'r') as file:
        return file.read()

def parse_binary_sort_table(content):
    """
    Parse the binary sort table from the markdown content.
    Returns a dictionary mapping binary codes to their lunar information.
    """
    # Find the table in the content
    table_start = content.find('| Binary')
    table_end = content.find('|---', table_start + 1000)  # Look far enough ahead
    if table_start == -1 or table_end == -1:
        return {}
    
    # Extract table rows
    lines = content[table_start:table_end].strip().split('\n')
    header = lines[0]
    separator = lines[1]
    rows = lines[2:]
    
    # Create a dictionary mapping binary codes to their lunar information
    binary_sort_data = {}
    for row in rows:
        if '|' not in row:
            continue
        cells = [cell.strip() for cell in row.split('|')]
        if len(cells) < 7:
            continue
        
        binary = cells[1].strip()
        decimal = cells[2].strip()
        season = cells[3].strip()
        lunar_cycle = cells[4].strip()
        lunar_phase = cells[5].strip()
        phase_half = cells[6].strip()
        
        binary_sort_data[binary] = {
            'decimal': decimal,
            'season': season,
            'lunar_cycle': lunar_cycle,
            'lunar_phase': lunar_phase,
            'phase_half': phase_half
        }
    
    return binary_sort_data

def parse_archetype_guide(content):
    """
    Parse the archetype guide data from the markdown content.
    Returns a dictionary with archetype information.
    """
    # Look for the Lookup table at the end of the archetype guide
    lookup_start = content.find('## Lookup')
    if lookup_start == -1:
        return {}
    
    table_start = content.find('| Binary', lookup_start)
    if table_start == -1:
        return {}
    
    # Extract table rows
    lines = content[table_start:].split('\n')
    header = lines[0]
    separator = lines[1]
    rows = lines[2:]
    
    # Create a dictionary mapping binary codes to their archetype information
    archetype_data = {}
    for row in rows:
        if not row.strip() or '|' not in row:
            continue
        
        cells = [cell.strip() for cell in row.split('|')]
        if len(cells) < 6:
            continue
        
        binary = cells[1].strip()
        decimal = cells[2].strip()
        season = cells[3].strip()
        resonant_season = cells[4].strip()
        archetype = cells[5].strip()
        
        archetype_data[binary] = {
            'decimal': decimal,
            'season': season,
            'resonant_season': resonant_season,
            'archetype': archetype
        }
    
    # Parse the inner/outer world rules
    inner_outer_rules = {}
    inner_active_section = content.find('The inner world is considered:')
    if inner_active_section != -1:
        inner_active_line = content[inner_active_section:inner_active_section + 200].split('\n')[1]
        inner_inactive_line = content[inner_active_section:inner_active_section + 200].split('\n')[2]
        inner_outer_rules['inner_active'] = 'two or more' in inner_active_line
    
    outer_active_section = content.find('The outer world is considered:')
    if outer_active_section != -1:
        outer_active_line = content[outer_active_section:outer_active_section + 200].split('\n')[1]
        outer_inactive_line = content[outer_active_section:outer_active_section + 200].split('\n')[2]
        inner_outer_rules['outer_active'] = 'two or more' in outer_active_line
    
    # Extract the archetype mapping table
    archetype_mapping = {}
    relation_section = content.find('| Relationship')
    if relation_section != -1:
        relation_table_lines = content[relation_section:relation_section + 500].split('\n')
        for i in range(2, min(6, len(relation_table_lines))):  # 4 archetypes
            if '|' in relation_table_lines[i]:
                cells = [cell.strip() for cell in relation_table_lines[i].split('|')]
                if len(cells) >= 5:
                    relation = cells[1].strip()
                    archetype = cells[2].strip()
                    color = cells[3].strip()
                    archetype_mapping[relation] = {
                        'archetype': archetype,
                        'color': color
                    }
    
    return {
        'archetype_data': archetype_data,
        'inner_outer_rules': inner_outer_rules,
        'archetype_mapping': archetype_mapping
    }

def parse_quick_reference_guide(content):
    """
    Parse the gender assignment rules and inner/outer world symbols from the quick reference guide.
    Returns dictionaries with extracted information.
    """
    result = {
        'gender_rules': {},
        'inner_world_symbols': {},
        'outer_world_symbols': {}
    }
    
    # Find the gender assignment section
    gender_section = content.find('## Gender')
    if gender_section != -1:
        # Extract the gender table
        table_start = content.find('| Number of "1" Bits', gender_section)
        if table_start != -1:
            lines = content[table_start:table_start + 500].split('\n')
            for line in lines[2:5]:  # Only looking at the three rules (0/6, 2/4, 3/5)
                if '|' not in line:
                    continue
                
                cells = [cell.strip() for cell in line.split('|')]
                if len(cells) < 3:
                    continue
                
                bit_count = cells[1].strip()
                gender_info = cells[2].strip()
                
                # Parse the bit count
                if '0 or 6' in bit_count:
                    key = 'neutral'
                    result['gender_rules'][0] = {'all': 'neutral'}
                    result['gender_rules'][6] = {'all': 'neutral'}
                elif '2 or 4' in bit_count:
                    result['gender_rules'][2] = {'hero_monster': 'masculine', 'fool_sage': 'feminine'}
                    result['gender_rules'][4] = {'hero_monster': 'masculine', 'fool_sage': 'feminine'}
                elif '3 or 5' in bit_count:
                    result['gender_rules'][3] = {'hero_monster': 'feminine', 'fool_sage': 'masculine'}
                    result['gender_rules'][5] = {'hero_monster': 'feminine', 'fool_sage': 'masculine'}
    
    # Find the Inner World section
    inner_world_section = content.find('### Inner World (Bits 1-3)')
    if inner_world_section != -1:
        table_start = content.find('| Pattern |', inner_world_section)
        if table_start != -1:
            # Skip header and separator lines
            table_content_start = content.find('\n', table_start)
            table_content_start = content.find('\n', table_content_start + 1)
            
            # Find the end of the table
            table_end = content.find('\n\n', table_content_start)
            if table_end == -1:  # If not found, look for next section
                table_end = content.find('###', table_content_start)
            
            if table_end != -1:
                lines = content[table_content_start:table_end].strip().split('\n')
                for line in lines:
                    if '|' not in line:
                        continue
                    
                    cells = [cell.strip() for cell in line.split('|')]
                    if len(cells) < 5:  # Pattern, Color, Trigram, Name, Description
                        continue
                    
                    pattern = cells[1].strip()
                    name = cells[4].strip() if len(cells) > 4 else ""
                    
                    if pattern and name:
                        result['inner_world_symbols'][pattern] = name
    
    # Find the Outer World section
    outer_world_section = content.find('### Outer World (Bits 4-6)')
    if outer_world_section != -1:
        table_start = content.find('| Pattern |', outer_world_section)
        if table_start != -1:
            # Skip header and separator lines
            table_content_start = content.find('\n', table_start)
            table_content_start = content.find('\n', table_content_start + 1)
            
            # Find the end of the table
            table_end = content.find('\n\n', table_content_start)
            if table_end == -1:  # If not found, look for next section
                table_end = content.find('##', table_content_start)
            
            if table_end != -1:
                lines = content[table_content_start:table_end].strip().split('\n')
                for line in lines:
                    if '|' not in line:
                        continue
                    
                    cells = [cell.strip() for cell in line.split('|')]
                    if len(cells) < 5:  # Pattern, Color, Trigram, Name, Description
                        continue
                    
                    pattern = cells[1].strip()
                    name = cells[4].strip() if len(cells) > 4 else ""
                    
                    if pattern and name:
                        result['outer_world_symbols'][pattern] = name
    
    return result

def validate_with_binary_sort(binary_code, lunar_info, binary_sort_data):
    """
    Validate that the calculated lunar information matches what's in the binary sort table.
    """
    if binary_code not in binary_sort_data:
        print(f"Warning: Binary code {binary_code} not found in binary_sort.md")
        return False
    
    # Get the expected values from binary_sort.md
    expected = binary_sort_data[binary_code]
    
    # Extract lunar phase number and name from the lunar_phase string (e.g., "0: Dark Moon")
    expected_phase_num = int(expected['lunar_phase'].split(':')[0].strip())
    expected_phase_name = expected['lunar_phase'].split(':')[1].strip()
    
    # Compare with what we calculated
    lunar_phase_num = (lunar_info.get('decimal_value', 0) // 2) % 8
    lunar_phase = lunar_info.get('phase', '')
    lunar_cycle = str(lunar_info.get('lunar_cycle', ''))
    
    # Determine phase half based on the half_name (more accurate than phase_half)
    phase_half = 'Early' if lunar_info.get('half_name', '').startswith(('Dark Moon (Early)', 'New Moon (Early)', 
                                                          'First Quarter (Early)', 'Waxing Gibbous (Early)',
                                                          'Full Moon (Early)', 'Waning Gibbous (Early)',
                                                          'Last Quarter (Early)', 'Balsamic Moon (Early)')) else 'Late'
    
    # Check for mismatches
    mismatches = []
    if expected_phase_num != lunar_phase_num:
        mismatches.append(f"Lunar phase number: Expected {expected_phase_num}, got {lunar_phase_num}")
    if expected_phase_name != lunar_phase:
        mismatches.append(f"Lunar phase name: Expected '{expected_phase_name}', got '{lunar_phase}'")
    if expected['lunar_cycle'] != lunar_cycle:
        mismatches.append(f"Lunar cycle: Expected {expected['lunar_cycle']}, got {lunar_cycle}")
    if expected['phase_half'] != phase_half:
        mismatches.append(f"Phase half: Expected {expected['phase_half']}, got {phase_half}")
    
    if mismatches:
        print("\nWarning: Lunar information doesn't match binary_sort.md:")
        for mismatch in mismatches:
            print(f"  - {mismatch}")
        return False
    
    return True

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

def calculate_lunar_phase(decimal_value, lunar_cycle_data, bit_count_1_6):
    """
    Calculate lunar phase information based on decimal value.
    
    This follows the lunar cycle calculation from lunar-cycle.yml:
    - lunar_phase: "(l->r decimal_value ÷ 2) % 8" - Yields phase 0-7
    - phase_half: "l->r decimal_value % 2" - 0 = Early, 1 = Late
    - lunar_cycle: "((l->r decimal_value % 64) ÷ 16) + 1" - Yields cycle 1-4 within the season
    """
    # Calculate lunar phase (0-7) based on decimal value
    lunar_phase_num = (decimal_value // 2) % 8
    
    # Calculate phase half (0 = Early, 1 = Late)
    phase_half = decimal_value % 2
    
    # Get phase data from lunar cycle system
    phase_data = lunar_cycle_data["lunar_cycle_system"]["phases"][str(lunar_phase_num)]
    phase_name = phase_data["name"]
    
    # Get half name and description
    if phase_half == 0:
        half_name = phase_data["first_half"]["name"]
        half_desc = phase_data["first_half"]["half_phase_desc"]
    else:
        half_name = phase_data["second_half"]["name"]
        half_desc = phase_data["second_half"]["half_phase_desc"]
    
    # Calculate lunar cycle (1-4) using the correct formula from lunar-cycle.yml
    # ((l->r decimal_value % 64) ÷ 16) + 1
    lunar_cycle_num = ((decimal_value % 64) // 16) + 1
    
    return {
        "phase": phase_name,
        "half_name": half_name,
        "half_desc": half_desc,
        "lunar_cycle": lunar_cycle_num,
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
    
    # Load reference guides
    try:
        archetype_guide = load_markdown_file(ARCHETYPE_GUIDE_PATH)
        quick_reference = load_markdown_file(QUICK_REFERENCE_PATH)
        binary_sort_content = load_markdown_file(BINARY_SORT_PATH)
        binary_sort_data = parse_binary_sort_table(binary_sort_content)
        quick_reference_data = parse_quick_reference_guide(quick_reference)
        print(f"Loaded reference guides: archetype-guide.md, quick-reference-guide.md, binary_sort.md")
    except Exception as e:
        print(f"Warning: Could not load one or more reference files: {e}")
        binary_sort_data = {}
        quick_reference_data = {'gender_rules': {}, 'inner_world_symbols': {}, 'outer_world_symbols': {}}
    
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
    
    # Verify archetype with archetype-guide.md
    inner_active = count_bits(inner_bits) >= 2
    outer_active = count_bits(outer_bits) >= 2
    print(f"Inner world: {'Active' if inner_active else 'Inactive'} (bits: {inner_bits})")
    print(f"Outer world: {'Active' if outer_active else 'Inactive'} (bits: {outer_bits})")
    print(f"Resonant season: {resonant_season_name}")
    print(f"Actual season: {season}")
    print(f"Archetype: {archetype}")
    
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
    print(f"Gender: {gender} (based on {bit_count_1_6} bits set to 1 in positions 1-6)")
    
    # Get inner and outer world data
    inner_trigram_data = get_trigram_data(inner_bits, core_systems)
    outer_trigram_data = get_trigram_data(outer_bits, core_systems)
    
    inner_world_meaning = get_inner_outer_world_data(inner_bits, composite_associations, "inner_world")
    outer_world_meaning = get_inner_outer_world_data(outer_bits, composite_associations, "outer_world")
    
    # Get inner and outer world symbols from quick reference guide
    inner_world_symbol = quick_reference_data['inner_world_symbols'].get(inner_bits, "Unknown Animal")
    outer_world_symbol = quick_reference_data['outer_world_symbols'].get(outer_bits, "Unknown Environment")
    print(f"Inner world symbol: {inner_world_symbol} (bits: {inner_bits})")
    print(f"Outer world symbol: {outer_world_symbol} (bits: {outer_bits})")
    
    # Get hexagram data
    hexagram = binary_code[0:6]
    hexagram_data = get_hexagram_data(hexagram, core_systems)
    
    # Calculate lunar cycle and phase information
    lunar_info = calculate_lunar_phase(decimal, lunar_cycle_data, bit_count_1_6)
    cycle_number = lunar_info["lunar_cycle"]
    cycle_names = {
        1: "Inception Cycle",
        2: "Development Cycle",
        3: "Culmination Cycle",
        4: "Transition Cycle"
    }
    cycle_name = cycle_names.get(cycle_number, "")
    
    # Validate against binary_sort.md
    if binary_sort_data:
        lunar_info_for_validation = {
            'decimal_value': decimal,
            'phase': lunar_info['phase'],
            'phase_half': lunar_info['half_desc'],
            'lunar_cycle': lunar_info['lunar_cycle']
        }
        validate_with_binary_sort(binary_code, lunar_info_for_validation, binary_sort_data)
    
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
                    "symbol": inner_world_symbol,
                    "meaning": inner_world_meaning.get("desc", "[Inner world meaning]")
                },
                
                # Outer World
                "outer_world": {
                    "color": outer_trigram_data["color"],
                    "trigram": outer_trigram_data["trigram"],
                    "symbol": outer_world_symbol,
                    "meaning": outer_world_meaning.get("desc", "[Outer world meaning]")
                },
                
                # Solar Season
                "solar_cycle": {
                    "season": season,
                    "tarot_suit": {"Winter": "Swords", "Spring": "Wands", "Summer": "Cups", "Fall": "Pentacles"}.get(season, ""),
                    "element": {"Winter": "Air", "Spring": "Fire", "Summer": "Water", "Fall": "Earth"}.get(season, "")
                },
                
                # Lunar cycle - added half_name for validation
                "lunar_cycle": {
                    "decimal_modulo": lunar_info["decimal_modulo"],
                    "phase": lunar_info["phase"],
                    "phase_half": lunar_info["half_desc"],
                    "half_name": lunar_info["half_name"],
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
                    "card_scene": f"[Detailed description of the card's imagery, incorporating {inner_world_symbol} (inner world symbol) and {outer_world_symbol} (outer world symbol), along with all symbolic elements, colors, and archetype]",
                    "universal_symbol": "[Core symbol that captures the essence of this card]",
                    "mood": "[Emotional/energetic quality of the card]",
                    
                    # Image generation prompt
                    "prompt_for_image_gen": f"""Limited color risograph-style illustration of [short scene description].
Use {inner_trigram_data['color']} for foreground elements (inner world: {inner_world_symbol}) and {outer_trigram_data['color']} for background/environment (outer world: {outer_world_symbol}), with {archetype_color} highlights.
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

def load_reference_files():
    """Load reference files and return their contents for validation."""
    reference_files = {}
    
    # Define reference file paths
    reference_paths = {
        'archetype_guide': ARCHETYPE_GUIDE_PATH,
        'quick_reference': QUICK_REFERENCE_PATH,
        'binary_sort': BINARY_SORT_PATH
    }
    
    # Try to load each reference file
    for name, path in reference_paths.items():
        try:
            content = load_markdown_file(path)
            reference_files[name] = content
            print(f"Loaded {os.path.basename(path)}")
        except Exception as e:
            print(f"Warning: Could not load {os.path.basename(path)}: {e}")
    
    # Parse binary sort table if available
    if 'binary_sort' in reference_files:
        binary_sort_data = parse_binary_sort_table(reference_files['binary_sort'])
        reference_files['binary_sort_data'] = binary_sort_data
        print(f"Parsed lunar information for {len(binary_sort_data)} cards from binary_sort.md")
    
    # Parse archetype guide if available
    if 'archetype_guide' in reference_files:
        archetype_guide_data = parse_archetype_guide(reference_files['archetype_guide'])
        reference_files['archetype_guide_data'] = archetype_guide_data
        if 'archetype_data' in archetype_guide_data:
            print(f"Parsed archetype information for {len(archetype_guide_data['archetype_data'])} cards from archetype-guide.md")
    
    # Parse quick reference guide if available
    if 'quick_reference' in reference_files:
        gender_rules = parse_quick_reference_guide(reference_files['quick_reference'])
        reference_files['gender_rules'] = gender_rules
        print(f"Parsed gender assignment rules from quick-reference-guide.md")
    
    return reference_files

def validate_archetype(binary_code, archetype, reference_files):
    """Validate the archetype against the archetype guide reference."""
    if 'archetype_guide' not in reference_files:
        print("Warning: archetype_guide not available for validation")
        return
    
    # If we have parsed archetype data
    if 'archetype_guide_data' in reference_files:
        archetype_data = reference_files['archetype_guide_data']['archetype_data']
        
        if binary_code in archetype_data:
            expected_archetype = archetype_data[binary_code]['archetype']
            expected_resonant_season = archetype_data[binary_code]['resonant_season']
            
            print("\nArchetype Validation:")
            print(f"  - Expected Archetype: {expected_archetype}")
            print(f"  - Calculated Archetype: {archetype}")
            print(f"  - Expected Resonant Season: {expected_resonant_season}")
            
            if expected_archetype != archetype:
                print(f"  - WARNING: Archetype mismatch! Expected {expected_archetype}, got {archetype}")
                return False
            
            return True
    
    return None  # Couldn't validate

def validate_gender(binary_code, archetype, gender, reference_files):
    """Validate the gender assignment against the quick reference guide."""
    if 'quick_reference' not in reference_files:
        print("Warning: quick_reference not available for validation")
        return
    
    # If we have parsed gender rules
    if 'gender_rules' in reference_files:
        gender_rules = reference_files['gender_rules']
        bit_count_1_6 = count_bits(binary_code[0:6])
        
        print("\nGender Validation:")
        print(f"  - Bit Count (positions 1-6): {bit_count_1_6}")
        print(f"  - Assigned Gender: {gender}")
        
        if bit_count_1_6 in gender_rules:
            rule = gender_rules[bit_count_1_6]
            
            if 'all' in rule:
                expected_gender = rule['all']
                print(f"  - Expected Gender: {expected_gender} (all archetypes)")
            else:
                if archetype in ["Hero", "Monster"]:
                    expected_gender = rule['hero_monster']
                    print(f"  - Expected Gender: {expected_gender} (Hero/Monster)")
                else:  # Fool or Sage
                    expected_gender = rule['fool_sage']
                    print(f"  - Expected Gender: {expected_gender} (Fool/Sage)")
            
            if expected_gender != gender:
                print(f"  - WARNING: Gender mismatch! Expected {expected_gender}, got {gender}")
                return False
            
            return True
    
    return None  # Couldn't validate

def validate_lunar_info(binary_code, lunar_info, reference_files):
    """Validate lunar cycle information against binary_sort.md."""
    if 'binary_sort_data' not in reference_files:
        print("Warning: binary_sort_data not available for validation")
        return False
    
    binary_sort_data = reference_files['binary_sort_data']
    if binary_code not in binary_sort_data:
        print(f"Warning: Binary code {binary_code} not found in binary_sort.md")
        return False
    
    # Print all available keys in lunar_info for debugging
    print("\nDebug: Lunar Info Dictionary Keys:")
    for key in sorted(lunar_info.keys()):
        print(f"  - {key}: {lunar_info[key]}")
    
    # Check for required keys with fallbacks
    lunar_phase = lunar_info.get('phase', 'Missing')
    lunar_half_name = lunar_info.get('half_name', lunar_info.get('phase_half', 'Missing'))
    lunar_cycle = lunar_info.get('cycle_number', lunar_info.get('cycle_name', 'Missing'))
    
    # Get the expected values from binary_sort.md
    expected = binary_sort_data[binary_code]
    
    # Extract lunar phase number and name from the lunar_phase string (e.g., "0: Dark Moon")
    expected_phase_num = int(expected['lunar_phase'].split(':')[0].strip())
    expected_phase_name = expected['lunar_phase'].split(':')[1].strip()
    
    # Determine phase half based on what's available
    # This is specifically for the 'half_desc' field in lunar_info
    early_half_descs = ['Deepening', 'Birthing', 'Challenging', 'Building', 'Illuminating', 'Sharing', 'Releasing', 'Distilling']
    
    if lunar_half_name != 'Missing':
        if isinstance(lunar_half_name, str) and ('Early' in lunar_half_name):
            phase_half = 'Early'
        else:
            # Check half_desc for early phases
            half_desc = lunar_info.get('phase_half', '')
            if half_desc in early_half_descs:
                phase_half = 'Early'
            else:
                phase_half = 'Late'
    else:
        # Check decimal modulo as the most reliable way - if even, it's Early, if odd, it's Late
        decimal_modulo = lunar_info.get('decimal_modulo', '')
        if isinstance(decimal_modulo, str) and '% 2 = 0' in decimal_modulo:
            phase_half = 'Early'
        else:
            phase_half = 'Late'
    
    # Print comparison information
    print("\nLunar Cycle Validation:")
    print(f"  - Expected Lunar Phase: {expected_phase_num}: {expected_phase_name}")
    print(f"  - Calculated Lunar Phase: {lunar_phase}")
    print(f"  - Expected Phase Half: {expected['phase_half']}")
    print(f"  - Calculated Phase Half: {phase_half}")
    print(f"  - Expected Lunar Cycle: {expected['lunar_cycle']}")
    print(f"  - Calculated Lunar Cycle: {lunar_cycle}")
    
    # Check for mismatches
    mismatches = []
    if expected_phase_name != lunar_phase:
        mismatches.append(f"Lunar phase name: Expected '{expected_phase_name}', got '{lunar_phase}'")
    if expected['phase_half'] != phase_half:
        mismatches.append(f"Phase half: Expected {expected['phase_half']}, got {phase_half}")
    
    # Special handling for lunar cycle comparison
    if lunar_cycle != 'Missing':
        try:
            # Try to convert lunar_cycle to string for comparison if it's a number
            if str(lunar_cycle) != expected['lunar_cycle']:
                mismatches.append(f"Lunar cycle: Expected {expected['lunar_cycle']}, got {lunar_cycle}")
        except:
            mismatches.append(f"Lunar cycle: Expected {expected['lunar_cycle']}, type mismatch with {lunar_cycle}")
    else:
        mismatches.append("Lunar cycle: Missing from calculated values")
    
    if mismatches:
        print("\n  WARNING: Lunar information doesn't match binary_sort.md:")
        for mismatch in mismatches:
            print(f"    - {mismatch}")
        return False
    
    return True

def main():
    """Main function to create a card from a binary code."""
    parser = argparse.ArgumentParser(description='Generate an 8-Bit Oracle card from a binary code.')
    parser.add_argument('binary_code', help='8-bit binary code (e.g., 10101010)')
    args = parser.parse_args()
    
    try:
        binary_code = args.binary_code
        
        # Load reference files
        print("\nLoading reference files for validation...")
        reference_files = load_reference_files()
        
        # Generate the card
        print("\nGenerating card...")
        card_data = generate_card(binary_code)
        
        # Validate lunar information
        lunar_info = card_data['card']['direct_associations']['lunar_cycle']
        lunar_valid = validate_lunar_info(binary_code, lunar_info, reference_files)
        
        # Validate archetype
        archetype = card_data['card']['direct_associations']['archetype']
        inner_bits = binary_code[0:3]
        outer_bits = binary_code[3:6]
        
        # Print inner and outer world info
        inner_active = count_bits(inner_bits) >= 2
        outer_active = count_bits(outer_bits) >= 2
        
        print("\nComponent Analysis:")
        print(f"  - Inner World: {'Active' if inner_active else 'Inactive'} (bits: {inner_bits}, {count_bits(inner_bits)}/3 bits set)")
        print(f"  - Outer World: {'Active' if outer_active else 'Inactive'} (bits: {outer_bits}, {count_bits(outer_bits)}/3 bits set)")
        print(f"  - Season: {card_data['card']['direct_associations']['solar_cycle']['season']} (bits: {binary_code[6:8]})")
        
        # Validate archetype against reference
        archetype_valid = validate_archetype(binary_code, archetype, reference_files)
        
        # Validate gender
        gender = card_data['card']['direct_associations']['gender']
        gender_valid = validate_gender(binary_code, archetype, gender, reference_files)
        
        # Save the card to a file
        output_path = save_card_file(binary_code, card_data)
        
        # Summary of validation results
        print("\nValidation Summary:")
        print(f"  - Lunar Info: {'✅ Valid' if lunar_valid else '❌ Has issues'}")
        print(f"  - Archetype: {'✅ Valid' if archetype_valid else '❌ Has issues' if archetype_valid is not None else '⚠️ Not validated'}")
        print(f"  - Gender: {'✅ Valid' if gender_valid else '❌ Has issues' if gender_valid is not None else '⚠️ Not validated'}")
        
        # Output
        print(f"\nCard for {binary_code} generated and saved to: {output_path}")
        print("\nNext steps:")
        print("1. Open the file and fill in the placeholder fields with meaningful content")
        print("2. Add keywords, symbols, and other specific details")
        print("3. Craft a compelling card description")
        print("4. Develop the imagery concept for the card")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()