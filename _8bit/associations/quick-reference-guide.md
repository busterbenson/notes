# 8-Bit Oracle Quick Reference Guide

## Essential Bit Meanings

| Bit | Position | Resource    | Question                                                  | Domain      |
|-----|----------|-------------|-----------------------------------------------------------|-------------|
| 1   | 1XXXXXXX | Intuition   | Do you trust your natural instincts?                      | Inner/Heart |
| 2   | X1XXXXXX | Ability     | Do you have the skills required?                          | Inner/Hands |
| 3   | XX1XXXXX | Capacity    | Do you have the time, space, and resources?               | Inner/Head  |
| 4   | XXX1XXXX | Expectations| Are you aligned with cultural norms?                      | Outer/Heart |
| 5   | XXXX1XXX | Support     | Do your relationships and community have your back?       | Outer/Hands |
| 6   | XXXXX1XX | Options     | Are your possible paths clear?                            | Outer/Head  |
| 7-8 | XXXXXX11 | Cycle Phase | What element, season, and suit characterizes the card?    | Cycle       |

## Inner & Outer World (3-Bit) Combinations

### Inner World (Bits 1-3)

| Pattern | Color   | Trigram | Name         | Description                                    |
|---------|---------|---------|---------------------------------------------------------------|
| 000     | Black   | Earth   | Ants         | Absence of inner resources                     |
| 001     | Blue    | Mountain| Bear         | Capacity to understand but lacking intuition   |
| 010     | Green   | Water   | Spider       | Technical ability present but lacking intuition|
| 011     | Cyan    | Wind    | Crow         | Skilled and resourceful but lacks intuition    |
| 100     | Red     | Thunder | Snake        | Strong intuition but lacking practical skills  |
| 101     | Magenta | Fire    | Fox          | Intuitive and resourceful but lacking skills   |
| 110     | Yellow  | Lake    | Turtle       | Intuitive and skilled but lacking resources    |
| 111     | White   | Heaven  | Monkey       | Complete presence of inner resources           |

### Outer World (Bits 4-6)

| Pattern | Color   | Trigram | Name         | Description                                          |
|---------|---------|---------|---------------------------------------------------------------------|
| 000     | Black   | Earth   | Cave         | Complete lack of outer resources                     |
| 001     | Blue    | Mountain| Tower        | Clear options but lacking alignment and support      |
| 010     | Green   | Water   | Forest       | Support present but lacking alignment and options    |
| 011     | Cyan    | Thunder | Chasm        | Support and options but misaligned with expectations |
| 100     | Red     | Wind    | Road         | Alignment with expectations but lacking support      |
| 101     | Magenta | Fire    | Desert       | Alignment and clear options but lacking support      |
| 110     | Yellow  | Lake    | Lake         | Alignment and support but unclear options            |
| 111     | White   | Heaven  | Village      | Complete presence of outer resources                 |

## Season (Bits 7-8)

| Bits | Season  | 
|------|---------|
| 00   | Winter  |
| 10   | Spring  |
| 11   | Summer  |
| 01   | Autumn  |

## Lunar Cycle, Phase, and Phase Half

### Lunar Cycle happens 4 times per season 
| lunar_cycle = ((decimal_value % 64) ÷ 16) + 1
*Examples:* 
- 00000000 = (0 % 64) / 16 = 0 + 1 = 1st cycle
- 10111010 = (93 % 64) / 16 = 3 + 1 = 2nd cycle
- 11111100 = (63 % 64) / 16 = 2 + 1 = 4th cycle
- 11111111 = (255 % 64) / 16 =   + 1 = 1st cycle
- 01010100 = (42 % 64) / 16 = 3 + 1 = 4th cycle
- 01010101 = (170 % 64) / 16 = 0 + 1 = 1st cycle
- 01010111 = (234 % 64) / 16 = 1 + 1 = 2nd cycle

