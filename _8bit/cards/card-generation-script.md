# 8-Bit Oracle Card Generation Workflow

This document outlines the process for generating rich, consistent card imagery for the 8-bit Oracle system using the card data files and style guidelines.

## Card Data Extraction Process

For optimal image generation, extract the following data points from each card's YAML file:

### Core Card Information
- **Binary Code**: The 8-bit binary pattern 
- **Decimal Value**: For lunar cycle calculations
- **Card Name**: From `oracle_card.card_name`
- **Archetype**: Sage, Fool, Hero, or Monster

### Color System
- **Inner World Color**: RGB value from the inner trigram (bits 1-3)
- **Inner World Meaning**: For thematic elements
- **Outer World Color**: RGB value from the outer trigram (bits 4-6)
- **Outer World Meaning**: For thematic elements
- **Archetype Color**: Based on archetype (Sage, Fool, Hero, Monster)

### Character and Scene
- **Character Description**: From `oracle_card.card_creature`
- **Gender Assignment**: Based on bit count rules
- **Scene Description**: From `oracle_card.card_scene`
- **Mood Keywords**: From `oracle_card.mood`
- **Universal Symbol**: From `oracle_card.universal_symbol`

### Symbolic Associations
- **Season**: From cycle bits (7-8)
- **Seasonal Elements**: Based on Winter, Spring, Summer, or Fall
- **Tarot Correspondence**: From `tarot.card`
- **I Ching Trigrams**: Both inner and outer
- **Lunar Information**:
  - Phase: Dark Moon, New Moon, First Quarter, etc.
  - Phase Half: Deepening, Emerging, Birthing, etc.
  - Complete Designation: e.g., "Dark Moon Deepening, Inception Cycle of Winter"

### Symbols and Keywords
- **3-5 Key Symbols**: From `basic_info.symbols`
- **3-5 Key Keywords**: From `basic_info.keywords`

## Enhanced Prompt Template

Once all data is extracted, format it into this enhanced prompt template:

```
# 8-Bit Oracle Card Generation Request

## Card Identity
Card: [CARD NAME] ([LUNAR PHASE DESIGNATION])
Binary: [XXXXXXXX]
Archetype: [SAGE/FOOL/HERO/MONSTER]
Decimal: [DDD]

## Color Specification
- Inner World Color: [COLOR NAME] (RGB: xxx,xxx,xxx) - representing [INNER MEANING]
- Outer World Color: [COLOR NAME] (RGB: xxx,xxx,xxx) - representing [OUTER MEANING]
- Archetype Color: [COLOR] - representing [ARCHETYPE]

## Character & Scene
- Gender: [MASCULINE/FEMININE/NEUTRAL]
- Character: [CHARACTER DESCRIPTION]
- Scene Context: [BRIEF SCENE DESCRIPTION]
- Core Symbol: [UNIVERSAL SYMBOL]
- Mood: [MOOD KEYWORDS]

## Symbolic Systems
- Season: [SEASON] - include [SPECIFIC SEASONAL ELEMENTS]
- Lunar Phase: [LUNAR PHASE + HALF] - represent as [DESCRIPTION]
- Tarot Association: [TAROT CARD] - incorporate [KEY TAROT SYMBOLS]
- I Ching: Inner trigram [TRIGRAM NAME], Outer trigram [TRIGRAM NAME]
- Key Symbols: [SYMBOL 1], [SYMBOL 2], [SYMBOL 3]
- Key Concepts: [KEYWORD 1], [KEYWORD 2], [KEYWORD 3]

## Technical Specifications
Follow the complete style guidelines in card-style-guidelines.md, with special attention to:
- Card dimensions: 1200 x 2000 pixels (3:5 ratio)
- Limited color palette: Inner world color, outer world color, archetype color + black outlines and white background
- Risograph/woodblock aesthetic with visible texture
- Title bar (15% height) with "[CARD TITLE]" and "[LUNAR PHASE • XXXXXXXX]" beneath

## Special Instructions
- Clearly distinguish inner world (character/foreground) from outer world (environment/background)
- Include the lunar phase indicator in the upper right corner
- Incorporate the character's archetypal nature into their appearance and posture
- Balance symbolic elements with narrative clarity
- Ensure the image evokes the mood keywords: [MOOD]
```

## Automated Data Extraction

To streamline this process, consider creating a script that:

1. Reads a card's YAML file
2. Extracts all relevant fields
3. Looks up associated color values and meanings
4. Formats the data into the enhanced prompt template
5. Outputs a ready-to-use prompt for image generation

### Example Python Pseudocode

```python
def generate_card_prompt(card_file_path):
    # Load YAML data
    card_data = load_yaml(card_file_path)
    
    # Extract basic information
    binary = card_data['binary']
    decimal = card_data['decimal']
    
    # Extract colors and meanings
    inner_bits = binary[0:3]
    outer_bits = binary[3:6]
    inner_color = get_color_for_trigram(inner_bits)
    outer_color = get_color_for_trigram(outer_bits)
    archetype = get_archetype(card_data)
    archetype_color = get_archetype_color(archetype)
    
    # Extract character and scene
    character = card_data['interpreted_meanings']['oracle_card']['card_creature']
    scene = card_data['interpreted_meanings']['oracle_card']['card_scene']
    mood = card_data['interpreted_meanings']['oracle_card']['mood']
    
    # Get lunar information
    lunar_phase = calculate_lunar_phase(decimal)
    lunar_half = calculate_lunar_half(decimal)
    
    # Format the prompt using template
    prompt = format_prompt_template(
        binary=binary,
        decimal=decimal,
        card_name=card_data['interpreted_meanings']['oracle_card']['card_name'],
        # ... all other extracted data
    )
    
    return prompt
```

## Implementation Recommendations

1. **Batch Processing**: Generate prompts for multiple cards at once
2. **Output Format**: Save prompts as individual text files for easy reference
3. **Visual References**: Include links to reference images for similar cards
4. **Automation**: Consider a system that automates the entire process from card definition to prompt generation
5. **Feedback Loop**: Implement a way to refine prompts based on generated results

## Integration with Image Generation

When submitting to image generation AI:

1. Provide this detailed prompt
2. Include the card-style-guidelines.md link or content
3. If possible, include examples of previously generated cards as reference
4. Request multiple variations and select the one that best follows the guidelines
5. Save final images in the appropriate card_images directory using the naming convention: `XXXXXXXX-card-name.png`

This approach ensures maximum consistency across the deck while capturing the rich symbolic language of each individual card.