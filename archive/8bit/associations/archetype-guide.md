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

| Inner World | Outer World   | Pattern | Resonant Season |
|-------------|---------------|---------|-----------------|
| Inactive (0) | Inactive (0) | 00      | Winter          |
| Active (1)   | Inactive (0) | 10      | Spring          |
| Active (1)   | Active (1)   | 11      | Summer          |
| Inactive (0) | Active (1)   | 01      | Fall            |

## The Four Archetypes

Each card expresses one of four archetypes, determined by the relationship between the card's resonant season and the season represented by its cycle bits (bits 7-8).

| Relationship    | Archetype   | Color        | Qualities                                  |
|-----------------|-------------|--------------|--------------------------------------------|
| Resonant Season | **Sage**    | Iridescent   | Integrated, wise, harmonious expression    |
| Next Season     | **Fool**    | Turquoise    | Innocent, new beginning, fresh perspective |
| Third Season    | **Hero**    | Gold         | Skilled, masterful, powerful expression    |
| Fourth Season   | **Monster** | Purple       | Excessive, challenging, shadow expression  |

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

## Lookup
| Binary    | L->R Decimal | Season | Resonant Season | Archetype |
|-----------|---------|--------|-----------------|-----------|
| 00000000  | 0       | Winter | Winter          | Sage      |
| 10000000  | 1       | Winter | Winter          | Sage      |
| 01000000  | 2       | Winter | Winter          | Sage      |
| 11000000  | 3       | Winter | Spring          | Monster   |
| 00100000  | 4       | Winter | Winter          | Sage      |
| 10100000  | 5       | Winter | Spring          | Monster   |
| 01100000  | 6       | Winter | Spring          | Monster   |
| 11100000  | 7       | Winter | Spring          | Monster   |
| 00010000  | 8       | Winter | Winter          | Sage      |
| 10010000  | 9       | Winter | Winter          | Sage      |
| 01010000  | 10      | Winter | Winter          | Sage      |
| 11010000  | 11      | Winter | Spring          | Monster   |
| 00110000  | 12      | Winter | Winter          | Sage      |
| 10110000  | 13      | Winter | Spring          | Monster   |
| 01110000  | 14      | Winter | Spring          | Monster   |
| 11110000  | 15      | Winter | Spring          | Monster   |
| 00001000  | 16      | Winter | Winter          | Sage      |
| 10001000  | 17      | Winter | Winter          | Sage      |
| 01001000  | 18      | Winter | Winter          | Sage      |
| 11001000  | 19      | Winter | Spring          | Monster   |
| 00101000  | 20      | Winter | Winter          | Sage      |
| 10101000  | 21      | Winter | Spring          | Monster   |
| 01101000  | 22      | Winter | Spring          | Monster   |
| 11101000  | 23      | Winter | Spring          | Monster   |
| 00011000  | 24      | Winter | Fall            | Fool      |
| 10011000  | 25      | Winter | Fall            | Fool      |
| 01011000  | 26      | Winter | Fall            | Fool      |
| 11011000  | 27      | Winter | Summer          | Hero      |
| 00111000  | 28      | Winter | Fall            | Fool      |
| 10111000  | 29      | Winter | Summer          | Hero      |
| 01111000  | 30      | Winter | Summer          | Hero      |
| 11111000  | 31      | Winter | Summer          | Hero      |
| 00000100  | 32      | Winter | Winter          | Sage      |
| 10000100  | 33      | Winter | Winter          | Sage      |
| 01000100  | 34      | Winter | Winter          | Sage      |
| 11000100  | 35      | Winter | Spring          | Monster   |
| 00100100  | 36      | Winter | Winter          | Sage      |
| 10100100  | 37      | Winter | Spring          | Monster   |
| 01100100  | 38      | Winter | Spring          | Monster   |
| 11100100  | 39      | Winter | Spring          | Monster   |
| 00010100  | 40      | Winter | Fall            | Fool      |
| 10010100  | 41      | Winter | Fall            | Fool      |
| 01010100  | 42      | Winter | Fall            | Fool      |
| 11010100  | 43      | Winter | Summer          | Hero      |
| 00110100  | 44      | Winter | Fall            | Fool      |
| 10110100  | 45      | Winter | Summer          | Hero      |
| 01110100  | 46      | Winter | Summer          | Hero      |
| 11110100  | 47      | Winter | Summer          | Hero      |
| 00001100  | 48      | Winter | Fall            | Fool      |
| 10001100  | 49      | Winter | Fall            | Fool      |
| 01001100  | 50      | Winter | Fall            | Fool      |
| 11001100  | 51      | Winter | Summer          | Hero      |
| 00101100  | 52      | Winter | Fall            | Fool      |
| 10101100  | 53      | Winter | Summer          | Hero      |
| 01101100  | 54      | Winter | Summer          | Hero      |
| 11101100  | 55      | Winter | Summer          | Hero      |
| 00011100  | 56      | Winter | Fall            | Fool      |
| 10011100  | 57      | Winter | Fall            | Fool      |
| 01011100  | 58      | Winter | Fall            | Fool      |
| 11011100  | 59      | Winter | Summer          | Hero      |
| 00111100  | 60      | Winter | Fall            | Fool      |
| 10111100  | 61      | Winter | Summer          | Hero      |
| 01111100  | 62      | Winter | Summer          | Hero      |
| 11111100  | 63      | Winter | Summer          | Hero      |
| 00000010  | 64      | Spring | Winter          | Fool      |
| 10000010  | 65      | Spring | Winter          | Fool      |
| 01000010  | 66      | Spring | Winter          | Fool      |
| 11000010  | 67      | Spring | Spring          | Sage      |
| 00100010  | 68      | Spring | Winter          | Fool      |
| 10100010  | 69      | Spring | Spring          | Sage      |
| 01100010  | 70      | Spring | Spring          | Sage      |
| 11100010  | 71      | Spring | Spring          | Sage      |
| 00010010  | 72      | Spring | Winter          | Fool      |
| 10010010  | 73      | Spring | Winter          | Fool      |
| 01010010  | 74      | Spring | Winter          | Fool      |
| 11010010  | 75      | Spring | Spring          | Sage      |
| 00110010  | 76      | Spring | Winter          | Fool      |
| 10110010  | 77      | Spring | Spring          | Sage      |
| 01110010  | 78      | Spring | Spring          | Sage      |
| 11110010  | 79      | Spring | Spring          | Sage      |
| 00001010  | 80      | Spring | Winter          | Fool      |
| 10001010  | 81      | Spring | Winter          | Fool      |
| 01001010  | 82      | Spring | Winter          | Fool      |
| 11001010  | 83      | Spring | Spring          | Sage      |
| 00101010  | 84      | Spring | Winter          | Fool      |
| 10101010  | 85      | Spring | Spring          | Sage      |
| 01101010  | 86      | Spring | Spring          | Sage      |
| 11101010  | 87      | Spring | Spring          | Sage      |
| 00011010  | 88      | Spring | Fall            | Hero      |
| 10011010  | 89      | Spring | Fall            | Hero      |
| 01011010  | 90      | Spring | Fall            | Hero      |
| 11011010  | 91      | Spring | Summer          | Monster   |
| 00111010  | 92      | Spring | Fall            | Hero      |
| 10111010  | 93      | Spring | Summer          | Monster   |
| 01111010  | 94      | Spring | Summer          | Monster   |
| 11111010  | 95      | Spring | Summer          | Monster   |
| 00000110  | 96      | Spring | Winter          | Fool      |
| 10000110  | 97      | Spring | Winter          | Fool      |
| 01000110  | 98      | Spring | Winter          | Fool      |
| 11000110  | 99      | Spring | Spring          | Sage      |
| 00100110  | 100     | Spring | Winter          | Fool      |
| 10100110  | 101     | Spring | Spring          | Sage      |
| 01100110  | 102     | Spring | Spring          | Sage      |
| 11100110  | 103     | Spring | Spring          | Sage      |
| 00010110  | 104     | Spring | Fall            | Hero      |
| 10010110  | 105     | Spring | Fall            | Hero      |
| 01010110  | 106     | Spring | Fall            | Hero      |
| 11010110  | 107     | Spring | Summer          | Monster   |
| 00110110  | 108     | Spring | Fall            | Hero      |
| 10110110  | 109     | Spring | Summer          | Monster   |
| 01110110  | 110     | Spring | Summer          | Monster   |
| 11110110  | 111     | Spring | Summer          | Monster   |
| 00001110  | 112     | Spring | Fall            | Hero      |
| 10001110  | 113     | Spring | Fall            | Hero      |
| 01001110  | 114     | Spring | Fall            | Hero      |
| 11001110  | 115     | Spring | Summer          | Monster   |
| 00101110  | 116     | Spring | Fall            | Hero      |
| 10101110  | 117     | Spring | Summer          | Monster   |
| 01101110  | 118     | Spring | Summer          | Monster   |
| 11101110  | 119     | Spring | Summer          | Monster   |
| 00011110  | 120     | Spring | Fall            | Hero      |
| 10011110  | 121     | Spring | Fall            | Hero      |
| 01011110  | 122     | Spring | Fall            | Hero      |
| 11011110  | 123     | Spring | Summer          | Monster   |
| 00111110  | 124     | Spring | Fall            | Hero      |
| 10111110  | 125     | Spring | Summer          | Monster   |
| 01111110  | 126     | Spring | Summer          | Monster   |
| 11111110  | 127     | Spring | Summer          | Monster   |
| 00000001  | 128     | Fall   | Winter          | Monster   |
| 10000001  | 129     | Fall   | Winter          | Monster   |
| 01000001  | 130     | Fall   | Winter          | Monster   |
| 11000001  | 131     | Fall   | Spring          | Fool      |
| 00100001  | 132     | Fall   | Winter          | Monster   |
| 10100001  | 133     | Fall   | Spring          | Fool      |
| 01100001  | 134     | Fall   | Spring          | Fool      |
| 11100001  | 135     | Fall   | Spring          | Fool      |
| 00010001  | 136     | Fall   | Winter          | Monster   |
| 10010001  | 137     | Fall   | Winter          | Fool      |
| 01010001  | 138     | Fall   | Winter          | Fool      |
| 11010001  | 139     | Fall   | Spring          | Fool      |
| 00110001  | 140     | Fall   | Winter          | Fool      |
| 10110001  | 141     | Fall   | Spring          | Fool      |
| 01110001  | 142     | Fall   | Spring          | Fool      |
| 11110001  | 143     | Fall   | Spring          | Fool      |
| 00001001  | 144     | Fall   | Winter          | Monster   |
| 10001001  | 145     | Fall   | Winter          | Fool      |
| 01001001  | 146     | Fall   | Winter          | Fool      |
| 11001001  | 147     | Fall   | Spring          | Fool      |
| 00101001  | 148     | Fall   | Winter          | Fool      |
| 10101001  | 149     | Fall   | Spring          | Fool      |
| 01101001  | 150     | Fall   | Spring          | Fool      |
| 11101001  | 151     | Fall   | Spring          | Fool      |
| 00011001  | 152     | Fall   | Fall            | Sage      |
| 10011001  | 153     | Fall   | Fall            | Sage      |
| 01011001  | 154     | Fall   | Fall            | Sage      |
| 11011001  | 155     | Fall   | Summer          | Monster   |
| 00111001  | 156     | Fall   | Fall            | Sage      |
| 10111001  | 157     | Fall   | Summer          | Monster   |
| 01111001  | 158     | Fall   | Summer          | Monster   |
| 11111001  | 159     | Fall   | Summer          | Monster   |
| 00000101  | 160     | Fall   | Winter          | Monster   |
| 10000101  | 161     | Fall   | Winter          | Monster   |
| 01000101  | 162     | Fall   | Winter          | Monster   |
| 11000101  | 163     | Fall   | Spring          | Fool      |
| 00100101  | 164     | Fall   | Winter          | Monster   |
| 10100101  | 165     | Fall   | Spring          | Fool      |
| 01100101  | 166     | Fall   | Spring          | Fool      |
| 11100101  | 167     | Fall   | Spring          | Fool      |
| 00010101  | 168     | Fall   | Fall            | Sage      |
| 10010101  | 169     | Fall   | Fall            | Sage      |
| 01010101  | 170     | Fall   | Fall            | Sage      |
| 11010101  | 171     | Fall   | Summer          | Monster   |
| 00110101  | 172     | Fall   | Fall            | Sage      |
| 10110101  | 173     | Fall   | Summer          | Monster   |
| 01110101  | 174     | Fall   | Summer          | Monster   |
| 11110101  | 175     | Fall   | Summer          | Monster   |
| 00001101  | 176     | Fall   | Fall            | Sage      |
| 10001101  | 177     | Fall   | Fall            | Sage      |
| 01001101  | 178     | Fall   | Fall            | Sage      |
| 11001101  | 179     | Fall   | Summer          | Monster   |
| 00101101  | 180     | Fall   | Fall            | Sage      |
| 10101101  | 181     | Fall   | Summer          | Monster   |
| 01101101  | 182     | Fall   | Summer          | Monster   |
| 11101101  | 183     | Fall   | Summer          | Monster   |
| 00011101  | 184     | Fall   | Fall            | Sage      |
| 10011101  | 185     | Fall   | Fall            | Sage      |
| 01011101  | 186     | Fall   | Fall            | Sage      |
| 11011101  | 187     | Fall   | Summer          | Monster   |
| 00111101  | 188     | Fall   | Fall            | Sage      |
| 10111101  | 189     | Fall   | Summer          | Monster   |
| 01111101  | 190     | Fall   | Summer          | Monster   |
| 11111101  | 191     | Fall   | Summer          | Monster   |
| 00000011  | 192     | Summer | Winter          | Hero      |
| 10000011  | 193     | Summer | Winter          | Hero      |
| 01000011  | 194     | Summer | Winter          | Hero      |
| 11000011  | 195     | Summer | Spring          | Fool      |
| 00100011  | 196     | Summer | Winter          | Hero      |
| 10100011  | 197     | Summer | Spring          | Fool      |
| 01100011  | 198     | Summer | Spring          | Fool      |
| 11100011  | 199     | Summer | Spring          | Fool      |
| 00010011  | 200     | Summer | Winter          | Hero      |
| 10010011  | 201     | Summer | Winter          | Hero      |
| 01010011  | 202     | Summer | Winter          | Hero      |
| 11010011  | 203     | Summer | Spring          | Fool      |
| 00110011  | 204     | Summer | Winter          | Hero      |
| 10110011  | 205     | Summer | Spring          | Fool      |
| 01110011  | 206     | Summer | Spring          | Fool      |
| 11110011  | 207     | Summer | Spring          | Fool      |
| 00001011  | 208     | Summer | Winter          | Hero      |
| 10001011  | 209     | Summer | Winter          | Hero      |
| 01001011  | 210     | Summer | Winter          | Fool      |
| 11001011  | 211     | Summer | Spring          | Fool      |
| 00101011  | 212     | Summer | Winter          | Hero      |
| 10101011  | 213     | Summer | Spring          | Fool      |
| 01101011  | 214     | Summer | Spring          | Fool      |
| 11101011  | 215     | Summer | Spring          | Fool      |
| 00011011  | 216     | Summer | Fall            | Monster   |
| 10011011  | 217     | Summer | Fall            | Monster   |
| 01011011  | 218     | Summer | Fall            | Monster   |
| 11011011  | 219     | Summer | Summer          | Sage      |
| 00111011  | 220     | Summer | Fall            | Monster   |
| 10111011  | 221     | Summer | Summer          | Sage      |
| 01111011  | 222     | Summer | Summer          | Sage      |
| 11111011  | 223     | Summer | Summer          | Sage      |
| 00000111  | 224     | Summer | Winter          | Hero      |
| 10000111  | 225     | Summer | Winter          | Hero      |
| 01000111  | 226     | Summer | Winter          | Hero      |
| 11000111  | 227     | Summer | Spring          | Fool      |
| 00100111  | 228     | Summer | Winter          | Hero      |
| 10100111  | 229     | Summer | Spring          | Fool      |
| 01100111  | 230     | Summer | Spring          | Fool      |
| 11100111  | 231     | Summer | Spring          | Fool      |
| 00010111  | 232     | Summer | Fall            | Monster   |
| 10010111  | 233     | Summer | Fall            | Monster   |
| 01010111  | 234     | Summer | Fall            | Monster   |
| 11010111  | 235     | Summer | Summer          | Sage      |
| 00110111  | 236     | Summer | Fall            | Monster   |
| 10110111  | 237     | Summer | Summer          | Sage      |
| 01110111  | 238     | Summer | Summer          | Sage      |
| 11110111  | 239     | Summer | Summer          | Sage      |
| 00001111  | 240     | Summer | Fall            | Monster   |
| 10001111  | 241     | Summer | Fall            | Monster   |
| 01001111  | 242     | Summer | Fall            | Monster   |
| 11001111  | 243     | Summer | Summer          | Sage      |
| 00101111  | 244     | Summer | Fall            | Monster   |
| 10101111  | 245     | Summer | Summer          | Sage      |
| 01101111  | 246     | Summer | Summer          | Sage      |
| 11101111  | 247     | Summer | Summer          | Sage      |
| 00011111  | 248     | Summer | Fall            | Monster   |
| 10011111  | 249     | Summer | Fall            | Monster   |
| 01011111  | 250     | Summer | Fall            | Monster   |
| 11011111  | 251     | Summer | Summer          | Sage      |
| 00111111  | 252     | Summer | Fall            | Monster   |
| 10111111  | 253     | Summer | Summer          | Sage      |
| 01111111  | 254     | Summer | Summer          | Sage      |
| 11111111  | 255     | Summer | Summer          | Sage      |
