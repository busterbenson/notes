#!/usr/bin/env python3
"""
8-Bit Oracle Associations Generator

This script generates "raw" association files for all four cards in a given
6-bit pattern (hexagram), pulling all relevant associations from the reference files.

Usage:
    python association-generator.py <6-bit_code>
    
Example:
    python association-generator.py 000000
"""

import sys
import os
import yaml
import re

# Configuration
CORE_SYSTEMS_PATH = '../associations/core-systems.yml'
COMPOSITE_ASSOCIATIONS_PATH = '../associations/composite-associations.yml'
LUNAR_CYCLE_PATH = '../associations/lunar-cycle.yml'
OUTPUT_DIR = 'compiled'

def load_yaml_file(file_path):
    """Load a YAML file and return its contents."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def matches_bit_mask(binary_code, bit_mask):
    """Check if a binary code matches a given bit mask pattern."""
    if len(binary_code) != len(bit_mask):
        return False
    
    for i in range(len(binary_code)):
        if bit_mask[i] not in ['X', '?'] and bit_mask[i] != binary_code[i]:
            return False
    return True

def count_bits(binary_str):
    """Count the number of '1's in a binary string."""
    return binary_str.count('1')

def convert_to_left_right_decimal(binary_code):
    """Convert binary code to decimal using left-to-right bit significance.
    
    The leftmost bit (bit 1) has value 1, the next bit (bit 2) has value 2,
    the next bit (bit 3) has value 4, and so on.
    """
    values = [1, 2, 4, 8, 16, 32, 64, 128]  # Power of 2 values for each bit position
    decimal = 0
    
    for i, bit in enumerate(binary_code):
        if bit == "1":
            decimal += values[i]
    
    return decimal

def get_associations_for_code(binary_code, core_systems, composite_associations, lunar_cycle):
    """Get all associations that apply to the given binary code."""
    # Calculate left-to-right decimal value
    lr_decimal = convert_to_left_right_decimal(binary_code)
    
    associations = {
        "binary_code": binary_code,
        "decimal_value": int(binary_code, 2),  # Standard right-to-left binary conversion
        "lr_decimal_value": lr_decimal,  # Left-to-right binary conversion
        "hexadecimal_value": hex(int(binary_code, 2))[2:].upper(),
        "bit_values": {
            "bit1": binary_code[0],
            "bit2": binary_code[1],
            "bit3": binary_code[2],
            "bit4": binary_code[3],
            "bit5": binary_code[4],
            "bit6": binary_code[5],
            "bit7": binary_code[6],
            "bit8": binary_code[7],
            "bit78": binary_code[6:8]
        },
        "bit_associations": {}
    }
    
    # Add bit definitions for each individual bit
    for i in range(1, 9):
        bit_key = f"bit{i}"
        if i <= 6:
            bit_def = core_systems["core_associations"]["bit_definitions"].get(bit_key)
            if bit_def:
                bit_value = binary_code[i-1]
                meaning = None
                
                # Get the meaning for the bit value - need to convert to int because YAML loads the keys as integers
                if bit_def.get("meanings"):
                    meaning = bit_def.get("meanings").get(int(bit_value))
                
                associations["bit_associations"][bit_key] = {
                    "position": bit_def.get("position"),
                    "name": bit_def.get("name"),
                    "domain": bit_def.get("domain"),
                    "question": bit_def.get("question"),
                    "value": bit_value,
                    "meaning": meaning
                }
    
    # Add bit78 cycle phase information
    bit78 = binary_code[6:8]
    bit78_info = core_systems["core_associations"]["bit_definitions"].get("bit78", {}).get("meanings", {}).get(bit78, {})
    associations["bit_associations"]["bit78"] = {
        "position": "7-8",
        "name": "Cycle Phase",
        "season": bit78_info.get("season"),
        "tarot_suit": bit78_info.get("tarot_suit"),
        "element": bit78_info.get("element")
    }
    
    # Get inner and outer world states
    bits_1_3 = binary_code[0:3]
    bits_4_6 = binary_code[3:6]
    
    # Add inner and outer world associations
    associations["inner_world"] = {
        "bits": bits_1_3,
        "color": core_systems["core_associations"]["rgb_colors"].get(bits_1_3, {}).get("name"),
        "trigram": core_systems["core_associations"]["i_ching_trigrams"].get(bits_1_3, {}).get("traditional_name"),
        "trigram_symbol": core_systems["core_associations"]["i_ching_trigrams"].get(bits_1_3, {}).get("trigram_symbol"),
        "8bit_trigram_name": core_systems["core_associations"]["i_ching_trigrams"].get(bits_1_3, {}).get("8bit_trigram_name"),
        "qualities": core_systems["core_associations"]["i_ching_trigrams"].get(bits_1_3, {}).get("qualities"),
        "rgb": core_systems["core_associations"]["rgb_colors"].get(bits_1_3, {}).get("rgb")
    }
    
    associations["outer_world"] = {
        "bits": bits_4_6,
        "color": core_systems["core_associations"]["rgb_colors"].get(bits_4_6, {}).get("name"),
        "trigram": core_systems["core_associations"]["i_ching_trigrams"].get(bits_4_6, {}).get("traditional_name"),
        "trigram_symbol": core_systems["core_associations"]["i_ching_trigrams"].get(bits_4_6, {}).get("trigram_symbol"),
        "8bit_trigram_name": core_systems["core_associations"]["i_ching_trigrams"].get(bits_4_6, {}).get("8bit_trigram_name"),
        "qualities": core_systems["core_associations"]["i_ching_trigrams"].get(bits_4_6, {}).get("qualities"),
        "rgb": core_systems["core_associations"]["rgb_colors"].get(bits_4_6, {}).get("rgb")
    }
    
    # Determine the inner and outer world states (active or inactive)
    inner_active = count_bits(bits_1_3) >= 2
    outer_active = count_bits(bits_4_6) >= 2
    
    inner_state = "inner1" if inner_active else "inner0"
    outer_state = "outer1" if outer_active else "outer0"
    
    associations["inner_world"]["state"] = inner_state
    associations["outer_world"]["state"] = outer_state
    
    # Process composite associations
    if "composite_associations" in composite_associations:
        associations["composite_frameworks"] = {}
        
        # Get inner and outer world data from composite associations
        inner_outer_frameworks = composite_associations["composite_associations"].get("inner_and_outer_worlds", {})
        
        # Process inner world
        inner_world_component = inner_outer_frameworks.get("inner_world", {})
        if inner_world_component and "meanings" in inner_world_component:
            inner_world_meaning = inner_world_component["meanings"].get(bits_1_3, {})
            if inner_world_meaning:
                associations["inner_world"].update({
                    "name": inner_world_meaning.get("name"),
                    "desc": inner_world_meaning.get("desc")
                })
        
        # Process outer world
        outer_world_component = inner_outer_frameworks.get("outer_world", {})
        if outer_world_component and "meanings" in outer_world_component:
            outer_world_meaning = outer_world_component["meanings"].get(bits_4_6, {})
            if outer_world_meaning:
                associations["outer_world"].update({
                    "name": outer_world_meaning.get("name"),
                    "desc": outer_world_meaning.get("desc")
                })
        
        # Process all composite frameworks
        for category, frameworks in composite_associations["composite_associations"].items():
            associations["composite_frameworks"][category] = {}
            
            # Special handling for inner_and_outer_worlds to ensure both components are populated
            if category == "inner_and_outer_worlds":
                inner_world_component = frameworks.get("inner_world", {})
                if inner_world_component and "meanings" in inner_world_component:
                    inner_world_meaning = inner_world_component["meanings"].get(bits_1_3, {})
                    if inner_world_meaning:
                        associations["composite_frameworks"][category]["inner_world"] = {
                            "bits": inner_world_component.get("bits"),
                            "bit_pattern": bits_1_3,
                            "description": inner_world_component.get("description")
                        }
                        # Add all properties from the meaning
                        for key, value in inner_world_meaning.items():
                            associations["composite_frameworks"][category]["inner_world"][key] = value
                
                outer_world_component = frameworks.get("outer_world", {})
                if outer_world_component and "meanings" in outer_world_component:
                    outer_world_meaning = outer_world_component["meanings"].get(bits_4_6, {})
                    if outer_world_meaning:
                        associations["composite_frameworks"][category]["outer_world"] = {
                            "bits": outer_world_component.get("bits"),
                            "bit_pattern": bits_4_6,
                            "description": outer_world_component.get("description")
                        }
                        # Add all properties from the meaning
                        for key, value in outer_world_meaning.items():
                            associations["composite_frameworks"][category]["outer_world"][key] = value
            
            for component_name, component_data in frameworks.items():
                # Skip inner_world and outer_world for inner_and_outer_worlds category as we've handled them specially
                if category == "inner_and_outer_worlds" and component_name in ["inner_world", "outer_world"]:
                    continue
                    
                bit_mask = component_data.get("bit_mask")
                
                if bit_mask:
                    # For each component, check each possible meaning pattern
                    for pattern, meaning_data in component_data.get("meanings", {}).items():
                        # Create an actual mask by replacing bit positions with actual values
                        # This is complex because we need to translate between the bit_mask (which uses X, ?) 
                        # and the actual bit pattern in the binary code
                        
                        # Check if we can directly use the pattern
                        # For example, if bit_mask is "???XXXXX" and pattern is "000",
                        # we need to check if binary_code[0:3] == "000"
                        
                        matches = False
                        
                        if bit_mask.startswith("???"):
                            # Inner world bits
                            if pattern == bits_1_3:
                                matches = True
                        elif bit_mask.startswith("XXX???"):
                            # Outer world bits
                            if pattern == bits_4_6:
                                matches = True
                        elif bit_mask == "?XX?XXXX" and pattern == binary_code[0] + binary_code[3]:
                            # Heart (bits 1 & 4)
                            matches = True
                        elif bit_mask == "X?XX?XXX" and pattern == binary_code[1] + binary_code[4]:
                            # Hands (bits 2 & 5)
                            matches = True
                        elif bit_mask == "XX?XX?XX" and pattern == binary_code[2] + binary_code[5]:
                            # Head (bits 3 & 6)
                            matches = True
                        elif bit_mask == "XXXXXX??":
                            # Cycle bits
                            if pattern == binary_code[6:8]:
                                matches = True
                        
                        if matches:
                            if category not in associations["composite_frameworks"]:
                                associations["composite_frameworks"][category] = {}
                            
                            component_entry = {
                                "bits": component_data.get("bits"),
                                "bit_pattern": pattern,
                                "description": component_data.get("description")
                            }
                            
                            # Add the meaning data
                            if isinstance(meaning_data, dict):
                                for key, value in meaning_data.items():
                                    component_entry[key] = value
                            else:
                                component_entry["meaning"] = meaning_data
                                
                            associations["composite_frameworks"][category][component_name] = component_entry
    
    # Add hexagram information (bits 1-6) with enhanced traditional meanings
    hexagram = binary_code[0:6]
    if hexagram in core_systems["core_associations"]["hexagrams"]:
        i_ching_data = core_systems["core_associations"]["hexagrams"][hexagram].get("i_ching", {})
        gene_key_data = core_systems["core_associations"]["hexagrams"][hexagram].get("gene_key", {})
        
        # Get inner and outer trigrams for enhanced symbolism
        inner_trigram = bits_1_3
        outer_trigram = bits_4_6
        inner_trigram_name = core_systems["core_associations"]["i_ching_trigrams"].get(inner_trigram, {}).get("traditional_name", "")
        outer_trigram_name = core_systems["core_associations"]["i_ching_trigrams"].get(outer_trigram, {}).get("traditional_name", "")
        inner_qualities = core_systems["core_associations"]["i_ching_trigrams"].get(inner_trigram, {}).get("qualities", "")
        outer_qualities = core_systems["core_associations"]["i_ching_trigrams"].get(outer_trigram, {}).get("qualities", "")
        
        # Enhanced I Ching symbolism
        traditional_meaning = i_ching_data.get("description", "")
        number = i_ching_data.get("number", "")
        traditional_name = i_ching_data.get("traditional_name", "")
        label = i_ching_data.get("label", "")
        
        # Enhanced Gene Key journey
        shadow = gene_key_data.get("shadow", "")
        gift = gene_key_data.get("gift", "")
        siddhi = gene_key_data.get("siddhi", "")
        gene_key_description = gene_key_data.get("description", "")
        
        # Create trigram relationship description
        trigram_relationship = f"The {inner_trigram_name} trigram ({inner_qualities}) beneath the {outer_trigram_name} trigram ({outer_qualities})"
        
        # Create natural elements mapping based on trigram combinations
        natural_elements = {
            "Earth-Earth": "Fertile soil, deep foundation, grounding",
            "Earth-Mountain": "Plateau, mesa, stable ground",
            "Earth-Water": "Marsh, swamp, subterranean waters",
            "Earth-Wind": "Plains, fields swept by breeze",
            "Earth-Thunder": "Trembling ground, earthquake",
            "Earth-Fire": "Volcanic landscape, thermal vents",
            "Earth-Lake": "Basin, depression filled with water",
            "Earth-Heaven": "Open land beneath vast sky",
            
            "Mountain-Earth": "Buried peak, mountain roots",
            "Mountain-Mountain": "Mountain range, highlands, retreat",
            "Mountain-Water": "Waterfall, mountain stream",
            "Mountain-Wind": "Windswept peak, mountain pass",
            "Mountain-Thunder": "Storm on the mountain, echo",
            "Mountain-Fire": "Volcanic mountain, beacon",
            "Mountain-Lake": "Mountain lake, high reservoir",
            "Mountain-Heaven": "Summit touching sky, highest point",
            
            "Water-Earth": "Underground river, aquifer",
            "Water-Mountain": "Water wearing down stone, persistence",
            "Water-Water": "Ocean depths, abyss, deep current",
            "Water-Wind": "Rippled surface, sailing vessel",
            "Water-Thunder": "Storm at sea, tidal wave",
            "Water-Fire": "Steam, fog, mist, transformative water",
            "Water-Lake": "Connected waters, inlet and outlet",
            "Water-Heaven": "Reflecting pool, mirror of sky",
            
            "Wind-Earth": "Dust storm, erosion, reshaping",
            "Wind-Mountain": "Wind carved formations, weathering",
            "Wind-Water": "Waves, movement across surface",
            "Wind-Wind": "Whirlwind, powerful air currents",
            "Wind-Thunder": "Approaching storm, changing pressure",
            "Wind-Fire": "Fanned flames, spreading fire",
            "Wind-Lake": "Gentle breeze across water",
            "Wind-Heaven": "Clear air, vast atmosphere",
            
            "Thunder-Earth": "Lightning striking ground, awakening",
            "Thunder-Mountain": "Lightning on peak, sudden illumination",
            "Thunder-Water": "Storm at sea, churning waters",
            "Thunder-Wind": "Thunderstorm moving across land",
            "Thunder-Thunder": "Continuous rolling thunder, awakening",
            "Thunder-Fire": "Lightning fire, sudden ignition",
            "Thunder-Lake": "Storm over water, dramatic reflection",
            "Thunder-Heaven": "Lightning connecting earth and sky",
            
            "Fire-Earth": "Molten core, inner heat",
            "Fire-Mountain": "Volcano, eruption, breakthrough",
            "Fire-Water": "Boiling water, transformation",
            "Fire-Wind": "Wildfire, rapidly spreading flame",
            "Fire-Thunder": "Fire and lightning, dual forces",
            "Fire-Fire": "Intense blaze, purification",
            "Fire-Lake": "Fire reflected in water, duality",
            "Fire-Heaven": "Sun, stars, celestial fire",
            
            "Lake-Earth": "Oasis, fertile depression",
            "Lake-Mountain": "Mountain lake, contained joy",
            "Lake-Water": "Connected waterways, flowing joy",
            "Lake-Wind": "Rippled lake surface, shared pleasure",
            "Lake-Thunder": "Disturbed waters, interrupted joy",
            "Lake-Fire": "Steam rising, transforming water",
            "Lake-Lake": "Linked pools, connected joy",
            "Lake-Heaven": "Open water reflecting sky",
            
            "Heaven-Earth": "Complete universe, totality",
            "Heaven-Mountain": "Sky over mountain, aspiration",
            "Heaven-Water": "Sky reflected in water, mirroring",
            "Heaven-Wind": "Dynamic sky, moving clouds",
            "Heaven-Thunder": "Powerful storm, dramatic sky",
            "Heaven-Fire": "Sun in sky, creative force",
            "Heaven-Lake": "Sky contained in reflection",
            "Heaven-Heaven": "Pure yang, ultimate creativity"
        }
        
        # Get the specific natural element for this hexagram
        natural_element = natural_elements.get(f"{inner_trigram_name}-{outer_trigram_name}", "")
        
        # Traditional life areas associated with hexagrams
        life_areas = {
            1: "Creative potential, leadership, initiation", 
            2: "Receptivity, nurturing, support",
            3: "Initial challenges, beginnings, growth",
            4: "Youth, learning, inexperience",
            5: "Patience, timing, waiting for right moment",
            6: "Conflict, disagreement, adversarial relationships",
            7: "Organization, discipline, structured approach",
            8: "Unity, alliance, joining forces",
            9: "Small restraint, gradual progress, minor obstacles",
            10: "Proper conduct, walking one's path carefully",
            11: "Harmony, peace, smooth functioning",
            12: "Stagnation, blockage, things coming to a halt",
            13: "Fellowship, community, common purpose",
            14: "Great possession, abundance, prosperity",
            15: "Modesty, humility, keeping a low profile",
            16: "Enthusiasm, excitement, inspired action",
            17: "Following, adapting, alignment with others",
            18: "Correcting decay, addressing problems",
            19: "Approach, drawing near, advancement",
            20: "Contemplation, observation, perspective",
            21: "Cutting through, decisive action, justice",
            22: "Grace, beauty, elegance, refinement",
            23: "Splitting apart, deterioration, breaking down",
            24: "Return, renewal, new beginnings",
            25: "Innocence, naturalness, spontaneity",
            26: "Containing power, restraining energy",
            27: "Nourishment, sustenance, proper care",
            28: "Critical mass, excessive pressure",
            29: "Repeated challenges, perseverance through danger",
            30: "Radiance, clarity, attachment to light",
            31: "Influence, attraction, courtship",
            32: "Duration, perseverance, endurance",
            33: "Retreat, strategic withdrawal",
            34: "Great power, strength, vigor",
            35: "Progress, advancement, moving forward",
            36: "Darkening of light, adversity, concealment",
            37: "Family, clan, established structures",
            38: "Opposition, polarity, contrast",
            39: "Obstruction, obstacles, difficulty",
            40: "Deliverance, liberation, release",
            41: "Decrease, reduction, letting go",
            42: "Increase, gain, addition, benefit",
            43: "Breakthrough, resolution, decisive action",
            44: "Coming to meet, unexpected encounter",
            45: "Gathering together, assembly, bringing together",
            46: "Pushing upward, gradual advancement",
            47: "Exhaustion, oppression, feeling confined",
            48: "The well, source, structure that provides",
            49: "Revolution, fundamental change",
            50: "The cauldron, transformation, establishing order",
            51: "Shock, sudden change, arousing",
            52: "Keeping still, meditation, stabilizing",
            53: "Development, gradual progress",
            54: "The marrying maiden, subordinate relationship",
            55: "Abundance, fullness, peak time",
            56: "The wanderer, transience, impermanence",
            57: "Gentle penetration, subtle influence",
            58: "Joy, pleasure, satisfaction, lake",
            59: "Dispersion, dissolution, breaking barriers",
            60: "Limitation, boundaries, structure",
            61: "Inner truth, centering, internal confidence",
            62: "Small exceeding, preponderance of small",
            63: "After completion, already fulfilled",
            64: "Before completion, not yet fulfilled"
        }
        
        # Get life area if number is available as int
        life_area = ""
        if isinstance(number, int):
            life_area = life_areas.get(number, "")
        
        # Build enhanced hexagram data with consolidated structure
        associations["hexagram"] = {
            "binary": hexagram,
            
            # Combined I Ching associations
            "iching_associations": {
                "number": number,
                "traditional_name": traditional_name,
                "label": label,
                "core_meaning": traditional_meaning,
                "life_area": life_area,
                "trigram_relationship": trigram_relationship,
                "natural_element": natural_element,
                "inner_trigram": {
                    "name": inner_trigram_name,
                    "qualities": inner_qualities,
                    "symbol": core_systems["core_associations"]["i_ching_trigrams"].get(inner_trigram, {}).get("trigram_symbol", "")
                },
                "outer_trigram": {
                    "name": outer_trigram_name,
                    "qualities": outer_qualities,
                    "symbol": core_systems["core_associations"]["i_ching_trigrams"].get(outer_trigram, {}).get("trigram_symbol", "")
                }
            },
            
            # Enhanced Gene Key journey with position awareness
            "evolutionary_journey": {
                "gene_key_number": gene_key_data.get("number", ""),
                "shadow_challenge": shadow,
                "shadow_description": f"The challenge of {shadow}: unconscious patterns that limit expression",
                "gift_potential": gift,
                "gift_description": f"The gift of {gift}: conscious transformation and breakthrough potential",
                "siddhi_realization": siddhi,
                "siddhi_description": f"The siddhi of {siddhi}: highest expression and enlightened potential",
                "journey_summary": gene_key_description
            }
        }
    
    # Determine archetype based on resonant season and current season
    resonant_season_key = f"{inner_state}-{outer_state}"
    resonant_season_mapping = core_systems["core_associations"]["archetype_system"]["inner_outer_to_archetype_and_resonant_season"].get(resonant_season_key, {})
    
    # Get the current season based on bits 7-8
    current_season_key = binary_code[6:8]
    seasons = {"00": "Winter", "10": "Spring", "11": "Summer", "01": "Fall"}
    current_season = seasons.get(current_season_key)
    
    # Find the archetype by looking up the current season in the resonant season mapping
    archetype = None
    for season_key, arch in resonant_season_mapping.items():
        if season_key == current_season_key:
            archetype = arch
            break
    
    # Find the resonant season (season where the card is a Sage)
    resonant_season = None
    for season_key, arch in resonant_season_mapping.items():
        if arch == "Sage":
            resonant_season = seasons.get(season_key)
            break
    
    # Add archetype information
    associations["archetype"] = {
        "name": archetype,
        "resonant_season_key": resonant_season_key,
        "resonant_season": resonant_season,
        "current_season": current_season,
        "color": core_systems["core_associations"]["archetype_system"]["archetype_colors"].get(archetype)
    }
    
    # Add archetype-specific information and gene key relationship
    if "hexagram" in associations and "evolutionary_journey" in associations["hexagram"]:
        gene_key_number = associations["hexagram"]["evolutionary_journey"].get("gene_key_number", "")
        shadow = associations["hexagram"]["evolutionary_journey"].get("shadow_challenge", "")
        gift = associations["hexagram"]["evolutionary_journey"].get("gift_potential", "")
        siddhi = associations["hexagram"]["evolutionary_journey"].get("siddhi_realization", "")
        
        # Set archetype's position in the evolutionary journey
        journey_position = ""
        journey_description = ""
        
        if archetype == "Sage":
            associations["archetype"]["gene_key_aspect"] = "siddhi"
            associations["archetype"]["gene_key_manifestation"] = siddhi
            associations["archetype"]["expression"] = f"The integrated, wise expression of {siddhi} - the culmination of this energy pattern"
            journey_position = "siddhi_realization"
            journey_description = f"This card embodies the culmination of the evolutionary journey as the Siddhi of {siddhi}, representing the highest potential of Gene Key {gene_key_number}."
        elif archetype == "Fool":
            associations["archetype"]["gene_key_aspect"] = "potential"
            associations["archetype"]["gene_key_manifestation"] = gene_key_number
            associations["archetype"]["expression"] = f"The innocent, fresh beginning of this energy pattern with untapped potential"
            journey_position = "initial_potential"
            journey_description = f"This card represents the starting point of the evolutionary journey for Gene Key {gene_key_number}, containing the potential to transform from {shadow} to {siddhi}."
        elif archetype == "Hero":
            associations["archetype"]["gene_key_aspect"] = "gift"
            associations["archetype"]["gene_key_manifestation"] = gift
            associations["archetype"]["expression"] = f"The skilled, masterful expression of {gift} - this energy pattern at its most effective"
            journey_position = "gift_expression"
            journey_description = f"This card represents the middle stage of the evolutionary journey, expressing the Gift of {gift}, the breakthrough potential of Gene Key {gene_key_number}."
        elif archetype == "Monster":
            associations["archetype"]["gene_key_aspect"] = "shadow"
            associations["archetype"]["gene_key_manifestation"] = shadow
            associations["archetype"]["expression"] = f"The challenge or excess of {shadow} - this energy pattern in imbalance"
            journey_position = "shadow_challenge"
            journey_description = f"This card embodies the Shadow aspect of Gene Key {gene_key_number} - {shadow}, representing the starting challenge of the evolutionary journey."
        
        # Add journey position to the evolutionary journey section
        associations["hexagram"]["evolutionary_journey"]["journey_position"] = journey_position
        associations["hexagram"]["evolutionary_journey"]["position_description"] = journey_description
    
    # Add cycle position information
    seasons_order = ["Winter", "Spring", "Summer", "Fall"]
    resonant_idx = seasons_order.index(resonant_season) if resonant_season in seasons_order else 0
    current_idx = seasons_order.index(current_season) if current_season in seasons_order else 0
    position_diff = (current_idx - resonant_idx) % 4
    
    cycle_positions = ["Resonant Season", "Next Season", "Third Season", "Fourth Season"]
    associations["archetype"]["cycle_position"] = cycle_positions[position_diff]
    associations["archetype"]["cycle_description"] = f"A {current_season} expression of a {resonant_season}-resonant pattern"
    
    # Determine gender based on bit count and archetype
    bit_count_1_6 = count_bits(binary_code[0:6])
    if bit_count_1_6 == 0 or bit_count_1_6 == 6:
        gender = "neutral"
    elif bit_count_1_6 in [3, 5]:
        gender = "feminine" if archetype in ["Hero", "Monster"] else "masculine"
    else:  # 2 or 4
        gender = "masculine" if archetype in ["Hero", "Monster"] else "feminine"
    
    associations["gender"] = gender
    
    # Add lunar cycle information
    decimal_value = int(binary_code, 2)
    lunar_phase_num = (decimal_value // 2) % 8
    phase_half = decimal_value % 2
    phase_half_name = "first_half" if phase_half == 0 else "second_half"
    
    lunar_cycle_num = (bit_count_1_6 % 4) + 1
    lunar_cycle_names = {
        1: "Inception Cycle",
        2: "Development Cycle",
        3: "Culmination Cycle",
        4: "Transition Cycle"
    }
    
    lunar_phase_name = lunar_cycle["lunar_cycle_system"]["phases"][str(lunar_phase_num)]["name"]
    lunar_phase_half_name = lunar_cycle["lunar_cycle_system"]["phases"][str(lunar_phase_num)][phase_half_name]["name"]
    
    # Get illumination percentage
    illumination_min = lunar_cycle["lunar_cycle_system"]["phases"][str(lunar_phase_num)][phase_half_name].get("illumination_min", "")
    illumination_max = lunar_cycle["lunar_cycle_system"]["phases"][str(lunar_phase_num)][phase_half_name].get("illumination_max", "")
    illumination = f"{illumination_min}-{illumination_max}" if illumination_min and illumination_max else ""
    
    associations["lunar_cycle"] = {
        "decimal_modulo": f"{decimal_value} % 8 = {lunar_phase_num}, {decimal_value} % 2 = {phase_half}",
        "phase": lunar_phase_name,
        "phase_half": lunar_phase_half_name,
        "illumination": illumination,
        "illumination_min": illumination_min,
        "illumination_max": illumination_max,
        "cycle_number": lunar_cycle_num,
        "cycle_name": lunar_cycle_names[lunar_cycle_num],
        "complete_designation": f"{lunar_phase_half_name}, {lunar_cycle_names[lunar_cycle_num]} of {current_season}"
    }
    
    # Get inner and outer trigram names for later use
    inner_trigram_name = associations["inner_world"].get("8bit_trigram_name", "")
    outer_trigram_name = associations["outer_world"].get("8bit_trigram_name", "")
    
    # Add image prompt components
    associations["image_components"] = {
        "colors": {
            "inner_world": associations["inner_world"].get("color"),
            "outer_world": associations["outer_world"].get("color"),
            "archetype": associations["archetype"].get("color"),
            "combined_palette": f"{associations['inner_world'].get('color')}, {associations['outer_world'].get('color')}, and {associations['archetype'].get('color')}"
        },
        "scene_elements": {
            "phase_symbol": f"{lunar_phase_name} ({illumination})",
            "season_element": f"{current_season} ({associations['bit_associations']['bit78'].get('element')})",
            "inner_world_symbol": associations["inner_world"].get("name", inner_trigram_name),
            "outer_world_symbol": associations["outer_world"].get("name", outer_trigram_name)
        },
        "key_symbols": {
            "heart": associations["composite_frameworks"]["inner_and_outer_worlds"]["heart"].get("name"),
            "hands": associations["composite_frameworks"]["inner_and_outer_worlds"]["hands"].get("name"),
            "head": associations["composite_frameworks"]["inner_and_outer_worlds"]["head"].get("name"),
            "archetype": archetype
        }
    }
    
    # Generate card classification 
    trigram_classifications = {
        "000": "Earth",
        "001": "Mountain",
        "010": "Water",
        "011": "Wind",
        "100": "Thunder",
        "101": "Fire",
        "110": "Lake",
        "111": "Heaven"
    }
    
    inner_class = trigram_classifications.get(bits_1_3, "")
    outer_class = trigram_classifications.get(bits_4_6, "")
    season_class = current_season
    
    # Create thematic classifications
    classifications = [
        f"{archetype} of {inner_class}",
        f"{outer_class} {archetype}",
        f"{season_class} {archetype}",
        f"{inner_class}-{outer_class} Pattern",
        f"{lunar_phase_name} Card"
    ]
    
    associations["classifications"] = classifications
    
    # Add symbolic associations that link different frameworks together
    hex_data = associations.get("hexagram", {})
    iching_associations = hex_data.get("iching_associations", {})
    evol_journey = hex_data.get("evolutionary_journey", {})
    
    # Get traditional meanings
    i_ching_label = iching_associations.get("label", "")
    i_ching_meaning = iching_associations.get("core_meaning", "")
    natural_element = iching_associations.get("natural_element", "")
    
    # Get Gene Key journey
    shadow = evol_journey.get("shadow_challenge", "")
    gift = evol_journey.get("gift_potential", "")
    siddhi = evol_journey.get("siddhi_realization", "")
    
    # Create symbolic objects that could be used in card imagery
    symbolic_objects = {
        "Earth": ["mountains", "clay", "fields", "soil", "stones", "caves", "roots"],
        "Mountain": ["boulders", "peaks", "cliffs", "trails", "highlands", "snow", "pine trees"],
        "Water": ["rivers", "oceans", "lakes", "rain", "mist", "wells", "waterfalls"],
        "Wind": ["clouds", "leaves", "flags", "feathers", "birds", "branches", "kites"],
        "Thunder": ["lightning", "storm clouds", "drums", "broken branches", "cracks", "sudden movements"],
        "Fire": ["flames", "candles", "sunlight", "hearths", "torches", "embers", "sparks"],
        "Lake": ["reflections", "ripples", "shores", "joy", "celebrations", "openness", "exchange"],
        "Heaven": ["sky", "stars", "circles", "crowns", "domes", "unity", "perfection"]
    }
    
    # Get symbolic objects for inner and outer trigrams
    inner_objects = symbolic_objects.get(inner_trigram_name, [])
    outer_objects = symbolic_objects.get(outer_trigram_name, [])
    
    # Create body parts that could be emphasized based on bit associations
    body_parts = {
        "heart": ["chest", "heart", "solar plexus", "emotional center"],
        "hands": ["hands", "arms", "shoulders", "tools", "instruments"],
        "head": ["head", "mind", "eyes", "third eye", "crown", "awareness"]
    }
    
    # Create elemental associations by season
    seasonal_elements = {
        "Winter": ["air", "breath", "wind", "clouds", "thought", "ideas", "intellect"],
        "Spring": ["fire", "spark", "flame", "energy", "action", "movement", "transformation"],
        "Summer": ["water", "flow", "waves", "emotions", "feelings", "connection", "intimacy"],
        "Fall": ["earth", "soil", "stone", "body", "matter", "foundation", "stability"]
    }
    
    # Gene Key symbolic objects representing the journey
    gene_key_objects = {
        "shadow": ["obstacles", "chains", "fog", "darkness", "weight", "masks", "barriers", "confusion"],
        "gift": ["tools", "bridges", "light", "keys", "maps", "doorways", "vessels", "wings"],
        "siddhi": ["crowns", "stars", "halos", "radiance", "crystals", "flowers", "fountains", "pure light"]
    }
    
    # Get shadow/gift/siddhi objects
    shadow_objects = gene_key_objects.get("shadow", [])
    gift_objects = gene_key_objects.get("gift", [])
    siddhi_objects = gene_key_objects.get("siddhi", [])
    
    # Collect seasonal symbolic elements
    seasonal_symbols = seasonal_elements.get(current_season, [])
    
    # Assemble symbolic associations across frameworks
    associations["symbolic_associations"] = {
        "core_symbolism": {
            "i_ching": {
                "label": i_ching_label,
                "meaning": i_ching_meaning,
                "natural_element": natural_element,
                "inner_trigram_objects": inner_objects,
                "outer_trigram_objects": outer_objects,
                "combined_image": f"{inner_trigram_name} beneath {outer_trigram_name}: {natural_element}"
            },
            "gene_key": {
                "shadow": shadow,
                "shadow_objects": shadow_objects,
                "gift": gift,
                "gift_objects": gift_objects,
                "siddhi": siddhi,
                "siddhi_objects": siddhi_objects,
                "evolutionary_narrative": f"The journey from {shadow} through {gift} to {siddhi}"
            },
            "body_symbolism": body_parts,
            "seasonal_elements": seasonal_symbols,
            "archetype_qualities": {
                "Sage": ["wisdom", "integration", "wholeness", "fulfillment", "completion"],
                "Fool": ["beginnings", "innocence", "openness", "potential", "curiosity"],
                "Hero": ["mastery", "skill", "accomplishment", "strength", "confidence"],
                "Monster": ["challenge", "excess", "shadow", "intensity", "transformation"]
            }.get(archetype, [])
        },
        
        # Suggested symbolic elements for card imagery based on all systems
        "suggested_symbols": [
            # Primary symbol from I Ching
            {"name": i_ching_label, "description": f"Symbolizing {i_ching_meaning}"},
            # Symbols from inner and outer trigrams
            {"name": inner_objects[0] if inner_objects else inner_trigram_name, "description": f"Representing inner {inner_trigram_name} energy"},
            {"name": outer_objects[0] if outer_objects else outer_trigram_name, "description": f"Representing outer {outer_trigram_name} energy"},
            # Symbol for the appropriate Gene Key aspect based on archetype
            {"name": siddhi_objects[0] if archetype == "Sage" and siddhi_objects else "light", 
             "description": f"Representing the siddhi of {siddhi}"},
            {"name": gift_objects[0] if archetype == "Hero" and gift_objects else "tool", 
             "description": f"Representing the gift of {gift}"},
            {"name": shadow_objects[0] if archetype == "Monster" and shadow_objects else "shadow", 
             "description": f"Representing the shadow of {shadow}"},
            # Seasonal symbol
            {"name": seasonal_symbols[0] if seasonal_symbols else current_season, 
             "description": f"Representing {current_season} element"},
            # Natural element from trigram combination
            {"name": natural_element.split(',')[0] if natural_element else "landscape", 
             "description": "Natural symbolic element from I Ching tradition"}
        ]
    }
    
    # Generate sample image prompt template with enhanced traditional meanings
    card_title = associations.get("card_name")
    if not card_title and "suggested_names" in associations:
        card_title = associations["suggested_names"]["primary"]
    
    if not card_title:
        card_title = f"{inner_trigram_name}{outer_trigram_name} in {current_season}"
        
    inner_color = associations["inner_world"].get("color", "")
    outer_color = associations["outer_world"].get("color", "")
    arch_color = associations["archetype"].get("color", "")
    
    inner_symbol = associations["inner_world"].get("name", inner_trigram_name)
    outer_symbol = associations["outer_world"].get("name", outer_trigram_name)
    heart_symbol = associations["composite_frameworks"]["inner_and_outer_worlds"]["heart"].get("name", "")
    hands_symbol = associations["composite_frameworks"]["inner_and_outer_worlds"]["hands"].get("name", "")
    head_symbol = associations["composite_frameworks"]["inner_and_outer_worlds"]["head"].get("name", "")
    
    # Get enhanced traditional meanings for symbolic imagery
    hex_data = associations.get("hexagram", {})
    iching_associations = hex_data.get("iching_associations", {})
    evol_journey = hex_data.get("evolutionary_journey", {})
    
    # Traditional I Ching elements
    i_ching_name = iching_associations.get("traditional_name", "")
    i_ching_label = iching_associations.get("label", "")
    i_ching_meaning = iching_associations.get("core_meaning", "")
    natural_element = iching_associations.get("natural_element", "")
    life_area = iching_associations.get("life_area", "")
    
    # Gene Key journey
    shadow = evol_journey.get("shadow_challenge", "")
    gift = evol_journey.get("gift_potential", "")
    siddhi = evol_journey.get("siddhi_realization", "")
    
    # Determine which aspect of the Gene Key journey to emphasize based on archetype
    gene_key_aspect = ""
    if archetype == "Sage":
        gene_key_aspect = f"The siddhi of {siddhi}"
    elif archetype == "Fool":
        gene_key_aspect = f"The potential journey from {shadow} to {gift}"
    elif archetype == "Hero":
        gene_key_aspect = f"The gift of {gift}"
    elif archetype == "Monster":
        gene_key_aspect = f"The shadow of {shadow}"
    
    # Get I Ching number if available
    i_ching_number = ""
    if "number" in iching_associations:
        i_ching_number = f"Hexagram {iching_associations['number']}"
    
    # Build a sample image prompt with enhanced traditional meanings
    sample_prompt = f"""LIMITED COLOR RISOGRAPH-STYLE ILLUSTRATION FOR "{card_title}" ({binary_code})

