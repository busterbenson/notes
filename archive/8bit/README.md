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

- `/cards/` - Card generation scripts and data files
  - `generate-card.py` - Python script to generate a complete card
  - `generate-card.sh` - Shell wrapper to generate a single card
  - `generate-hexagram.sh` - Script to generate all four seasonal cards for a hexagram
  - `card-template.yml` - Template for card structure
  - `card-example-00000000.yml` - Example card with all fields filled in
  - `/generated/` - Generated card files with complete structure
  - `/arcs/` - Narrative arc documentation for hexagrams
  - `/image_prompts/` - Custom image generation prompts

- `/card_images/` - Generated card images
  - Images named by pattern (e.g., `00000000-void-mirror.png`)

## Card Generation Workflow

For the complete, detailed workflow on generating cards, creating narrative arcs, and filling in card details, please refer to the [README.md](/cards/README.md) in the cards directory.

The comprehensive guide includes:
- Generating card templates with the correct associations
- Creating narrative arcs for hexagrams
- Filling in creative card details
- Generating card images
- Validating card associations
- Example prompts for working with AI assistants like Claude

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