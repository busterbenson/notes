#!/usr/bin/env python3
"""
Validate Tree Files

This script validates the format and structure of tree and genus YAML files
to ensure they meet the required schema and contain all necessary sections.

Usage:
    python3 validate_tree_files.py [path_to_directory]

If no path is provided, it will use the default tree and genus directories.
"""

import os
import sys
import yaml
import re
from collections import defaultdict

# Default paths
TREE_DIR = "/Users/buster/projects/notes/_trees/trees"
GENUS_DIR = "/Users/buster/projects/notes/_trees/genus"

# Required sections for tree files
TREE_REQUIRED_SECTIONS = [
    "common_name",
    "scientific_name",
    "scientific_genus",
    "common_genus",
    "family",
    "summary",
    "identification_path",
    "features",
    "kid_friendly_identification",
    "seasonal_timeline",
    "confirmation_checklist",
    "look_alikes",
    "cultural_significance",
    "range_within_california",
    "physical_characteristics",
    "decision_tree_placement",
]

# Required sections for genus files
GENUS_REQUIRED_SECTIONS = [
    "common_name",
    "scientific_name",
    "taxonomic_level",
    "family",
    "summary",
    "included_species",
    "identification_path",
    "features",
    "kid_friendly_identification",
    "seasonal_timeline",
    "confirmation_checklist",
    "look_alikes",
    "cultural_significance",
    "range_within_california",
    "physical_characteristics",
    "decision_tree_placement",
]

# Required subsections for tree features
TREE_FEATURES_SUBSECTIONS = [
    "always_true",
    "usually_true",
    "sometimes_true",
    "never_true"
]

# Required subsections for identification_path
IDENTIFICATION_PATH_SUBSECTIONS = [
    "primary_markers",
    "secondary_markers",
    "seasonal_markers",
    "similar_species_differentiation"
]

# Required subsections for kid_friendly_identification
KID_FRIENDLY_SUBSECTIONS = [
    "primary_identifier",
    "memorable_comparison",
    "touch_tip",
    "smell_tip",
    "fun_fact",
    "detective_steps"
]

