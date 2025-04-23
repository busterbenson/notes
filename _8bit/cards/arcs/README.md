# 8-Bit Oracle Card Narrative Arcs

## Overview

This directory contains narrative arc documentation for the 8-Bit Oracle card system. Narrative arcs capture the storytelling and thematic continuity across related cards, providing a deeper understanding of how individual cards participate in larger patterns and journeys.

All narrative arcs follow the archetypal progression of Fool → Hero → Monster → Sage, which corresponds to the seasonal progression of Spring → Summer → Fall → Winter. This cycle represents the natural development of consciousness from initial awakening, through mastery and challenge, to integration and transcendence, potentially beginning a new cycle at a higher level.

## Integration with Card Generation

When using the new card generation tools, narrative arcs play an important role:

1. Generate cards for a hexagram:
   ```bash
   cd /Users/buster/projects/notes/_8bit/cards
   ./generate-hexagram.sh 101010
   ```

2. Create or update the narrative arc file for the hexagram at `/hexagram/101010.md`

3. Use the narrative arc to inform the details you add to each of the four generated card files, ensuring consistency across the seasonal variations.

## Purpose

The narrative arcs serve multiple functions in the oracle system:

1. **Coherence** - Ensure thematic and visual consistency across related cards
2. **Depth** - Add layers of meaning through contextual relationships
3. **Guidance** - Provide structure for card description generation
4. **Interpretation** - Enhance reading insights when multiple related cards appear

## Directory Structure

The arcs are organized into several categories:

- `/hexagram/` - Narrative arcs for each 6-bit hexagram (spanning its 4 seasonal expressions)
- `/trigram/` - Narrative arcs for each trigram combination (planned)
- `/journeys/` - Narrative arcs for specific evolutionary journeys (planned)
- `/patterns/` - Narrative arcs for mathematical or structural patterns (planned)

## File Format

Each narrative arc file follows a consistent structure:

1. **Overview** - Brief introduction to the arc and its significance
2. **Narrative Fable** - A short story that embodies the arc's journey in accessible, symbolic form
3. **Core Theme** - The central narrative thread that connects all cards in the arc
4. **Evolutionary Journey** - How the cards represent stages in consciousness development
5. **Visual Narrative Continuity** - How visual elements evolve across the cards
6. **Character Development** - How archetypes or characters progress through the arc
7. **Symbolic Continuity** - Consistent symbolic elements that appear across cards
8. **Narrative Arc Structure** - Detailed breakdown of each stage in the journey
9. **Integration Points** - Connections to psychological or spiritual frameworks
10. **Usage in Card Description Generation** - Guidance for maintaining consistency
11. **Questions for Integration** - Prompts for readings involving multiple cards in the arc

## Usage

When generating card descriptions, consult the relevant narrative arc files to ensure each card:

1. Maintains visual and thematic consistency with its related cards
2. Correctly expresses its particular stage in the larger journey
3. Contains appropriate references to other cards in the arc
4. Balances its unique identity with its role in the larger pattern

When multiple cards from the same narrative arc appear in a reading, the arc documentation provides additional context for interpretation beyond what's contained in the individual cards.

## Development Status

- Hexagram arcs: In progress (1/64 complete)
- Trigram arcs: Planned
- Journey arcs: Planned
- Pattern arcs: Planned

## Contribution Guidelines

When adding new narrative arcs:

1. Follow the established template structure
2. Ensure consistency with existing card descriptions
3. Cross-reference related arcs for coherence
4. Balance specificity with open-ended interpretation