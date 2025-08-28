# 8-Bit Oracle Card Images (v2)

This directory contains the v2 version of 8-bit Oracle card images following the refined lunar cycle system and standardized style guidelines.

## Directory Structure

Card images should be organized in subdirectories based on their bit patterns:
- First create a directory for the first 6 bits: e.g., `/000000/`
- Within that directory, place image files with the naming convention: 
  - `{binary}-{card-name}.{version}.png`
  - Example: `00000000-void-mirror.0.png`

Example path: `/v2/000000/00000000-void-mirror.0.png`

## Image Specifications

All card images should follow these specifications:
- **Dimensions**: 1200 x 2000 pixels (3:5 ratio)
- **Resolution**: 300 DPI
- **Format**: PNG with transparency
- **Color Mode**: RGB

## Style Guidelines

All images must adhere to the style guidelines described in `/cards/card-style-guidelines.md`, including:
- Limited color palette (3 colors plus black and white)
- Risograph/woodblock print aesthetic
- Consistent title bar placement
- Standard lunar phase indicator
- Representation of inner/outer world colors
- Archetype color highlights

## Multiple Variations

If multiple versions of a card image are created, use numbered suffixes:
- `00000000-void-mirror.0.png`
- `00000000-void-mirror.1.png`
- `00000000-void-mirror.2.png`

## Final Selection

The preferred version for a card should be indicated in the card's YAML file.