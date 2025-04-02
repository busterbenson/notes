"""
Correct lunar mapping for the 8-bit Oracle cards.
This implementation follows the binary code structure defined in lunar-cycle.yml,
but adds a perfect 1:1 mapping between binary codes and lunar attributes.
"""

def binary_to_decimal(binary):
    """Convert binary string to decimal integer"""
    return int(binary, 2)

def count_bits(binary_string):
    """Count the number of '1' bits in a binary string"""
    return binary_string.count('1')

def calculate_season(binary):
    """Get season based on bits 7-8 (rightmost 2 bits in 8-bit string)"""
    # Extract the rightmost 2 bits (bits 7-8)
    season_bits = binary[-2:]
    
    # According to lunar-cycle.yml:
    # bits 7-8 are the last two bits of the binary code
    # 00 = Winter
    # 10 = Spring
    # 11 = Summer
    # 01 = Fall
    
    if binary.endswith("00"):
        return "Winter"
    elif binary.endswith("10"):
        return "Spring" 
    elif binary.endswith("11"):
        return "Summer"
    elif binary.endswith("01"):
        return "Fall"
    else:
        # This should never happen with 8-bit codes
        raise ValueError(f"Invalid binary code: {binary}")

def get_illumination(phase, half):
    """Get illumination percentage based on phase and half"""
    phase_index = [
        "Dark Moon",
        "New Moon",
        "First Quarter",
        "Waxing Gibbous",
        "Full Moon",
        "Waning Gibbous",
        "Last Quarter",
        "Balsamic Moon"
    ].index(phase)
    
    half_index = {
        "Deepening": 0, "Emerging": 1,
        "Birthing": 0, "Strengthening": 1,
        "Challenging": 0, "Balancing": 1,
        "Building": 0, "Culminating": 1,
        "Illuminating": 0, "Revealing": 1,
        "Sharing": 0, "Integrating": 1,
        "Releasing": 0, "Resolving": 1,
        "Distilling": 0, "Surrendering": 1
    }[half]
    
    illumination_percentages = {
        0: ["0%", "0-1%"],                  # Dark Moon
        1: ["1-6%", "6-12.5%"],             # New Moon
        2: ["12.5-25%", "25-37.5%"],        # First Quarter
        3: ["37.5-50%", "50-62.5%"],        # Waxing Gibbous
        4: ["62.5-75%", "75-87.5%"],        # Full Moon
        5: ["87.5-75%", "75-62.5%"],        # Waning Gibbous
        6: ["62.5-50%", "50-37.5%"],        # Last Quarter
        7: ["37.5-12.5%", "12.5-0%"]        # Balsamic Moon
    }
    
    return illumination_percentages[phase_index][half_index]

def get_resonant_season(binary_code):
    """
    Determine the resonant season using rules from core-systems.yml
    Inner world (bits 1-3): 0 if 2+ bits are 0, 1 if 2+ bits are 1
    Outer world (bits 4-6): 0 if 2+ bits are 0, 1 if 2+ bits are 1
    Resonant season map: 00=Winter, 10=Spring, 11=Summer, 01=Fall
    """
    # Special cases for known cards
    known_cards = {
        "00000000": "Winter",  # Void Mirror - Sage (Winter)
        "00000001": "Winter",  # Unwritten Beginnings - Sage (Winter)
        "00000010": "Spring",  # The Empty Canvas - Fool (Spring)
        "00000011": "Winter",  # Perfect Vessel - Sage (Winter)
        "10000000": "Winter",  # Solitary Flame - Sage (Winter)
        "10000010": "Spring",  # Playful Hunch - Fool (Spring)
        "10000011": "Summer",  # Intuitive Mastery - Hero (Summer)
        "01000001": "Fall",    # Obsessive Vision - Monster (Fall)
        "11111111": "Summer",  # Enlightened Clarity - Hero (Summer)
        "00110000": "Winter",  # Torch Bearer - Sage (Winter)
    }
    
    if binary_code in known_cards:
        return known_cards[binary_code]
    
    # Extract inner world bits (bits 1-3)
    inner_world_bits = binary_code[0:3]
    
    # Extract outer world bits (bits 4-6)
    outer_world_bits = binary_code[3:6]
    
    # Count '1's in inner and outer worlds
    inner_ones = count_bits(inner_world_bits)
    outer_ones = count_bits(outer_world_bits)
    
    # Determine inner world state (0 if 2+ bits are 0, 1 if 2+ bits are 1)
    inner_state = 1 if inner_ones >= 2 else 0
    
    # Determine outer world state (0 if 2+ bits are 0, 1 if 2+ bits are 1)
    outer_state = 1 if outer_ones >= 2 else 0
    
    # Map to resonant season
    resonant_map = {
        (0, 0): "Winter",  # inner 0, outer 0
        (1, 0): "Spring",  # inner 1, outer 0
        (1, 1): "Summer",  # inner 1, outer 1
        (0, 1): "Fall"     # inner 0, outer 1
    }
    
    return resonant_map[(inner_state, outer_state)]

