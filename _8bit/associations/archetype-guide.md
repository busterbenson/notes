# Archetype Guide

## Overview

The 8-bit Oracle employs a four-archetype system that maps to the four seasons and their energies. Each card has both an inherent archetype that is determined by the inner and outer world resource patterns. This guide explains how the system works and how archetypes interact with seasonal cycles.

## Determining Inner and Outer World States

The foundation of the archetype system is based on the state of the inner and outer world resources.

### Inner World (Bits 1-3)

- **Bit 1:** Intuition - Do you trust your natural instincts? (bit_mask: 1XXXXXXX)
- **Bit 2:** Ability - Do you have the skills and know-how? (bit_mask: X1XXXXXX)
- **Bit 3:** Capacity - Do your circumstances provide enough resources? (bit_mask: XX1XXXXX)

The inner world is considered:
- **Active (1)** if two or more of these bits are 1  (bit_mask: ???XXXXX)
- **Inactive (0)** if two or more of these bits are 0 (bit_mask: ???XXXXX)

### Outer World (Bits 4-6)

- **Bit 4:** Expectations - Are you aligned with cultural norms? (bit_mask: XXX1XXXX)
- **Bit 5:** Support - Do your relationships support you? (bit_mask: XXXX1XXX)
- **Bit 6:** Options - Are possible paths clear to you? (bit_mask: XXXXX1XX)

The outer world is considered:
- **Active (1)** if two or more of these bits are 1 (bit_mask: XXX???XX)
- **Inactive (0)** if two or more of these bits are 0 (bit_mask: XXX???XX)

## Resonant Season Mapping

The combination of inner and outer world states creates four possible patterns, each associated with a season:

| Inner World | Outer World | Pattern | Resonant Season |
|-------------|-------------|---------|-----------------|
| Inactive (0) | Inactive (0) | 00    | Winter |
| Active (1)   | Inactive (0) | 10    | Spring |
| Active (1)   | Active (1)   | 11    | Summer |
| Inactive (0) | Active (1)   | 01    | Fall   |

## The Four Archetypes

Each card expresses one of four archetypes, determined by the relationship between the card's resonant season and the season represented by its cycle bits (bits 7-8).

| Relationship | Archetype | Color | Qualities |
|--------------|-----------|-------|-----------|
| Resonant Season | **Sage**    | Iridescent   | Integrated, wise, harmonious expression |
| Next Season     | **Fool**    | Turquoise    | Innocent, new beginning, fresh perspective |
| Third Season    | **Hero**    | Gold         | Skilled, masterful, powerful expression |
| Fourth Season   | **Monster** | Purple       | Excessive, challenging, shadow expression |

### Seasonal Progression and Narrative Cycles

The natural progression of seasons follows this order:
Winter → Spring → Summer → Fall → Winter

For example, if a card's resonant season is Winter:
- Sage expression = Winter
- Fool expression = Spring (next season)
- Hero expression = Summer (third season)
- Monster expression = Fall (fourth season)

### Narrative Arc of Archetypes

In terms of narrative progression and consciousness development, the archetypal journey always begins with the Fool (Spring) and proceeds through a natural cycle:

1. **Fool (Spring)** - The beginning of the journey; awakening, innocence, first awareness
2. **Hero (Summer)** - The development phase; mastery, achievement, full expression
3. **Monster (Fall)** - The challenge phase; transformation, release, shadow integration
4. **Sage (Winter)** - The integration phase; wisdom, completion, transcendence

After the Sage phase, the cycle potentially begins again at a higher level, with the Sage transcending to become a new kind of Fool. This spiral of development is reflected in the seasonal progression of each hexagram's four cards.

## Archetype Qualities

