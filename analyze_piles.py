#!/usr/bin/env python3
"""Analyze piles usage across all blog posts."""

import os
import re
import yaml
from collections import Counter, defaultdict
from pathlib import Path

def extract_front_matter(file_path):
    """Extract YAML front matter from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

    # Match front matter between --- delimiters
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            yaml_content = match.group(1)
            # Try to normalize tabs to spaces for better YAML parsing
            yaml_content = yaml_content.replace('\t', '  ')
            return yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            # Print first error for debugging
            if not hasattr(extract_front_matter, '_printed_error'):
                print(f"YAML parse error in {file_path}: {e}")
                extract_front_matter._printed_error = True
            return None
    return None

def analyze_posts():
    """Analyze all posts and their piles."""
    posts_dir = Path('_posts')

    all_piles = Counter()
    pile_combinations = Counter()
    posts_by_pile = defaultdict(list)
    posts_without_piles = []
    post_data = []

    total_files = 0
    failed_parsing = 0

    for md_file in sorted(posts_dir.rglob('*.md')):
        total_files += 1
        front_matter = extract_front_matter(md_file)

        if not front_matter:
            failed_parsing += 1
            continue

        title = front_matter.get('title', 'Untitled')
        piles = front_matter.get('piles', [])
        date = front_matter.get('date', '')

        # Normalize piles to list
        if isinstance(piles, str):
            piles = [piles]
        elif piles is None:
            piles = []

        post_info = {
            'file': str(md_file),
            'title': title,
            'date': date,
            'piles': piles
        }
        post_data.append(post_info)

        if piles:
            # Count individual piles
            for pile in piles:
                all_piles[pile] += 1
                posts_by_pile[pile].append(title)

            # Count pile combinations
            pile_combo = tuple(sorted(piles))
            pile_combinations[pile_combo] += 1
        else:
            posts_without_piles.append((str(md_file), title))

    return {
        'total_files': total_files,
        'failed_parsing': failed_parsing,
        'total_posts': len(post_data),
        'posts_with_piles': len([p for p in post_data if p['piles']]),
        'posts_without_piles': posts_without_piles,
        'all_piles': all_piles,
        'pile_combinations': pile_combinations,
        'posts_by_pile': posts_by_pile,
        'post_data': post_data
    }

if __name__ == '__main__':
    results = analyze_posts()

    print("=" * 80)
    print("PILE ANALYSIS SUMMARY")
    print("=" * 80)
    print(f"\nTotal markdown files found: {results['total_files']}")
    print(f"Failed to parse front matter: {results['failed_parsing']}")
    print(f"Successfully parsed posts: {results['total_posts']}")
    print(f"Posts with piles: {results['posts_with_piles']}")
    print(f"Posts without piles: {len(results['posts_without_piles'])}")
    print(f"Unique piles: {len(results['all_piles'])}")

    print("\n" + "=" * 80)
    print("PILE USAGE FREQUENCY (sorted by count)")
    print("=" * 80)
    for pile, count in results['all_piles'].most_common():
        print(f"{pile:40} {count:3} posts")

    print("\n" + "=" * 80)
    print("COMMON PILE COMBINATIONS")
    print("=" * 80)
    for combo, count in sorted(results['pile_combinations'].items(),
                                key=lambda x: x[1], reverse=True)[:20]:
        if len(combo) > 1:
            print(f"{count:3} posts: {', '.join(combo)}")

    print("\n" + "=" * 80)
    print(f"POSTS WITHOUT PILES ({len(results['posts_without_piles'])} total)")
    print("=" * 80)
    for file_path, title in results['posts_without_piles'][:10]:
        print(f"  {title}")
    if len(results['posts_without_piles']) > 10:
        print(f"  ... and {len(results['posts_without_piles']) - 10} more")

    # Save detailed data to JSON for further analysis
    import json
    with open('pile_analysis.json', 'w', encoding='utf-8') as f:
        # Convert Counter objects to dicts for JSON serialization
        output = {
            'summary': {
                'total_posts': results['total_posts'],
                'posts_with_piles': results['posts_with_piles'],
                'posts_without_piles_count': len(results['posts_without_piles'])
            },
            'all_piles': dict(results['all_piles']),
            'pile_combinations': {str(k): v for k, v in results['pile_combinations'].items()},
            'posts': results['post_data']
        }
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("Detailed analysis saved to pile_analysis.json")
    print("=" * 80)
