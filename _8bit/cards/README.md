# 8-Bit Oracle Card System

The 8-Bit Oracle is a divination system based on 8-bit binary patterns, combining elements of I Ching, Gene Keys, Tarot, and other traditional wisdom systems.

## Directory Structure

- `compiled/` - Raw associations generated for each card (YAML format)
- `completed/` - Card descriptions with enhanced information (Markdown format)
- `card_images/completed/` - Image files for all cards
- `arcs/` - Narrative arc files for hexagrams
- `image_prompts/` - Custom image generation prompts for cards
- `archived_scripts/` - Deprecated scripts kept for reference

## Card Structure

Each 8-bit card (00000000 to 11111111) consists of:

- Bits 1-3: Inner World Trigram
- Bits 4-6: Outer World Trigram
- Bits 7-8: Seasonal Expression

The combination of bits 1-6 forms the hexagram (000000 to 111111) which maps to traditional I Ching hexagrams and Gene Keys.

## Card Generation Process (v3)

This is the workflow for creating v3 enhanced cards with rich descriptions:

1. **Generate Raw Associations**:
   ```
   ./generate-card.sh --associations 000000
   ```
   This creates associations for a hexagram in the `compiled/` directory.

2. **Create Narrative Arcs** (Required for visual coherence):
   For each hexagram, create a narrative arc that connects the four seasonal cards:
   ```
   # Create a new narrative arc file
   mkdir -p arcs/hexagram
   touch arcs/hexagram/101010.md
   ```
   Use the template in `arcs/hexagram/000000.md` as a guide. The narrative arc is essential for creating visually distinct yet thematically connected seasonal cards.

3. **Generate Full Card with Template**:
   ```
   ./generate-card.sh 00000000
   ```
   This creates a template markdown file in `completed/000000/00000000.md` with empty sections to fill in.

4. **Fill in Card Description**:
   Edit the markdown file to add:
   - Essence (5-7 words)
   - Card Name
   - Key Symbols (3-5)
   - Visual Description (150-200 words)
   - Questions for Reflection (covering different fractal levels)
   - Connections to other cards
   - Technical Description
   
   **IMPORTANT**: The card description MUST be completed before proceeding to image generation. The details you provide here will be incorporated into the image prompt.

5. **Enhance Card with Associations**:
   After completing the card description, enhance it with system associations:
   ```
   python create-enhanced-card.py 00000000 completed/000000/00000000.md
   ```
   This adds:
   - System associations section with symbol and archetype connections
   - Binary, decimal, and hexadecimal conversions
   - I Ching correlations and evolutionary journey information
   - Color assignments and related card references

6. **Create a Custom Image Prompt**:
   
   ```
   # Create directory for image prompts if it doesn't exist
   mkdir -p image_prompts/000000
   
   # Create a markdown file for the image prompt
   touch image_prompts/000000/00000000.md
   ```
   
   Use the files in `image_prompts/101010/` as templates. A good custom image prompt should:
   - Include all the key information from the card description
   - Emphasize the archetype-specific elements (Sage, Fool, Hero, or Monster)
   - Maintain narrative continuity with other cards in the hexagram
   - Provide clear visual specifications for composition, color palette, and style

7. **Generate Card Image**:
   Use the finalized custom image prompt to create card artwork.
   Save images to `card_images/completed/[hexagram]/[binary_code]-[card-name].png`.
   
   **NOTE**: Image generation should ALWAYS happen after both the narrative arc AND the card description have been completed to ensure visual and thematic coherence.

## Ensuring Archetypal Integration and Visual Transformation

For hexagram narrative arcs, follow the guidelines in `arc-transformation-guidelines.md` to ensure dramatic visual transformation across seasonal cards while fully integrating archetypal qualities. Key principles include:

