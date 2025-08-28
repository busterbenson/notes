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

#### Prompt for Generating a Narrative Arc with Claude

Use this template to ask Claude to generate a narrative arc for a hexagram:

```
Please create a narrative arc for the 8-Bit Oracle hexagram [XXXXXX].

I need a comprehensive narrative arc document that will provide consistent storytelling across all four seasonal expressions of this hexagram.

For context:
- This hexagram corresponds to I Ching hexagram [#] [NAME] ([LABEL])
- The Gene Key journey is from [SHADOW] through [GIFT] to [SIDDHI]
- The inner trigram is [TRIGRAM NAME] and the outer trigram is [TRIGRAM NAME]
- The primary quality of this hexagram is [DESCRIPTION]

Please structure the narrative arc with these sections:
1. Overview - A brief introduction to this hexagram's significance and energy
2. Narrative Fable - A short story that embodies this hexagram's journey through the seasons
3. Core Theme - The central narrative thread connecting all four seasonal expressions
4. Evolutionary Journey - How this hexagram represents stages in consciousness development
5. Visual Narrative Continuity - How visual elements should evolve across the four seasonal cards
6. Character Development - How the central figure/entity transforms through the four archetypal expressions (Fool → Hero → Monster → Sage)
7. Symbolic Continuity - Key symbols that should appear in all four cards but transform seasonally
8. Narrative Arc Structure - Detailed breakdown of each seasonal card's storyline
9. Integration Points - Connections to psychological or spiritual frameworks
10. Questions for Integration - Reflective prompts for readings involving multiple cards in this hexagram

Ensure the narrative shows dramatic transformation across seasons while maintaining thematic continuity.
```

Replace the bracketed information with details from the generated card file or associations files.

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

#### Prompt for Completing Card Details with Claude

Use this template to ask Claude to complete the details for a specific card:

```
Please help me complete the 8-Bit Oracle card for binary code [XXXXXXXX].

I have the generated template with all the basic associations, but I need help filling in the creative and interpretive elements to create a rich, cohesive card. I'll provide the key information from the generated file and the narrative arc for this hexagram.

Key Information:
- Binary: [XXXXXXXX]
- Decimal: [DDD]
- Archetype: [ARCHETYPE]
- Gender: [GENDER]
- Season: [SEASON]
- Inner World: [INNER TRIGRAM] ([INNER COLOR])
- Outer World: [OUTER TRIGRAM] ([OUTER COLOR])
- Archetype Color: [COLOR]
- Lunar Phase: [PHASE] - [HALF] ([CYCLE_NAME] of [SEASON])
- I Ching Hexagram: [NUMBER] [NAME] ([LABEL])
- Gene Key Journey: [SHADOW] → [GIFT] → [SIDDHI]

Narrative Arc Context:
[PASTE RELEVANT SECTIONS FROM THE HEXAGRAM'S NARRATIVE ARC]

Please provide the following elements for this card:

1. Basic Info:
   - A rich, detailed description (150-200 words) of this card's core energy and meaning
   - 6 evocative keywords that capture this card's essence
   - 6 symbolic elements that would represent this card visually

2. Interpreted Meanings:
   - Card Name: An evocative name that captures this energy (consider subtle mythological references)
   - Card Creature: A detailed description of a [GENDER] mythological figure that embodies this card's energy
   - Question Posed: A profound, reflective question this card asks the querent
   - Card Scene: A vivid, detailed description (200-250 words) of the card's imagery, incorporating:
     * The [INNER COLOR] for foreground elements
     * The [OUTER COLOR] for background elements
     * [ARCHETYPE COLOR] highlights
     * The lunar phase symbolism
     * Seasonal elements appropriate for [SEASON]
     * The archetypal energy of the [ARCHETYPE]
   - Universal Symbol: The core symbolic element that captures this card's essence
   - Mood: The emotional/energetic quality of this card

3. Fractal Manifestations:
   - For each level (quantum, biological, psychological, social, ecological, cosmic), provide:
     * A specific pattern that manifests this card's energy at that scale
     * An insight about reality this pattern reveals

4. Image Generation Prompt:
   - A complete, detailed prompt for generating this card's image, incorporating all the visual elements

Make sure all elements align with:
- The [ARCHETYPE] expression in [SEASON]
- The [GENDER] energy
- The combination of [INNER TRIGRAM] and [OUTER TRIGRAM]
- The Journey from [SHADOW] through [GIFT] to [SIDDHI]
- The narrative arc for this hexagram
```

Replace the bracketed information with details from the generated card file and the narrative arc document. Adjust the "Narrative Arc Context" section to include the most relevant portions of the narrative arc for this specific card's season and archetype.

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