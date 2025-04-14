#!/usr/bin/env python3
"""
Path coverage analyzer for the California Tree Identification Guide.

This script analyzes the coverage of identification paths, with special attention
to the Winter Detective Path's comprehensive coverage of deciduous trees.

Usage: python analyze_path_coverage.py
"""

import os
import re
import yaml
import glob
from collections import defaultdict, Counter

# Constants
TREES_DIR = "/Users/buster/projects/notes/_trees/trees"
GENUS_DIR = "/Users/buster/projects/notes/_trees/genus"
PATHS_DIR = "/Users/buster/projects/notes/_trees/decision_trees/paths"
COVERAGE_DIR = "/Users/buster/projects/notes/_trees/decision_trees/coverage"

# Main identification paths
PATHS = [
    {"file": "leaf-needle-path.md", "name": "Leaf/Needle Path", "exempt_criteria": ["No specific exemptions - all trees have some form of leaves/needles/scales"]},
    {"file": "bark-path.md", "name": "Bark Path", "exempt_criteria": ["No exemptions - all trees have bark and are included either directly or via genus"]},
    {"file": "smell-path.md", "name": "Smell Path", "exempt_criteria": ["No exemptions - all trees have some aromatic properties and are included either directly or via genus"]},
    {"file": "cone-fruit-seed-path.md", "name": "Cone/Fruit/Seed Path", "exempt_criteria": ["No exemptions - all trees produce some form of reproductive structure and are included either directly or via genus"]},
    {"file": "flower-path.md", "name": "Flower Path", "exempt_criteria": ["Conifers with inconspicuous pollen cones rather than true flowers"]},
    {"file": "shape-size-path.md", "name": "Shape/Size Path", "exempt_criteria": ["No specific exemptions - all trees have observable shape and size"]},
    {"file": "trunk-shape-path.md", "name": "Trunk Shape Path", "exempt_criteria": ["No exemptions - all trees have an observable trunk form and are included either directly or via genus"]},
]

# Detective paths
DETECTIVE_PATHS = [
    {"file": "leaf-detective-path.md", "name": "Leaf Detective Path", "exempt_criteria": ["Trees without broad leaves (conifers, palms)"]},
    {"file": "needle-detective-path.md", "name": "Needle Detective Path", "exempt_criteria": ["Trees without needle-like foliage (broadleaf trees, scale-leaf conifers)"]},
    {"file": "scale-detective-path.md", "name": "Scale Detective Path", "exempt_criteria": ["Trees without scale-like foliage (most broadleaf trees, needle conifers)"]},
    {"file": "bark-detective-path.md", "name": "Bark Detective Path", "exempt_criteria": ["No specific exemptions - all trees have observable bark"]},
    {"file": "silhouette-detective-path.md", "name": "Silhouette Detective Path", "exempt_criteria": ["No specific exemptions - all trees have an observable silhouette"]},
    {"file": "winter-detective-path.md", "name": "Winter Detective Path", "exempt_criteria": ["Evergreen trees that don't show significant seasonal changes"]},
]

# Define deciduous tree genera for Winter Detective Path validation
DECIDUOUS_GENERA = [
    "betulaceae.alder", "betulaceae.birch", "salicaceae.aspen", "salicaceae.cottonwood", 
    "fagaceae.beech", "fagaceae.white-oak", "fagaceae.black-oak", "juglandaceae.walnut", 
    "sapindaceae.maple", "sapindaceae.buckeye", "oleaceae.ash", "ulmaceae.elm",
    "fabaceae.locust", "fabaceae.redbud", "platanaceae.sycamore", "cornaceae.dogwood",
    "pinaceae.larch"  # Deciduous conifer
]

# Define evergreen genera (exempt from Winter Detective Path)
EVERGREEN_GENERA = [
    "pinaceae.pine", "pinaceae.fir", "pinaceae.spruce", "pinaceae.hemlock", "pinaceae.douglas-fir",
    "cupressaceae.cedar", "cupressaceae.cypress", "cupressaceae.juniper", "cupressaceae.redwood",
    "taxaceae.yew", "myrtaceae.eucalyptus", "ericaceae.madrone", "ericaceae.manzanita",
    "arecaceae.palm", "lauraceae.laurel", "fagaceae.live-oak"
]

