# California Tree Guide - Project Decisions & Documentation

This document tracks key decisions, design choices, and implementation details for the California Tree Identification Guide. It serves as a reference for future maintenance and enhancement of the guide.

## Project Overview

The California Tree Identification Guide is designed to help children (ages 8-10) identify trees throughout California using observable features rather than technical botanical knowledge. The guide uses a kid-friendly decision tree approach with multiple entry points based on different tree features.

## Key Statistics

- **Total Tree Coverage**: 165 trees
  - 135 individual species profiles
  - 29 genus-level profiles covering 30 additional species
- **Tree Types**:
  - Conifer trees (needles or scales): 60
  - Broadleaf trees: 86
  - Other (Joshua Tree, California Fan Palm): 3
- **Path Types**:
  - 6 Main Feature Paths
  - 6 Detective Paths
  - 10 Group-specific Pages

## Design Decisions

### 1. Path Organization

Instead of traditional taxonomic organization, we created multiple entry points based on observable features:

- **Main Feature Paths**:
  - Leaf/Needle Path (leaf-needle-path.md)
  - Bark Path (bark-path.md)
  - Smell Path (smell-path.md)
  - Cone/Fruit/Seed Path (cone-fruit-seed-path.md)
  - Flower Path (flower-path.md)
  - Shape/Size Path (shape-size-path.md)

- **Detective Paths**:
  - Leaf Detective Path (leaf-detective-path.md)
  - Needle Detective Path (needle-detective-path.md)
  - Scale Detective Path (scale-detective-path.md)
  - Bark Detective Path (bark-detective-path.md)
  - Silhouette Detective Path (silhouette-detective-path.md)
  - Winter Detective Path (winter-detective-path.md)

### 2. Genus-Level Groupings

For certain trees, we decided to use genus-level groupings rather than individual species profiles when:
- Trees are rarely encountered in California
- Species would be difficult for children to distinguish
- Trees share distinctive genus-level features
- Trees are commonly referred to collectively (e.g., "Birch trees")

These genus files are stored in the `/genus/` directory, while individual species are in the `/trees/` directory.

### 3. Kid-Friendly Features

We implemented several features specifically designed for the target audience (children ages 8-10):

- **Simple Language**: Avoiding botanical jargon throughout all sections
- **"I'm Not Sure" Options**: Help sections at key decision points for uncertain users
- **Cross-Navigation**: "What Else Can You See?" sections linking to alternative paths
- **Difficulty Ratings**: Star system (★, ★★, ★★★) to indicate identification difficulty
- **Seasonal Indicators**: Icons and bloom time ranges for seasonal features
- **Visual ASCII Structure**: Hierarchical tree structure with indentation for visual clarity

### 4. Enhanced Navigation Features

We implemented several features to improve usability:

- **Group Pages**: Dedicated pages for similar species groups (e.g., Oak Group, Pine Group)
- **Multiple Entry Points**: Users can start identification from whatever feature they notice first
- **Winter Identification**: Special path for identifying trees when leaves are absent
- **Cross-References**: Links between related paths and groups

## Implementation Details

### 1. Reference Structure

All paths use a consistent markdown structure:

```
├── MAIN CATEGORY
│   ├── SUBCATEGORY
│   │   ├── SPECIFIC FEATURE → TREE GROUP
│   │   │   ├── Species: Description
│   │   │   ├── Species: Description
│   │   │   └── Species: Description
```

### 2. Decision Tree Navigation Format

Each decision node follows a standardized format:
- Main feature or question
- Options with distinguishing characteristics
- Terminal nodes with species identification
- Occasional redirects to other paths when needed

### 3. Group References

Tree group references use the format:
- `[Group Name](groups/group-name.md)`

### 4. Detective Paths

Detective paths provide more technical information using the same visual structure but with more detailed observations needed.

## Recent Enhancement Decisions

### March-April 2025 Updates

1. **Path Reference Fixes**:
   - Updated references to group files from "trees/group-name.md" to "groups/group-name.md"
   - Applied this change consistently across all path files

2. **Cross-Navigation Sections**:
   - Added "What Else Can You See?" sections to all main path files
   - These provide links to alternative paths based on other observable features
   - Used kid-friendly language focused on what children can actually observe

3. **"I'm Not Sure" Options**:
   - Added help sections for uncertain users at key decision points
   - Implemented in leaf-needle-path.md, bark-path.md, smell-path.md
   - Written in kid-friendly language with simple visual comparisons

4. **Seasonal Indicators**:
   - Added seasonal icons and bloom time ranges to flower-path.md
   - Added seasonal guide legend to provide context about timing
   - Included notes about seasonal availability of flowers

5. **Difficulty Ratings**:
   - Added difficulty rating system (★, ★★, ★★★) to leaf-needle-path.md
   - Applied ratings consistently to conifer identification
   - Added difficulty guide legend explaining the rating system

## Future Enhancement Ideas

1. **Quick Reference Cards**: Printable one-page guides for common trees
2. **Visual Starting Guide**: A flowchart for selecting the best path to start with
3. **Habitat-Based Entry Point**: New path for identifying trees by where they grow
4. **Regional California Path**: Path focused on trees found in specific CA regions
5. **Interactive Quiz Section**: Self-test identification exercises

## Maintenance Notes

### File Organization

- Main path files in /decision_trees/paths/
- Group descriptions in /decision_trees/paths/groups/
- Tree data files in separate directories:
  - Species files: /trees/
  - Genus files: /genus/

### Testing & Updates

When updating path files:
1. Check file links to ensure they point to the correct locations
2. Validate tree references against tree-tracking.md
3. Ensure consistency in formatting and navigation structure
4. Review kid-friendly language throughout all sections

Last Updated: April 11, 2025