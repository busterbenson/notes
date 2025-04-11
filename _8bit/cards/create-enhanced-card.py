#\!/usr/bin/env python3
"""
8-Bit Oracle Enhanced Card Creator

This script takes a binary code and a card description, combines them with 
associations data, and enhances the card description file with additional
information.

Usage:
    python create-enhanced-card.py <binary_code> <description_file>
    
Example:
    python create-enhanced-card.py 00000000 completed/000000/00000000.md
"""

import sys
import os
import yaml
import argparse
import re
from datetime import datetime

# Configuration
COMPILED_DIR = "compiled"
MARKDOWN_SEPARATOR = "\n\n---\n\n"

def load_yaml_file(file_path):
    """Load a YAML file and return its contents."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def load_description_file(file_path):
    """Load and parse the card description file."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Check if file already has the enhanced content (separated by markdown)
    if MARKDOWN_SEPARATOR in content:
        content = content.split(MARKDOWN_SEPARATOR)[0]
    
    return content

def find_association_file(binary_code):
    """Find the association file for the given binary code."""
    hexagram = binary_code[:6]
    file_path = os.path.join(COMPILED_DIR, hexagram, f"{binary_code}.yml")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Association file for {binary_code} not found at {file_path}")
    
    return file_path

def extract_card_name(description_content):
    """Extract the card name from the description content."""
    match = re.search(r'### 2\. CARD NAME\s+(.*?)(?=###|\Z)', description_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Fallback to looking for a line with "CARD NAME" in all caps
    lines = description_content.split('\n')
    for line in lines:
        if line.strip() and line.strip().isupper() and "CARD NAME" not in line:
            return line.strip()
    
    return "Unknown Card"

def extract_essence(description_content):
    """Extract the essence from the description content."""
    match = re.search(r'### 1\. ESSENCE\s+(.*?)(?=###|\Z)', description_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Try to find essence section in other format
    lines = description_content.split('\n')
    for i, line in enumerate(lines):
        if "ESSENCE" in line.upper() and i+1 < len(lines) and lines[i+1].strip():
            return lines[i+1].strip()
    
    return ""

def extract_key_symbols(description_content):
    """Extract key symbols from the description content."""
    match = re.search(r'### 3\. KEY SYMBOLS\s+(.*?)(?=###|\Z)', description_content, re.DOTALL)
    if match:
        symbols_text = match.group(1).strip()
        symbols = [symbol.strip().strip('-').strip() for symbol in symbols_text.split('\n') if symbol.strip()]
        return symbols
    
    # Try to find key symbols section in other format
    symbols = []
    lines = description_content.split('\n')
    found_symbols_section = False
    
    for i, line in enumerate(lines):
        if "KEY SYMBOLS" in line.upper():
            found_symbols_section = True
            continue
        
        if found_symbols_section and line.strip().startswith('-'):
            symbols.append(line.strip().strip('-').strip())
        elif found_symbols_section and len(symbols) > 0 and not line.strip():
            break
    
    return symbols

def extract_full_description(description_content):
    """Extract the full card description."""
    match = re.search(r'### 4\. CARD DESCRIPTION\s+(.*?)(?=###|\Z)', description_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Try to find card description in other format
    description_text = ""
    lines = description_content.split('\n')
    found_description_section = False
    
    for i, line in enumerate(lines):
        if "CARD DESCRIPTION" in line.upper():
            found_description_section = True
            continue
        
        if found_description_section and i+1 < len(lines):
            # Skip empty lines at the beginning
            if not description_text and not line.strip():
                continue
            
            # Stop at next section heading
            if line.startswith('###') or line.startswith('##'):
                break
                
            description_text += line + '\n'
    
    return description_text.strip()

def get_season_name(bit78):
    """Get the season name from bits 7-8."""
    seasons = {
        "00": "Winter",
        "10": "Spring",
        "11": "Summer",
        "01": "Fall"
    }
    return seasons.get(bit78, "Unknown")

def format_associations_markdown(binary_code, associations):
    """Format the associations data as markdown."""
    hexagram_data = associations.get('hexagram', {})
    iching = hexagram_data.get('iching_associations', {})
    journey = hexagram_data.get('evolutionary_journey', {})
    
    inner_world = associations.get('inner_world', {})
    outer_world = associations.get('outer_world', {})
    archetype = associations.get('archetype', {})
    
    bit_assoc = associations.get('bit_associations', {}).get('bit78', {})
    season = bit_assoc.get('season', '')
    element = bit_assoc.get('element', '')
    
    lunar_cycle = associations.get('lunar_cycle', {})
    related_cards = associations.get('related_cards', {})
    symbolism = associations.get('symbolic_associations', {})
    
    # Format the associations as markdown
    markdown = f"""# SYSTEM ASSOCIATIONS

## Basic Information
- **Binary Code:** {binary_code}
- **Decimal:** {int(binary_code, 2)}
- **Hexadecimal:** {hex(int(binary_code, 2))[2:].upper()}

## Hexagram (Bits 1-6: {binary_code[:6]})
- **I Ching Number:** {iching.get('label', '')}
- **I Ching Name:** {iching.get('name', '')}
- **Keywords:** {', '.join(iching.get('keywords', []))}
- **Natural Element:** {symbolism.get('i_ching', {}).get('natural_element', '')}

## Evolutionary Journey
- **Position:** {journey.get('journey_position', '').replace('_', ' ').title()} - {journey.get('position_description', '')}
- **Shadow Challenge:** {journey.get('shadow_challenge', '')}
- **Gift Potential:** {journey.get('gift_potential', '')}
- **Siddhi Realization:** {journey.get('siddhi_realization', '')}

## Archetype
- **Name:** {archetype.get('name', '')}
- **Color:** {archetype.get('color', '')}
- **Qualities:** {', '.join(symbolism.get('archetype_qualities', []))}

## Inner World (Bits 1-3: {binary_code[:3]})
- **Name:** {inner_world.get('name', '')}
- **Color:** {inner_world.get('color', '')}

## Outer World (Bits 4-6: {binary_code[3:6]})
- **Name:** {outer_world.get('name', '')}
- **Color:** {outer_world.get('color', '')}

## Season & Element (Bits 7-8: {binary_code[6:8]})
- **Season:** {season}
- **Element:** {element}
- **Seasonal Elements:** {', '.join(symbolism.get('seasonal_elements', []))}

## Lunar Cycle
- **Phase:** {lunar_cycle.get('phase', '')}
- **Phase Half:** {lunar_cycle.get('phase_half', '')}

## Related Cards
- **Opposite:** {related_cards.get('opposite', '')}
- **Same Card (Winter):** {related_cards.get('same_card_winter', '')}
- **Same Card (Spring):** {related_cards.get('same_card_spring', '')}
- **Same Card (Summer):** {related_cards.get('same_card_summer', '')}
- **Same Card (Fall):** {related_cards.get('same_card_fall', '')}
"""
    
    return markdown

def update_description_file(binary_code, description_file, associations):
    """Update the card description file with enhanced content."""
    # Load the original description content
    original_content = load_description_file(description_file)
    
    # Format associations as markdown
    associations_md = format_associations_markdown(binary_code, associations)
    
    # Create the enhanced content - just add the associations without the image prompt
    enhanced_content = f"{original_content}{MARKDOWN_SEPARATOR}{associations_md}"
    
    # Write back to the same file
    with open(description_file, 'w') as file:
        file.write(enhanced_content)
    
    return description_file

def main():
    """Main function to create an enhanced card."""
    parser = argparse.ArgumentParser(description='Create an enhanced 8-Bit Oracle card.')
    parser.add_argument('binary_code', help='8-bit binary code (e.g., 00000000)')
    parser.add_argument('description_file', help='Path to the card description file')
    args = parser.parse_args()
    
    try:
        binary_code = args.binary_code
        hexagram = binary_code[:6]
        
        # Verify binary code format
        if not re.match(r'^[01]{8}$', binary_code):
            raise ValueError("Binary code must be exactly 8 bits (0s and 1s)")
        
        # Load the association data
        association_file = find_association_file(binary_code)
        associations = load_yaml_file(association_file)
        
        # Load the description content
        description_content = load_description_file(args.description_file)
        
        # Update the description file with associations only
        output_path = update_description_file(binary_code, args.description_file, associations)
        
        print(f"Enhanced card description saved to: {output_path}")
        print("\nNext steps:")
        print("1. Review the enhanced description file and ensure all sections are completed:")
        print("   - Essence (5-7 words)")
        print("   - Card Name")
        print("   - Key Symbols (3-5)")
        print("   - Visual Description (150-200 words)")
        print("   - Questions for Reflection")
        print("   - Connections to other cards")
        print("\n2. Create a custom image prompt in the image_prompts directory:")
        print(f"   mkdir -p image_prompts/{hexagram}")
        print(f"   touch image_prompts/{hexagram}/{binary_code}.md")
        print("\n   Use the examples in image_prompts/101010/ as templates")
        print("\n3. Use the custom image prompt to generate card artwork")
        print(f"   Save the image to: card_images/completed/{hexagram}/{binary_code}-[card-name].png")
        print("\nIMPORTANT: Image generation should ALWAYS happen after both the narrative arc AND all card")
        print("           description sections have been completed to ensure visual and thematic coherence.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
