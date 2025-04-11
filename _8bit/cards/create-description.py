#!/usr/bin/env python3
"""
8-Bit Oracle Card Description Generator

This script generates a structured card description in markdown format based on the
hexagram and seasonal expression, following the enhanced v3 format with expanded
reflection questions covering different fractal levels.

Usage:
    python create-description.py <binary_code>
    
Example:
    python create-description.py 00000000
"""

import sys
import os
import yaml
import argparse
import re
from datetime import datetime
from pathlib import Path

# Configuration
COMPILED_DIR = "compiled"
OUTPUT_DIR = "completed"
ARCS_DIR = "arcs"
PROMPT_TEMPLATE_PATH = "card-synthesis-prompt.md"

def load_yaml_file(file_path):
    """Load a YAML file and return its contents."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def load_prompt_template():
    """Load the card synthesis prompt template."""
    with open(PROMPT_TEMPLATE_PATH, 'r') as file:
        template = file.read()
    return template

def load_narrative_arc(hexagram):
    """Load the narrative arc information for a hexagram if it exists."""
    arc_path = Path(ARCS_DIR) / "hexagram" / f"{hexagram}.md"
    if not arc_path.exists():
        return None
    
    with open(arc_path, 'r') as file:
        arc_content = file.read()
    return arc_content

def find_association_file(binary_code):
    """Find the association file for the given binary code."""
    hexagram = binary_code[:6]
    file_path = os.path.join(COMPILED_DIR, hexagram, f"{binary_code}.yml")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Association file for {binary_code} not found at {file_path}")
    
    return file_path

def create_blank_description(binary_code, associations):
    """Create a blank card description template from the associations."""
    # Extract key information
    hexagram_data = associations.get('hexagram', {})
    iching = hexagram_data.get('iching_associations', {})
    journey = hexagram_data.get('evolutionary_journey', {})
    
    # Get colors and elements
    inner_world = associations.get('inner_world', {})
    outer_world = associations.get('outer_world', {})
    archetype = associations.get('archetype', {})
    
    inner_color = inner_world.get('color', '')
    outer_color = outer_world.get('color', '')
    
    season = associations.get('bit_associations', {}).get('bit78', {}).get('season', '')
    element = associations.get('bit_associations', {}).get('bit78', {}).get('element', '')
    
    # Extract symbolic elements
    symbolism = associations.get('symbolic_associations', {})
    natural_element = symbolism.get('i_ching', {}).get('natural_element', '')
    seasonal_elements = symbolism.get('seasonal_elements', [])
    archetype_qualities = symbolism.get('archetype_qualities', [])
    
    # Create naming inspirations section
    naming_section = f"""
## Card Naming Inspirations
Consider these elements when crafting the perfect name for this card:

