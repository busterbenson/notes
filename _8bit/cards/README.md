# 8-bit Oracle Cards

This repository contains files related to the 8-bit Oracle card system - a divination system based on 8-bit binary patterns.

## Key Files

### Card Sorting
- `sorts/lunisolar_sort.md` - Complete ordered listing of all 256 cards in order of seasons and lunar cycles
- `sorts/lunisolar_sort_reference.md` - File with script to generate the circular arrangement

### Card Generation
- `card-template.yml` - Template for creating new cards
- `card-generator.py` - Script to generate card YAML files
- `card-style-guidelines.md` - Visual styling guidelines for cards
- `generate-card.sh` - Helper script for card generation

## Circular Arrangement

The cards are arranged in a circular pattern with several key properties:

1. **Four Concentric Circles** for seasons:
   - Winter (00) - Sage archetype
   - Spring (10) - Fool archetype 
   - Summer (11) - Hero archetype
   - Fall (01) - Monster archetype

2. **Bit-Significance Optimization**:
   - Inner world bits (1-3) change most frequently (87.5% of transitions)
   - Bit 1 (Intuition) changes every other position (50.0%)
   - Only one bit changes between adjacent positions

3. **Accurate Metadata**:
   - Resonant season and archetype based on inner/outer world balance
   - Lunar cycle, phase, and half phase based on bits 1-6, as defined in associations/lunar-cycle.yml and in sorts/lunisolar_sort_reference.md
   - Full information for all 256 cards

## Usage

1. View the complete card order in `sorts/lunisolar_sort.md`

## Card Structure

Each card has an 8-bit binary code where:
- Bits 1-3: Inner world resources (Intuition, Ability, Capacity)
- Bits 4-6: Outer world resources (Expectations, Support, Options)
- Bits 7-8: Seasonal cycle (Winter, Spring, Summer, Fall)

## Moon Phase System

The lunar phase is determined by:
- Phase (8 phases): Decimal value of bits 1-6 modulo 8
- Half (Deepening/Emerging): Determined by bit 7