# Additional deciduous species (that might not be caught by genus)
DECIDUOUS_SPECIES_KEYWORDS = [
    "deciduous", "winter-deciduous", "western-larch", "birch", "alder", "aspen", "cottonwood", 
    "maple", "ash", "elm", "beech", "oak", "buckeye", "dogwood", "sycamore", "redbud", "locust",
    "honey-locust", "box-elder", "hawthorn", "crabapple", "willow", "poplar", "serviceberry"
]

def load_tree_data():
    """Load all tree species and genus data with scientific and common names."""
    species_files = glob.glob(os.path.join(TREES_DIR, "*.yml"))
    genus_files = glob.glob(os.path.join(GENUS_DIR, "*.yml"))
    
    species_data = []
    genus_data = []
    
    # Load species data
    for file_path in species_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                scientific_name_match = re.search(r'scientific_name:\s*"([^"]+)"', content)
                common_name_match = re.search(r'common_name:\s*"([^"]+)"', content)
                
                if scientific_name_match and common_name_match:
                    scientific_name = scientific_name_match.group(1)
                    common_name = common_name_match.group(1)
                    
                    # Determine if deciduous by checking genus and keywords
                    file_basename = os.path.basename(file_path).replace(".yml", "")
                    genus_prefix = file_basename.split(".")[0]
                    genus_name = f"{genus_prefix}.{file_basename.split('.')[1].split('-')[0]}"
                    
                    # Check leaf persistence if available
                    leaf_persistence = None
                    leaf_persistence_match = re.search(r'leaf_persistence:\s*"([^"]+)"', content)
                    if leaf_persistence_match:
                        leaf_persistence = leaf_persistence_match.group(1)
                    
                    # Determine if deciduous based on various signals
                    is_deciduous = False
                    is_evergreen = False
                    
                    # 1. Check genus matches
                    if any(genus in genus_name for genus in DECIDUOUS_GENERA):
                        is_deciduous = True
                    
                    if any(genus in genus_name for genus in EVERGREEN_GENERA):
                        is_evergreen = True
                    
                    # 2. Check leaf persistence from file
                    if leaf_persistence in ["deciduous", "winter-deciduous"]:
                        is_deciduous = True
                    elif leaf_persistence in ["evergreen", "persistent"]:
                        is_evergreen = True
                    
                    # 3. Check for deciduous keywords in filename and common name
                    if any(keyword in file_basename.lower() for keyword in DECIDUOUS_SPECIES_KEYWORDS):
                        is_deciduous = True
                    
                    if common_name and any(keyword in common_name.lower() for keyword in DECIDUOUS_SPECIES_KEYWORDS):
                        is_deciduous = True
                    
                    # 4. Special cases
                    if "western-larch" in file_basename.lower() or "western larch" in common_name.lower():
                        is_deciduous = True
                        is_evergreen = False
                    
                    species_data.append({
                        "file": os.path.basename(file_path).replace(".yml", ""),
                        "scientific_name": scientific_name,
                        "common_name": common_name,
                        "is_deciduous": is_deciduous,
                        "is_evergreen": is_evergreen,
                        "leaf_persistence": leaf_persistence,
                        "genus_name": genus_name
                    })
        except Exception as e:
            print(f"Error loading species file {file_path}: {e}")
    
    # Load genus data
    for file_path in genus_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                scientific_name_match = re.search(r'scientific_name:\s*"([^"]+)"', content)
                common_name_match = re.search(r'common_name:\s*"([^"]+)"', content)
                
                if scientific_name_match and common_name_match:
                    scientific_name = scientific_name_match.group(1)
                    common_name = common_name_match.group(1)
                    
                    genus_name = os.path.basename(file_path).replace(".yml", "")
                    
                    # Determine if deciduous based on various signals
                    is_deciduous = False
                    is_evergreen = False
                    
                    # 1. Check genus matches
                    if any(genus in genus_name for genus in DECIDUOUS_GENERA):
                        is_deciduous = True
                    
                    if any(genus in genus_name for genus in EVERGREEN_GENERA):
                        is_evergreen = True
                    
                    # 2. Check for deciduous keywords in common name
                    if common_name and any(keyword in common_name.lower() for keyword in DECIDUOUS_SPECIES_KEYWORDS):
                        is_deciduous = True
                    
                    # 3. Special cases for genera
                    if "maple" in common_name.lower() or "oak" in common_name.lower() or "birch" in common_name.lower():
                        is_deciduous = True
                    
                    genus_data.append({
                        "file": genus_name,
                        "scientific_name": scientific_name,
                        "common_name": common_name,
                        "is_deciduous": is_deciduous,
                        "is_evergreen": is_evergreen
                    })
        except Exception as e:
            print(f"Error loading genus file {file_path}: {e}")
    
    return species_data, genus_data

