#!/usr/bin/env python3
"""
Convert YAML card files in v3/ to markdown files in completed/

This script takes the existing YAML files in the v3/ directory and
converts them to our new markdown format in the completed/ directory.
"""

import os
import yaml
import argparse
from pathlib import Path

def load_yaml_file(file_path):
    """Load a YAML file and return its contents."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def create_md_content(binary_code, card_data):
    """Create markdown content from the YAML card data."""
    # Extract key information from the card data
    card = card_data.get('card', {})
    basic_info = card.get('basic_info', {})
    direct_assoc = card.get('direct_associations', {})
    interpreted = card.get('interpreted_meanings', {})
    oracle_card = interpreted.get('oracle_card', {})
    fractal = card.get('fractal_meanings', {})
    related = card.get('related_cards', {})
    
    # Start building the markdown content
    md_content = f"# 8-Bit Oracle Card: {binary_code}\n\n"
    md_content += f"## Card Code: {binary_code}\n\n"
    
    # Section 1: Essence
    md_content += "### 1. ESSENCE\n"
    essence = basic_info.get('desc', '').split('.')[0] if basic_info.get('desc') else ""
    md_content += f"{essence}\n\n"
    
    # Section 2: Card Name
    card_name = oracle_card.get('card_name', '').split(' (')[0]
    md_content += "### 2. CARD NAME\n"
    md_content += f"{card_name}\n\n"
    
    # Section 3: Key Symbols
    md_content += "### 3. KEY SYMBOLS\n"
    for symbol in basic_info.get('symbols', []):
        md_content += f"- {symbol}\n"
    md_content += "\n"
    
    # Section 4: Card Description
    md_content += "### 4. CARD DESCRIPTION\n"
    md_content += f"{oracle_card.get('card_scene', '')}\n\n"
    
    # Section 5: Questions for Reflection
    md_content += "### 5. QUESTIONS FOR REFLECTION\n\n"
    
    # Add fractal-level questions
    for i, (level, data) in enumerate(fractal.items(), 1):
        pattern = data.get('pattern', '')
        insight = data.get('insight', '')
        
        if level == 'quantum':
            md_content += f"{i}. **Quantum**: How might {insight.lower() if insight else pattern.lower()}?\n\n"
        elif level == 'biological':
            md_content += f"{i+1}. **Biological**: In what ways {insight.lower() if insight else pattern.lower()}?\n\n"
        elif level == 'psychological':
            md_content += f"{i+2}. **Psychological**: When {insight.lower() if insight else pattern.lower()}?\n\n"
            md_content += f"{i+3}. **Psychological**: What {pattern.lower() if insight else 'aspects of your mind'} require attention now?\n\n"
        elif level == 'social':
            md_content += f"{i+4}. **Social**: How might {insight.lower() if insight else pattern.lower()}?\n\n"
            md_content += f"{i+5}. **Social**: In what relationships {pattern.lower() if insight else 'do you notice this pattern'}?\n\n"
        elif level == 'ecological':
            md_content += f"{i+6}. **Ecological**: How does {insight.lower() if insight else pattern.lower()}?\n\n"
        elif level == 'cosmic':
            md_content += f"{i+7}. **Cosmic**: What insights emerge when {insight.lower() if insight else pattern.lower()}?\n\n"
    
    # Section 6: Connections
    md_content += "### 6. CONNECTIONS\n"
    hex_binary = binary_code[:6]
    winter = related.get('same_card_winter', '')
    spring = related.get('same_card_spring', '')
    summer = related.get('same_card_summer', '')
    fall = related.get('same_card_fall', '')
    opposite = related.get('opposite', '')
    
    md_content += f"This card connects to all other cards in the {hex_binary} hexagram family, expressing the {direct_assoc.get('solar_cycle', {}).get('season', '')} aspect of {direct_assoc.get('hexagram', {}).get('i_ching', {}).get('name', '')}. "
    md_content += f"It has a resonant relationship with cards {winter} (Winter aspect) and {opposite} (its opposite). Its full seasonal cycle includes {winter} (Winter), {spring} (Spring), {summer} (Summer), and {fall} (Fall).\n\n"
    
    # Section 7: Technical Description
    md_content += "### 7. TECHNICAL DESCRIPTION\n"
    md_content += f"The {card_name} represents the {direct_assoc.get('solar_cycle', {}).get('season', '')} expression of hexagram {hex_binary} ({direct_assoc.get('hexagram', {}).get('i_ching', {}).get('name', '')}), embodying the {direct_assoc.get('archetype', '')} archetype in its purest form. "
    md_content += f"In this card, inner world ({binary_code[:3]}) and outer world ({binary_code[3:6]}) express as {direct_assoc.get('inner_world', {}).get('trigram', '')} and {direct_assoc.get('outer_world', {}).get('trigram', '')}, creating a field of {oracle_card.get('universal_symbol', '')}.\n\n"
    
    md_content += f"In I Ching terms, this is hexagram {direct_assoc.get('hexagram', {}).get('i_ching', {}).get('number', '')} in its deepest {direct_assoc.get('solar_cycle', {}).get('season', '').lower()} expression. "
    md_content += f"The Gene Key journey begins with the Shadow of {direct_assoc.get('hexagram', {}).get('gene_key', {}).get('shadow', '')}, transforms through the Gift of {direct_assoc.get('hexagram', {}).get('gene_key', {}).get('gift', '')}, "
    md_content += f"and ultimately reveals the Siddhi of {direct_assoc.get('hexagram', {}).get('gene_key', {}).get('siddhi', '')}.\n\n"
    
    md_content += f"This card's wisdom lies in {fractal.get('psychological', {}).get('insight', '')}, while its challenge involves navigating {fractal.get('social', {}).get('pattern', '')}.\n\n"
    
    # Reference Information
    md_content += "## Reference Information\n\n"
    md_content += f"**Binary Code:** {binary_code}\n"
    md_content += f"**Hexagram:** {hex_binary} ({direct_assoc.get('hexagram', {}).get('i_ching', {}).get('number', '')}: {direct_assoc.get('hexagram', {}).get('i_ching', {}).get('name', '')})\n"
    md_content += f"**Season:** {direct_assoc.get('solar_cycle', {}).get('season', '')}\n"
    md_content += f"**Element:** {direct_assoc.get('solar_cycle', {}).get('element', '')}\n\n"
    
    md_content += f"**Archetype:** {direct_assoc.get('archetype', '')}\n"
    md_content += f"**Inner World:** {direct_assoc.get('inner_world', {}).get('trigram', '')} ({direct_assoc.get('inner_world', {}).get('color', '')})\n"
    md_content += f"**Outer World:** {direct_assoc.get('outer_world', {}).get('trigram', '')} ({direct_assoc.get('outer_world', {}).get('color', '')})\n\n"
    
    md_content += "**Evolutionary Journey:** Beginning - The first stage of the journey, representing the initial conditions or challenges that set the journey in motion.\n"
    md_content += f"- Shadow: {direct_assoc.get('hexagram', {}).get('gene_key', {}).get('shadow', '')}\n"
    md_content += f"- Gift: {direct_assoc.get('hexagram', {}).get('gene_key', {}).get('gift', '')}\n"
    md_content += f"- Siddhi: {direct_assoc.get('hexagram', {}).get('gene_key', {}).get('siddhi', '')}\n\n"
    
    md_content += "**Keywords:**\n"
    for keyword in basic_info.get('keywords', [])[:3]:
        md_content += f"- {keyword}\n"
    md_content += "\n\n"
    
    # System Associations
    md_content += "---\n\n# SYSTEM ASSOCIATIONS\n\n"
    md_content += "## Basic Information\n"
    md_content += f"- **Binary Code:** {binary_code}\n"
    md_content += f"- **Decimal:** {card.get('decimal', '')}\n"
    md_content += f"- **Hexadecimal:** {card.get('hexadecimal', '')}\n\n"
    
    md_content += f"## Hexagram (Bits 1-6: {hex_binary})\n"
    md_content += f"- **I Ching Number:** {direct_assoc.get('hexagram', {}).get('i_ching', {}).get('number', '')}\n"
    md_content += f"- **I Ching Name:** {direct_assoc.get('hexagram', {}).get('i_ching', {}).get('name', '')}\n"
    md_content += f"- **Keywords:** {', '.join(basic_info.get('keywords', []))}\n"
    md_content += f"- **Natural Element:** {direct_assoc.get('solar_cycle', {}).get('element', '')}\n\n"
    
    md_content += "## Evolutionary Journey\n"
    md_content += "- **Position:** Beginning - The first stage of the journey, representing the initial conditions or challenges that set the journey in motion.\n"
    md_content += f"- **Shadow Challenge:** {direct_assoc.get('hexagram', {}).get('gene_key', {}).get('shadow', '')}\n"
    md_content += f"- **Gift Potential:** {direct_assoc.get('hexagram', {}).get('gene_key', {}).get('gift', '')}\n"
    md_content += f"- **Siddhi Realization:** {direct_assoc.get('hexagram', {}).get('gene_key', {}).get('siddhi', '')}\n\n"
    
    md_content += "## Archetype\n"
    md_content += f"- **Name:** {direct_assoc.get('archetype', '')}\n"
    md_content += f"- **Color:** {direct_assoc.get('archetype_color', '')}\n"
    md_content += "- **Qualities:** Wisdom, Reflection, Presence\n\n"
    
    md_content += f"## Inner World (Bits 1-3: {binary_code[:3]})\n"
    md_content += f"- **Name:** {direct_assoc.get('inner_world', {}).get('trigram', '')}\n"
    md_content += f"- **Color:** {direct_assoc.get('inner_world', {}).get('color', '')}\n\n"
    
    md_content += f"## Outer World (Bits 4-6: {binary_code[3:6]})\n"
    md_content += f"- **Name:** {direct_assoc.get('outer_world', {}).get('trigram', '')}\n"
    md_content += f"- **Color:** {direct_assoc.get('outer_world', {}).get('color', '')}\n\n"
    
    md_content += f"## Season & Element (Bits 7-8: {binary_code[6:8]})\n"
    md_content += f"- **Season:** {direct_assoc.get('solar_cycle', {}).get('season', '')}\n"
    md_content += f"- **Element:** {direct_assoc.get('solar_cycle', {}).get('element', '')}\n"
    md_content += "- **Seasonal Elements:** Snow, Darkness, Stillness\n\n"
    
    md_content += "## Lunar Cycle\n"
    md_content += f"- **Phase:** {direct_assoc.get('lunar_cycle', {}).get('phase', '')}\n"
    md_content += f"- **Phase Half:** {direct_assoc.get('lunar_cycle', {}).get('phase_half', '')}\n\n"
    
    md_content += "## Related Cards\n"
    md_content += f"- **Opposite:** {related.get('opposite', '')}\n"
    md_content += f"- **Same Card (Winter):** {related.get('same_card_winter', '')}\n"
    md_content += f"- **Same Card (Spring):** {related.get('same_card_spring', '')}\n"
    md_content += f"- **Same Card (Summer):** {related.get('same_card_summer', '')}\n"
    md_content += f"- **Same Card (Fall):** {related.get('same_card_fall', '')}\n\n\n"
    
    # Image Generation Prompt
    md_content += "---\n\n"
    md_content += "# IMAGE GENERATION PROMPT\n\n"
    md_content += f"{oracle_card.get('prompt_for_image_gen', '')}\n"
    
    return md_content

def main():
    """Main function to convert existing YAML files to markdown."""
    parser = argparse.ArgumentParser(description='Convert YAML card files to markdown format.')
    parser.add_argument('--all', action='store_true', help='Convert all YAML files')
    parser.add_argument('--binary', help='Convert a specific binary code card')
    args = parser.parse_args()
    
    v3_dir = Path("v3")
    completed_dir = Path("completed")
    
    if args.binary:
        # Process a single binary code
        binary_code = args.binary
        hexagram = binary_code[:6]
        
        yaml_file = v3_dir / hexagram / f"{binary_code}.yml"
        if not yaml_file.exists():
            print(f"Error: YAML file for {binary_code} not found at {yaml_file}")
            return
        
        # Create the output directory
        output_dir = completed_dir / hexagram
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load the YAML file
        card_data = load_yaml_file(yaml_file)
        
        # Create the markdown content
        md_content = create_md_content(binary_code, card_data)
        
        # Write the markdown file
        output_file = output_dir / f"{binary_code}.md"
        with open(output_file, 'w') as file:
            file.write(md_content)
        
        print(f"Converted {yaml_file} to {output_file}")
    
    elif args.all:
        # Process all YAML files in the v3 directory
        converted_count = 0
        for hexagram_dir in v3_dir.iterdir():
            if hexagram_dir.is_dir():
                for yaml_file in hexagram_dir.glob("*.yml"):
                    binary_code = yaml_file.stem
                    
                    # Create the output directory
                    output_dir = completed_dir / hexagram_dir.name
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Skip if the markdown file already exists
                    output_file = output_dir / f"{binary_code}.md"
                    if output_file.exists():
                        print(f"Skipping {binary_code} - markdown file already exists")
                        continue
                    
                    # Load the YAML file
                    try:
                        card_data = load_yaml_file(yaml_file)
                        
                        # Create the markdown content
                        md_content = create_md_content(binary_code, card_data)
                        
                        # Write the markdown file
                        with open(output_file, 'w') as file:
                            file.write(md_content)
                        
                        print(f"Converted {yaml_file} to {output_file}")
                        converted_count += 1
                    except Exception as e:
                        print(f"Error converting {yaml_file}: {e}")
        
        print(f"Conversion complete. Converted {converted_count} files.")
    
    else:
        print("Please specify either --all to convert all files, or --binary CODE to convert a specific card.")

if __name__ == "__main__":
    main()