Create a limited-color risograph-style illustration that captures the essence of the {card_title} card - representing {i_ching_label} ({i_ching_name}, {i_ching_number}) as a {archetype} expression in {current_season}.

CARD DIMENSIONS AND STYLE:
- 1200 x 2000 pixels (3:5 ratio)
- Woodblock print/risograph aesthetic with bold lines and limited colors
- Strong contrast between elements with minimalist composition
- Incorporate traditional I Ching symbolism with modern interpretation

COLOR PALETTE:
- Primary: {inner_color} (for inner world character)
- Secondary: {outer_color} (for outer world environment)
- Accent: {arch_color} (representing the {archetype} archetype)
- White/off-white background with subtle texture
- Use colors symbolically to represent the journey from {shadow} to {siddhi}

CHARACTER DESCRIPTION (INNER WORLD):
- A {gender} {archetype.lower()} embodying the qualities of {inner_symbol}
- Expression and posture reflecting {gene_key_aspect}
- Incorporate symbolic elements of {inner_trigram_name} ({inner_qualities})
- Character represents the inner experience of {i_ching_label}

SCENE DESCRIPTION (OUTER WORLD):
- An environment that reflects {current_season} and {outer_symbol}
- Incorporate natural elements: {natural_element}
- Lunar phase showing as a {lunar_phase_name} ({illumination})
- Landscape/environment elements symbolizing {life_area}
- Scene represents the outer expression of {i_ching_label}