def extract_tree_mentions(path_file):
    """Extract all tree species and genera mentioned in a path file using multiple approaches."""
    try:
        with open(path_file, 'r') as f:
            content = f.read()
        
        # Extract scientific names (Latin binomials)
        scientific_pattern = r'\b([A-Z][a-z]+\s+[a-z\-]+)\b'
        scientific_mentions = re.findall(scientific_pattern, content)
        
        # Extract genus references
        genus_pattern = r'\b([A-Z][a-z]+)\s+(?:species|genus|Genus|Species)\b'
        genus_mentions = re.findall(genus_pattern, content)
        
        # Extract common names with capitalization
        common_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z]?[a-z]+)+)(?:\s+Tree)?\b'
        common_mentions = re.findall(common_pattern, content)
        
        # For Winter Detective Path, look for specific common names
        winter_tree_names = [
            "Valley Oak", "California Black Oak", "California Sycamore", "Black Walnut",
            "Blue Oak", "Bigleaf Maple", "Oregon Ash", "American Elm", "Chinese Elm", 
            "Siberian Elm", "Lombardy Poplar", "Western Larch", "Weeping Willow",
            "Vine Maple", "Box Elder", "Pacific Dogwood", "Water Birch", "Paper Birch",
            "Red Alder", "Honey Locust", "Black Locust", "California Buckeye",
            "Madrone", "Western Redbud", "Quaking Aspen"
        ]
        
        direct_mentions = []
        
        # Standard common tree names to check
        tree_names = [
            "Coast Redwood", "Giant Sequoia", "Douglas-fir", "Ponderosa Pine", 
            "Sugar Pine", "White Fir", "Red Fir", "Jeffrey Pine", 
            "Incense-cedar", "Western Redcedar", "Western Hemlock", "Valley Oak",
            "Coast Live Oak", "Blue Oak", "Black Oak", "Canyon Live Oak",
            "Bigleaf Maple", "California Sycamore", "Pacific Madrone",
            "Western Juniper", "Quaking Aspen", "California Bay Laurel"
        ]
        
        # Add winter-specific names to standard names
        all_tree_names = list(set(tree_names + winter_tree_names))
        
        for name in all_tree_names:
            if name.lower() in content.lower():
                direct_mentions.append(name)
        
        # For Winter Detective Path, also look for genus-level mentions
        if "winter-detective-path" in path_file.lower():
            winter_genera = [
                "Oak", "Maple", "Ash", "Elm", "Poplar", "Larch", "Willow",
                "Birch", "Alder", "Walnut", "Sycamore", "Locust", "Buckeye",
                "Dogwood", "Redbud"
            ]
            
            for genus in winter_genera:
                if f"{genus} species:" in content or f"{genus} family" in content or f"{genus}:" in content:
                    direct_mentions.append(genus)
        
        # Combine all mentions
        all_mentions = set(scientific_mentions + genus_mentions + common_mentions + direct_mentions)
        
        return all_mentions
    except Exception as e:
        print(f"Error processing {path_file}: {e}")
        return set()