**Core Meanings:**
- I Ching: {iching.get('name', '')} (#{iching.get('label', '')})
- Shadow → Gift → Siddhi: {journey.get('shadow_challenge', '')} → {journey.get('gift_potential', '')} → {journey.get('siddhi_realization', '')}
- Journey Stage: {journey.get('journey_position', '').replace('_', ' ').title()} - {journey.get('position_description', '')}

**Energetic Qualities:**
- Archetype: {archetype.get('name', '')} ({', '.join(archetype_qualities) if archetype_qualities else ''})
- Season: {season} with {element} element
- Inner World: {inner_world.get('name', '')} ({inner_color})
- Outer World: {outer_world.get('name', '')} ({outer_color})

**Symbolic Elements:**
- Natural Element: {natural_element}
- Seasonal Symbols: {', '.join(seasonal_elements) if seasonal_elements else ''}
- I Ching Keywords: {', '.join(iching.get('keywords', [])) if iching.get('keywords') else ''}

**Naming Approaches:**
1. A paradoxical pairing that reveals the card's core tension (e.g., "Fertile Emptiness," "Silent Thunder")
2. A metaphorical state embodying transformation (e.g., "Threshold of Becoming")
3. An image-rich phrase from visual symbolism (e.g., "Midnight Blossom")
4. A poetic essence with emotional depth (e.g., "Whisper Before Dawn")
5. A subtle evocation of mythological or fable themes (e.g., "Underworld Reflection," "Echo's Promise," "Stones of Wisdom")

**Mythological/Fable Themes to Subtly Evoke:**
- For Winter/Dormancy themes: Enchanted sleep, underworld journeys, mirrors, suspended animation, hibernation wisdom
- For Spring/Emergence themes: Reflective pools, metamorphosis, unexpected beauty, stolen light, first flight
- For Summer/Fullness themes: Golden touch, royal illusions, soaring heights, abundant feast, crowned glory
- For Fall/Release themes: Rebirth from ashes, sacred wounds, ancient seas, farewell voyages, falling feathers

Remember, the perfect name evokes the unique spirit of this exact binary pattern while avoiding generic seasonal labels. It should feel mystical yet accessible, with mythological allusions that are subtle enough to have "plausible deniability" - suggesting a connection to familiar stories without directly naming characters or explicitly referencing specific tales.
"""
    
    # Create reference section
    reference_section = f"""
## Reference Information

**Binary Code:** {binary_code}
**Hexagram:** {binary_code[:6]} ({iching.get('label', '')}: {iching.get('name', '')})
**Season:** {season}
**Element:** {element}

**Archetype:** {archetype.get('name', '')}
**Inner World:** {inner_world.get('name', '')} ({inner_color})
**Outer World:** {outer_world.get('name', '')} ({outer_color})

**Evolutionary Journey:** {journey.get('journey_position', '').replace('_', ' ').title()} - {journey.get('position_description', '')}
- Shadow: {journey.get('shadow_challenge', '')}
- Gift: {journey.get('gift_potential', '')}
- Siddhi: {journey.get('siddhi_realization', '')}

**Keywords:**
- {iching.get('keywords', [''])[0] if iching.get('keywords') else ''}
- {journey.get('gift_potential', '')}
- {seasonal_elements[0] if seasonal_elements else ''}
"""

    # Get template and update with binary code
    template = load_prompt_template()
    template = template.replace("[INSERT-BINARY-CODE]", binary_code)
    
    # Load narrative arc information if available
    hexagram = binary_code[:6]
    narrative_arc = load_narrative_arc(hexagram)
    
    # Create narrative arc section if available
    narrative_arc_section = ""
    if narrative_arc:
        # Determine season based on bits 7-8
        season_bits = binary_code[6:8]
        season_mapping = {
            "00": "Winter",
            "10": "Spring",
            "11": "Summer",
            "01": "Fall"
        }
        season = season_mapping.get(season_bits, "Unknown")
        
        narrative_arc_section = f"""
## Narrative Arc Context
This card is part of the {hexagram} hexagram narrative arc, representing the {season} expression of this energy pattern.

The following information provides context about how this card fits into the larger story of this hexagram:

```
{narrative_arc}
```

When creating this card's description, ensure that it:
1. Maintains thematic continuity with other cards in this hexagram family
2. Appropriately represents the {season} stage of this journey
3. Contains references to the central motifs that evolve through this narrative arc
4. Shows DRAMATIC VISUAL TRANSFORMATION compared to other seasonal cards

IMPORTANT: Follow the guidelines in the arc-transformation-guidelines.md file to ensure that this card represents a distinctly different scene from the other seasonal cards - not merely a variation of the same scene but a fundamentally different moment in the narrative journey. The character, environment, and symbolic elements should all be visually transformed to represent this specific stage.
"""
    
    # Add the naming inspiration, narrative arc (if available), and reference information at the end
    template += "\n" + naming_section + "\n"
    if narrative_arc_section:
        template += narrative_arc_section + "\n"
    template += reference_section
    
    return template

def save_description_file(binary_code, content):
    """Save the card description to the appropriate directory structure."""
    hexagram = binary_code[:6]
    directory = os.path.join(OUTPUT_DIR, hexagram)
    os.makedirs(directory, exist_ok=True)
    
    file_path = os.path.join(directory, f"{binary_code}.md")
    with open(file_path, 'w') as file:
        file.write(content)
    
    return file_path

def main():
    """Main function to create a card description template."""
    parser = argparse.ArgumentParser(description='Create an 8-Bit Oracle card description template.')
    parser.add_argument('binary_code', help='8-bit binary code (e.g., 00000000)')
    args = parser.parse_args()
    
    try:
        binary_code = args.binary_code
        
        # Verify binary code format
        if not re.match(r'^[01]{8}$', binary_code):
            raise ValueError("Binary code must be exactly 8 bits (0s and 1s)")
        
        # Load the association data
        association_file = find_association_file(binary_code)
        associations = load_yaml_file(association_file)
        
        # Create the description template
        description_content = create_blank_description(binary_code, associations)
        
        # Save the description template
        output_path = save_description_file(binary_code, description_content)
        print(f"Card description template saved to: {output_path}")
        print("\nNext steps:")
        print("1. FIRST, ensure the narrative arc for this hexagram is completed in arcs/hexagram/")
        print("2. Open the file and fill in EACH SECTION with rich, visual descriptions:")
        print("   - Essence (5-7 words)")
        print("   - Card Name")
        print("   - Key Symbols (3-5)")
        print("   - Visual Description (150-200 words)")
        print("   - Questions for Reflection (covering different fractal levels)")
        print("   - Connections to other cards")
        print("3. Once ALL sections are complete, proceed to image generation")
        print("\nIMPORTANT: Card descriptions MUST be completed before image generation")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()