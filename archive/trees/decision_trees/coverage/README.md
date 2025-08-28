# Path Coverage Analysis

This directory contains tools and reports for analyzing the coverage of identification paths in the California Tree Guide.

## Files in this Directory

- **`analyze_path_coverage.py`**: Script that analyzes each identification path to determine how many tree species and genera are included, which are exempt, and whether the path is complete.

- **`PATH_COVERAGE_STATS.md`**: Comprehensive statistics for all paths, including:
  - Overall coverage numbers for each path
  - Lists of included species and genera
  - Validation of path completeness

- **`WINTER_PATH_COVERAGE.md`**: Detailed analysis specifically for the Winter Detective Path, including:
  - Coverage statistics for deciduous trees
  - Trees categorized by winter identification features
  - Kid-friendly language assessment
  - Recommendations for enhancement

## Latest Coverage Analysis (2025-04-14)

### Winter Detective Path Coverage

The Winter Detective Path provides exceptional coverage of deciduous trees for winter identification:

- **81 of 81** deciduous species (100% coverage)
- **16 of 17** deciduous genera covered
- Comprehensive coverage of all major deciduous tree features visible in winter
- Kid-friendly language with visual comparisons

This path is specifically designed for identifying deciduous trees in winter when they lack leaves. It focuses on:

1. Tree shape from a distance
2. Branching patterns (opposite vs. alternate)
3. Bark characteristics
4. Bud features
5. Special winter clues (persistent fruits, catkins, etc.)

### Major Findings

Our coverage analysis revealed:

1. **Excellent Overall Coverage**: All paths provide complete coverage of their respective tree categories.
2. **Complete Winter Path Coverage**: The Winter Detective Path now covers 100% of deciduous species in the database.
3. **Kid-Friendly Language**: The Winter Path uses age-appropriate comparisons and terms suitable for children 8-10 years old.
4. **Streamlined Structure**: The guide structure was simplified by removing redundant detective paths, keeping only the essential Winter Detective Path.

## How to Use

### Running the Path Analysis

To update the path coverage statistics (if paths are modified):

```bash
# Navigate to the project root
cd /Users/buster/projects/notes/_trees

# Run the analysis script
python decision_trees/coverage/analyze_path_coverage.py
```

This will generate updated `PATH_COVERAGE_STATS.md` and `WINTER_PATH_COVERAGE.md` files with the latest coverage information.

### Interpreting the Stats

The coverage statistics show:
- How many species and genera are included in each path
- How many are considered exempt from the path
- Whether each path provides comprehensive coverage
- Sample listings of trees included in each path

### Path Completeness

A path is considered complete when:
- All 159 species and 36 genera in our database are either explicitly included in the path or have a valid reason to be exempt
- For the Winter Detective Path, completeness is evaluated against the subset of deciduous trees (81 species, 17 genera)

### Completeness vs. Usability

**Important Project Decision**: For this guide, we have chosen to prioritize **completeness over unwieldiness**. While this may sometimes result in longer, more detailed paths, it ensures that:

1. No trees are excluded from identification
2. All species are accounted for explicitly or through genus-level references
3. Children can identify any California tree they encounter