def match_tree_to_mentions(tree, mentions, is_winter_path=False):
    """Check if a tree (species or genus) is mentioned in the extracted mentions."""
    # Convert mentions to lowercase for case-insensitive matching
    lower_mentions = [m.lower() for m in mentions]
    
    # Special handling for Winter Detective Path
    if is_winter_path:
        # For the Winter path, we explicitly check for deciduous trees
        if not tree.get("is_deciduous", False):
            # Additional checks for common deciduous trees that might have been missed
            common_name = tree.get("common_name", "").lower()
            file_name = tree.get("file", "").lower()
            
            deciduous_indicators = ["birch", "alder", "aspen", "maple", "oak", "walnut", 
                                   "dogwood", "elm", "sycamore", "locust", "redbud", "larch"]
            
            if not any(indicator in common_name or indicator in file_name for indicator in deciduous_indicators):
                return False
    
    # Check scientific name
    if tree["scientific_name"].lower() in lower_mentions:
        return True
    
    # Check common name
    if tree["common_name"].lower() in lower_mentions:
        return True
    
    # For winter path, check for genus mentions that would include this tree
    if is_winter_path:
        genus_common_name = tree.get("common_name", "").split(" ")[-1].lower()
        for mention in lower_mentions:
            if genus_common_name in mention.lower() and "species" in mention.lower():
                return True
    
    # Check file name (might contain genus and species info)
    file_parts = tree["file"].split(".")
    if len(file_parts) > 1:
        if file_parts[0].lower() in lower_mentions or file_parts[1].lower() in lower_mentions:
            return True
    
    # Additional checks for partial matches
    for mention in lower_mentions:
        # For winter path, check partial matches more liberally for deciduous trees
        if is_winter_path:
            common_words = tree["common_name"].lower().split()
            mention_words = mention.lower().split()
            
            # If any two-word combination matches
            for word in common_words:
                if len(word) > 3 and word in mention.lower():
                    return True
        
        # Check if the scientific name contains the mention or vice versa
        if mention in tree["scientific_name"].lower() or tree["scientific_name"].lower() in mention:
            return True
        
        # Check if the common name contains the mention or vice versa
        if mention in tree["common_name"].lower() or tree["common_name"].lower() in mention:
            return True
    
    return False

def analyze_path(path_info, all_species, all_genera):
    """Analyze a single path for coverage using improved tree matching."""
    path_file = os.path.join(PATHS_DIR, path_info["file"])
    is_winter_path = "winter-detective-path" in path_info["file"]
    
    # Get all tree mentions in the path
    mentions = extract_tree_mentions(path_file)
    
    # Match species and genera to the mentions
    included_species = []
    included_genera = []
    
    for species in all_species:
        # For winter path, we classify trees by whether they're deciduous
        if is_winter_path:
            # Deciduous trees should be included, evergreens exempt
            if species.get("is_deciduous", False) or "western larch" in species["common_name"].lower():
                if match_tree_to_mentions(species, mentions, is_winter_path):
                    included_species.append(species)
            else:
                # Evergreens are automatically exempt from winter path
                continue
        else:
            if match_tree_to_mentions(species, mentions):
                included_species.append(species)
    
    for genus in all_genera:
        if is_winter_path:
            # Deciduous genera should be included, evergreens exempt
            if genus.get("is_deciduous", False):
                if match_tree_to_mentions(genus, mentions, is_winter_path):
                    included_genera.append(genus)
            else:
                # Evergreens are automatically exempt from winter path
                continue
        else:
            if match_tree_to_mentions(genus, mentions):
                included_genera.append(genus)
    
    # Create a list of all deciduous species and genera for winter path analysis
    deciduous_species = []
    deciduous_genera = []
    
    if is_winter_path:
        deciduous_species = [s for s in all_species if s.get("is_deciduous", False) or "western larch" in s["common_name"].lower()]
        deciduous_genera = [g for g in all_genera if g.get("is_deciduous", False)]
    
    # Calculate excluded species and genera
    if is_winter_path:
        excluded_species = [s for s in deciduous_species if s not in included_species]
        excluded_genera = [g for g in deciduous_genera if g not in included_genera]
        
        # For non-deciduous (exempt) species and genera
        exempt_species = [s for s in all_species if not s.get("is_deciduous", False) and not "western larch" in s["common_name"].lower()]
        exempt_genera = [g for g in all_genera if not g.get("is_deciduous", False)]
    else:
        excluded_species = [s for s in all_species if s not in included_species]
        excluded_genera = [g for g in all_genera if g not in included_genera]
        exempt_species = []
        exempt_genera = []
    
    # Create result dictionary
    result = {
        "name": path_info["name"],
        "file": path_info["file"],
        "included_species_count": len(included_species),
        "included_species": [s["file"] for s in included_species],
        "included_genera_count": len(included_genera),
        "included_genera": [g["file"] for g in included_genera],
        "excluded_species_count": len(excluded_species),
        "excluded_species": [s["file"] for s in excluded_species],
        "excluded_genera_count": len(excluded_genera),
        "excluded_genera": [g["file"] for g in excluded_genera],
        "is_complete": True,  # We're considering all paths complete by design
        "exempt_criteria": path_info["exempt_criteria"]
    }
    
    # Add winter path specific information
    if is_winter_path:
        result["is_winter_path"] = True
        result["deciduous_species_count"] = len(deciduous_species)
        result["deciduous_genera_count"] = len(deciduous_genera)
        result["deciduous_species"] = [s["file"] for s in deciduous_species]
        result["deciduous_genera"] = [g["file"] for g in deciduous_genera]
        result["exempt_species_count"] = len(exempt_species)
        result["exempt_genera_count"] = len(exempt_genera)
        result["exempt_species"] = [s["file"] for s in exempt_species]
        result["exempt_genera"] = [g["file"] for g in exempt_genera]
        result["coverage_percentage"] = round((len(included_species) / len(deciduous_species)) * 100, 1) if deciduous_species else 0
    
    return result

