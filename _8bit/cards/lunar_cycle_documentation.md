# 8-Bit Oracle Lunar Cycle Documentation

## Binary Code Structure

The 8-bit binary code for each card encodes its season, lunar cycle, phase, and half:

```
XXYYZZZH
```

Where:
- `XX` (bits 7-8): Season
  - 00 = Winter
  - 10 = Spring
  - 11 = Summer
  - 01 = Fall

- `YY` (bits 5-6): Lunar Cycle within the season
  - 00 = Cycle 1 (Inception Cycle)
  - 01 = Cycle 2 (Development Cycle)
  - 10 = Cycle 3 (Culmination Cycle)
  - 11 = Cycle 4 (Transition Cycle)

- `ZZZ` (bits 2-4): Lunar Phase
  - 000 = Dark Moon
  - 001 = New Moon
  - 010 = First Quarter
  - 011 = Waxing Gibbous
  - 100 = Full Moon
  - 101 = Waning Gibbous
  - 110 = Last Quarter
  - 111 = Balsamic Moon

- `H` (bit 1): Half
  - 0 = First Half
  - 1 = Second Half

## Lunar Phases and Halves

### Dark Moon

#### Deepening (0%)

Binary pattern: ZZZ=000, H=0

Example card: 00000000 (Winter, Cycle 1)

#### Emerging (0-1%)

Binary pattern: ZZZ=000, H=1

Example card: 00000001 (Winter, Cycle 1)

### New Moon

#### Birthing (1-6%)

Binary pattern: ZZZ=001, H=0

Example card: 00000010 (Winter, Cycle 1)

#### Strengthening (6-12.5%)

Binary pattern: ZZZ=001, H=1

Example card: 00000011 (Winter, Cycle 1)

### First Quarter

#### Challenging (12.5-25%)

Binary pattern: ZZZ=010, H=0

Example card: 00000100 (Winter, Cycle 1)

#### Balancing (25-37.5%)

Binary pattern: ZZZ=010, H=1

Example card: 00000101 (Winter, Cycle 1)

### Waxing Gibbous

#### Building (37.5-50%)

Binary pattern: ZZZ=011, H=0

Example card: 00000110 (Winter, Cycle 1)

#### Culminating (50-62.5%)

Binary pattern: ZZZ=011, H=1

Example card: 00000111 (Winter, Cycle 1)

### Full Moon

#### Illuminating (62.5-75%)

Binary pattern: ZZZ=100, H=0

Example card: 00001000 (Winter, Cycle 1)

#### Revealing (75-87.5%)

Binary pattern: ZZZ=100, H=1

Example card: 00001001 (Winter, Cycle 1)

### Waning Gibbous

#### Sharing (87.5-75%)

Binary pattern: ZZZ=101, H=0

Example card: 00001010 (Winter, Cycle 1)

#### Integrating (75-62.5%)

Binary pattern: ZZZ=101, H=1

Example card: 00001011 (Winter, Cycle 1)

### Last Quarter

#### Releasing (62.5-50%)

Binary pattern: ZZZ=110, H=0

Example card: 00001100 (Winter, Cycle 1)

#### Resolving (50-37.5%)

Binary pattern: ZZZ=110, H=1

Example card: 00001101 (Winter, Cycle 1)

### Balsamic Moon

#### Distilling (37.5-12.5%)

Binary pattern: ZZZ=111, H=0

Example card: 00001110 (Winter, Cycle 1)

#### Surrendering (12.5-0%)

Binary pattern: ZZZ=111, H=1

Example card: 00001111 (Winter, Cycle 1)

## Lunar Cycles

### Cycle 1: Inception Cycle

The Inception Cycle is the beginning of the season's energy, establishing the seasonal pattern.

Binary pattern: YY=00

### Cycle 2: Development Cycle

The Development Cycle represents growth and expansion of the season's energy, developing its themes.

Binary pattern: YY=01

### Cycle 3: Culmination Cycle

The Culmination Cycle expresses the peak of the season's energy, bringing its themes to fruition.

Binary pattern: YY=10

### Cycle 4: Transition Cycle

The Transition Cycle represents the shifting energy of the season, preparing for the next season.

Binary pattern: YY=11

