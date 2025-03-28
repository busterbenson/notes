# 8-bit Oracle: Project Summary

The 8-bit Oracle is a multidimensional divination and self-reflection system consisting of 256 unique cards, each represented by an 8-bit binary number (00000000 to 11111111). The system creates a bridge between digital binary logic and ancient wisdom traditions, offering a versatile framework for personal insight, divination, and symbolic communication.

## Core Structure

Each card's 8-bit sequence encodes multiple layers of meaning:

### Bit Positions (1-6): Questions of Being
1. **Intuition (Inner/Heart)**: "Do you trust your natural instincts to direct you down the right path?" (0=No, 1=Yes)
2. **Ability (Inner/Hands)**: "Do you have the skills and know-how required to address this question on your own?"
3. **Capacity (Inner/Head)**: "Do your current circumstances provide enough time, space, and resources to address this?"
4. **Expectations (Outer/Heart)**: "Are you aligned with how cultural norms and expectations would want you to address this?"
5. **Support (Outer/Hands)**: "Do your closest relationships and community have your back in this?"
6. **Options (Outer/Head)**: "Are the possible paths that you could choose from clear to you right now?"

### Bit Positions (7-8): Cycles of Nature
Together represent cyclic elements:
- **00**: New moon / Winter / Swords / Air
- **10**: Waxing moon / Spring / Wands / Fire
- **11**: Full moon / Summer / Cups / Water
- **01**: Waning moon / Fall / Pentacles / Earth

## Intersecting Dimensions

The system creates meaningful patterns through overlapping conceptual frameworks:

- **Inner & Outer Worlds**: 
  - Bits 1-3 relate to the inner self, forming the "Inner World"
  - Bits 4-6 connect to the external environment, forming the "Outer World"
  - These groupings determine a card's resonant season and archetype

- **Modes of Experience**: Pairs of bits link to aspects of human experience:
  - Bits 1 & 4: Heart/feelings
  - Bits 2 & 5: Hands/actions
  - Bits 3 & 6: Head/thoughts

- **Traditional Systems**:
  - **I Ching Structure**: 
    - Bits 1-3 form the lower trigram of the I Ching (read bottom to top)
    - Bits 4-6 form the upper trigram of the I Ching (read bottom to top)
    - Together they create the complete hexagram (e.g., 001 = Mountain trigram)
    - Each hexagram appears 4 times in the deck, modified by the final two bits
  
  - **Tarot Correspondences**:
    - The 64 six-bit patterns (bits 1-6) map to major arcana, court cards, and number cards
    - Bits 7-8 modify these with seasonal/elemental qualities
    - Four seasonal variations of each core card create 256 unique cards

## Resonant Seasons and Archetypes

A key feature of the system is how each 6-bit pattern has a resonant season based on its inner/outer world balance:

- **Inner 0, Outer 0 → Winter (00) = Fool**
  - Cards with primarily 0s in both inner and outer worlds
  - Express innocent curiosity, beginner's mind, potential
  
- **Inner 0, Outer 1 → Spring (01) = Hero**
  - Cards with primarily 0s in inner world, primarily 1s in outer world 
  - Express masterful action, confident achievement, skill

- **Inner 1, Outer 1 → Summer (11) = Monster**
  - Cards with primarily 1s in both inner and outer worlds
  - Express excess, shadow aspects, overwhelming power

- **Inner 1, Outer 0 → Fall (10) = Sage**
  - Cards with primarily 1s in inner world, primarily 0s in outer world
  - Express mature wisdom, integration, transcendent understanding

Each 6-bit pattern appears in all four seasons, creating a narrative cycle where the card's energy evolves through different archetypal expressions while maintaining its core essence.

## Card Structure

Each card in the system is defined by several layers of information:

1. **Basic Information**: Binary code, numeric values, keywords, symbols
2. **Direct Associations**: Mappings to traditional systems (I Ching, Tarot, etc.)
3. **Interpreted Meanings**: Synthesized interpretations that integrate all associations
4. **Oracle Card**: Creative expression of the card as part of a divination deck, including:
   - Card name
   - Mythological creature
   - Question posed
   - Scene description
   - Universal symbol
   - Mood
   - Image generation prompt