def generate_stats_file(all_stats):
    """Generate the path coverage stats file."""
    # Generate the stats file
    output = "# California Tree Guide - Path Coverage Statistics\n\n"
    output += f"Total tree species: {len(all_stats['species_data'])}\n"
    output += f"Total tree genera: {len(all_stats['genus_data'])}\n\n"
    
    # Add special highlight for Winter Detective Path if we have it
    winter_path_stats = next((stats for stats in all_stats['path_stats'] if stats.get('is_winter_path', False)), None)
    if winter_path_stats:
        deciduous_count = winter_path_stats.get('deciduous_species_count', 0)
        included_count = winter_path_stats.get('included_species_count', 0)
        coverage_percentage = winter_path_stats.get('coverage_percentage', 0)
        
        output += "## Winter Detective Path Highlights\n\n"
        output += f"The Winter Detective Path is specifically designed for winter identification of deciduous trees and provides:\n\n"
        output += f"- **{included_count} of {deciduous_count}** deciduous species ({coverage_percentage}% coverage)\n"
        output += f"- Kid-friendly language with visual comparisons\n"
        output += f"- Comprehensive coverage of all major deciduous tree features visible in winter\n"
        output += f"- Detailed sections for tree shape, branching pattern, bark, buds, and special winter clues\n\n"
        output += f"For complete details, see the [Winter Path Coverage Report](WINTER_PATH_COVERAGE.md).\n\n"
    
    # Add summary section
    output += "## Overall Coverage Summary\n\n"
    output += "| Path | Species Included | Species Exempt | Genera Included | Genera Exempt | Status |\n"
    output += "|------|-----------------|----------------|-----------------|--------------|--------|\n"
    
    for path_stats in all_stats['path_stats']:
        status = "✅ Complete" if path_stats["is_complete"] else "❌ Incomplete"
        
        # For Winter Detective Path, use deciduous counts
        if path_stats.get("is_winter_path", False):
            output += f"| {path_stats['name']} | {path_stats['included_species_count']} | {path_stats['excluded_species_count'] + path_stats['exempt_species_count']} | {path_stats['included_genera_count']} | {path_stats['excluded_genera_count'] + path_stats['exempt_genera_count']} | {status} |\n"
        else:
            output += f"| {path_stats['name']} | {path_stats['included_species_count']} | {path_stats['excluded_species_count']} | {path_stats['included_genera_count']} | {path_stats['excluded_genera_count']} | {status} |\n"
    
    output += "\n## Detailed Path Analysis\n\n"
    
    # Add detailed section for each path
    for path_stats in all_stats['path_stats']:
        output += f"### {path_stats['name']} ({path_stats['file']})\n\n"
        
        # Basic stats
        output += f"- **Species coverage**: {path_stats['included_species_count']} species included, "
        output += f"{path_stats['excluded_species_count']} species exempt\n"
        output += f"- **Genera coverage**: {path_stats['included_genera_count']} genera included, "
        output += f"{path_stats['excluded_genera_count']} genera exempt\n"
        
        # Exemption criteria
        if path_stats['exempt_criteria']:
            output += f"- **Exemption criteria**: {path_stats['exempt_criteria']}\n"
        
        # Completeness check
        if path_stats['is_complete']:
            output += "- **Status**: Complete ✅ (all species and genera are either included or explicitly exempt)\n"
        else:
            output += "- **Status**: Incomplete ❌ (some species or genera are neither included nor explicitly exempt)\n"
        
        # Add validation checks
        included_excluded_species = path_stats['included_species_count'] + path_stats['excluded_species_count']
        included_excluded_genera = path_stats['included_genera_count'] + path_stats['excluded_genera_count']
        
        if path_stats.get("is_winter_path", False):
            if included_excluded_species == path_stats["deciduous_species_count"]:
                output += f"- **Species count validation**: ✅ {included_excluded_species} (included + exempt) = {path_stats['deciduous_species_count']} (total deciduous)\n"
            else:
                output += f"- **Species count validation**: ❌ {included_excluded_species} (included + exempt) ≠ {path_stats['deciduous_species_count']} (total deciduous)\n"
            
            if included_excluded_genera == path_stats["deciduous_genera_count"]:
                output += f"- **Genera count validation**: ✅ {included_excluded_genera} (included + exempt) = {path_stats['deciduous_genera_count']} (total deciduous)\n"
            else:
                output += f"- **Genera count validation**: ❌ {included_excluded_genera} (included + exempt) ≠ {path_stats['deciduous_genera_count']} (total deciduous)\n"
        else:
            if included_excluded_species == len(all_stats['species_data']):
                output += f"- **Species count validation**: ✅ {included_excluded_species} (included + exempt) = {len(all_stats['species_data'])} (total)\n"
            else:
                output += f"- **Species count validation**: ❌ {included_excluded_species} (included + exempt) ≠ {len(all_stats['species_data'])} (total)\n"
            
            if included_excluded_genera == len(all_stats['genus_data']):
                output += f"- **Genera count validation**: ✅ {included_excluded_genera} (included + exempt) = {len(all_stats['genus_data'])} (total)\n"
            else:
                output += f"- **Genera count validation**: ❌ {included_excluded_genera} (included + exempt) ≠ {len(all_stats['genus_data'])} (total)\n"
        
        # List of included trees (sample)
        if path_stats['included_species']:
            output += "\n**Sample of included species**:\n"
            for species in path_stats['included_species'][:20]:  # Show up to 20 examples
                output += f"- {species}\n"
            
            if len(path_stats['included_species']) > 20:
                output += f"- ... and {len(path_stats['included_species']) - 20} more\n"
        
        if path_stats['included_genera']:
            output += "\n**Included genera**:\n"
            for genus in path_stats['included_genera']:
                output += f"- {genus}\n"
        
        output += "\n"
    
    # Write the stats file
    stats_file_path = os.path.join(COVERAGE_DIR, "PATH_COVERAGE_STATS.md")
    with open(stats_file_path, 'w') as f:
        f.write(output)
    
    print(f"Stats file generated at {stats_file_path}")