### Lunar Phase happens once per Lunar Cycle per Season (0 = dark moon, 4 = full moon)
| lunar_phase: decimal_value % 8 
*Phases:*
- 0: Dark Moon 
- 1: New Moon
- 2: First Quarter
- 3: Waxing Gibbous
- 4: Full Moon 
- 5: Waning Gibbous
- 6: Last Quarter
- 7: Balsamic Moon
*Examples:*
- 00000000 = (0 / 2) % 8 = 0: Dark Moon
- 10111010 = (93 / 2) % 8 = 6: Last Quarter
- 11111100 = (63 / 2) % 7 = 7: Balsamic Moon
- 11111111 = (255 / 2) % 8 = 0: Dark Moon
- 01010100 = (42 / 2) % 8 = 5: Waning Gibbous
- 01010101 = (170 / 2) % 8 = 5: Waning Gibbous
- 01010111 = (234 / 2) % 8 = 5: Waning Gibbous

### Each Lunar Phase within a Cycle and Season has 2 halves (0 = Early, 1 = Late)
| phase_half: decimal_value % 2

### Examples (see full mapping in sorts/binary_sort.md)
|-------------|--------------|-------------|-------------|-------------------|-------|
| 8bit binary | L->R Decimal | Season      | Lunar Cycle | Phase             | Half  |
|-------------|--------------|-------------|-------------|-------------------|-------| 
| 00000000    | 0            | Winter      | 1st         | 0: Dark Moon      | Early |
| 10111010    | 93           | Spring      | 2nd         | 6: Last Quarter   | Late  | 
| 11111100    | 63           | Winter      | 4th         | 7: Balsamic Moon  | Late  |
| 11111111    | 255          | Summer      | 1st         | 0: Dark Moon      | Late  |
| 01010100    | 42           | Winter      | 4th         | 5: Waning Gibbous | Early |
| 01010101    | 170          | Fall        | 1st         | 5: Waning Gibbous | Early |
| 01010111    | 170          | Summer      | 2nd         | 5: Waning Gibbous | Early |
|-------------|--------------|-------------|-------------|-------------------|-------|

## Archetypes
Archetypes are described in the archetype-guide.md file in full, but essentially each card has a "resonant season" determined by the first 6 bits, where the first 3 (inner world) are mapped to either 0 or 1 depending on which one has more bits, and the same is done for the second 3 bits (outer world). If inner world reduces to 1 and outer world reduces to 0, then the resonant season is 10, or Spring. That is then compared to the 7th and 8th bits, which describe the season of this card. 

If the resonant season is the same as the card's season, then the archetype is Sage. Moving forward one season at a time, from the resonant season, will determine the archetypes of other cards that have the same first 6 bits. 

For example:
- If the resonant season is Winter, and the season is Winter, then the archetype is Sage.
- If the resonant season is Spring, and the season is Spring, then the archetype is Sage.
- If the resonant season is Summer, and the season is Summer, then the archetype is Sage.
- If the resonant season is Fall, and the season is Fall, then the archetype is Sage.
- If the resonant season is Winter, and the season is Spring, then the archetype is Fool.
- If the resonant season is Winter, and the season is Summer, then the archetype is Hero.
- If the resonant season is Winter, and the season is Fall, then the archetype is Monster.

| Binary    | Decimal | Season | Resonant Season | Archetype |
|-----------|---------|--------|-----------------|-----------|
| 00000000  | 0       | Winter | Winter          | Sage      |
| 10111010  | 93      | Spring | Summer          | Monster   |
| 11111100  | 63      | Winter | Summer          | Hero      |
| 11111111  | 255     | Summer | Summer          | Sage      |
| 01010100  | 42      | Winter | Winter          | Sage      |
| 01010101  | 170     | Fall   | Fall            | Sage      |
| 01010111  | 234     | Summer | Fall            | Monster   |

## Gender
The gender of each card's archetypes is determined by counting the number of "1" bits in positions 1-6 (the resource bits). This count creates a systematic approach to gender assignment that connects to the card's fundamental energy pattern.

| Number of "1" Bits | Gender Assignment                                          |
|--------------------|------------------------------------------------------------|
| 0 or 6 bits        | All archetypes are gender-neutral                          |
| 2 or 4 bits        | Hero and Monster are masculine, Fool and Sage are feminine |
| 3 or 5 bits        | Hero and Monster are feminine, Fool and Sage are masculine |