1. **Archetype Embodiment**: Each card must fully express its specific archetype (Sage, Fool, Hero, or Monster) in all visual and thematic elements
2. **Character Evolution**: Characters should undergo substantial transformation in appearance, role, and state of being
3. **Environmental Extremes**: Settings should change dramatically across seasons (not just coloration)
4. **Scale and Perspective Shifts**: Use different viewpoints and scales across the four cards
5. **Time Progression**: Move through different times of day that correspond to the seasons
6. **Symbolic Object Transformation**: Core symbols should transform while maintaining thematic connection

The archetype should inform every aspect of the card design:
- **Sage cards:** Embody wisdom, timelessness, integration of opposites with symmetrical composition
- **Fool cards:** Express curiosity, newness, possibility with dynamic, asymmetrical composition 
- **Hero cards:** Convey purpose, mastery, achievement with focused energy and directional flow
- **Monster cards:** Manifest transformation, dissolution, revelation with complex, tension-filled composition

When creating image prompts, use the examples in `image_prompts/101010/` and the template in `enhanced-image-prompt-template.md` to maintain consistency while ensuring each card has a visually distinct expression.

### Maintaining Consistency Within a Hexagram

For the four seasonal cards in a hexagram, maintain consistency through:

1. **Central Symbol Evolution:** Use the same central symbol (like the cauldron in hexagram 101010) but show it in different states that reflect each season
2. **Character Progression:** Show the same character (like the fox) in different stages of development across the seasons
3. **Color Palette Consistency:** Maintain the inner world (magenta) and outer world (green) colors while varying the accent color by archetype:
   - Sage: Purple/Iridescent
   - Fool: Turquoise
   - Hero: Gold
   - Monster: Purple/Deep Blue
4. **Environment Evolution:** Transform the same environment (like the forest) through seasonal changes
5. **Cross-References:** Include specific references to other cards in the hexagram in each description

## Fractal Levels for Reflection Questions

For the "Questions for Reflection" section, include 6-8 questions spanning these fractal levels:

- **Quantum/Biological**: Patterns at subatomic or biological systems level
- **Psychological**: Personal mindset, thoughts, feelings, individual experience
- **Social/Relational**: Interpersonal dynamics, relationships, community
- **Ecological/Cosmic**: Environmental connections, universal patterns

## Card Description Format

Follow this structure for all card descriptions:

### 1. ESSENCE (5-7 words)
A crystallized seed phrase capturing the card's fundamental energy

### 2. CARD NAME
A memorable, evocative title that balances mystery with clarity

### 3. KEY SYMBOLS (3-5)
Essential archetypal symbols that distill the card's meaning visually

### 4. CARD DESCRIPTION (150-200 words)
A purely visual scene an artist could paint, using concrete, specific imagery. Focus on what appears in the illustration with precise visual details.

### 5. QUESTIONS FOR REFLECTION
6-8 transformative questions spanning different fractal levels (quantum/biological, psychological, social/relational, ecological/cosmic)

### 6. CONNECTIONS
Brief notes on how this card relates to others in the system

### 7. TECHNICAL DESCRIPTION
Analysis of the card's symbolic elements and systems connections

## Enhanced Card Content

After running `create-enhanced-card.py`, each card description will be enhanced with:

1. **System Associations**
   - Basic information (binary, decimal, hexadecimal)
   - Hexagram information (I Ching number, name, keywords)
   - Evolutionary Journey (position, shadow, gift, siddhi)
   - Archetype data (name, color, qualities)
   - Inner/Outer World details
   - Season & Element information
   - Lunar Cycle data
   - Related Cards references

2. **Image Generation Prompt**
   - Card dimensions and style specifications
   - Color palette based on inner/outer world colors
   - Key symbolic elements list
   - Character & scene integration guidance
   - Mood and conceptual depth information
   - Layout specifications for consistent design

## Generating Full 8-Bit Card Set

For each hexagram (000000 to 111111), create four seasonal variations:
- Winter (00)
- Spring (10)
- Summer (11)
- Fall (01)

This results in a total of 256 unique cards (64 hexagrams × 4 seasons).