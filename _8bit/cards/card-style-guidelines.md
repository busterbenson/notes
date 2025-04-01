# 8-Bit Oracle Card Generation Style Guide

## Project Overview

The 8-Bit Oracle is a divination system based on 8-bit binary patterns that combines elements of tarot, I Ching, astrology, and other symbolic frameworks into a cohesive system. Each card represents a unique binary pattern where:

- **Bits 1-3**: Inner world resources (Intuition, Ability, Capacity)
- **Bits 4-6**: Outer world resources (Expectations, Support, Options)
- **Bits 7-8**: Seasonal cycle (Winter, Spring, Summer, Fall)

Each card embodies a specific archetype (Sage, Fool, Hero, or Monster) and lunar phase based on mathematical properties of its pattern. The binary structure creates a system where each card represents a specific day in the natural calendar, linking cosmic patterns to human experience.

The imagery for each card should visually represent these symbolic layers while maintaining a consistent aesthetic across the deck. Cards should evoke their binary nature through a limited color palette that represents inner world, outer world, and archetypal energies.

## Card Dimensions and Layout
- **Aspect Ratio**: 3:5 (traditional tarot card proportions)
- **Resolution**: 1200 x 2000 pixels
- **Orientation**: Portrait
- **Safe Zone**: Keep essential elements 10% away from edges

## Typography and Text Elements
- **Title Bar**: Full-width band at bottom, height = 15% of card
- **Title Text**: Centered, bold sans-serif (Futura or similar), all caps, white text
- **Subtitle**: Centered below title, smaller size, containing lunar phase and 8-bit code
- **Text Format**: "[CARD TITLE]" in large size with "[LUNAR PHASE • BINARY CODE]" in smaller size below

## Color System
- **Limited Palette**: Exactly 3 colors per card plus black and white (background)
  1. Inner World Color: Based on the inner trigram's RGB color
  2. Outer World Color: Based on the outer trigram's RGB color
  3. Archetype Color: Sage (Iridescent/Silver), Fool (Turquoise), Hero (Gold), Monster (Purple)
- **Background**: Always white or off-white paper texture
- **Black Lines**: Used for all outlines and details
- **Color Opacity**: Varies between 60-100% to create texture and depth
- **Color Application**: Inner world color for foreground elements and character, outer world color for environment and background, archetype color for highlights and symbolic elements

## Illustration Style
- **Technique**: Risograph/woodblock print aesthetic with visible texture
- **Line Work**: Bold, confident black outlines of varying thickness
- **Texture**: Visible grain and slightly imperfect ink distribution
- **Composition**: Clear focal point centered or using rule of thirds
- **Depth**: Limited perspective, somewhat flattened but not completely 2D
- **Abstraction Level**: Balanced between symbolic and representational

## Mandatory Elements
- **Lunar Phase Indicator**: Small icon in upper right corner showing exact lunar phase
- **Seasonal Elements**: Background elements that subtly indicate the season
  - Winter: Snow, bare trees, stars, crystals, stillness
  - Spring: New growth, buds, rain, dawn light, movement
  - Summer: Full bloom, sun, abundance, vibrancy, fullness
  - Fall: Falling leaves, harvest elements, dusk light, transition

- **Character Representation**: Follow gender assignment rules precisely
  - Include character description from card template
  - Maintain consistent representation of archetypes (Sage, Fool, Hero, Monster)
  - Sage: Chimeric/multifaceted appearance, timeless
  - Fool: Youthful appearance, movement, spontaneity
  - Hero: Peak form, dynamic pose, masterful presence
  - Monster: Exaggerated, animal/creature hybrid, shadow aspects

- **Scene Setting**: Follow card scene description closely while applying style guidelines
  - Include at least 3 symbolic elements mentioned in card description
  - Ensure scene evokes the mood keywords provided

## Unique Symbolic Systems
- **Inner/Outer World**: Clear visual distinction between character (inner) and environment (outer)
- **I Ching Trigrams**: Subtle incorporation of relevant trigram shapes
- **Lunar Phase**: Visual elements representing the specific lunar phase half
- **Binary Pattern**: Subtle background elements can suggest the card's binary pattern

## Production Notes
- **Layering**: Create clearly separated layers of foreground, midground, background
- **Overlap**: Ensure proper element overlap for depth without overcomplicating
- **Halftones**: Use halftone dots or lines for gradient effects
- **Registration**: Slight misregistration of colors (1-2 pixels) to emulate print process

## Example Prompt Format

```
Create a limited-color risograph-style illustration for the 8-bit Oracle card "[CARD NAME] ([LUNAR PHASE])".

Card dimensions: 1200 x 2000 pixels (3:5 ratio)
Style: Woodblock print/risograph aesthetic with bold lines and limited colors

COLOR PALETTE:
- Inner World (character/foreground): [COLOR] (RGB: xxx,xxx,xxx)
- Outer World (environment/background): [COLOR] (RGB: xxx,xxx,xxx)
- Archetype Highlights: [COLOR] (RGB: xxx,xxx,xxx)
- Black for all lines and details
- White/off-white background

CARD ELEMENTS:
- Main character: [CHARACTER DESCRIPTION]
- Scene: [SCENE DESCRIPTION]
- Lunar phase indicator: Show [LUNAR PHASE] in upper right corner
- Season: Include subtle [SEASON] elements (e.g., [EXAMPLES])
- Symbols: Include [SYMBOL 1], [SYMBOL 2], and [SYMBOL 3]

LAYOUT:
- Full width title bar at bottom (15% of height)
- Title "[CARD TITLE]" in bold, centered, all caps
- Subtitle "[LUNAR PHASE • XXXXXXXX]" below in smaller text
- Main illustration above title bar

STYLE NOTES:
- Bold black outlines with varying thickness
- Visible texture and grain
- Colors applied as flat areas with slight misregistration
- Limited perspective but clear spatial relationships
- Risograph/woodblock print texture throughout
```