### Fool
The Fool represents innocence, new beginnings, and fresh perspectives. It appears when a card's resonant season is followed by its cycle bits' season. The Fool archetype embodies potential and untested energy, where the card's pattern is moving into a new phase with openness and curiosity. The fool manifests in cards as characters in childhood or at the threshold of a journey. In the narrative cycle, the Fool is always the beginning point - the awakening of consciousness to new possibilities. In the Gene Key associations (found in core-systems.yml and gene-keys-reference.md), the Fool is associated with the gene key's raw potential, outside of the more specific nuances of the shadow, gift, and siddhi.

### Hero
The Hero represents skill, mastery, and accomplished power. It appears when a card's resonant season is two steps ahead of its cycle bits' season. The Hero archetype embodies competence and achievement, where the card's pattern has matured and developed strong capabilities, and yet also has the seed of its own shadow. The hero will often manifest in cards as the peak form of an individual human character, but usually as a snapshot in time that will inevitably change and lose that moment of perfection. In the narrative cycle, the Hero follows the Fool, representing the development and mastery phase of consciousness. In the Gene Key associations (found in core-systems.yml and gene-keys-reference.md), the Hero is associated with the gift version of the gene key that is associated with the card in question.

### Monster
The Monster represents the seed of the hero's shadow realized: the resultant excess, challenges caused by the solutions of the past, and shadow aspects that the hero didn't want to confront. It appears when a card's resonant season is three steps ahead of (or one step behind) its cycle bits' season. The Monster archetype embodies the imbalanced or exaggerated expression of the card's qualities, where energy has become distorted or overwhelming. The monster will often manifest in cards as an animal/creature/monster that represents the shadow of the hero it's related to. In the narrative cycle, the Monster follows the Hero, representing the challenge and transformation phase of consciousness. In the Gene Key associations (found in core-systems.yml and gene-keys-reference.md), the Monster is associated with the shadow version of the gene key that is associated with the card in question.

### Sage
The Sage represents a collective state of wisdom, integration, and harmony between its energy's strengths AND acceptance and accountability for its shadow, across individuals and time. It appears when a card's resonant season matches its cycle bits' season. The Sage archetype embodies the most balanced expression of the card's energy, where inner and outer worlds are appropriately aligned with the cycle phase. The sage manifests in cards as multifaceted and chimeric in nature (a union of several characters/creatures/groups), whole in time more than space, because they integrate cycles of change and growth. In the narrative cycle, the Sage follows the Monster, representing the integration and transcendence phase of consciousness. The Sage contains the wisdom of the entire cycle and ultimately transcends it to become a new kind of Fool at a higher level. In the Gene Key associations (found in core-systems.yml and gene-keys-reference.md), the Sage is associated with the siddhi version of the gene key that is associated with the card in question.

## Example Applications

### Card 00000000 (The Moon in Winter)
- **Inner World:** 0 (all bits off)
- **Outer World:** 0 (all bits off)
- **Resonant Season:** Winter
- **Cycle Bits:** 00 = Winter
- **Archetype:** Sage (Winter resonance in Winter cycle)
- **Expression:** The integrated wisdom of the void, perfect emptiness and potential

### Card 11100001 (Return in Spring)
- **Inner World:** 1 (bits 1-3 all on)
- **Outer World:** 0 (bits 4-5 off, bit 6 on)
- **Resonant Season:** Spring
- **Cycle Bits:** 01 = Spring
- **Archetype:** Sage (Spring resonance in Spring cycle)
- **Expression:** The integrated wisdom of renewal and growth, harmonious beginning

## Usage in Readings

The archetype of a card provides insight into how its energy is currently manifesting and the quality of its expression:

- **Sage cards** suggest alignment and wisdom. The situation is unfolding in a balanced way.
- **Fool cards** indicate new beginnings and untested potential. Fresh approaches are favored.
- **Hero cards** point to competence and achievement. Skill and mastery are available.
- **Monster cards** reveal challenges and excess. Something may be out of balance or exaggerated.

The archetype system provides a framework for understanding the qualitative expression of each card's binary pattern, adding nuance and depth to readings.