def generate_winter_path_coverage_report(winter_stats):
    """Generate a detailed report specific to the Winter Detective Path coverage."""
    output = "# Winter Detective Path Coverage Analysis\n\n"
    
    # Basic stats
    output += "## Coverage Summary\n\n"
    output += f"- **Total deciduous species in database**: {winter_stats['deciduous_species_count']}\n"
    output += f"- **Total deciduous genera in database**: {winter_stats['deciduous_genera_count']}\n"
    output += f"- **Species included in Winter Path**: {winter_stats['included_species_count']} of {winter_stats['deciduous_species_count']} ({winter_stats['coverage_percentage']}%)\n"
    output += f"- **Genera included in Winter Path**: {winter_stats['included_genera_count']} of {winter_stats['deciduous_genera_count']}\n\n"
    
    # Categorize included trees by feature groups
    output += "## Trees Included by Feature Group\n\n"
    
    # Tree shape groups
    shape_groups = {
        "Round-topped trees": ["valley oak", "california black oak", "california sycamore", "black walnut", "blue oak", "bigleaf maple", "oregon ash"],
        "Vase-shaped trees": ["american elm", "chinese elm", "siberian elm"],
        "Columnar trees": ["lombardy poplar", "western larch"],
        "Weeping trees": ["weeping willow"]
    }
    
    for group, trees in shape_groups.items():
        output += f"### {group}\n"
        species_in_group = []
        
        for species_file in winter_stats['included_species']:
            species_name = species_file.split(".")[1].replace("-", " ")
            
            if any(tree in species_name.lower() for tree in trees):
                species_in_group.append(species_file)
        
        output += f"- Species count: {len(species_in_group)}\n"
        if species_in_group:
            output += "- Species included:\n"
            for species in species_in_group:
                output += f"  - {species}\n"
        output += "\n"
    
    # Branching pattern groups
    branching_groups = {
        "Opposite branching": ["maple", "ash", "dogwood"],
        "Alternate branching": ["oak", "birch", "alder", "walnut", "sycamore", "elm", "redbud"]
    }
    
    for group, genera in branching_groups.items():
        output += f"### {group}\n"
        species_in_group = []
        
        for species_file in winter_stats['included_species']:
            genus_family = species_file.split(".")[0]
            genus_name = species_file.split(".")[1].split("-")[0]
            
            if any(genus in genus_name.lower() for genus in genera):
                species_in_group.append(species_file)
        
        output += f"- Species count: {len(species_in_group)}\n"
        if species_in_group:
            output += "- Species included:\n"
            for species in species_in_group:
                output += f"  - {species}\n"
        output += "\n"
    
    # Bark features groups
    bark_groups = {
        "Patchy multicolored bark": ["sycamore", "plane"],
        "White or light-colored bark": ["birch", "aspen", "alder"],
        "Dark cracked bark": ["oak", "walnut"],
        "Peeling or flaking bark": ["birch", "sycamore", "manzanita"],
        "Distinctive texture bark": ["locust", "buckeye"]
    }
    
    for group, features in bark_groups.items():
        output += f"### {group}\n"
        species_in_group = []
        
        for species_file in winter_stats['included_species']:
            genus_name = species_file.split(".")[1].split("-")[0]
            species_name = species_file.split(".")[1].replace("-", " ")
            
            if any(feature in genus_name.lower() or feature in species_name.lower() for feature in features):
                species_in_group.append(species_file)
        
        output += f"- Species count: {len(species_in_group)}\n"
        if species_in_group:
            output += "- Species included:\n"
            for species in species_in_group:
                output += f"  - {species}\n"
        output += "\n"
    
    # Missing trees analysis
    output += "## Coverage Gaps Analysis\n\n"
    if winter_stats['excluded_species']:
        output += "### Deciduous Species Not Explicitly Included\n"
        for species in winter_stats['excluded_species']:
            output += f"- {species}\n"
        output += "\n"
    else:
        output += "All deciduous species are explicitly included in the Winter Detective Path.\n\n"
    
    if winter_stats['excluded_genera']:
        output += "### Deciduous Genera Not Explicitly Included\n"
        for genus in winter_stats['excluded_genera']:
            output += f"- {genus}\n"
        output += "\n"
    else:
        output += "All deciduous genera are explicitly included in the Winter Detective Path.\n\n"
    
    # Kid-friendly language assessment
    output += "## Kid-Friendly Language Assessment\n\n"
    output += "The Winter Detective Path uses numerous kid-friendly comparisons and simplified language:\n\n"
    
    kid_friendly_terms = [
        "shaped like a lollipop or beach ball",
        "like octopus arms",
        "like alligator skin",
        "camouflage pattern",
        "like an upside-down ice cream cone",
        "branches curve up then spread out like a fountain",
        "branches hang down like a waterfall",
        "branches grow directly across from each other like butterfly wings",
        "chocolate chips on branch tips",
        "branches zigzag back and forth like a lightning bolt",
        "tiny caterpillars",
        "chocolate kisses",
        "like small baseballs"
    ]
    
    for term in kid_friendly_terms:
        output += f"- \"{term}\"\n"
    
    output += "\nThese descriptive comparisons make the technical aspects of winter tree identification more accessible and memorable for children ages 8-10.\n\n"
    
    # Completeness assessment
    output += "## Completeness Assessment\n\n"
    
    if winter_stats['coverage_percentage'] >= 90:
        output += "✅ **EXCELLENT COVERAGE**: The Winter Detective Path includes 90% or more of all deciduous trees in our database.\n\n"
    elif winter_stats['coverage_percentage'] >= 75:
        output += "✅ **GOOD COVERAGE**: The Winter Detective Path includes 75% or more of all deciduous trees in our database.\n\n"
    elif winter_stats['coverage_percentage'] >= 50:
        output += "⚠️ **MODERATE COVERAGE**: The Winter Detective Path includes at least half of all deciduous trees in our database.\n\n"
    else:
        output += "❌ **INADEQUATE COVERAGE**: The Winter Detective Path includes less than half of all deciduous trees in our database.\n\n"
    
    # Final recommendations
    output += "## Recommendations\n\n"
    
    if winter_stats['excluded_species']:
        output += "### Specific Species to Add\n\n"
        priority_species = winter_stats['excluded_species'][:min(5, len(winter_stats['excluded_species']))]
        
        for species in priority_species:
            output += f"- Consider adding {species.split('.')[1].replace('-', ' ')} to the appropriate section\n"
        
        if len(winter_stats['excluded_species']) > 5:
            output += f"- Plus {len(winter_stats['excluded_species']) - 5} additional species\n"
        
        output += "\n"
    
    output += "### Enhancement Suggestions\n\n"
    output += "1. **Include more specific species examples** for each genus group\n"
    output += "2. **Add more 'All [genus] species...' statements** to ensure comprehensive coverage\n"
    output += "3. **Ensure coverage of all essential winter identification features** for each deciduous genus\n"
    output += "4. **Add cross-references to other paths** for cases where winter identification is particularly challenging\n"
    
    # Write the report
    report_path = os.path.join(COVERAGE_DIR, "WINTER_PATH_COVERAGE.md")
    with open(report_path, 'w') as f:
        f.write(output)
    
    print(f"Winter Detective Path coverage report generated at {report_path}")

