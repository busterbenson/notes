#!/usr/bin/env python3
"""Sample posts for theme analysis."""

import json
import random
from pathlib import Path
from collections import defaultdict

with open('pile_analysis.json', 'r') as f:
    data = json.load(f)

posts = data['posts']

# Sample strategy:
# 1. Posts from different decades
# 2. Posts with different pile combinations
# 3. Posts without piles
# 4. Top piles represented

samples = {
    'no_piles': [],
    'single_pile': defaultdict(list),
    'multiple_piles': [],
    'by_decade': defaultdict(list)
}

for post in posts:
    # Extract year from file path
    year_match = Path(post['file']).parts[1]  # e.g., '2023'
    decade = f"{year_match[:3]}0s"

    samples['by_decade'][decade].append(post)

    if not post['piles']:
        samples['no_piles'].append(post)
    elif len(post['piles']) == 1:
        samples['single_pile'][post['piles'][0]].append(post)
    else:
        samples['multiple_piles'].append(post)

# Select diverse sample
selected = []

# 2 from each decade
for decade in sorted(samples['by_decade'].keys()):
    selected.extend(random.sample(samples['by_decade'][decade],
                                   min(2, len(samples['by_decade'][decade]))))

# 5 without piles
selected.extend(random.sample(samples['no_piles'],
                               min(5, len(samples['no_piles']))))

# 2 from each top pile
top_piles = ['self-reflection', 'year-in-review', 'behavior-change',
             'project', 'dialogue', 'cognitive-biases', 'self-tracking']
for pile in top_piles:
    if pile in samples['single_pile']:
        selected.extend(random.sample(samples['single_pile'][pile],
                                       min(1, len(samples['single_pile'][pile]))))

# 5 with multiple piles
selected.extend(random.sample(samples['multiple_piles'],
                               min(5, len(samples['multiple_piles']))))

# Deduplicate
selected = list({p['file']: p for p in selected}.values())

print(f"Selected {len(selected)} posts for analysis\n")
print("=" * 80)
for post in sorted(selected, key=lambda x: x['file']):
    piles_str = ', '.join(post['piles']) if post['piles'] else '(no piles)'
    print(f"{post['file']}")
    print(f"  Title: {post['title']}")
    print(f"  Piles: {piles_str}")
    print()
