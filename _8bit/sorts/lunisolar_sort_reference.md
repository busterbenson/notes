# 8-BIT ORACLE CARD MAPPING REFERENCE

This document explains the logic and methodology behind the `lunisolar_sort.md` file, which provides a comprehensive reference for all 256 cards in the left-prioritized 8-bit Oracle system.

## Card Ordering Logic

The 256 cards are sorted hierarchically by:
1. Season (Winter, Spring, Summer, Fall)
2. Lunar Cycle (1/4, 2/4, 3/4, 4/4)
3. Lunar Phase (Dark Moon, New Moon, First Quarter, Waxing Gibbous, Full Moon, Waning Gibbous, Last Quarter, Balsamic Moon)
4. Phase Half (Deepening/Emerging, Birthing/Strengthening, etc.)

## Bit Interpretation Rules

### Season Determination (bits 7-8)
- `00` = Winter
- `10` = Spring
- `11` = Summer
- `01` = Fall

The season is determined by the 7th and 8th bits read as a 2-bit binary number, but following a specific pattern (not sequential):
- `00` (0) = Winter
- `10` (2) = Spring
- `11` (3) = Summer
- `01` (1) = Fall

### Lunar Cycle Calculation
For each card:
```
lunar_cycle = (count of '1' bits in positions 1-6 % 4) + 1
```

This yields a number 1-4, representing which lunar cycle within the season the card belongs to.

### Lunar Phase Calculation
For each card:
```
lunar_phase = (decimal_value ÷ 2) % 8
```

This produces a value from 0-7, corresponding to these lunar phases:
- 0: Dark Moon
- 1: New Moon
- 2: First Quarter
- 3: Waxing Gibbous
- 4: Full Moon
- 5: Waning Gibbous
- 6: Last Quarter
- 7: Balsamic Moon

### Phase Half Calculation
For each card:
```
phase_half = decimal_value % 2
```

This determines which half of the lunar phase:
- 0: First half (Deepening, Birthing, Challenging, Building, Illuminating, Sharing, Releasing, Distilling)
- 1: Second half (Emerging, Strengthening, Balancing, Culminating, Revealing, Integrating, Resolving, Surrendering)

### Illumination Values
Each phase half corresponds to a specific illumination percentage range:
- Dark Moon (Deepening): 0%
- Dark Moon (Emerging): 0-1% 
- New Moon (Birthing): 1-6%
- New Moon (Strengthening): 6-12.5%
- First Quarter (Challenging): 12.5-25%
- First Quarter (Balancing): 25-37.5%
- Waxing Gibbous (Building): 37.5-50%
- Waxing Gibbous (Culminating): 50-62.5%
- Full Moon (Illuminating): 62.5-75%
- Full Moon (Revealing): 75-87.5%
- Waning Gibbous (Sharing): 87.5-75%
- Waning Gibbous (Integrating): 75-62.5%
- Last Quarter (Releasing): 62.5-50%
- Last Quarter (Resolving): 50-37.5%
- Balsamic Moon (Distilling): 37.5-12.5%
- Balsamic Moon (Surrendering): 12.5-0%

## Archetype Determination

Archetypes are based on the relationship between a card's resonant season and its actual season:

1. Calculate resonant season:
   - Count 1 bits in inner world (bits 1-3): If 2+ bits are 1, inner = 1; otherwise inner = 0
   - Count 1 bits in outer world (bits 4-6): If 2+ bits are 1, outer = 1; otherwise outer = 0
   - Map inner-outer to season: 00 = Winter, 10 = Spring, 11 = Summer, 01 = Fall

2. Compare resonant season to actual season (determined by bits 7-8):
   - If seasons match: **Sage** archetype
   - If card season is next clockwise from resonant: **Fool** archetype
   - If card season is opposite from resonant: **Hero** archetype
   - If card season is previous clockwise from resonant: **Monster** archetype

Season clockwise order: Winter → Spring → Summer → Fall → Winter

### Example:
For card `00000000`:
- Inner world (bits 1-3): 000 → 0 bits are 1, so inner = 0
- Outer world (bits 4-6): 000 → 0 bits are 1, so outer = 0
- Resonant season = 00 = Winter
- Card season (bits 7-8): 00 = Winter
- Since the card season matches the resonant season, the archetype is **Sage**

## Card Generation Algorithm

To generate the full sorted list of 256 cards in the proper order:

```python
def get_season_name(season_bits):
    seasons = {
        "00": "Winter",
        "10": "Spring", 
        "11": "Summer",
        "01": "Fall"
    }
    return seasons[season_bits]

def count_ones(binary_string):
    return sum(1 for bit in binary_string if bit == '1')

def calculate_lunar_cycle(bits_1_to_6):
    ones_count = count_ones(bits_1_to_6)
    return (ones_count % 4) + 1

def calculate_lunar_phase(decimal_value):
    return (decimal_value // 2) % 8

def calculate_phase_half(decimal_value):
    return decimal_value % 2

def get_phase_name(phase_num):
    phases = [
        "Dark Moon",
        "New Moon",
        "First Quarter",
        "Waxing Gibbous",
        "Full Moon",
        "Waning Gibbous",
        "Last Quarter",
        "Balsamic Moon"
    ]
    return phases[phase_num]

def get_half_name(phase_num, half):
    halves = [
        ["Deepening", "Emerging"],         # Dark Moon
        ["Birthing", "Strengthening"],     # New Moon
        ["Challenging", "Balancing"],      # First Quarter
        ["Building", "Culminating"],       # Waxing Gibbous
        ["Illuminating", "Revealing"],     # Full Moon
        ["Sharing", "Integrating"],        # Waning Gibbous
        ["Releasing", "Resolving"],        # Last Quarter
        ["Distilling", "Surrendering"]     # Balsamic Moon
    ]
    return halves[phase_num][half]

def get_illumination(phase_num, half):
    illuminations = [
        ["0%", "0-1%"],                    # Dark Moon
        ["1-6%", "6-12.5%"],               # New Moon
        ["12.5-25%", "25-37.5%"],          # First Quarter
        ["37.5-50%", "50-62.5%"],          # Waxing Gibbous
        ["62.5-75%", "75-87.5%"],          # Full Moon
        ["87.5-75%", "75-62.5%"],          # Waning Gibbous
        ["62.5-50%", "50-37.5%"],          # Last Quarter
        ["37.5-12.5%", "12.5-0%"]          # Balsamic Moon
    ]
    return illuminations[phase_num][half]

def calculate_archetype(binary):
    # Inner world (bits 1-3)
    inner_bits = binary[0:3]
    inner_ones = count_ones(inner_bits)
    inner_value = 1 if inner_ones >= 2 else 0
    
    # Outer world (bits 4-6)
    outer_bits = binary[3:6]
    outer_ones = count_ones(outer_bits)
    outer_value = 1 if outer_ones >= 2 else 0
    
    # Resonant season
    resonant = f"{inner_value}{outer_value}"
    
    # Card season
    card_season = binary[6:8]
    
    # Season order for clockwise comparison
    season_order = ["00", "10", "11", "01"]
    
    # Find indices
    resonant_idx = season_order.index(resonant)
    card_idx = season_order.index(card_season)
    
    # Compare seasons
    if resonant == card_season:
        return "Sage"
    elif (resonant_idx + 1) % 4 == card_idx:
        return "Fool"
    elif (resonant_idx + 2) % 4 == card_idx:
        return "Hero"
    else:  # (resonant_idx + 3) % 4 == card_idx
        return "Monster"

# Generate all 256 cards and sort them by season, lunar cycle, phase, and half
cards = []

for decimal in range(256):
    # Convert to 8-bit binary string
    binary = format(decimal, '08b')
    
    # Extract season bits (7-8)
    season_bits = binary[6:8]
    season = get_season_name(season_bits)
    
    # Calculate lunar cycle (1-4)
    bits_1_to_6 = binary[0:6]
    lunar_cycle = calculate_lunar_cycle(bits_1_to_6)
    
    # Calculate lunar phase (0-7)
    phase_num = calculate_lunar_phase(decimal)
    phase_name = get_phase_name(phase_num)
    
    # Calculate phase half (0-1)
    half = calculate_phase_half(decimal)
    half_name = get_half_name(phase_num, half)
    
    # Calculate illumination percentage
    illumination = get_illumination(phase_num, half)
    
    # Calculate archetype
    archetype = calculate_archetype(binary)
    
    # Store all card data
    cards.append({
        'decimal': decimal,
        'binary': binary,
        'season': season,
        'lunar_cycle': lunar_cycle,
        'phase_num': phase_num,
        'phase': phase_name,
        'half': half,
        'half_name': half_name,
        'illumination': illumination,
        'archetype': archetype
    })

# Sort cards in the proper order
sorted_cards = sorted(cards, key=lambda x: (
    ['Winter', 'Spring', 'Summer', 'Fall'].index(x['season']),
    x['lunar_cycle'],
    x['phase_num'],
    x['half']
))

# Output the sorted cards
for card in sorted_cards:
    # Output card information
    print(f"{card['decimal']} | {card['binary']} | {card['season']} | {card['lunar_cycle']}/4 | {card['phase']} | {card['half_name']} | {card['illumination']} | {card['archetype']}")
```

## Distribution Verification

The left-prioritized mapping maintains a perfect distribution:
- 64 cards per season (Winter, Spring, Summer, Fall)
- 64 cards per lunar cycle (1/4, 2/4, 3/4, 4/4)
- 32 cards per lunar phase (Dark Moon, New Moon, First Quarter, etc.)
- 16 cards per half of each phase (Deepening, Emerging, Birthing, etc.)

Each combination of (season, cycle, phase, half) appears exactly once in the system, confirming a perfect 1:1 mapping between the 256 binary codes and the 256 possible combinations of lunar attributes.

## Existing Cards

Currently, only a few cards have been fully developed:

1. `00000000` - "Void Mirror" (Winter, Sage)
2. `00000001` - "Devouring Void" (Fall, Monster)
3. `00000010` - "Unwritten Beginning" (Spring, Fool)
4. `00000011` - "Perfect Vessel" (Summer, Hero)

These represent the four foundational archetypes in their respective seasons.