## Generating Oracle Card Images

To generate images for the oracle cards, use the prompt_for_image_gen field in each card's YAML file. These prompts are carefully crafted to maintain consistency across the deck while capturing each card's unique energy.

### Instructions for Image Generation (for LLMs/Image Models)

1. **Style Guidelines**:
   - Create a limited color risograph-style illustration
   - Use full-bleed composition with the card title integrated into the design
   - Follow the style blend of Rider-Waite Smith tarot symbolism with modern graphic sensibility
   - Incorporate subtle element symbols appropriate to the card's season (Air/Winter, Fire/Spring, Water/Summer, Earth/Fall)
   - Maintain consistency in line weight, texture, and overall aesthetic across all cards

2. **Color Palette**:
   - Use a restricted color palette (3-4 colors maximum)
   - Map inner and outer world colors to foreground and background:
     - Use inner world color (from bits 1-3) for foreground elements and character
     - Use outer world color (from bits 4-6) for background and environment
     - Add accent colors based on seasonal energy
   - Align colors with the card's seasonal energy:
     - Winter/Fool: Deep blues, blacks, whites
     - Spring/Hero: Reds, oranges, yellows
     - Summer/Monster: Deep blues, purples, intense whites
     - Fall/Sage: Earth tones, rusty oranges, browns

3. **Key Elements to Include**:
   - The named mythological creature/character
   - The universal symbol described in the card
   - Clear seasonal indicators (specific moon phase, seasonal elements)
   - The 8-bit binary code of the card (e.g., "00000000")
   - The title of the card incorporated into the design
   - Mood expression through composition, lighting, and character expression

4. **Composition Guidelines**:
   - Place the focal character/creature prominently 
   - Include the scene elements described in the prompt
   - Ensure the universal symbol is clearly identifiable
   - Balance negative space with detailed elements
   - Use geometric patterns and clean lines consistent with risograph printing

## Project Structure

- `/associations.yml` - Core mappings between bits and various systems
- `/card-example.yml` - Template structure for card definitions
- `/cards/` - Directory containing all 256 card definitions
  - `/cards/[hexagram]/` - Folders for each of the 64 hexagrams
    - `/cards/[hexagram]/[hexagram][season].yml` - Individual card files

## Applications

The 8-bit Oracle functions as:
- A divination tool for drawing random cards to gain insight
- A framework for self-reflection by answering the six questions to identify matching patterns
- A symbolic language capable of articulating complex circumstances with precision
- A creative platform for developing unique characters, imagery, stories, art, and music for each card

## Development Roadmap

1. **Complete Card Definitions**: Create all 256 card definitions with full descriptions
2. **Generate Card Imagery**: Create consistent visual representations for all cards
3. **Interactive Tools**: Develop interfaces for divination and self-reflection
4. **Expanded Interpretations**: Add more detailed readings and card combinations

## Card Generation Process

Creating a complete card set for each hexagram requires thorough research, deep symbolic thinking, and consistent application of the system's multi-layered structure. Follow this comprehensive process for each new hexagram:

### Research Phase

1. **Hexagram Analysis**:
   - Look up the hexagram in the `associations.yml` file to identify its I Ching correspondences:
     * Number, name, and traditional meaning
     * Gene Key shadow, gift, and siddhi attributes
   - Analyze the trigram components (bits 1-3 and bits 4-6) and their meanings
   - Note any Tarot correspondences associated with this hexagram pattern
   
2. **Structure Determination**:
   - Count the number of 1s in bits 1-3 to determine Inner World characteristics
   - Count the number of 1s in bits 4-6 to determine Outer World characteristics
   - Calculate the resonant season using the Inner/Outer World pattern:
     * Inner 0, Outer 0 → Winter is resonant
     * Inner 0, Outer 1 → Fall is resonant
     * Inner 1, Outer 0 → Spring is resonant
     * Inner 1, Outer 1 → Summer is resonant
   - Determine the full archetype cycle based on resonant season
   - Calculate gender assignments by counting total 1s in positions 1-6:
     * For 3 or 5 bits set to 1: Hero and Monster are feminine, Fool and Sage are masculine
     * For 2 or 4 bits set to 1: Hero and Monster are masculine, Fool and Sage are feminine
     * For 0 or 6 bits set to 1: All archetypes are gender-neutral
   
