# Pile Audit & Taxonomy Redesign

## What I've Created For You

I've conducted a comprehensive audit of all 154 blog posts and your current "piles" (tags) system, and created:

1. **Analysis of current state** - pile_analysis.json
2. **Proposed new taxonomy** - pile_taxonomy_proposal.md
3. **Automated mappings** - pile_mappings_proposed.json
4. **Interactive review tool** - review_pile_mappings.html

---

## Current State Summary

**Your blog posts:**
- 154 posts total analyzed
- 139 posts with piles (90%)
- 15 posts without piles (10%)
- 41 unique piles currently

**Top current piles:**
1. self-reflection (31 posts)
2. year-in-review (22 posts)
3. behavior-change (21 posts)
4. project (17 posts)
5. dialogue (13 posts)
6. 750-words (12 posts)
7. self-tracking (10 posts)

**Problems identified:**
- Inconsistent granularity (very specific vs. very broad)
- Type confusion (content types mixed with topics)
- Conceptual overlap between related piles
- Spelling error: "resiliance" → "resilience"
- Missing key themes (philosophy, spirituality, identity, mortality)

---

## Proposed Solution

### New Taxonomy: 4 Dimensions

I'm proposing reorganizing your piles into 4 clear dimensions:

#### 1. **CONTENT TYPE** (How you're writing)
- reflection, year-review, dialogue, essay, experiment, guide, update, fiction, curation

#### 2. **LIFE DOMAINS** (What area of life)
- identity, relationships, work, health, mortality, creativity, learning, society

#### 3. **INTELLECTUAL DOMAINS** (What you're thinking about)
- psychology, cognitive-science, philosophy, systems-thinking, game-theory, behavior-change, technology, spirituality

#### 4. **SPECIFIC RECURRING TOPICS** (Your signature themes)
- self-tracking, codex-vitae, cognitive-biases, 750words, prisoner-dilemma, fundamental-purpose, meta-crisis, symbols, internal-voices, negative-space, wicked-problems

### Key Changes

**Consolidations:**
- self-reflection → reflection (cleaner)
- year-in-review → year-review (consistent)
- 750-words → 750words (no hyphen)
- cognitive-biases + critical-thinking → cognitive-science (broader)
- personal-mythology → identity
- being-a-creator → creativity + work
- product-management → work
- quality-time → relationships

**New additions:**
- philosophy (missing despite heavy use)
- spirituality (psychedelics, cosmology, mindfulness)
- identity (masks, authenticity, self-discovery)
- mortality (death as motivator/meaning-maker)
- prisoner-dilemma (your recent tournament work)
- symbols (tarot, meaning systems)
- essay, experiment, guide (content types)

**Result:**
- 33 unique piles (down from 41)
- More consistent granularity
- Better coverage of your themes
- Clearer organization

---

## How To Review & Approve

### Step 1: Read the Proposal

Open **pile_taxonomy_proposal.md** and read the full rationale. This explains:
- The 4 dimensions
- All pile mappings (old → new)
- Usage guidelines
- Benefits of the approach

### Step 2: Review the Interactive Tool

1. Open **review_pile_mappings.html** in your web browser
2. The tool shows all 154 posts with their proposed pile mappings
3. For each post you can see:
   - Old piles (in red)
   - New piles (in green)
   - Suggested additions (in orange)
   - Final proposed piles

### Step 3: Review Each Post

Use the interactive tool to:

**Filter options:**
- "Changed Only" - see just posts with pile changes (101 posts)
- "With Suggestions" - posts with AI-suggested additions (21 posts)
- "Pending Review" - posts you haven't decided on yet
- Search bar - find specific posts by title

**For each post, you can:**
- ✓ **Approve** - Accept the proposed piles
- ✎ **Edit Piles** - Manually customize the piles (comma-separated)
- ✗ **Keep Original** - Reject and keep old piles

