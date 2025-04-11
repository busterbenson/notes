# 8-Bit Oracle Associations

This directory contains reference documents and mappings for the 8-Bit Oracle divination system. These files provide detailed explanations of the symbolic frameworks and their integration within the system.

## Core Reference Files

- **core-systems.yml**: Main structured data file containing all bit definitions, patterns, and meaning systems
- **archetype-guide.md**: Explanation of the archetype system (Sage, Fool, Hero, Monster)
- **bits-to-decimal.yml**: How to convert bits to decimals, prioritizing bits left-to-right 
- **fractal-manifestations.md**: Framework for interpreting patterns across different scales
- **gender-assignment.md**: Rules for gender assignment in different archetypes
- **gene-keys-reference.md**: Overview of the Gene Keys system and its integration 
- **lunar-cycle.yml**: Complete lunar cycle system with phase-half precision mapping
- **quick-reference-guide.md**: Concise lookup tables for card interpretation

## Composite Association Files

- **composite-associations.yml**: Uses the associations in the core assocations reference files, and builds upon them, combining or expanding on them within a larger context.

## Using These References

While the `core-systems.yml` file contains the structured data needed for card generation, the markdown and yaml files provide deeper context, rationale, and detailed explanations that wouldn't fit well in YAML format.

The files in this directory serve several purposes:

1. **Documentation**: They explain the reasoning behind specific mappings and associations
2. **Learning Resources**: They help users understand the complex symbolic systems integrated in the oracle
3. **Reference Material**: They provide details that can enrich card interpretations
4. **System Architecture**: They document how different symbolic systems interrelate

## Bit Masks

Some associations will include a "bit_mask" attribute that will describe which bits in the 8-bit sequence are mapped to a specific association. The 3 values that the bit_mask can have are 1, 0, and X. 1 means that that bit must be a 1 to map to the related association, and similarly 0 means that the bit must be a 0 in that spot to be associated. X means that it doesn't matter if the bit in that location is a 0 or a 1. For example, 1XXXXXXX for "intuition" means that the first bit MUST be a 1, and the other 7 bits can be 0s or 1s. On the other hand, 000000XX means that the first 6 bits MUST be 0x for the association to be value, although the last 2 bits can be 0 or 1. 

In some cases, ? will also be used to simply denote which bit(s) are relevant to the association, in the sense that the bit_mask for the inner_world is ???XXXXX, meaning that the first 3 bits are what determine the inner_world, and that those values can be 0s or 1s, but that the 4th through 8th bits are not relevant to determining the inner_world.

## Generating Cards

### To generate all the compiled card asssociation files:
Simply run:
  cd /Users/buster/projects/notes/_8bit/cards
  ./generate-all-associations.py

## Related Resources

For the development history and analysis that led to these associations, see the documents in the `/mapping_plans/` directory.