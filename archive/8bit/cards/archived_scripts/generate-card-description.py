#!/usr/bin/env python3
"""
8-Bit Oracle Card Description Generator

This script takes a binary code and generates a full card description prompt
ready to be used with ChatGPT or similar LLMs. It combines the raw associations
from the compiled data with a synthesis prompt template to create a deep,
resonant card interpretation.

Usage:
    python generate-card-description.py <binary_code>
    
Example:
    python generate-card-description.py 00000000
"""

import sys
import os
import yaml
import argparse
import json

# Configuration
COMPILED_DIR = "compiled"
PROMPT_TEMPLATE_PATH = "card-synthesis-prompt.md"
OUTPUT_DIR = "card_descriptions"

def load_yaml_file(file_path):
    """Load a YAML file and return its contents."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def load_prompt_template():
    """Load the card synthesis prompt template."""
    with open(PROMPT_TEMPLATE_PATH, 'r') as file:
        return file.read()

def find_association_file(binary_code):
    """Find the appropriate association file for the given binary code."""
    if len(binary_code) != 8:
        raise ValueError("Binary code must be 8 bits (e.g., 00000000)")
    
    hexagram = binary_code[:6]
    full_code = binary_code
    
    file_path = os.path.join(COMPILED_DIR, hexagram, f"{full_code}.yml")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Association file for {binary_code} not found at {file_path}")
    
    return file_path

def generate_context_summary(associations):
    """Generate a summary of the key associations for context."""
    # Extract key information
    binary_code = associations.get('binary_code', '')
    
    # Basic Info
    hexagram_data = associations.get('hexagram', {})
    iching = hexagram_data.get('iching_associations', {})
    journey = hexagram_data.get('evolutionary_journey', {})
    
    # Archetype
    archetype = associations.get('archetype', {})
    archetype_name = archetype.get('name', '')
    
    # Seasonal info
    season = associations.get('bit_associations', {}).get('bit78', {}).get('season', '')
    
    # Inner and outer world
    inner_world = associations.get('inner_world', {})
    outer_world = associations.get('outer_world', {})
    
    # Lunar cycle
    lunar_cycle = associations.get('lunar_cycle', {})
    
    # Name suggestions
    suggested_names = associations.get('suggested_names', {})
    
    # Symbolic associations
    symbolic_associations = associations.get('symbolic_associations', {})
    suggested_symbols = symbolic_associations.get('suggested_symbols', [])
    core_symbolism = symbolic_associations.get('core_symbolism', {})
    
    # Extract richer symbolic information
    i_ching_symbolism = core_symbolism.get('i_ching', {})
    gene_key_symbolism = core_symbolism.get('gene_key', {})
    seasonal_elements = core_symbolism.get('seasonal_elements', [])
    archetype_qualities = core_symbolism.get('archetype_qualities', [])
    
    # Extract bit meaning information
    bit_associations = associations.get('bit_associations', {})
    bit_meanings = {}
    for i in range(1, 7):
        bit_key = f'bit{i}'
        if bit_key in bit_associations:
            bit_data = bit_associations[bit_key]
            bit_meanings[bit_key] = {
                "name": bit_data.get('name', ''),
                "domain": bit_data.get('domain', ''),
                "value": bit_data.get('value', ''),
                "meaning": bit_data.get('meaning', '')
            }
    
    # Build context summary
    context = {
        "binary_code": binary_code,
        "binary_structure": {
            "bits_1_3": binary_code[0:3] + " (Inner World: " + inner_world.get('trigram', '') + ")",
            "bits_4_6": binary_code[3:6] + " (Outer World: " + outer_world.get('trigram', '') + ")",
            "bits_7_8": binary_code[6:8] + " (Season: " + season + ")",
            "bit_meanings": bit_meanings
        },
        "hexagram": {
            "binary": hexagram_data.get('binary', ''),
            "i_ching": {
                "number": iching.get('number', ''),
                "name": iching.get('traditional_name', ''),
                "label": iching.get('label', ''),
                "meaning": iching.get('core_meaning', ''),
                "trigram_relationship": iching.get('trigram_relationship', '')
            },
            "gene_key": {
                "number": journey.get('gene_key_number', ''),
                "shadow": journey.get('shadow_challenge', ''),
                "gift": journey.get('gift_potential', ''),
                "siddhi": journey.get('siddhi_realization', ''),
                "journey_position": journey.get('journey_position', ''),
                "journey_description": journey.get('position_description', '')
            }
        },
        "archetype": {
            "name": archetype_name,
            "expression": archetype.get('expression', ''),
            "cycle_position": archetype.get('cycle_position', '')
        },
        "worlds": {
            "inner": {
                "trigram": inner_world.get('trigram', ''),
                "name": inner_world.get('name', ''),
                "quality": inner_world.get('qualities', '')
            },
            "outer": {
                "trigram": outer_world.get('trigram', ''),
                "name": outer_world.get('name', ''),
                "quality": outer_world.get('qualities', '')
            }
        },
        "season": season,
        "lunar_phase": lunar_cycle.get('phase', ''),
        "lunar_cycle": lunar_cycle.get('complete_designation', ''),
        "suggested_names": suggested_names.get('alternatives', []) if 'alternatives' in suggested_names else [],
        "primary_name": suggested_names.get('primary', '') if 'primary' in suggested_names else '',
        "key_symbols": [symbol.get('name', '') for symbol in suggested_symbols if 'name' in symbol][:5],
        "symbolism": {
            "i_ching": {
                "natural_element": i_ching_symbolism.get('natural_element', ''),
                "combined_image": i_ching_symbolism.get('combined_image', '')
            },
            "gene_key": {
                "shadow_objects": gene_key_symbolism.get('shadow_objects', []),
                "gift_objects": gene_key_symbolism.get('gift_objects', []),
                "siddhi_objects": gene_key_symbolism.get('siddhi_objects', []),
                "evolutionary_narrative": gene_key_symbolism.get('evolutionary_narrative', '')
            },
            "seasonal_elements": seasonal_elements,
            "archetype_qualities": archetype_qualities
        },
        "related_cards": {
            "opposite": associations.get('related_cards', {}).get('opposite', ''),
            "same_hexagram_cycle": [
                associations.get('related_cards', {}).get('same_hexagram_winter', ''),
                associations.get('related_cards', {}).get('same_hexagram_spring', ''),
                associations.get('related_cards', {}).get('same_hexagram_summer', ''),
                associations.get('related_cards', {}).get('same_hexagram_fall', '')
            ]
        }
    }
    
    return context

def create_synthesis_prompt(binary_code, associations):
    """Create a synthesis prompt for the given binary code using the template."""
    # Load template
    template = load_prompt_template()
    
    # Replace binary code placeholder
    prompt = template.replace("[INSERT-BINARY-CODE]", binary_code)
    
    # Generate context summary
    context = generate_context_summary(associations)
    
    # Add context json at the end of the prompt
    prompt += "\n\n## Association Context (JSON)\n\n```json\n"
    prompt += json.dumps(context, indent=2)
    prompt += "\n```\n"
    
    return prompt

def main():
    """Main function to generate a card description prompt."""
    parser = argparse.ArgumentParser(description='Generate an 8-Bit Oracle card description prompt.')
    parser.add_argument('binary_code', help='8-bit binary code (e.g., 00000000)')
    parser.add_argument('-o', '--output', help='Output file path (default: stdout)')
    args = parser.parse_args()
    
    try:
        # Find and load the association file
        file_path = find_association_file(args.binary_code)
        associations = load_yaml_file(file_path)
        
        # Create synthesis prompt
        prompt = create_synthesis_prompt(args.binary_code, associations)
        
        # Create output directory if it doesn't exist
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Write to file or stdout
        if args.output:
            output_path = args.output
        else:
            output_path = os.path.join(OUTPUT_DIR, f"{args.binary_code}_description_prompt.md")
            
        with open(output_path, 'w') as file:
            file.write(prompt)
            
        print(f"Card description prompt generated and saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()