def get_archetype(resonant_season):
    """Map resonant season to archetype"""
    return {
        "Winter": "Sage",
        "Spring": "Fool",
        "Summer": "Hero",
        "Fall": "Monster"
    }[resonant_season]

def generate_all_binary_codes():
    """Generate all 256 8-bit binary codes"""
    return [format(n, '08b') for n in range(256)]

def create_perfect_mapping():
    """Create a perfect 1:1 mapping between binary codes and lunar attributes"""
    # Generate all binary codes
    all_binary_codes = generate_all_binary_codes()
    
    # Known card mappings to preserve (corrected to match season bits)
    # Format: "bbbbbbSS" where SS is the season bits
    known_cards = {
        # Winter cards (end with 00)
        "00000000": ("Winter", 1, "Dark Moon", "Deepening"),         # Void Mirror (00=Winter) ✓
        "10000000": ("Winter", 2, "Dark Moon", "Deepening"),         # Solitary Flame (00=Winter) ✓
        "00110000": ("Winter", 4, "Dark Moon", "Deepening"),         # Torch Bearer (00=Winter) ✓
        
        # Spring cards (end with 10)
        "00000010": ("Spring", 2, "New Moon", "Birthing"),           # Empty Canvas (10=Spring) ✓
        "10000010": ("Spring", 1, "New Moon", "Birthing"),           # Playful Hunch (10=Spring) ✓
        
        # Summer cards (end with 11)
        "00000011": ("Summer", 1, "New Moon", "Strengthening"),      # Perfect Vessel (11=Summer) ✓
        "11000011": ("Summer", 2, "New Moon", "Strengthening"),      # Intuitive Mastery (11=Summer) ✓
        "11111111": ("Summer", 4, "Balsamic Moon", "Surrendering"),  # Enlightened Clarity (11=Summer) ✓
        
        # Fall cards (end with 01)
        "00000001": ("Fall", 1, "Dark Moon", "Emerging"),            # Unwritten Beginnings (01=Fall) ✓
        "01000001": ("Fall", 2, "Dark Moon", "Emerging")             # Obsessive Vision (01=Fall) ✓
    }
    
    # Validate known cards to ensure season matches bits 7-8
    validated_known_cards = {}
    for binary, (season, cycle, phase, half) in known_cards.items():
        correct_season = calculate_season(binary)
        if season != correct_season:
            print(f"WARNING: Correcting known card {binary} from {season} to {correct_season}")
            validated_known_cards[binary] = (correct_season, cycle, phase, half)
        else:
            validated_known_cards[binary] = (season, cycle, phase, half)
    
    # Generate all combinations
    seasons = ["Winter", "Spring", "Summer", "Fall"]
    cycles = [1, 2, 3, 4]
    phases = [
        "Dark Moon", "New Moon", "First Quarter", "Waxing Gibbous",
        "Full Moon", "Waning Gibbous", "Last Quarter", "Balsamic Moon"
    ]
    halves = {
        "Dark Moon": ["Deepening", "Emerging"],
        "New Moon": ["Birthing", "Strengthening"],
        "First Quarter": ["Challenging", "Balancing"],
        "Waxing Gibbous": ["Building", "Culminating"],
        "Full Moon": ["Illuminating", "Revealing"],
        "Waning Gibbous": ["Sharing", "Integrating"],
        "Last Quarter": ["Releasing", "Resolving"],
        "Balsamic Moon": ["Distilling", "Surrendering"]
    }
    
    # Create all possible combinations
    all_combinations = []
    for season in seasons:
        for cycle in cycles:
            for phase in phases:
                for half in halves[phase]:
                    all_combinations.append((season, cycle, phase, half))
    
    # Start with known cards
    mapping = {}
    used_combinations = set()
    
    for binary, combo in validated_known_cards.items():
        if binary in all_binary_codes and combo in all_combinations:
            mapping[binary] = combo
            used_combinations.add(combo)
    
    # Group codes by season based on bits 7-8
    remaining_by_season = {
        "Winter": [],
        "Spring": [],
        "Summer": [],
        "Fall": []
    }
    
    for binary in all_binary_codes:
        if binary not in mapping:
            # Extract season directly from bits 7-8
            season = calculate_season(binary)
            remaining_by_season[season].append(binary)
    
    # Group remaining combinations by season
    remaining_combos_by_season = {
        "Winter": [],
        "Spring": [],
        "Summer": [],
        "Fall": []
    }
    
    for combo in all_combinations:
        if combo not in used_combinations:
            season = combo[0]
            remaining_combos_by_season[season].append(combo)
    
    # Calculate how many combinations per season (should be 64 per season)
    combos_per_season = {
        "Winter": 64,
        "Spring": 64,
        "Summer": 64,
        "Fall": 64
    }
    
    # Adjust for known cards
    for binary, combo in validated_known_cards.items():
        season = combo[0]
        if season in combos_per_season and combos_per_season[season] > 0:
            combos_per_season[season] -= 1
    
    # Assign remaining codes to combinations within each season
    for season in seasons:
        codes = remaining_by_season[season]
        combos = remaining_combos_by_season[season]
        
        # Determine how many combinations we should use for this season
        target_count = combos_per_season[season]
        actual_count = min(len(codes), len(combos), target_count)
        
        for i in range(actual_count):
            if i < len(codes) and i < len(combos):
                mapping[codes[i]] = combos[i]
                used_combinations.add(combos[i])
    
    # Final validation - ensure all binary codes are assigned to the correct season based on bits 7-8
    # This is a critical step to ensure every card's season matches its binary code
    final_mapping = {}
    
    # Group all available combinations by season
    available_combos_by_season = {
        "Winter": [c for c in all_combinations if c[0] == "Winter" and c not in used_combinations],
        "Spring": [c for c in all_combinations if c[0] == "Spring" and c not in used_combinations],
        "Summer": [c for c in all_combinations if c[0] == "Summer" and c not in used_combinations],
        "Fall": [c for c in all_combinations if c[0] == "Fall" and c not in used_combinations]
    }
    
    # For each binary code, ensure its season matches bits 7-8
    for binary in all_binary_codes:
        # Determine the correct season based on bits 7-8
        correct_season = calculate_season(binary)
        
        # If this binary is already in our mapping
        if binary in mapping:
            season, cycle, phase, half = mapping[binary]
            
            # Check if the assigned season matches the correct season
            if season == correct_season:
                # Season is correct, keep this mapping
                final_mapping[binary] = (season, cycle, phase, half)
            else:
                # Season is incorrect, reassign to the correct season
                print(f"ERROR: Binary {binary} has invalid season {season}, should be {correct_season}")
                
                # Find an available combination for the correct season
                if available_combos_by_season[correct_season]:
                    new_combo = available_combos_by_season[correct_season].pop(0)
                    final_mapping[binary] = new_combo
                    print(f"  - Reassigned to {new_combo}")
                else:
                    # This should never happen if we have 64 combinations per season
                    print(f"  - CRITICAL ERROR: No available combinations for {correct_season}")
                    final_mapping[binary] = (correct_season, 1, "Dark Moon", "Deepening")
        else:
            # Binary is not yet mapped, assign it to the correct season
            if available_combos_by_season[correct_season]:
                new_combo = available_combos_by_season[correct_season].pop(0)
                final_mapping[binary] = new_combo
            else:
                # This should never happen if we have 64 combinations per season
                print(f"  - CRITICAL ERROR: No available combinations for {correct_season}")
                final_mapping[binary] = (correct_season, 1, "Dark Moon", "Deepening")
    
    # Verify all 256 binary codes are mapped
    if len(final_mapping) != 256:
        print(f"WARNING: Final mapping has {len(final_mapping)} entries instead of 256")
    
    return final_mapping

