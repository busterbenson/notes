# 8-Bit Oracle Card Repository

This directory contains all 256 card files for the 8-Bit Oracle divination system. Each card is represented by an 8-bit binary pattern and stored in a YAML file named after its binary pattern.

## Card Structure

Each card follows this basic structure:
- **Binary Pattern**: 8 digits of 0s and 1s (e.g., 00000000)
- **Bit Values**: Meaning of each activated (1) or unactivated (0) bit
- **Inner World**: State of bits 1-3 representing internal resources
- **Outer World**: State of bits 4-6 representing external resources
- **Cycle Phase**: State of bits 7-8 representing elemental and cyclical phase

## Card Types

### Major Arcana (22 cards)
- These correspond to the 22 Major Arcana cards of the Tarot
- All have even parity (even number of 1s in bits 1-6)
- Associated with Hebrew letters and Tarot archetypes

### Minor Arcana Numbers (10 cards)
- These correspond to the 10 numbered cards of the Tarot (Ace through Ten)
- All have even parity (even number of 1s in bits 1-6)
- Associated with the Sephiroth of the Kabbalistic Tree of Life

### Seasonal Variations (4 variations for each archetype)
- Each archetype appears in all four seasonal phases (bits 7-8)
  - 00: Winter/Air/Swords/New Moon
  - 01: Spring/Fire/Wands/Waxing Moon
  - 11: Summer/Water/Cups/Full Moon
  - 10: Autumn/Earth/Pentacles/Waning Moon

### Odd Parity Cards
- The 32 cards with odd parity (odd number of 1s in bits 1-6)
- These represent transitional or shadow aspects of the archetypes

## File Naming Convention

Cards are named according to their 8-bit binary pattern, with the naming convention "Card of Season":
- `00000000.yml` - Moon of Winter
- `11111111.yml` - Sun of Summer
- `10000000.yml` - Magician of Winter

## Reading the Cards

To read or interpret a card:
1. Look at each individual bit to understand which resources are available
2. Analyze the inner world (bits 1-3) and outer world (bits 4-6) configurations
3. Consider the elemental phase (bits 7-8)
4. Reference the associated systems (I Ching, Tarot, Kabbalah, Music) for deeper insight

## Card Examples

- `00000000.yml` - Moon of Winter (complete absence of resources)
- `11111111.yml` - Sun of Summer (complete presence of all resources)
- `10000000.yml` - Magician of Winter (intuition alone)
- `00111111.yml` - World of Summer (capacity + all outer resources)
- `01010101.yml` - Five of Spring (alternating pattern of resources)