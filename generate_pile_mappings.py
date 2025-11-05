#!/usr/bin/env python3
"""Generate pile mapping proposals for all posts."""

import json
import re
from pathlib import Path

# Load current post data
with open('pile_analysis.json', 'r') as f:
    data = json.load(f)

# Mapping from old piles to new piles
PILE_MAPPING = {
    # Direct mappings (keep or rename)
    'self-reflection': ['reflection'],
    'year-in-review': ['year-review', 'reflection'],
    'dialogue': ['dialogue'],
    'fiction': ['fiction'],
    'game-theory': ['game-theory'],
    'systems-thinking': ['systems-thinking'],
    'technology': ['technology'],
    'self-tracking': ['self-tracking'],
    'codex-vitae': ['codex-vitae'],
    'fundamental-purpose': ['fundamental-purpose'],
    'internal-voices': ['internal-voices'],
    'negative-space': ['negative-space'],
    'wicked-problems': ['wicked-problems'],
    'meta-crisis': ['meta-crisis'],
    'symbol-languages': ['symbols'],

    # Consolidations
    '750-words': ['750words', 'work'],
    'cognitive-biases': ['cognitive-science', 'cognitive-biases'],
    'critical-thinking': ['cognitive-science'],
    'mindset': ['psychology', 'behavior-change'],
    'behavior-change': ['behavior-change'],
    'resiliance': ['behavior-change'],  # Fix spelling
    'personal-mythology': ['identity'],
    'being-a-creator': ['creativity', 'work'],
    'product-management': ['work'],
    'rules-to-live-by': ['codex-vitae'],
    'quality-time': ['relationships'],
    'family': ['relationships'],
    'community': ['relationships', 'society'],
    'social-issues': ['society'],

    # Topic-based
    'project': ['update', 'work'],
    'book': ['creativity', 'work'],
    'death': ['mortality'],
    'health': ['health'],
    'security': ['technology'],
    'artificial-intelligence': ['technology'],
    'mindfulness': ['spirituality'],
    'thought-experiment': ['philosophy'],
    'cognitive-dissonance': ['psychology', 'cognitive-science'],

    # Remove (merge into others)
    'complaining': [],  # Remove
    'fruitful': [],  # Remove
    'medium': ['work'],  # Too specific
}

# Title/content-based suggestions
TITLE_PATTERNS = {
    r'\d+:': ['year-review', 'reflection'],  # "47: CHALANT"
    r'year.{0,10}review': ['year-review', 'reflection'],
    r'annual.{0,10}review': ['year-review', 'reflection'],
    r'cognitive bias': ['cognitive-science', 'cognitive-biases'],
    r'belief': ['philosophy', 'codex-vitae'],
    r'cosmology': ['philosophy', 'spirituality'],
    r'death|mortal|legacy': ['mortality'],
    r'prisoner.{0,5}dilemma': ['prisoner-dilemma', 'game-theory'],
    r'750.?words': ['750words', 'work'],
    r'experiment|trying|challenge': ['experiment'],
    r'how to|guide|framework': ['guide'],
    r'conversation|interview|dialogue': ['dialogue'],
    r'track|metric|quantif': ['self-tracking'],
    r'mask|authentic|identity|who am i': ['identity'],
    r'relationship|family|friend|connect': ['relationships'],
    r'spirit|psychedelic|consciousness|meditat': ['spirituality'],
    r'system|complex|emerg': ['systems-thinking'],
    r'Oakland|school|civic|society|social': ['society'],
}

def suggest_piles_from_title(title):
    """Suggest additional piles based on title keywords."""
    suggestions = set()
    title_lower = title.lower()

    for pattern, piles in TITLE_PATTERNS.items():
        if re.search(pattern, title_lower):
            suggestions.update(piles)

    return list(suggestions)

def map_post_piles(post):
    """Map old piles to new piles and suggest additions."""
    old_piles = post['piles']
    new_piles = set()

    # Map existing piles
    for old_pile in old_piles:
        if old_pile in PILE_MAPPING:
            new_piles.update(PILE_MAPPING[old_pile])

    # Add title-based suggestions
    title_suggestions = suggest_piles_from_title(post['title'])
    suggested_additions = set(title_suggestions) - new_piles

    return {
        'file': post['file'],
        'title': post['title'],
        'old_piles': old_piles,
        'new_piles': sorted(list(new_piles)),
        'suggested_additions': sorted(list(suggested_additions)),
        'total_piles': sorted(list(new_piles | suggested_additions))
    }

# Process all posts
mapped_posts = []
for post in data['posts']:
    mapped = map_post_piles(post)
    mapped_posts.append(mapped)

# Generate statistics
total_posts = len(mapped_posts)
posts_changed = len([p for p in mapped_posts if set(p['old_piles']) != set(p['new_piles'])])
posts_with_additions = len([p for p in mapped_posts if p['suggested_additions']])

# Count new pile usage
new_pile_counts = {}
for post in mapped_posts:
    for pile in post['total_piles']:
        new_pile_counts[pile] = new_pile_counts.get(pile, 0) + 1

print("=" * 80)
print("PILE MAPPING ANALYSIS")
print("=" * 80)
print(f"\nTotal posts: {total_posts}")
print(f"Posts with pile changes: {posts_changed}")
print(f"Posts with suggested additions: {posts_with_additions}")
print(f"Unique new piles: {len(new_pile_counts)}")

print("\n" + "=" * 80)
print("NEW PILE USAGE FREQUENCY (proposed)")
print("=" * 80)
for pile, count in sorted(new_pile_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{pile:30} {count:3} posts")

print("\n" + "=" * 80)
print("SAMPLE MAPPINGS (first 20 posts with changes)")
print("=" * 80)

sample_count = 0
for post in mapped_posts:
    if set(post['old_piles']) != set(post['new_piles']) and sample_count < 20:
        print(f"\nTitle: {post['title'][:70]}")
        print(f"  Old: {', '.join(post['old_piles']) if post['old_piles'] else '(none)'}")
        print(f"  New: {', '.join(post['new_piles'])}")
        if post['suggested_additions']:
            print(f"  Suggested additions: {', '.join(post['suggested_additions'])}")
        sample_count += 1

# Save full mapping to JSON
output = {
    'summary': {
        'total_posts': total_posts,
        'posts_changed': posts_changed,
        'posts_with_additions': posts_with_additions,
        'unique_piles': len(new_pile_counts)
    },
    'new_pile_counts': new_pile_counts,
    'mapped_posts': mapped_posts
}

with open('pile_mappings_proposed.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 80)
print("Full mappings saved to: pile_mappings_proposed.json")
print("=" * 80)
