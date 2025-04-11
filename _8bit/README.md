# 8-Bit Oracle

A divination system based on 8-bit binary patterns, combining elements of tarot, I Ching, and other symbolic frameworks.

## Project Structure

### Directories

- `/associations/` - Reference documents and core data
  - `core-systems.yml` - Core associations for bits, trigrams, elements, etc.
  - `archetype-guide.md` - Guide to the Sage/Fool/Hero/Monster system
  - `gender-assignment.md` - Documentation for gender assignment rules
  - `fractal-manifestations.md` - Framework for fractal interpretation
  - `tarot-final-mapping.md` - Final mapping of tarot cards to bit patterns
  - `hebrew-letter-major-arcana.md` - Hebrew letter associations
  - `gene-keys-reference.md` - Gene Keys correspondences
  - `quick-reference-guide.md` - Quick lookup for associations

- `/mapping_plans/` - Development documents for the tarot-to-binary mapping
  - Contains evaluation and analysis of different mapping approaches

#### Cards and card images stored in folders like v3 (currently on v3) 
#### When archived they will be moved to the archive/v3 folder
- `/cards/[version]/[6-bit code]/[8-bit code].yml` - Individual card files organized by pattern similarity
  - `card-template.yml` - Template for creating new cards with complete structure
  - `card-example-00000000.yml` - Example card (The Moon in Winter) with all fields filled in
  - Organized in subdirectories by first 6 bits (e.g., `/000000/`, `/010010/`)
  - Each card is named by its binary pattern (e.g., `00000000.yml`)

- `/card_images/` - Generated card images organized by pattern similarity
  - Same subdirectory structure as `/cards/`
  - Images may have multiple versions with numbering (e.g., `00000000-void-mirror.0.png`)

## Card Generation Workflow

1. **Create a new card file**:
   - Copy `/cards/card-template.yml` to the appropriate subdirectory in `/cards/`
   - Name it according to its binary pattern (e.g., `01010101.yml`)
   - Fill in all fields based on the template

2. **Generate card image**:
   - Use the `prompt_for_image_gen` field in your card file
   - Pass this to your image generation system
   - Save the result in the corresponding subdirectory in `/card_images/`
   - Name format: `{binary}-{card_name}.{version}.png` (e.g., `00000000-void-mirror.0.png`)

## Binary Pattern Structure

- **Bits 1-3** (Inner World): Intuition, Ability, Capacity
- **Bits 4-6** (Outer World): Expectations, Support, Options
- **Bits 7-8** (Cycle): Seasonal/Elemental phase
  - `00`: Winter/Air/Swords/New Moon
  - `10`: Spring/Fire/Wands/Waxing Moon
  - `11`: Summer/Water/Cups/Full Moon
  - `01`: Fall/Earth/Pentacles/Waning Moon

## Archetypes and Seasons

Each hexagram pattern (bits 1-6) has a resonant season where it appears as the Sage archetype. The pattern cycles through the archetypes in this order:

1. **Sage**: Wisdom, transcendence, integration (resonant season)
2. **Fool**: Innocence, new beginnings, spontaneity
3. **Hero**: Skill, mastery, directed action
4. **Monster**: Shadow, excess, challenge

## Gender Assignment

Gender of archetypes is determined by bit count:
- For patterns with 0 or 6 bits set to 1: All archetypes are gender-neutral
- For patterns with 3 or 5 bits set to 1: Hero and Monster are feminine, Fool and Sage are masculine
- For patterns with 2 or 4 bits set to 1: Hero and Monster are masculine, Fool and Sage are feminine
