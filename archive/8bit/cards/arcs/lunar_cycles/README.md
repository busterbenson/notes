# Lunar Cycle Narrative Arcs

## Overview

The lunar cycle narrative arcs provide a framework for understanding how cards within the same lunar cycle relate to each other across the stages of the lunar month. Each season contains four lunar cycles, for a total of 16 distinct lunar cycles across the entire 8-Bit Oracle system.

## Structure

Each lunar cycle contains 16 cards, representing the 8 phases of the moon, each with an early and late half:

1. **Dark Moon**
   - Early (Deepening)
   - Late (Emerging)

2. **New Moon**
   - Early (Birthing)
   - Late (Strengthening)

3. **First Quarter**
   - Early (Challenging)
   - Late (Balancing)

4. **Waxing Gibbous**
   - Early (Building)
   - Late (Culminating)

5. **Full Moon**
   - Early (Illuminating)
   - Late (Revealing)

6. **Waning Gibbous**
   - Early (Sharing)
   - Late (Integrating)

7. **Last Quarter**
   - Early (Releasing)
   - Late (Resolving)

8. **Balsamic Moon**
   - Early (Distilling)
   - Late (Surrendering)

## Seasonal Lunar Cycles

### Winter
- [Winter Cycle 1](winter-1.md) - Inception Cycle of Winter
- [Winter Cycle 2](winter-2.md) - Development Cycle of Winter
- [Winter Cycle 3](winter-3.md) - Culmination Cycle of Winter
- [Winter Cycle 4](winter-4.md) - Transition Cycle of Winter

### Spring
- [Spring Cycle 1](spring-1.md) - Inception Cycle of Spring
- [Spring Cycle 2](spring-2.md) - Development Cycle of Spring
- [Spring Cycle 3](spring-3.md) - Culmination Cycle of Spring
- [Spring Cycle 4](spring-4.md) - Transition Cycle of Spring

### Summer
- [Summer Cycle 1](summer-1.md) - Inception Cycle of Summer
- [Summer Cycle 2](summer-2.md) - Development Cycle of Summer
- [Summer Cycle 3](summer-3.md) - Culmination Cycle of Summer
- [Summer Cycle 4](summer-4.md) - Transition Cycle of Summer

### Fall
- [Fall Cycle 1](fall-1.md) - Inception Cycle of Fall
- [Fall Cycle 2](fall-2.md) - Development Cycle of Fall
- [Fall Cycle 3](fall-3.md) - Culmination Cycle of Fall
- [Fall Cycle 4](fall-4.md) - Transition Cycle of Fall

## Usage in Card Development

When developing card descriptions and imagery:

1. **Identify the Lunar Cycle**: Determine which of the 16 lunar cycles the card belongs to based on its binary code

2. **Understand the Phase Position**: Identify which phase of the moon the card represents and whether it's the early or late half of that phase

3. **Incorporate Cycle Themes**: Draw on the themes, symbolism, and narrative elements from the appropriate lunar cycle arc document

4. **Maintain Visual Continuity**: Ensure that card imagery reflects both the lunar phase and the appropriate seasonal context

## Calculation Method

The lunar phase and cycle position can be calculated from the card's decimal value as follows:

- **Lunar Cycle**: `((decimal_value % 64) ÷ 16) + 1` (Yields cycle 1-4 within the season)
- **Lunar Phase**: `(decimal_value ÷ 2) % 8` (Yields phase 0-7)
- **Phase Half**: `decimal_value % 2` (0 = Early, 1 = Late)
