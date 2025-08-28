# 8-Bit Oracle Archive (v1)

This directory contains the original version of 8-bit Oracle cards and images prior to the implementation of the refined lunar cycle system and standardized card generation process.

## Contents

- `/cards/` - Original card YAML files organized by binary pattern
- `/card_images/` - Original card images organized by binary pattern
- `card-template.yml` - Original card template
- `card-example-00000000.yml` - Original example card

## Notes on v1 System

The v1 cards used a simpler version of the lunar cycle mapping:
- Lunar phases were directly tied to the seasonal cycles (bits 7-8)
- The system didn't provide one-to-one mapping between calendar days and cards
- Card imagery and descriptions had less standardized guidelines

This archive is maintained for reference purposes. All new card development should follow the v2 system specifications, which include:

1. Enhanced lunar cycle system with phase halves
2. Consistent card generation process and style guidelines
3. Direct mapping between calendar days and specific cards
4. Standardized imagery with consistent elements and layout

## Migration to v2

For converting v1 cards to v2 format:

1. Update lunar phase information according to the decimal modulo formula
2. Incorporate phase half designation
3. Add lunar cycle number based on bit count
4. Update card names to include lunar phase information
5. Follow the new style guidelines for image generation

Refer to the main documentation for complete details on the v2 system.