3. **Color and Element Research**:
   - Identify the RGB colors for both Inner World (bits 1-3) and Outer World (bits 4-6)
   - Note the qualities associated with these colors
   - Research the seasonal elements for each variation (Air/Winter, Fire/Spring, Water/Summer, Earth/Fall)
   - Consider how colors and elements might interact, contrast, or harmonize

4. **Symbolic Research**:
   - Study the I Ching text for the hexagram to understand its traditional meanings and symbolism
   - Research the Gene Keys interpretation for psychological/evolutionary dimensions
   - If Tarot associations exist, explore the card's traditional imagery and symbolism
   - Consider historical, cultural, and mythological expressions of the core pattern

### Synthesis and Integration

5. **Core Pattern Identification**:
   - Identify the central pattern or dynamic represented by the hexagram
   - Define how this pattern manifests differently through each archetype (Sage, Fool, Hero, Monster)
   - Consider how the pattern might express through different seasonal energies

6. **Fractal Scale Integration**:
   - Develop expressions of the core pattern at multiple scales of existence:
     * Quantum: How does this pattern appear at the subatomic level?
     * Biological: How does it manifest in living systems and organisms?
     * Psychological: How does it express in human cognition and emotion?
     * Social: How does it appear in human relationships and communities?
     * Ecological: How does it manifest in broader natural systems?
     * Cosmic: How might this pattern express at universal scales?
   - Ensure coherence between scales while respecting their unique contexts
   - Look for scientific, philosophical, or spiritual principles that unify these expressions

7. **Opposing and Related Patterns**:
   - Determine the binary opposite of the hexagram by inverting all bits
   - Research this opposite pattern to understand the complementary dynamic
   - Identify meaningful thematic pairs that share important characteristics
   - Consider how the pattern relates to other cards in the system

### Card Creation

8. **Naming and Conceptualization**:
   - Create evocative names for each seasonal variation that capture its essence
   - Develop distinct archetypal characters that embody each expression
   - Formulate insightful questions that probe the pattern's relevance to human experience
   - Design a universal symbol that encapsulates the core dynamic

9. **Scene Development**:
   - Create rich scene descriptions that integrate:
     * **The appropriate gender expression for each archetype (REQUIRED)** - always determine the gender based on bit count and apply consistently through all card elements
     * Seasonal elements and qualities
     * Inner and outer world colors
     * Fractal expressions of the pattern at multiple scales
     * I Ching, Gene Key, and Tarot symbolism where relevant
   - Ensure scenes illustrate the core pattern while differentiating archetypal expressions
   - The gender assignment (masculine, feminine, or gender-neutral) MUST be clearly reflected in:
     * All descriptive text about the character
     * Pronouns used throughout the scene description
     * Physical descriptions and attributes
     * The image generation prompt
   - Include appropriate symbolic objects, environments, and interactions

10. **Technical Specifications**:
    - Define the exact binary code, decimal, and hexadecimal values
    - Set appropriate color values for inner world, outer world, and accents
    - Create accurate image generation prompts following style guidelines
    - Document all related cards and their relationships

### Quality Assurance

11. **Consistency Checks**:
    - Verify alignment with structural rules (season determination, archetype cycle, gender assignment)
    - Ensure symbolic consistency across all four seasonal variations
    - Check that fractal expressions maintain the same core pattern while varying appropriately by archetype
    - Confirm that colors, elements, and seasons are correctly integrated

12. **Coherence Review**:
    - Evaluate whether the cards collectively tell a coherent story about the pattern's evolution
    - Verify that the cards create meaningful connections to related patterns in the system
    - Assess whether the cards offer valuable insight for divination and self-reflection

## Related Cards Logic

Each card in the 8-bit Oracle system has meaningful relationships with other cards in the deck. These relationships help navigate the system's complex interconnections and provide additional context for interpretations.

### Seasonal Variations and Cycles

Every 6-bit pattern (bits 1-6) appears in all four seasons, creating a narrative arc as the card evolves through different archetypal expressions:

1. **Determining the Resonant Season**:
   - Each 6-bit pattern has a "resonant season" where it appears as its most integrated form (the Sage archetype)
   - The resonant season is determined by the balance of 0s and 1s in the inner and outer worlds:
     * Inner 0 (majority 0s in bits 1-3), Outer 0 (majority 0s in bits 4-6) → Winter is resonant (Sage in Winter)
     * Inner 0 (majority 0s in bits 1-3), Outer 1 (majority 1s in bits 4-6) → Fall is resonant (Sage in Fall)
     * Inner 1 (majority 1s in bits 1-3), Outer 0 (majority 0s in bits 4-6) → Spring is resonant (Sage in Spring)
     * Inner 1 (majority 1s in bits 1-3), Outer 1 (majority 1s in bits 4-6) → Summer is resonant (Sage in Summer)

2. **Archetype Cycle**:
   - Starting from the resonant season (when the card is a Sage), the archetypes follow this cycle:
     * Resonant season = Sage archetype
     * Next season in cycle = Fool archetype 
     * Following season = Hero archetype
     * Final season = Monster archetype
   - This creates a complete narrative journey for each 6-bit pattern as it moves through the seasons

3. **Gender Assignment System**:
   - The gender of each card's archetypal character is determined by counting the number of 1s in bits 1-6:
     * For 3 or 5 bits set to 1: Hero and Monster are feminine, Fool and Sage are masculine
     * For 2 or 4 bits set to 1: Hero and Monster are masculine, Fool and Sage are feminine
     * For 0 or 6 bits set to 1: All archetypes are gender-neutral
   - This creates balanced gender representation across the deck while maintaining consistent patterns
   - **IMPORTANT**: The gender assignment MUST be explicitly reflected in all aspects of the card, including:
     * The card_creature description (use clear gender terms like "feminine", "masculine", "male", "female")
     * The card_scene narrative (use appropriate pronouns and gendered descriptors)
     * The prompt_for_image_gen (specify gender for clear image generation)
   - Examples:
     * Card 101101 (The Clinging) has 4 bits set to 1, so Hero and Monster are masculine, Fool and Sage are feminine
     * Card 010010 (The Abysmal) has 2 bits set to 1, so Hero and Monster are masculine, Fool and Sage are feminine
     * Card 000000 (The Moon) has 0 bits set to 1, so all its archetypes are gender-neutral

4. **Related Cards in Each Card File**:
   Each card file contains a `related_cards` section that identifies:
   - The same 6-bit pattern in different seasons (full_cycle array)
   - The card's opposite (inverting all 8 bits)
   - Thematic pairs and meaningful connections
   - The order of cards in the full_cycle is based on the card's resonant season:
     * Starts with the resonant season (Sage)
     * Follows with the subsequent seasons in natural order: Winter → Spring → Summer → Fall
     * Example: If Summer is resonant, the order is: Summer(Sage) → Fall(Fool) → Winter(Hero) → Spring(Monster)

### Determining Card Relationships Example

For card `00000000` (The Moon in Winter):
- 6-bit pattern: 000000
- Inner world (bits 1-3): 000 (all 0s → Inner = 0)
- Outer world (bits 4-6): 000 (all 0s → Outer = 0)
- Inner 0, Outer 0 means Winter is the resonant season (Sage in Winter)
- Card `00000000` is therefore the Winter version (Sage archetype)
- The full cycle follows from Winter in the natural seasonal order: 
  * Winter (00) = `00000000` = Sage
  * Spring (10) = `00000010` = Fool
  * Summer (11) = `00000011` = Hero
  * Fall (01) = `00000001` = Monster
- The opposite card is `11111111` (The Sun in Summer), which inverts all bits
- With 0 bits set to 1, all archetypes for this 6-bit pattern are gender-neutral

These relationships create a rich tapestry of interconnected meanings that help reveal deeper insights when cards are read together or in sequence.

## Philosophical Foundation

The system embraces paradox and interconnection, acknowledging that all circumstances are part of larger cycles. It offers precision through binary logic while recognizing the cyclical nature of existence. By synthesizing ancient wisdom traditions with contemporary symbolic frameworks, the 8-bit Oracle creates a unique tool for navigating life's complexities.