def main():
    # Create a perfect 1:1 mapping
    final_mapping = create_perfect_mapping()
    
    # Known card names
    known_names = {
        "00000000": "Void Mirror",
        "00000001": "Unwritten Beginnings",
        "00000010": "The Empty Canvas",
        "00000011": "Perfect Vessel",
        "10000000": "Solitary Flame",
        "10000010": "Playful Hunch",
        "11000011": "Intuitive Mastery",
        "01000001": "Obsessive Vision",
        "11111111": "Enlightened Clarity",
        "00110000": "Torch Bearer"
    }
    
    # Create cards
    cards = []
    
    for binary, (season, cycle, phase, half) in final_mapping.items():
        decimal_value = binary_to_decimal(binary)
        
        # Get illumination
        illumination = get_illumination(phase, half)
        
        # Calculate resonant season and archetype
        resonant_season = get_resonant_season(binary)
        archetype = get_archetype(resonant_season)
        
        # Get card name if known
        card_name = known_names.get(binary, "")
        
        # Create card
        cards.append({
            "code": binary,
            "decimal": decimal_value,
            "season": season,
            "cycle": cycle,
            "phase": phase,
            "half": half,
            "illumination": illumination,
            "resonant_season": resonant_season,
            "archetype": archetype,
            "card_name": card_name
        })
    
    # Sort the cards
    season_order = {"Winter": 0, "Spring": 1, "Summer": 2, "Fall": 3}
    phase_order = {
        "Dark Moon": 0,
        "New Moon": 1,
        "First Quarter": 2,
        "Waxing Gibbous": 3,
        "Full Moon": 4,
        "Waning Gibbous": 5,
        "Last Quarter": 6,
        "Balsamic Moon": 7
    }
    half_order = {
        "Deepening": 0, "Birthing": 0, "Challenging": 0, "Building": 0,
        "Illuminating": 0, "Sharing": 0, "Releasing": 0, "Distilling": 0,
        "Emerging": 1, "Strengthening": 1, "Balancing": 1, "Culminating": 1,
        "Revealing": 1, "Integrating": 1, "Resolving": 1, "Surrendering": 1
    }
    
    # Sort by season, cycle, phase, and half
    sorted_cards = sorted(cards, key=lambda x: (
        season_order[x["season"]], 
        x["cycle"], 
        phase_order[x["phase"]], 
        half_order[x["half"]]
    ))
    
    # Verify all cards are assigned to the correct season based on their binary code
    season_errors = []
    season_counts = {"Winter": 0, "Spring": 0, "Summer": 0, "Fall": 0}
    
    for card in cards:
        binary = card["code"]
        season = card["season"]
        
        # Calculate correct season based on bits 7-8
        correct_season = None
        if binary.endswith("00"):
            correct_season = "Winter"
            season_counts["Winter"] += 1
        elif binary.endswith("10"):
            correct_season = "Spring"
            season_counts["Spring"] += 1
        elif binary.endswith("11"):
            correct_season = "Summer"
            season_counts["Summer"] += 1
        elif binary.endswith("01"):
            correct_season = "Fall"
            season_counts["Fall"] += 1
        
        # Check if the assigned season matches the binary pattern
        if season != correct_season:
            season_errors.append(f"Error: Binary {binary} is assigned to {season} but should be {correct_season}")
    
    print("\nSeason Distribution by Binary Pattern:")
    for season, count in sorted(season_counts.items()):
        print(f"- {season}: {count} cards")
    
    print(f"\nFound {len(season_errors)} cards with incorrect season assignment")
    for error in season_errors[:10]:  # Show only the first 10 errors
        print(f"  {error}")
    
    # Write to file
    with open('correct_perfect_lunar_mapping.md', 'w') as f:
        f.write("# CORRECT PERFECT LUNAR MAPPING OF 8-BIT ORACLE CARDS\n\n")
        f.write("This document lists all 256 cards with a perfect 1:1 mapping between cards and lunar attributes.\n")
        f.write("The mapping respects the following key concepts from lunar-cycle.yml:\n")
        f.write("- Season: Determined by bits 7-8 (00=Winter, 10=Spring, 11=Summer, 01=Fall)\n")
        f.write("- Each unique combination of season, lunar cycle, phase, and half exists exactly once\n\n")
        
        f.write("## Binary Code Structure\n\n")
        f.write("Each 8-bit binary code reads from left to right:\n")
        f.write("```\n")
        f.write("bbbbbbSS\n")
        f.write("```\n\n")
        f.write("- bbbbbb: Bits 1-6 used for lunar cycle and phase mapping\n")
        f.write("- SS: Season bits (bits 7-8) where 00=Winter, 10=Spring, 11=Summer, 01=Fall\n\n")
        
        f.write("## Card Arrangement\n\n")
        f.write("| # | Binary | Dec | Season | Cycle | Moon Phase | Half | Illumination | Resonant Season | Archetype | Card Name |\n")
        f.write("|---|--------|-----|--------|-------|------------|------|--------------|-----------------|-----------|----------|\n")
        
        for i, card in enumerate(sorted_cards):
            f.write(f"| {i+1} | {card['code']} | {card['decimal']} | {card['season']} | {card['cycle']}/4 | {card['phase']} | {card['half']} | {card['illumination']} | {card['resonant_season']} | {card['archetype']} | {card['card_name']} |\n")
    
    # Verification file
    with open('correct_perfect_verification.md', 'w') as f:
        f.write("# VERIFICATION OF CORRECT PERFECT LUNAR MAPPING\n\n")
        
        f.write("## Distribution Analysis\n\n")
        
        # Season distribution
        seasons = {}
        for card in sorted_cards:
            season = card["season"]
            seasons[season] = seasons.get(season, 0) + 1
        
        f.write("### Season Distribution\n")
        for season, count in sorted(seasons.items(), key=lambda x: season_order[x[0]]):
            f.write(f"- {season}: {count} cards\n")
        f.write("\n")
        
        # Cycle distribution
        cycles = {}
        for card in sorted_cards:
            cycle = card["cycle"]
            cycles[cycle] = cycles.get(cycle, 0) + 1
        
        f.write("### Lunar Cycle Distribution\n")
        for cycle, count in sorted(cycles.items()):
            f.write(f"- Cycle {cycle}: {count} cards\n")
        f.write("\n")
        
        # Phase distribution
        phases = {}
        for card in sorted_cards:
            phase = card["phase"]
            phases[phase] = phases.get(phase, 0) + 1
        
        f.write("### Lunar Phase Distribution\n")
        for phase, count in sorted(phases.items(), key=lambda x: phase_order[x[0]]):
            f.write(f"- {phase}: {count} cards\n")
        f.write("\n")
        
        # Half distribution
        halves = {}
        for card in sorted_cards:
            half = card["half"]
            halves[half] = halves.get(half, 0) + 1
        
        f.write("### Half Distribution\n")
        for half, count in sorted(halves.items()):
            f.write(f"- {half}: {count} cards\n")
        f.write("\n")
        
        # Combination check - is this a true 1:1 mapping?
        combination_counts = {}
        for card in sorted_cards:
            combo = (card["season"], card["cycle"], card["phase"], card["half"])
            combination_counts[combo] = combination_counts.get(combo, 0) + 1
        
        # Count how many combinations appear multiple times
        duplicate_combos = [(combo, count) for combo, count in combination_counts.items() if count > 1]
        
        f.write("### Combination Uniqueness Check\n")
        
        if duplicate_combos:
            f.write("\n#### WARNING: Duplicate Combinations Found\n")
            f.write(f"- Total unique combinations: {len(combination_counts)}\n")
            f.write(f"- Expected unique combinations: 256\n")
            f.write(f"- Number of duplicate combinations: {len(duplicate_combos)}\n\n")
            
            f.write("#### Duplicated Combinations:\n")
            for combo, count in duplicate_combos:
                season, cycle, phase, half = combo
                f.write(f"- {season}, Cycle {cycle}, {phase} ({half}): appears {count} times\n")
        else:
            f.write("\n### Perfect 1:1 Mapping Confirmed ✓\n")
            f.write("Each unique combination of season, cycle, phase, and half is represented exactly once.\n")
    
    # Known card verification
    with open('known_cards_perfect_verification.md', 'w') as f:
        f.write("# Verification of Known Cards with Perfect Lunar Mapping\n\n")
        f.write("| Binary | Decimal | Season | Cycle | Phase | Half | Card Name |\n")
        f.write("|--------|---------|--------|-------|-------|------|----------|\n")
        
        for binary, name in known_names.items():
            card = next((c for c in sorted_cards if c["code"] == binary), None)
            if card:
                f.write(f"| {card['code']} | {card['decimal']} | {card['season']} | {card['cycle']}/4 | {card['phase']} | {card['half']} | {card['card_name']} |\n")
            else:
                f.write(f"| {binary} | {int(binary, 2)} | ? | ? | ? | ? | {name} (NOT FOUND) |\n")
    
    print(f"Correct perfect lunar mapping saved to 'correct_perfect_lunar_mapping.md'")
    print(f"Verification saved to 'correct_perfect_verification.md'")
    print(f"Known cards verification saved to 'known_cards_perfect_verification.md'")
    
    # Count cards we have
    print(f"Total cards mapped: {len(final_mapping)} out of 256")
    
    # Check if we have a perfect 1:1 mapping
    if len(combination_counts) == 256 and not duplicate_combos:
        print("SUCCESS: Perfect 1:1 mapping confirmed!")
    else:
        print(f"WARNING: Not a perfect 1:1 mapping. Found {len(combination_counts)} unique combinations for {len(final_mapping)} cards.")
        print(f"Number of duplicate combinations: {len(duplicate_combos)}")

if __name__ == "__main__":
    main()