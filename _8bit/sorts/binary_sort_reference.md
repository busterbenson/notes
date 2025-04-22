# 8-BIT ORACLE BINARY SORT REFERENCE

This document explains the logic and methodology behind the `binary_sort.md` file, which provides a comprehensive reference for all 256 cards in the 8-bit Oracle system sorted by binary value with left-to-right bit significance.

## Left-to-Right Binary Interpretation

In the 8-bit Oracle system, binary codes are interpreted with **left-to-right priority**:

1. The leftmost bit (bit 1) has the value 2^0 = 1
2. The second bit from left (bit 2) has the value 2^1 = 2
3. The third bit from left (bit 3) has the value 2^2 = 4
4. The fourth bit from left (bit 4) has the value 2^3 = 8
5. The fifth bit from left (bit 5) has the value 2^4 = 16
6. The sixth bit from left (bit 6) has the value 2^5 = 32
7. The seventh bit from left (bit 7) has the value 2^6 = 64
8. The eighth bit from left (bit 8) has the value 2^7 = 128

## Binary Sort Order

When sorting cards by binary value:

1. We consider the binary string from left to right
2. This means `10000000` (decimal 1) comes before `01000000` (decimal 2), because we compare the leftmost position first
3. The binary sort produces this specific progressive pattern:
   - The leftmost bit (bit 1) changes every other card
   - The second bit (bit 2) changes every 4 cards
   - The third bit (bit 3) changes every 8 cards
   - And so on

## Correct Binary Sequence (First 16 Cards)

The first 16 cards in proper left-to-right binary order:

```
00000000 = 0    (Void Mirror)
10000000 = 1
01000000 = 2
11000000 = 3
00100000 = 4
10100000 = 5
01100000 = 6
11100000 = 7
00010000 = 8
10010000 = 9
01010000 = 10
11010000 = 11
00110000 = 12
10110000 = 13
01110000 = 14
11110000 = 15
```

Later in the sequence, the known cards appear at these positions:
- `00000001` = 128 (Devouring Void) - position 129
- `00000010` = 64 (Unwritten Beginning) - position 65
- `00000011` = 192 (Perfect Vessel) - position 193

## Card Attribute Calculations

Each card's attributes are calculated based on its binary representation:

### Season Determination (bits 7-8)
- `00` = Winter
- `10` = Spring
- `11` = Summer
- `01` = Fall

### Lunar Cycle Calculation
For each card:
```
lunar_cycle = (count of '1' bits % 4) + 1
```

### Lunar Phase Calculation
For each card:
```
lunar_phase = (l->r decimal_value ÷ 2) % 8
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
phase_half = l->r decimal_value % 2
```

This determines which half of the lunar phase:
- 0: First half (Deepening, Birthing, Challenging, Building, Illuminating, Sharing, Releasing, Distilling)
- 1: Second half (Emerging, Strengthening, Balancing, Culminating, Revealing, Integrating, Resolving, Surrendering)

### Archetype Determination
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

## Importance

This left-to-right priority is critical to maintain consistency across all aspects of the 8-bit Oracle system:

1. It's used for converting binary to decimal
2. It's used for determining lunar phases and cycles
3. It's used for sorting cards in binary order
4. The sort order follows natural bit significance in a left-to-right reading system

## Known Cards

Currently, only four cards have been fully developed:

1. `00000000` - "Void Mirror" (Winter, Sage)
2. `00000010` - "Unwritten Beginning" (Spring, Fool)
3. `00000011` - "Perfect Vessel" (Summer, Hero)
4. `00000001` - "Devouring Void" (Fall, Monster)

These represent the four foundational archetypes in their respective seasons.