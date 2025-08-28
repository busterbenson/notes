# 8-Bit Oracle Cards (v2)

This directory contains the v2 version of 8-bit Oracle cards following the refined lunar cycle system and standardized card generation process.

## Directory Structure

Cards should be organized in subdirectories based on their bit patterns:
- First create a directory for the first 6 bits: e.g., `/000000/`
- Within that directory, place card files named with the full 8-bit pattern: e.g., `00000000.yml`

Example path: `/v2/000000/00000000.yml`

## Card Creation Process

1. Start with the card template (`/cards/card-template.yml`)
2. Calculate all essential properties including:
   - Decimal and hexadecimal values
   - Inner and outer world meanings
   - Hexagram correspondences
   - Lunar phase using the decimal modulo formula
   - Lunar cycle number using the bit count formula
   - Complete lunar designation

3. Create rich descriptive elements:
   - Card name including lunar phase
   - Character description following archetype and gender rules
   - Scene description incorporating seasonal and lunar symbolism
   - Keywords and symbols that capture the card's essence

4. Generate image prompts following the style guidelines in `card-style-guidelines.md`

## Lunar Phase Calculation

- Phase = (decimal_value ÷ 2) % 8
- Phase Half = decimal_value % 2
- Lunar Cycle = (bit_count_positions_1_6 % 4) + 1

## Image Generation

Card images should be generated following the style guidelines and saved in the corresponding directory under `/card_images/v2/`.

## Example

See `card-example-00000000.yml` for a complete example of a v2 card.