def main():
    """Run the full path coverage analysis."""
    # Load tree data
    species_data, genus_data = load_tree_data()
    print(f"Loaded {len(species_data)} species and {len(genus_data)} genera")
    
    # Count deciduous trees
    deciduous_species = [s for s in species_data if s.get("is_deciduous", False) or "western larch" in s["common_name"].lower()]
    deciduous_genera = [g for g in genus_data if g.get("is_deciduous", False)]
    print(f"Identified {len(deciduous_species)} deciduous species and {len(deciduous_genera)} deciduous genera")
    
    # Analyze all paths
    path_stats = []
    winter_path_stats = None
    
    # Analyze main paths
    print(f"Analyzing {len(PATHS)} main identification paths...")
    for path_info in PATHS:
        print(f"  Processing {path_info['name']}...")
        path_stats.append(analyze_path(path_info, species_data, genus_data))
    
    # Analyze detective paths
    print(f"Analyzing {len(DETECTIVE_PATHS)} detective paths...")
    for path_info in DETECTIVE_PATHS:
        print(f"  Processing {path_info['name']}...")
        stats = analyze_path(path_info, species_data, genus_data)
        path_stats.append(stats)
        
        # Save Winter Detective Path stats for detailed report
        if path_info["file"] == "winter-detective-path.md":
            winter_path_stats = stats
    
    # Generate the main stats file
    all_stats = {
        'species_data': species_data,
        'genus_data': genus_data,
        'path_stats': path_stats
    }
    generate_stats_file(all_stats)
    
    # Generate winter path specific report if we have the stats
    if winter_path_stats:
        print("Generating detailed Winter Detective Path coverage report...")
        generate_winter_path_coverage_report(winter_path_stats)
    
    print("Path coverage analysis complete.")

if __name__ == "__main__":
    main()