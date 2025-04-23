# Image Prompts for 8-Bit Oracle Cards

This directory contains custom image generation prompts for the 8-Bit Oracle cards. These prompts are organized by hexagram and provide detailed specifications for creating visually distinct yet thematically connected artwork for each card.

## Directory Structure

The image prompts are organized by hexagram:

```
image_prompts/
  ├── 000000/              # Hexagram 000000
  │   ├── 00000000.md      # Winter card
  │   ├── 00000010.md      # Spring card
  │   ├── 00000011.md      # Summer card
  │   └── 00000001.md      # Fall card
  ├── 101010/              # Hexagram 101010
  │   ├── 10101000.md      # Winter card
  │   ├── 10101010.md      # Spring card
  │   ├── 10101011.md      # Summer card
  │   └── 10101001.md      # Fall card
  └── [other hexagrams]
```

## Integration with Card Generation

These image prompts can be created from the image prompt sections in the generated card YAML files:

1. Generate a card using the new card generation tools:
   ```bash
   cd /Users/buster/projects/notes/_8bit/cards
   ./generate-card.sh 10101010
   ```

2. Fill in the card details in the generated YAML file, including the `prompt_for_image_gen` section.

3. Extract the completed image prompt and save it as a separate file in this directory for reference and organization.

## Image Prompt Structure

Each image prompt follows a consistent structure:

1. **Introduction and Card Identity**
   - Card name and binary code
   - Essence statement
   - Dramatic distinction requirement

2. **Archetype Integration**
   - Character energy
   - Environmental resonance
   - Visual language
   - Symbolic expression
   - Time quality

3. **Technical Specifications**
   - Card dimensions and style
   - Margin guidelines
   - Typography and font guidance
   - Color palette

4. **Content Elements**
   - Key symbolic elements
   - Full visual description
   - Seasonal narrative coherence
   - Character and scene integration

5. **Layout Requirements**
   - Title bar specifications
   - Card naming and text placement

## Example and Templates

- The `101010/` hexagram provides complete examples of well-structured image prompts for all four seasonal cards
- Use these as templates when creating new prompts
- Reference `../enhanced-image-prompt-template.md` for additional guidance

## Creating New Image Prompts

When creating a new image prompt:

1. Use the completed `prompt_for_image_gen` section from the generated card YAML file
2. Ensure strong archetype integration based on the seasonal archetype
3. Emphasize visual distinction while maintaining thematic connection to other cards in the hexagram
4. Include specific references to how the central motifs evolve across the four seasonal cards

## Archetype-Specific Elements

Each seasonal archetype requires specific visual qualities in the image prompts:

- **Spring/Sage:** Symmetrical, balanced composition with integration of opposites
- **Summer/Fool:** Dynamic, asymmetrical composition with playful, spontaneous energy
- **Fall/Hero:** Directional composition with focused energy and purposeful action
- **Winter/Monster:** Complex, tension-filled composition with transformative, boundary-crossing elements

## Usage in Image Generation

These prompts should be used with AI image generation tools or provided to artists as comprehensive guidelines for creating the card artwork. The detailed specifications ensure consistency across the 8-Bit Oracle deck while allowing for dramatic visual distinction between the seasons.