**Tips:**
- Review "Changed Only" first to see biggest impacts
- Check "With Suggestions" to see AI-detected themes
- Use "Approve All Visible" to bulk-approve filtered results

### Step 4: Export Your Decisions

1. Click "Export Decisions (JSON)" button
2. Copy the generated JSON
3. Save it as `pile_decisions.json` in this directory
4. Send it to me (or just tell me you're done and I'll read it)

---

## What Happens Next

Once you've reviewed and exported your decisions:

1. **I'll create an automated script** that:
   - Reads your pile_decisions.json
   - Updates the front matter of all approved posts
   - Preserves rejected posts as-is
   - Applies your custom edits

2. **I'll run the script** and show you:
   - Summary of changes
   - Sample of updated files
   - Any errors or issues

3. **You review the changes** in git:
   - Use `git diff` to see what changed
   - Verify it looks correct

4. **I'll commit and push** the approved changes to your branch

---

## Files Created

### Analysis Files
- **analyze_piles.py** - Python script that analyzed all posts
- **pile_analysis.json** - Raw analysis data (current state)
- **sample_posts_for_analysis.py** - Script that sampled diverse posts

### Proposal Files
- **pile_taxonomy_proposal.md** - Comprehensive proposal with reasoning
- **generate_pile_mappings.py** - Script that generated proposed mappings
- **pile_mappings_proposed.json** - All 154 posts with proposed new piles

### Review Tool
- **review_pile_mappings.html** - Interactive web-based review interface

### Documentation
- **PILE_AUDIT_README.md** - This file!

---

## Quick Start

```bash
# 1. Open the interactive review tool
open review_pile_mappings.html
# (or just double-click it)

# 2. Review the proposal document
cat pile_taxonomy_proposal.md

# 3. Go through posts and approve/edit/reject

# 4. Export your decisions when done

# 5. Let me know you're ready for implementation!
```

---

## Sample Mappings Preview

Here are some example mappings to give you a feel:

**"47 - CHALANT!" (2023 year review)**
- Old: `self-reflection`, `year-in-review`
- New: `reflection`, `year-review`, `identity`, `psychology`, `spirituality`

**"Cognitive Bias Cheat Sheet"**
- Old: `cognitive-biases`
- New: `curation`, `cognitive-science`, `cognitive-biases`

**"Disconnect Saturdays"**
- Old: `behavior-change`
- New: `experiment`, `behavior-change`, `relationships`, `technology`

**"Death Bed Game"**
- Old: `death`, `self-tracking`
- New: `guide`, `self-tracking`, `mortality`, `behavior-change`

**"750 words a day..."**
- Old: `project`, `750-words`
- New: `update`, `750words`, `work`

---

## Questions & Feedback

As you review, consider:

1. **Do the 4 dimensions make sense?** Too many? Too few?
2. **Are pile names good?** Any you'd rename?
3. **Right granularity?** Too specific or too broad anywhere?
4. **Missing themes?** Anything I didn't capture?
5. **Multiple piles per post?** Most posts will have 3-5 piles - is that okay?

Add comments directly in the review tool's custom edits, or just keep notes and we'll discuss!

---

## Philosophy Behind the Proposal

Based on reading your work (especially "Chalant" and your cosmology questionnaire), I designed this taxonomy to honor:

1. **Both quantification AND illegibility** - systematic frameworks alongside messy personal becoming
2. **Multiple perspectives** - posts can be many things at once (reflection + guide + philosophy)
3. **Your evolution** - from masks/systems toward authenticity/feelings, reflected in pile options
4. **Intellectual depth** - philosophy, spirituality, psychology as first-class domains
5. **Practical usability** - clear enough for navigation, flexible enough for complexity

The goal isn't to force your rich, multifaceted writing into neat boxes, but to create **multiple pathways** for readers (and future-you) to discover related content.

---

## Ready?

Open `review_pile_mappings.html` and let's do this! 🚀

Questions? Concerns? Want to modify the proposal before reviewing? Just let me know!