def validate_yaml_file(file_path):
    """
    Validate a YAML file to ensure it can be parsed correctly.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        (bool, dict): A tuple of (is_valid, parsed_yaml)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return True, data
    except Exception as e:
        return False, f"Error parsing YAML: {str(e)}"

def validate_tree_file(file_path):
    """
    Validate a tree YAML file.
    
    Args:
        file_path: Path to the tree YAML file
        
    Returns:
        (bool, list): A tuple of (is_valid, errors)
    """
    is_valid_yaml, data = validate_yaml_file(file_path)
    if not is_valid_yaml:
        return False, [data]
    
    errors = []
    
    # Check if 'tree' is the root element
    if 'tree' not in data:
        return False, ["Missing root 'tree' element"]
    
    tree_data = data['tree']
    
    # Check required sections
    for section in TREE_REQUIRED_SECTIONS:
        if section not in tree_data:
            errors.append(f"Missing required section: {section}")
    
    # Check features subsections if features exists
    if 'features' in tree_data:
        for subsection in TREE_FEATURES_SUBSECTIONS:
            if subsection not in tree_data['features']:
                errors.append(f"Missing required features subsection: {subsection}")
                
        # Validate feature_id format
        feature_sections = [
            ('always_true', tree_data['features'].get('always_true', [])),
            ('usually_true', tree_data['features'].get('usually_true', [])),
            ('sometimes_true', tree_data['features'].get('sometimes_true', [])),
            ('never_true', tree_data['features'].get('never_true', []))
        ]
        
        for section_name, features in feature_sections:
            for i, feature in enumerate(features):
                if 'feature_id' not in feature:
                    errors.append(f"Missing feature_id in '{section_name}' at index {i}")
                elif not re.match(r"^[A-Z]+-[A-Z]+-\d+$", feature['feature_id']):
                    errors.append(f"Invalid feature_id format in '{section_name}': {feature['feature_id']}")
    
    # Check identification_path subsections if it exists
    if 'identification_path' in tree_data:
        for subsection in IDENTIFICATION_PATH_SUBSECTIONS:
            if subsection not in tree_data['identification_path']:
                errors.append(f"Missing required identification_path subsection: {subsection}")
    
    # Check kid_friendly_identification subsections if it exists
    if 'kid_friendly_identification' in tree_data:
        for subsection in KID_FRIENDLY_SUBSECTIONS:
            if subsection not in tree_data['kid_friendly_identification']:
                errors.append(f"Missing required kid_friendly_identification subsection: {subsection}")
        
        # Check detective_steps structure if it exists
        if 'detective_steps' in tree_data['kid_friendly_identification']:
            steps = tree_data['kid_friendly_identification']['detective_steps']
            for i, step in enumerate(steps):
                if 'step' not in step:
                    errors.append(f"Missing 'step' number in detective_steps at index {i}")
                if 'instruction' not in step:
                    errors.append(f"Missing 'instruction' in detective_steps at index {i}")
                if 'yes_next' not in step:
                    errors.append(f"Missing 'yes_next' in detective_steps at index {i}")
                if 'no_next' not in step:
                    errors.append(f"Missing 'no_next' in detective_steps at index {i}")
    
    # Check seasonal_timeline if it exists
    if 'seasonal_timeline' in tree_data:
        seasons = tree_data['seasonal_timeline']
        expected_seasons = {'Spring', 'Summer', 'Fall', 'Winter'}
        found_seasons = set()
        
        for i, season_data in enumerate(seasons):
            if 'season' not in season_data:
                errors.append(f"Missing 'season' in seasonal_timeline at index {i}")
            else:
                found_seasons.add(season_data['season'])
            
            if 'visual_changes' not in season_data:
                errors.append(f"Missing 'visual_changes' in seasonal_timeline at index {i}")
            if 'reproductive_activity' not in season_data:
                errors.append(f"Missing 'reproductive_activity' in seasonal_timeline at index {i}")
            if 'identification_tips' not in season_data:
                errors.append(f"Missing 'identification_tips' in seasonal_timeline at index {i}")
            if 'kid_friendly_tip' not in season_data:
                errors.append(f"Missing 'kid_friendly_tip' in seasonal_timeline at index {i}")
        
        missing_seasons = expected_seasons - found_seasons
        if missing_seasons:
            errors.append(f"Missing seasons in seasonal_timeline: {', '.join(missing_seasons)}")
    
    return len(errors) == 0, errors

def validate_genus_file(file_path):
    """
    Validate a genus YAML file.
    
    Args:
        file_path: Path to the genus YAML file
        
    Returns:
        (bool, list): A tuple of (is_valid, errors)
    """
    is_valid_yaml, data = validate_yaml_file(file_path)
    if not is_valid_yaml:
        return False, [data]
    
    errors = []
    
    # Check if 'genus' is the root element
    if 'genus' not in data:
        return False, ["Missing root 'genus' element"]
    
    genus_data = data['genus']
    
    # Check required sections
    for section in GENUS_REQUIRED_SECTIONS:
        if section not in genus_data:
            errors.append(f"Missing required section: {section}")
    
    # Check included_species if it exists
    if 'included_species' in genus_data:
        species_list = genus_data['included_species']
        if not isinstance(species_list, list) or len(species_list) == 0:
            errors.append("included_species should be a non-empty list")
        else:
            for i, species in enumerate(species_list):
                if 'name' not in species:
                    errors.append(f"Missing 'name' in included_species at index {i}")
                if 'scientific_name' not in species:
                    errors.append(f"Missing 'scientific_name' in included_species at index {i}")
                if 'distinguishing_features' not in species:
                    errors.append(f"Missing 'distinguishing_features' in included_species at index {i}")
                if 'california_context' not in species:
                    errors.append(f"Missing 'california_context' in included_species at index {i}")
    
    # Check features subsections if features exists (similar to tree files)
    if 'features' in genus_data:
        for subsection in TREE_FEATURES_SUBSECTIONS:
            if subsection not in genus_data['features']:
                errors.append(f"Missing required features subsection: {subsection}")
                
        # Validate feature_id format
        feature_sections = [
            ('always_true', genus_data['features'].get('always_true', [])),
            ('usually_true', genus_data['features'].get('usually_true', [])),
            ('sometimes_true', genus_data['features'].get('sometimes_true', [])),
            ('never_true', genus_data['features'].get('never_true', []))
        ]
        
        for section_name, features in feature_sections:
            for i, feature in enumerate(features):
                if 'feature_id' not in feature:
                    errors.append(f"Missing feature_id in '{section_name}' at index {i}")
                elif not re.match(r"^[A-Z]+-[A-Z]+-\d+$", feature['feature_id']):
                    errors.append(f"Invalid feature_id format in '{section_name}': {feature['feature_id']}")
    
    # Check other sections similar to tree files
    if 'identification_path' in genus_data:
        for subsection in IDENTIFICATION_PATH_SUBSECTIONS:
            if subsection not in genus_data['identification_path']:
                errors.append(f"Missing required identification_path subsection: {subsection}")
    
    if 'kid_friendly_identification' in genus_data:
        for subsection in KID_FRIENDLY_SUBSECTIONS:
            if subsection not in genus_data['kid_friendly_identification']:
                errors.append(f"Missing required kid_friendly_identification subsection: {subsection}")
    
    # Check seasonal_timeline if it exists
    if 'seasonal_timeline' in genus_data:
        seasons = genus_data['seasonal_timeline']
        expected_seasons = {'Spring', 'Summer', 'Fall', 'Winter'}
        found_seasons = set()
        
        for i, season_data in enumerate(seasons):
            if 'season' not in season_data:
                errors.append(f"Missing 'season' in seasonal_timeline at index {i}")
            else:
                found_seasons.add(season_data['season'])
            
            if 'visual_changes' not in season_data:
                errors.append(f"Missing 'visual_changes' in seasonal_timeline at index {i}")
            if 'reproductive_activity' not in season_data:
                errors.append(f"Missing 'reproductive_activity' in seasonal_timeline at index {i}")
            if 'identification_tips' not in season_data:
                errors.append(f"Missing 'identification_tips' in seasonal_timeline at index {i}")
            if 'kid_friendly_tip' not in season_data:
                errors.append(f"Missing 'kid_friendly_tip' in seasonal_timeline at index {i}")
        
        missing_seasons = expected_seasons - found_seasons
        if missing_seasons:
            errors.append(f"Missing seasons in seasonal_timeline: {', '.join(missing_seasons)}")
    
    return len(errors) == 0, errors

def validate_directory(directory, validator_func):
    """
    Validate all YAML files in a directory.
    
    Args:
        directory: Directory path to validate
        validator_func: Function to use for validation
        
    Returns:
        dict: A dictionary of validation results
    """
    results = {
        'valid_files': [],
        'invalid_files': defaultdict(list),
        'count': {
            'total': 0,
            'valid': 0,
            'invalid': 0
        }
    }
    
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.yml'):
            file_path = os.path.join(directory, filename)
            is_valid, errors = validator_func(file_path)
            
            results['count']['total'] += 1
            
            if is_valid:
                results['valid_files'].append(filename)
                results['count']['valid'] += 1
            else:
                results['invalid_files'][filename] = errors
                results['count']['invalid'] += 1
    
    return results

def print_validation_summary(results, file_type):
    """
    Print a summary of validation results.
    
    Args:
        results: Dictionary of validation results
        file_type: Type of files validated (e.g., "tree", "genus")
    """
    print(f"\n{'-'*50}")
    print(f"VALIDATION RESULTS FOR {file_type.upper()} FILES")
    print(f"{'-'*50}")
    print(f"Total files: {results['count']['total']}")
    print(f"Valid files: {results['count']['valid']}")
    print(f"Invalid files: {results['count']['invalid']}")
    
    if results['count']['invalid'] > 0:
        print("\nIssues found in the following files:")
        for filename, errors in results['invalid_files'].items():
            print(f"\n{filename}:")
            for error in errors:
                print(f"  - {error}")
    
    print(f"{'-'*50}\n")

def main():
    """
    Main function to run the validation.
    """
    # Use command line argument for directory if provided
    tree_dir = TREE_DIR
    genus_dir = GENUS_DIR
    
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
        tree_dir = os.path.join(base_dir, 'trees')
        genus_dir = os.path.join(base_dir, 'genus')
    
    print(f"Validating tree files in: {tree_dir}")
    tree_results = validate_directory(tree_dir, validate_tree_file)
    print_validation_summary(tree_results, "tree")
    
    print(f"Validating genus files in: {genus_dir}")
    genus_results = validate_directory(genus_dir, validate_genus_file)
    print_validation_summary(genus_results, "genus")
    
    # Return overall success/failure
    return tree_results['count']['invalid'] == 0 and genus_results['count']['invalid'] == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)