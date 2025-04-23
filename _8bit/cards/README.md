# 8-Bit Oracle Card Generation Tools

This directory contains tools for generating 8-Bit Oracle cards based on binary codes.

## Overview

The 8-Bit Oracle is a binary-based system for divination and self-reflection. Each card is represented by an 8-bit binary code (e.g., `10101010`).

- The first 6 bits (`xxxxxx__`) represent the hexagram (inner and outer resources)
- The last 2 bits (`______xx`) represent the season (Winter=00, Spring=10, Summer=11, Fall=01)

## Complete Card Creation Workflow

Follow these steps to create a fully developed card:

### 1. Generate the Card Template

Generate the basic structure for your card:

```bash
# For a single card
./generate-card.sh 10101010

# For all four seasonal variations of a hexagram
./generate-hexagram.sh 101010

# To generate all 256 possible cards
./generate-all-cards.py
```

This creates YAML files in the `generated/` directory with correct associations, but placeholder content.

### 2. Create or Update the Narrative Arc

Each hexagram (first 6 bits) should have a narrative arc that provides consistent storytelling across its four seasonal cards:

1. Create a markdown file at `arcs/hexagram/<6-bit-code>.md` if it doesn't exist
2. Follow the structure in existing arc files, including:
   - **Overview** - Brief introduction to the hexagram's significance
   - **Narrative Fable** - A short story that embodies the hexagram's journey
   - **Core Theme** - The central narrative thread
   - **Visual Narrative Continuity** - How visual elements evolve across seasons
   - **Character Development** - How archetypes progress through the arc

Example: `arcs/hexagram/101010.md` for all cards with binary pattern 101010xx.

### 3. Fill in Card Details

Edit the generated YAML file (`generated/<binary-code>.yml`) to replace placeholders with meaningful content:

1. **Basic Info Section**:
   - Write a comprehensive description of the card's core energy and meaning
   - Add 5-6 evocative keywords that capture the card's essence
   - Add 5-6 symbolic elements that represent the card visually

2. **Direct Associations**: 
   - These are mostly pre-filled by the generator
   - Review for accuracy, particularly the meanings of inner/outer worlds

3. **Interpreted Meanings**:
   - **Card Name**: Create an evocative name that reflects the card's energy
   - **Card Creature**: Describe a mythological figure that embodies the card's energy
   - **Question Posed**: Create a reflective question this card asks the querent
   - **Card Scene**: Write a detailed visual description of the card imagery
   - **Universal Symbol**: Identify a core symbol that captures the essence
   - **Mood**: Describe the emotional/energetic quality

4. **Image Prompt**:
   - Complete the image generation prompt with specific details
   - Ensure it incorporates the correct colors and symbolic elements
   - Include references to the seasonal and archetypal elements

5. **Fractal Meanings**:
   - Develop interpretations of how this pattern manifests at different scales
   - Fill in all six fractal levels from quantum to cosmic

Refer to `card-example-00000000.yml` for a fully completed example.

### 4. Generate Card Image

Use the completed image prompt to create the card image:

1. Copy the completed image prompt from the YAML file
2. Submit it to an AI image generation service (like Midjourney or DALL-E)
3. Save the final image to `card_images/completed/<binary-code>-card-name.png`
4. Consider generating multiple variations and selecting the best one

### 5. Validate Card Associations

Verify that the card's associations are correctly calculated:

1. **Lunar Cycle Validation**:
   - Check that lunar phase, phase half, and cycle match what's in `/sorts/binary_sort.md`
   - The lunar phase should be `(decimal_value ÷ 2) % 8`
   - The phase half should be `decimal_value % 2` (0 = Early, 1 = Late)
   - The lunar cycle should be `((decimal_value % 64) ÷ 16) + 1`

2. **Archetype Validation**:
   - Verify the archetype is correctly determined based on resonant and actual seasons
   - Count 1s in inner world (bits 1-3): if 2+ bits are 1, inner = 1; otherwise inner = 0
   - Count 1s in outer world (bits 4-6): if 2+ bits are 1, outer = 1; otherwise outer = 0
   - Map inner-outer to resonant season: 00 = Winter, 10 = Spring, 11 = Summer, 01 = Fall
   - Compare resonant season to actual season (bits 7-8)

3. **Gender Validation**:
   - Count the number of 1s in bits 1-6:
   - If 0 or 6 bits: All archetypes should be gender-neutral
   - If 3 or 5 bits: Hero/Monster should be feminine, Fool/Sage should be masculine
   - If 2 or 4 bits: Hero/Monster should be masculine, Fool/Sage should be feminine

### 6. Refine and Iterate

Review the complete card and make refinements:

1. Check that the card name, description, and image are consistent
2. Ensure all symbolic elements are appropriate for the card's energy
3. Verify that the card fits within the narrative arc for its hexagram
4. Check that related cards section is filled with appropriate connections

## Scripts

### Generate a Single Card

To generate a single card:

```bash
./generate-card.sh <binary_code>
```

Example:

```bash
./generate-card.sh 10101010
```

This will create a YAML file for the card in the `generated/` directory.

### Generate All Cards for a Hexagram

To generate all four seasonal variations for a specific hexagram:

```bash
./generate-hexagram.sh <6-bit_code>
```

Example:

```bash
./generate-hexagram.sh 101010
```

This will create four YAML files (one for each season) in the `generated/` directory.

## Generated Card Files

The generated card files contain:

- Basic information (binary code, decimal, hexadecimal)
- Direct associations (archetype, gender, colors, trigrams, etc.)
- Interpreted meanings (card name, description, imagery)
- Related cards (same hexagram in different seasons, opposites)
- Bit values and fractal meanings

## Directory Structure

- `generate-card.py` - Python script for generating a single card
- `generate-card.sh` - Shell wrapper for the Python script
- `generate-hexagram.sh` - Shell script to generate all four seasonal cards for a hexagram
- `generate-all-cards.py` - Script to generate all 256 possible cards
- `generated/` - Directory containing generated card files
- `card-template.yml` - Template for card structure
- `card-example-00000000.yml` - Example of a completed card
- `arcs/` - Directory containing narrative arcs for hexagrams
- `image_prompts/` - Directory for extracted image prompts
- `archived_scripts/` - Directory containing older scripts that have been replaced

## Dependencies

These scripts rely on several reference files:

- `../associations/core-systems.yml` - Core bit definitions and meanings
- `../associations/composite-associations.yml` - Combined frameworks
- `../associations/lunar-cycle.yml` - Lunar phase information
- `../associations/gender-assignment.md` - Gender assignment rules

## Card Attributes

Key attributes of each card include:

- **Archetype**: Sage, Fool, Hero, or Monster (based on the relationship between resonant season and card season)
- **Gender**: Masculine, feminine, or neutral (based on bit count)
- **Inner World**: Meaning derived from bits 1-3
- **Outer World**: Meaning derived from bits 4-6
- **Season**: Derived from bits 7-8
- **Lunar Phase**: Calculated based on decimal value

## Example Usage

```bash
# Generate the Void Mirror card (00000000)
./generate-card.sh 00000000

# Generate all four seasonal variations of hexagram 000000
./generate-hexagram.sh 000000

# Generate all cards for a random hexagram
RANDOM_HEX=$(python -c "import random; print(''.join([str(random.randint(0, 1)) for _ in range(6)]))")
./generate-hexagram.sh $RANDOM_HEX
```