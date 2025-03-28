#!/usr/bin/env python3
import re
import sys

# Example tree file to update
tree_file = sys.argv[1]
scientific_genus = sys.argv[2]
common_genus = sys.argv[3]

# Read the tree file
with open(tree_file, 'r') as file:
    content = file.read()

# Check if the file already has genus information
if re.search(r'scientific_genus:', content):
    print(f"File {tree_file} already has genus information. Skipping.")
    sys.exit(0)

# Find the family line and what comes after
family_pattern = r'(\s+)(family:\s*"[^"]+"|family:\s*\'[^\']+\')(\s*\n)'
family_match = re.search(family_pattern, content)
if not family_match:
    print(f"Could not find family line in {tree_file}.")
    sys.exit(1)

# Get the indentation
indent = family_match.group(1)

# Determine quote style
quote_style = '"' if '"' in family_match.group(2) else "'"

# Direct replacement
new_content = re.sub(
    family_pattern,
    f'\\1\\2\\3\\1scientific_genus: {quote_style}{scientific_genus}{quote_style}\\3\\1common_genus: {quote_style}{common_genus}{quote_style}\\3',
    content,
    count=1
)

# Write the updated content
with open(tree_file, 'w') as file:
    file.write(new_content)

print(f"Added genus information to {tree_file}: {scientific_genus} ({common_genus})")