SYMBOLIC ELEMENTS:
- {heart_symbol} (representing emotional state)
- {hands_symbol} (representing abilities and support)
- {head_symbol} (representing mental clarity)
- Traditional I Ching symbolism for {i_ching_name}
- Symbol representing the journey from {shadow} to {gift} to {siddhi}
- Subtle hexagram pattern (6 lines) incorporated into design
- Element symbols related to {current_season} and {associations["bit_associations"]["bit78"].get("element")}

CONCEPTUAL MEANING TO CONVEY:
- Core meaning: {i_ching_meaning}
- Life area: {life_area}
- Gene Key journey: {evol_journey.get("journey_summary", "")}
- Archetype significance: {associations["archetype"].get("expression", "")}

LAYOUT SPECIFICATIONS:
- Full width title bar at bottom (15% of card height)
- "{card_title}" in bold, centered
- "{binary_code} • {i_ching_number}" in smaller text below

This card represents {i_ching_label} as a {archetype.lower()} expression of {inner_class}-{outer_class} energy in {current_season}, embodying the journey from {shadow} through {gift} to {siddhi}.
"""
    
    associations["sample_image_prompt"] = sample_prompt
    
    # Add related cards
    opposite_decimal = int(binary_code, 2) ^ 0xFF  # XOR with all 1s to flip all bits
    opposite_binary = format(opposite_decimal, '08b')
    
    # Add known cornerstone card names
    cornerstone_cards = {
        "00000000": "Void Mirror",
        "00000010": "Unwritten Beginning",
        "00000011": "Perfect Vessel",
        "00000001": "Devouring Void"
    }
    
    # Get card name if it's a cornerstone card
    card_name = None
    if binary_code in cornerstone_cards:
        card_name = cornerstone_cards[binary_code]
    
    # Already got these earlier
    # inner_trigram_name and outer_trigram_name are defined above
    
    # Create suggested name components
    name_components = {
        "inner_trigram": inner_trigram_name,
        "outer_trigram": outer_trigram_name,
        "combined_trigrams": f"{inner_trigram_name}{outer_trigram_name}",
        "season": current_season,
        "element": associations["bit_associations"]["bit78"].get("element"),
        "phase": associations["lunar_cycle"]["phase"],
        "phase_half": associations["lunar_cycle"]["phase_half"],
        "archetype": archetype
    }
    
    # Generate a suggested card name if it's not a cornerstone card
    if not card_name:
        # Get I Ching label and other traditional data for naming
        hex_data = associations.get("hexagram", {})
        iching_associations = hex_data.get("iching_associations", {})
        evol_journey = hex_data.get("evolutionary_journey", {})
        
        i_ching_label = iching_associations.get("label", "")
        i_ching_name = iching_associations.get("traditional_name", "")
        shadow = evol_journey.get("shadow_challenge", "")
        gift = evol_journey.get("gift_potential", "")
        siddhi = evol_journey.get("siddhi_realization", "")
        
        # Different name patterns based on archetype
        if archetype == "Sage":
            name_pattern = f"The {siddhi} of {inner_trigram_name}{outer_trigram_name}"
            if i_ching_label:
                name_pattern = f"The {i_ching_label}"
        elif archetype == "Fool":
            name_pattern = f"{inner_trigram_name}{outer_trigram_name} Beginning"
            if i_ching_label:
                name_pattern = f"Awakening {i_ching_label}"
        elif archetype == "Hero":
            name_pattern = f"The {gift} of {inner_trigram_name}{outer_trigram_name}"
            if i_ching_label:
                name_pattern = f"Mastering {i_ching_label}"
        elif archetype == "Monster":
            name_pattern = f"The {shadow} of {inner_trigram_name}{outer_trigram_name}"
            if i_ching_label:
                name_pattern = f"Challenging {i_ching_label}"
        else:
            name_pattern = f"{inner_trigram_name}{outer_trigram_name} in {current_season}"
        
        # Alternative name suggestions that incorporate traditional meanings
        alt_name1 = f"The {inner_trigram_name}{outer_trigram_name} of {current_season}"
        alt_name2 = f"{i_ching_label} {associations['lunar_cycle']['phase']}"
        alt_name3 = f"{inner_trigram_name}{outer_trigram_name} {i_ching_name}"
        alt_name4 = f"The {archetype} of {i_ching_label}"
        
        associations["suggested_names"] = {
            "primary": name_pattern,
            "alternatives": [alt_name1, alt_name2, alt_name3, alt_name4],
            "traditional_name": f"{i_ching_name} ({i_ching_label})"
        }
    
    associations["card_name"] = card_name
    associations["name_components"] = name_components
    
    associations["related_cards"] = {
        "same_hexagram_winter": f"{hexagram}00",
        "same_hexagram_spring": f"{hexagram}10",
        "same_hexagram_summer": f"{hexagram}11",
        "same_hexagram_fall": f"{hexagram}01",
        "opposite": opposite_binary,
        "full_cycle": [f"{hexagram}{bits}" for bits in ["00", "10", "11", "01"]]
    }
    
    return associations

def generate_hexagram_associations(hexagram_code):
    """Generate association files for all four cards in a hexagram."""
    # Validate hexagram code
    if not (len(hexagram_code) == 6 and all(bit in '01' for bit in hexagram_code)):
        print(f"Error: Invalid hexagram code '{hexagram_code}'. Must be 6 bits of 0s and 1s.")
        return False
    
    # Load data
    core_systems = load_yaml_file(CORE_SYSTEMS_PATH)
    composite_associations = load_yaml_file(COMPOSITE_ASSOCIATIONS_PATH)
    lunar_cycle = load_yaml_file(LUNAR_CYCLE_PATH)
    
    # Create output directory
    output_dir = os.path.join(OUTPUT_DIR, hexagram_code)
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate associations for each season (bit patterns 00, 10, 11, 01)
    for season_bits in ["00", "10", "11", "01"]:
        binary_code = hexagram_code + season_bits
        associations = get_associations_for_code(binary_code, core_systems, composite_associations, lunar_cycle)
        
        # Save to YAML file
        file_path = os.path.join(output_dir, f"{binary_code}.yml")
        with open(file_path, 'w') as file:
            yaml.dump(associations, file, default_flow_style=False, sort_keys=False)
        
        print(f"Generated associations for {binary_code}, saved to {file_path}")
    
    return True

def main():
    """Main function to generate associations for a hexagram."""
    if len(sys.argv) != 2:
        print("Usage: python association-generator.py <6-bit_code>")
        sys.exit(1)
    
    hexagram_code = sys.argv[1]
    
    print(f"Generating association files for hexagram: {hexagram_code}")
    
    # Generate associations
    if not generate_hexagram_associations(hexagram_code):
        sys.exit(1)
    
    print("\nDone! Generated association files for all four seasonal variations.")

if __name__ == "__main__":
    main()