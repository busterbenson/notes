# CORRECT PERFECT LUNAR MAPPING OF 8-BIT ORACLE CARDS

This document lists all 256 cards with a perfect 1:1 mapping between cards and lunar attributes.
The mapping respects the following key concepts from lunar-cycle.yml:
- Season: Determined by bits 7-8 (00=Winter, 10=Spring, 11=Summer, 01=Fall)
- Each unique combination of season, lunar cycle, phase, and half exists exactly once

## Binary Code Structure

Each 8-bit binary code reads from left to right:
```
bbbbbbSS
```

- bbbbbb: Bits 1-6 used for lunar cycle and phase mapping
- SS: Season bits (bits 7-8) where 00=Winter, 10=Spring, 11=Summer, 01=Fall

## Card Arrangement

| # | Binary | Dec | Season | Cycle | Moon Phase | Half | Illumination | Resonant Season | Archetype | Card Name |
|---|--------|-----|--------|-------|------------|------|--------------|-----------------|-----------|----------|
| 1 | 00000000 | 0 | Winter | 1/4 | Dark Moon | Deepening | 0% | Winter | Sage | Void Mirror |
| 2 | 00000100 | 4 | Winter | 1/4 | Dark Moon | Emerging | 0-1% | Winter | Sage |  |
| 3 | 00001000 | 8 | Winter | 1/4 | New Moon | Birthing | 1-6% | Winter | Sage |  |
| 4 | 00001100 | 12 | Winter | 1/4 | New Moon | Strengthening | 6-12.5% | Fall | Monster |  |
| 5 | 00010000 | 16 | Winter | 1/4 | First Quarter | Challenging | 12.5-25% | Winter | Sage |  |
| 6 | 00010100 | 20 | Winter | 1/4 | First Quarter | Balancing | 25-37.5% | Fall | Monster |  |
| 7 | 00011000 | 24 | Winter | 1/4 | Waxing Gibbous | Building | 37.5-50% | Fall | Monster |  |
| 8 | 00011100 | 28 | Winter | 1/4 | Waxing Gibbous | Culminating | 50-62.5% | Fall | Monster |  |
| 9 | 00100000 | 32 | Winter | 1/4 | Full Moon | Illuminating | 62.5-75% | Winter | Sage |  |
| 10 | 00100100 | 36 | Winter | 1/4 | Full Moon | Revealing | 75-87.5% | Winter | Sage |  |
| 11 | 00101000 | 40 | Winter | 1/4 | Waning Gibbous | Sharing | 87.5-75% | Winter | Sage |  |
| 12 | 00101100 | 44 | Winter | 1/4 | Waning Gibbous | Integrating | 75-62.5% | Fall | Monster |  |
| 13 | 00110100 | 52 | Winter | 1/4 | Last Quarter | Releasing | 62.5-50% | Fall | Monster |  |
| 14 | 00111000 | 56 | Winter | 1/4 | Last Quarter | Resolving | 50-37.5% | Fall | Monster |  |
| 15 | 00111100 | 60 | Winter | 1/4 | Balsamic Moon | Distilling | 37.5-12.5% | Fall | Monster |  |
| 16 | 01000000 | 64 | Winter | 1/4 | Balsamic Moon | Surrendering | 12.5-0% | Winter | Sage |  |
| 17 | 10000000 | 128 | Winter | 2/4 | Dark Moon | Deepening | 0% | Winter | Sage | Solitary Flame |
| 18 | 01000100 | 68 | Winter | 2/4 | Dark Moon | Emerging | 0-1% | Winter | Sage |  |
| 19 | 01001000 | 72 | Winter | 2/4 | New Moon | Birthing | 1-6% | Winter | Sage |  |
| 20 | 01001100 | 76 | Winter | 2/4 | New Moon | Strengthening | 6-12.5% | Fall | Monster |  |
| 21 | 01010000 | 80 | Winter | 2/4 | First Quarter | Challenging | 12.5-25% | Winter | Sage |  |
| 22 | 01010100 | 84 | Winter | 2/4 | First Quarter | Balancing | 25-37.5% | Fall | Monster |  |
| 23 | 01011000 | 88 | Winter | 2/4 | Waxing Gibbous | Building | 37.5-50% | Fall | Monster |  |
| 24 | 01011100 | 92 | Winter | 2/4 | Waxing Gibbous | Culminating | 50-62.5% | Fall | Monster |  |
| 25 | 01100000 | 96 | Winter | 2/4 | Full Moon | Illuminating | 62.5-75% | Spring | Fool |  |
| 26 | 01100100 | 100 | Winter | 2/4 | Full Moon | Revealing | 75-87.5% | Spring | Fool |  |
| 27 | 01101000 | 104 | Winter | 2/4 | Waning Gibbous | Sharing | 87.5-75% | Spring | Fool |  |
| 28 | 01101100 | 108 | Winter | 2/4 | Waning Gibbous | Integrating | 75-62.5% | Summer | Hero |  |
| 29 | 01110000 | 112 | Winter | 2/4 | Last Quarter | Releasing | 62.5-50% | Spring | Fool |  |
| 30 | 01110100 | 116 | Winter | 2/4 | Last Quarter | Resolving | 50-37.5% | Summer | Hero |  |
| 31 | 01111000 | 120 | Winter | 2/4 | Balsamic Moon | Distilling | 37.5-12.5% | Summer | Hero |  |
| 32 | 01111100 | 124 | Winter | 2/4 | Balsamic Moon | Surrendering | 12.5-0% | Summer | Hero |  |
| 33 | 10000100 | 132 | Winter | 3/4 | Dark Moon | Deepening | 0% | Winter | Sage |  |
| 34 | 10001000 | 136 | Winter | 3/4 | Dark Moon | Emerging | 0-1% | Winter | Sage |  |
| 35 | 10001100 | 140 | Winter | 3/4 | New Moon | Birthing | 1-6% | Fall | Monster |  |
| 36 | 10010000 | 144 | Winter | 3/4 | New Moon | Strengthening | 6-12.5% | Winter | Sage |  |
| 37 | 10010100 | 148 | Winter | 3/4 | First Quarter | Challenging | 12.5-25% | Fall | Monster |  |
| 38 | 10011000 | 152 | Winter | 3/4 | First Quarter | Balancing | 25-37.5% | Fall | Monster |  |
| 39 | 10011100 | 156 | Winter | 3/4 | Waxing Gibbous | Building | 37.5-50% | Fall | Monster |  |
| 40 | 10100000 | 160 | Winter | 3/4 | Waxing Gibbous | Culminating | 50-62.5% | Spring | Fool |  |
| 41 | 10100100 | 164 | Winter | 3/4 | Full Moon | Illuminating | 62.5-75% | Spring | Fool |  |
| 42 | 10101000 | 168 | Winter | 3/4 | Full Moon | Revealing | 75-87.5% | Spring | Fool |  |
| 43 | 10101100 | 172 | Winter | 3/4 | Waning Gibbous | Sharing | 87.5-75% | Summer | Hero |  |
| 44 | 10110000 | 176 | Winter | 3/4 | Waning Gibbous | Integrating | 75-62.5% | Spring | Fool |  |
| 45 | 10110100 | 180 | Winter | 3/4 | Last Quarter | Releasing | 62.5-50% | Summer | Hero |  |
| 46 | 10111000 | 184 | Winter | 3/4 | Last Quarter | Resolving | 50-37.5% | Summer | Hero |  |
| 47 | 10111100 | 188 | Winter | 3/4 | Balsamic Moon | Distilling | 37.5-12.5% | Summer | Hero |  |
| 48 | 11000000 | 192 | Winter | 3/4 | Balsamic Moon | Surrendering | 12.5-0% | Spring | Fool |  |
| 49 | 00110000 | 48 | Winter | 4/4 | Dark Moon | Deepening | 0% | Winter | Sage | Torch Bearer |
| 50 | 11000100 | 196 | Winter | 4/4 | Dark Moon | Emerging | 0-1% | Spring | Fool |  |
| 51 | 11001000 | 200 | Winter | 4/4 | New Moon | Birthing | 1-6% | Spring | Fool |  |
| 52 | 11001100 | 204 | Winter | 4/4 | New Moon | Strengthening | 6-12.5% | Summer | Hero |  |
| 53 | 11010000 | 208 | Winter | 4/4 | First Quarter | Challenging | 12.5-25% | Spring | Fool |  |
| 54 | 11010100 | 212 | Winter | 4/4 | First Quarter | Balancing | 25-37.5% | Summer | Hero |  |
| 55 | 11011000 | 216 | Winter | 4/4 | Waxing Gibbous | Building | 37.5-50% | Summer | Hero |  |
| 56 | 11011100 | 220 | Winter | 4/4 | Waxing Gibbous | Culminating | 50-62.5% | Summer | Hero |  |
| 57 | 11100000 | 224 | Winter | 4/4 | Full Moon | Illuminating | 62.5-75% | Spring | Fool |  |
| 58 | 11100100 | 228 | Winter | 4/4 | Full Moon | Revealing | 75-87.5% | Spring | Fool |  |
| 59 | 11101000 | 232 | Winter | 4/4 | Waning Gibbous | Sharing | 87.5-75% | Spring | Fool |  |
| 60 | 11101100 | 236 | Winter | 4/4 | Waning Gibbous | Integrating | 75-62.5% | Summer | Hero |  |
| 61 | 11110000 | 240 | Winter | 4/4 | Last Quarter | Releasing | 62.5-50% | Spring | Fool |  |
| 62 | 11110100 | 244 | Winter | 4/4 | Last Quarter | Resolving | 50-37.5% | Summer | Hero |  |
| 63 | 11111000 | 248 | Winter | 4/4 | Balsamic Moon | Distilling | 37.5-12.5% | Summer | Hero |  |
| 64 | 11111100 | 252 | Winter | 4/4 | Balsamic Moon | Surrendering | 12.5-0% | Summer | Hero |  |
| 65 | 00000110 | 6 | Spring | 1/4 | Dark Moon | Deepening | 0% | Winter | Sage |  |
| 66 | 00001010 | 10 | Spring | 1/4 | Dark Moon | Emerging | 0-1% | Winter | Sage |  |
| 67 | 10000010 | 130 | Spring | 1/4 | New Moon | Birthing | 1-6% | Spring | Fool | Playful Hunch |
| 68 | 00001110 | 14 | Spring | 1/4 | New Moon | Strengthening | 6-12.5% | Fall | Monster |  |
| 69 | 00010010 | 18 | Spring | 1/4 | First Quarter | Challenging | 12.5-25% | Winter | Sage |  |
| 70 | 00010110 | 22 | Spring | 1/4 | First Quarter | Balancing | 25-37.5% | Fall | Monster |  |
| 71 | 00011010 | 26 | Spring | 1/4 | Waxing Gibbous | Building | 37.5-50% | Fall | Monster |  |
| 72 | 00011110 | 30 | Spring | 1/4 | Waxing Gibbous | Culminating | 50-62.5% | Fall | Monster |  |
| 73 | 00100010 | 34 | Spring | 1/4 | Full Moon | Illuminating | 62.5-75% | Winter | Sage |  |
| 74 | 00100110 | 38 | Spring | 1/4 | Full Moon | Revealing | 75-87.5% | Winter | Sage |  |
| 75 | 00101010 | 42 | Spring | 1/4 | Waning Gibbous | Sharing | 87.5-75% | Winter | Sage |  |
| 76 | 00101110 | 46 | Spring | 1/4 | Waning Gibbous | Integrating | 75-62.5% | Fall | Monster |  |
| 77 | 00110010 | 50 | Spring | 1/4 | Last Quarter | Releasing | 62.5-50% | Winter | Sage |  |
| 78 | 00110110 | 54 | Spring | 1/4 | Last Quarter | Resolving | 50-37.5% | Fall | Monster |  |
| 79 | 00111010 | 58 | Spring | 1/4 | Balsamic Moon | Distilling | 37.5-12.5% | Fall | Monster |  |
| 80 | 00111110 | 62 | Spring | 1/4 | Balsamic Moon | Surrendering | 12.5-0% | Fall | Monster |  |
| 81 | 01000010 | 66 | Spring | 2/4 | Dark Moon | Deepening | 0% | Winter | Sage |  |
| 82 | 01000110 | 70 | Spring | 2/4 | Dark Moon | Emerging | 0-1% | Winter | Sage |  |
| 83 | 00000010 | 2 | Spring | 2/4 | New Moon | Birthing | 1-6% | Spring | Fool | The Empty Canvas |
| 84 | 01001010 | 74 | Spring | 2/4 | New Moon | Strengthening | 6-12.5% | Winter | Sage |  |
| 85 | 01001110 | 78 | Spring | 2/4 | First Quarter | Challenging | 12.5-25% | Fall | Monster |  |
| 86 | 01010010 | 82 | Spring | 2/4 | First Quarter | Balancing | 25-37.5% | Winter | Sage |  |
| 87 | 01010110 | 86 | Spring | 2/4 | Waxing Gibbous | Building | 37.5-50% | Fall | Monster |  |
| 88 | 01011010 | 90 | Spring | 2/4 | Waxing Gibbous | Culminating | 50-62.5% | Fall | Monster |  |
| 89 | 01011110 | 94 | Spring | 2/4 | Full Moon | Illuminating | 62.5-75% | Fall | Monster |  |
| 90 | 01100010 | 98 | Spring | 2/4 | Full Moon | Revealing | 75-87.5% | Spring | Fool |  |
| 91 | 01100110 | 102 | Spring | 2/4 | Waning Gibbous | Sharing | 87.5-75% | Spring | Fool |  |
| 92 | 01101010 | 106 | Spring | 2/4 | Waning Gibbous | Integrating | 75-62.5% | Spring | Fool |  |
| 93 | 01101110 | 110 | Spring | 2/4 | Last Quarter | Releasing | 62.5-50% | Summer | Hero |  |
| 94 | 01110010 | 114 | Spring | 2/4 | Last Quarter | Resolving | 50-37.5% | Spring | Fool |  |
| 95 | 01110110 | 118 | Spring | 2/4 | Balsamic Moon | Distilling | 37.5-12.5% | Summer | Hero |  |
| 96 | 01111010 | 122 | Spring | 2/4 | Balsamic Moon | Surrendering | 12.5-0% | Summer | Hero |  |
| 97 | 01111110 | 126 | Spring | 3/4 | Dark Moon | Deepening | 0% | Summer | Hero |  |
| 98 | 10000110 | 134 | Spring | 3/4 | Dark Moon | Emerging | 0-1% | Winter | Sage |  |
| 99 | 10001010 | 138 | Spring | 3/4 | New Moon | Birthing | 1-6% | Winter | Sage |  |
| 100 | 10001110 | 142 | Spring | 3/4 | New Moon | Strengthening | 6-12.5% | Fall | Monster |  |
| 101 | 10010010 | 146 | Spring | 3/4 | First Quarter | Challenging | 12.5-25% | Winter | Sage |  |
| 102 | 10010110 | 150 | Spring | 3/4 | First Quarter | Balancing | 25-37.5% | Fall | Monster |  |
| 103 | 10011010 | 154 | Spring | 3/4 | Waxing Gibbous | Building | 37.5-50% | Fall | Monster |  |
| 104 | 10011110 | 158 | Spring | 3/4 | Waxing Gibbous | Culminating | 50-62.5% | Fall | Monster |  |
| 105 | 10100010 | 162 | Spring | 3/4 | Full Moon | Illuminating | 62.5-75% | Spring | Fool |  |
| 106 | 10100110 | 166 | Spring | 3/4 | Full Moon | Revealing | 75-87.5% | Spring | Fool |  |
| 107 | 10101010 | 170 | Spring | 3/4 | Waning Gibbous | Sharing | 87.5-75% | Spring | Fool |  |
| 108 | 10101110 | 174 | Spring | 3/4 | Waning Gibbous | Integrating | 75-62.5% | Summer | Hero |  |
| 109 | 10110010 | 178 | Spring | 3/4 | Last Quarter | Releasing | 62.5-50% | Spring | Fool |  |
| 110 | 10110110 | 182 | Spring | 3/4 | Last Quarter | Resolving | 50-37.5% | Summer | Hero |  |
| 111 | 10111010 | 186 | Spring | 3/4 | Balsamic Moon | Distilling | 37.5-12.5% | Summer | Hero |  |
| 112 | 10111110 | 190 | Spring | 3/4 | Balsamic Moon | Surrendering | 12.5-0% | Summer | Hero |  |
| 113 | 11000010 | 194 | Spring | 4/4 | Dark Moon | Deepening | 0% | Spring | Fool |  |
| 114 | 11000110 | 198 | Spring | 4/4 | Dark Moon | Emerging | 0-1% | Spring | Fool |  |
| 115 | 11001010 | 202 | Spring | 4/4 | New Moon | Birthing | 1-6% | Spring | Fool |  |
| 116 | 11001110 | 206 | Spring | 4/4 | New Moon | Strengthening | 6-12.5% | Summer | Hero |  |
| 117 | 11010010 | 210 | Spring | 4/4 | First Quarter | Challenging | 12.5-25% | Spring | Fool |  |
| 118 | 11010110 | 214 | Spring | 4/4 | First Quarter | Balancing | 25-37.5% | Summer | Hero |  |
| 119 | 11011010 | 218 | Spring | 4/4 | Waxing Gibbous | Building | 37.5-50% | Summer | Hero |  |
| 120 | 11011110 | 222 | Spring | 4/4 | Waxing Gibbous | Culminating | 50-62.5% | Summer | Hero |  |
| 121 | 11100010 | 226 | Spring | 4/4 | Full Moon | Illuminating | 62.5-75% | Spring | Fool |  |
| 122 | 11100110 | 230 | Spring | 4/4 | Full Moon | Revealing | 75-87.5% | Spring | Fool |  |
| 123 | 11101010 | 234 | Spring | 4/4 | Waning Gibbous | Sharing | 87.5-75% | Spring | Fool |  |
| 124 | 11101110 | 238 | Spring | 4/4 | Waning Gibbous | Integrating | 75-62.5% | Summer | Hero |  |
| 125 | 11110010 | 242 | Spring | 4/4 | Last Quarter | Releasing | 62.5-50% | Spring | Fool |  |
| 126 | 11110110 | 246 | Spring | 4/4 | Last Quarter | Resolving | 50-37.5% | Summer | Hero |  |
| 127 | 11111010 | 250 | Spring | 4/4 | Balsamic Moon | Distilling | 37.5-12.5% | Summer | Hero |  |
| 128 | 11111110 | 254 | Spring | 4/4 | Balsamic Moon | Surrendering | 12.5-0% | Summer | Hero |  |
| 129 | 00000111 | 7 | Summer | 1/4 | Dark Moon | Deepening | 0% | Winter | Sage |  |
| 130 | 00001011 | 11 | Summer | 1/4 | Dark Moon | Emerging | 0-1% | Winter | Sage |  |
| 131 | 00001111 | 15 | Summer | 1/4 | New Moon | Birthing | 1-6% | Fall | Monster |  |
| 132 | 00000011 | 3 | Summer | 1/4 | New Moon | Strengthening | 6-12.5% | Winter | Sage | Perfect Vessel |
| 133 | 00010011 | 19 | Summer | 1/4 | First Quarter | Challenging | 12.5-25% | Winter | Sage |  |
| 134 | 00010111 | 23 | Summer | 1/4 | First Quarter | Balancing | 25-37.5% | Fall | Monster |  |
| 135 | 00011011 | 27 | Summer | 1/4 | Waxing Gibbous | Building | 37.5-50% | Fall | Monster |  |
| 136 | 00011111 | 31 | Summer | 1/4 | Waxing Gibbous | Culminating | 50-62.5% | Fall | Monster |  |
| 137 | 00100011 | 35 | Summer | 1/4 | Full Moon | Illuminating | 62.5-75% | Winter | Sage |  |
| 138 | 00100111 | 39 | Summer | 1/4 | Full Moon | Revealing | 75-87.5% | Winter | Sage |  |
| 139 | 00101011 | 43 | Summer | 1/4 | Waning Gibbous | Sharing | 87.5-75% | Winter | Sage |  |
| 140 | 00101111 | 47 | Summer | 1/4 | Waning Gibbous | Integrating | 75-62.5% | Fall | Monster |  |
| 141 | 00110011 | 51 | Summer | 1/4 | Last Quarter | Releasing | 62.5-50% | Winter | Sage |  |
| 142 | 00110111 | 55 | Summer | 1/4 | Last Quarter | Resolving | 50-37.5% | Fall | Monster |  |
| 143 | 00111011 | 59 | Summer | 1/4 | Balsamic Moon | Distilling | 37.5-12.5% | Fall | Monster |  |
| 144 | 00111111 | 63 | Summer | 1/4 | Balsamic Moon | Surrendering | 12.5-0% | Fall | Monster |  |
| 145 | 01000011 | 67 | Summer | 2/4 | Dark Moon | Deepening | 0% | Winter | Sage |  |
| 146 | 01000111 | 71 | Summer | 2/4 | Dark Moon | Emerging | 0-1% | Winter | Sage |  |
| 147 | 01001011 | 75 | Summer | 2/4 | New Moon | Birthing | 1-6% | Winter | Sage |  |
| 148 | 11000011 | 195 | Summer | 2/4 | New Moon | Strengthening | 6-12.5% | Spring | Fool | Intuitive Mastery |
| 149 | 01001111 | 79 | Summer | 2/4 | First Quarter | Challenging | 12.5-25% | Fall | Monster |  |
| 150 | 01010011 | 83 | Summer | 2/4 | First Quarter | Balancing | 25-37.5% | Winter | Sage |  |
| 151 | 01010111 | 87 | Summer | 2/4 | Waxing Gibbous | Building | 37.5-50% | Fall | Monster |  |
| 152 | 01011011 | 91 | Summer | 2/4 | Waxing Gibbous | Culminating | 50-62.5% | Fall | Monster |  |
| 153 | 01011111 | 95 | Summer | 2/4 | Full Moon | Illuminating | 62.5-75% | Fall | Monster |  |
| 154 | 01100011 | 99 | Summer | 2/4 | Full Moon | Revealing | 75-87.5% | Spring | Fool |  |
| 155 | 01100111 | 103 | Summer | 2/4 | Waning Gibbous | Sharing | 87.5-75% | Spring | Fool |  |
| 156 | 01101011 | 107 | Summer | 2/4 | Waning Gibbous | Integrating | 75-62.5% | Spring | Fool |  |
| 157 | 01101111 | 111 | Summer | 2/4 | Last Quarter | Releasing | 62.5-50% | Summer | Hero |  |
| 158 | 01110011 | 115 | Summer | 2/4 | Last Quarter | Resolving | 50-37.5% | Spring | Fool |  |
| 159 | 01110111 | 119 | Summer | 2/4 | Balsamic Moon | Distilling | 37.5-12.5% | Summer | Hero |  |
| 160 | 01111011 | 123 | Summer | 2/4 | Balsamic Moon | Surrendering | 12.5-0% | Summer | Hero |  |
| 161 | 01111111 | 127 | Summer | 3/4 | Dark Moon | Deepening | 0% | Summer | Hero |  |
| 162 | 10000011 | 131 | Summer | 3/4 | Dark Moon | Emerging | 0-1% | Summer | Hero |  |
| 163 | 10000111 | 135 | Summer | 3/4 | New Moon | Birthing | 1-6% | Winter | Sage |  |
| 164 | 10001011 | 139 | Summer | 3/4 | New Moon | Strengthening | 6-12.5% | Winter | Sage |  |
| 165 | 10001111 | 143 | Summer | 3/4 | First Quarter | Challenging | 12.5-25% | Fall | Monster |  |
| 166 | 10010011 | 147 | Summer | 3/4 | First Quarter | Balancing | 25-37.5% | Winter | Sage |  |
| 167 | 10010111 | 151 | Summer | 3/4 | Waxing Gibbous | Building | 37.5-50% | Fall | Monster |  |
| 168 | 10011011 | 155 | Summer | 3/4 | Waxing Gibbous | Culminating | 50-62.5% | Fall | Monster |  |
| 169 | 10011111 | 159 | Summer | 3/4 | Full Moon | Illuminating | 62.5-75% | Fall | Monster |  |
| 170 | 10100011 | 163 | Summer | 3/4 | Full Moon | Revealing | 75-87.5% | Spring | Fool |  |
| 171 | 10100111 | 167 | Summer | 3/4 | Waning Gibbous | Sharing | 87.5-75% | Spring | Fool |  |
| 172 | 10101011 | 171 | Summer | 3/4 | Waning Gibbous | Integrating | 75-62.5% | Spring | Fool |  |
| 173 | 10101111 | 175 | Summer | 3/4 | Last Quarter | Releasing | 62.5-50% | Summer | Hero |  |
| 174 | 10110011 | 179 | Summer | 3/4 | Last Quarter | Resolving | 50-37.5% | Spring | Fool |  |
| 175 | 10110111 | 183 | Summer | 3/4 | Balsamic Moon | Distilling | 37.5-12.5% | Summer | Hero |  |
| 176 | 10111011 | 187 | Summer | 3/4 | Balsamic Moon | Surrendering | 12.5-0% | Summer | Hero |  |
| 177 | 10111111 | 191 | Summer | 4/4 | Dark Moon | Deepening | 0% | Summer | Hero |  |
| 178 | 11000111 | 199 | Summer | 4/4 | Dark Moon | Emerging | 0-1% | Spring | Fool |  |
| 179 | 11001011 | 203 | Summer | 4/4 | New Moon | Birthing | 1-6% | Spring | Fool |  |
| 180 | 11001111 | 207 | Summer | 4/4 | New Moon | Strengthening | 6-12.5% | Summer | Hero |  |
| 181 | 11010011 | 211 | Summer | 4/4 | First Quarter | Challenging | 12.5-25% | Spring | Fool |  |
| 182 | 11010111 | 215 | Summer | 4/4 | First Quarter | Balancing | 25-37.5% | Summer | Hero |  |
| 183 | 11011011 | 219 | Summer | 4/4 | Waxing Gibbous | Building | 37.5-50% | Summer | Hero |  |
| 184 | 11011111 | 223 | Summer | 4/4 | Waxing Gibbous | Culminating | 50-62.5% | Summer | Hero |  |
| 185 | 11100011 | 227 | Summer | 4/4 | Full Moon | Illuminating | 62.5-75% | Spring | Fool |  |
| 186 | 11100111 | 231 | Summer | 4/4 | Full Moon | Revealing | 75-87.5% | Spring | Fool |  |
| 187 | 11101011 | 235 | Summer | 4/4 | Waning Gibbous | Sharing | 87.5-75% | Spring | Fool |  |
| 188 | 11101111 | 239 | Summer | 4/4 | Waning Gibbous | Integrating | 75-62.5% | Summer | Hero |  |
| 189 | 11110011 | 243 | Summer | 4/4 | Last Quarter | Releasing | 62.5-50% | Spring | Fool |  |
| 190 | 11110111 | 247 | Summer | 4/4 | Last Quarter | Resolving | 50-37.5% | Summer | Hero |  |
| 191 | 11111011 | 251 | Summer | 4/4 | Balsamic Moon | Distilling | 37.5-12.5% | Summer | Hero |  |
| 192 | 11111111 | 255 | Summer | 4/4 | Balsamic Moon | Surrendering | 12.5-0% | Summer | Hero | Enlightened Clarity |
| 193 | 00000101 | 5 | Fall | 1/4 | Dark Moon | Deepening | 0% | Winter | Sage |  |
| 194 | 00000001 | 1 | Fall | 1/4 | Dark Moon | Emerging | 0-1% | Winter | Sage | Unwritten Beginnings |
| 195 | 00001001 | 9 | Fall | 1/4 | New Moon | Birthing | 1-6% | Winter | Sage |  |
| 196 | 00001101 | 13 | Fall | 1/4 | New Moon | Strengthening | 6-12.5% | Fall | Monster |  |
| 197 | 00010001 | 17 | Fall | 1/4 | First Quarter | Challenging | 12.5-25% | Winter | Sage |  |
| 198 | 00010101 | 21 | Fall | 1/4 | First Quarter | Balancing | 25-37.5% | Fall | Monster |  |
| 199 | 00011001 | 25 | Fall | 1/4 | Waxing Gibbous | Building | 37.5-50% | Fall | Monster |  |
| 200 | 00011101 | 29 | Fall | 1/4 | Waxing Gibbous | Culminating | 50-62.5% | Fall | Monster |  |
| 201 | 00100001 | 33 | Fall | 1/4 | Full Moon | Illuminating | 62.5-75% | Winter | Sage |  |
| 202 | 00100101 | 37 | Fall | 1/4 | Full Moon | Revealing | 75-87.5% | Winter | Sage |  |
| 203 | 00101001 | 41 | Fall | 1/4 | Waning Gibbous | Sharing | 87.5-75% | Winter | Sage |  |
| 204 | 00101101 | 45 | Fall | 1/4 | Waning Gibbous | Integrating | 75-62.5% | Fall | Monster |  |
| 205 | 00110001 | 49 | Fall | 1/4 | Last Quarter | Releasing | 62.5-50% | Winter | Sage |  |
| 206 | 00110101 | 53 | Fall | 1/4 | Last Quarter | Resolving | 50-37.5% | Fall | Monster |  |
| 207 | 00111001 | 57 | Fall | 1/4 | Balsamic Moon | Distilling | 37.5-12.5% | Fall | Monster |  |
| 208 | 00111101 | 61 | Fall | 1/4 | Balsamic Moon | Surrendering | 12.5-0% | Fall | Monster |  |
| 209 | 01000101 | 69 | Fall | 2/4 | Dark Moon | Deepening | 0% | Winter | Sage |  |
| 210 | 01000001 | 65 | Fall | 2/4 | Dark Moon | Emerging | 0-1% | Fall | Monster | Obsessive Vision |
| 211 | 01001001 | 73 | Fall | 2/4 | New Moon | Birthing | 1-6% | Winter | Sage |  |
| 212 | 01001101 | 77 | Fall | 2/4 | New Moon | Strengthening | 6-12.5% | Fall | Monster |  |
| 213 | 01010001 | 81 | Fall | 2/4 | First Quarter | Challenging | 12.5-25% | Winter | Sage |  |
| 214 | 01010101 | 85 | Fall | 2/4 | First Quarter | Balancing | 25-37.5% | Fall | Monster |  |
| 215 | 01011001 | 89 | Fall | 2/4 | Waxing Gibbous | Building | 37.5-50% | Fall | Monster |  |
| 216 | 01011101 | 93 | Fall | 2/4 | Waxing Gibbous | Culminating | 50-62.5% | Fall | Monster |  |
| 217 | 01100001 | 97 | Fall | 2/4 | Full Moon | Illuminating | 62.5-75% | Spring | Fool |  |
| 218 | 01100101 | 101 | Fall | 2/4 | Full Moon | Revealing | 75-87.5% | Spring | Fool |  |
| 219 | 01101001 | 105 | Fall | 2/4 | Waning Gibbous | Sharing | 87.5-75% | Spring | Fool |  |
| 220 | 01101101 | 109 | Fall | 2/4 | Waning Gibbous | Integrating | 75-62.5% | Summer | Hero |  |
| 221 | 01110001 | 113 | Fall | 2/4 | Last Quarter | Releasing | 62.5-50% | Spring | Fool |  |
| 222 | 01110101 | 117 | Fall | 2/4 | Last Quarter | Resolving | 50-37.5% | Summer | Hero |  |
| 223 | 01111001 | 121 | Fall | 2/4 | Balsamic Moon | Distilling | 37.5-12.5% | Summer | Hero |  |
| 224 | 01111101 | 125 | Fall | 2/4 | Balsamic Moon | Surrendering | 12.5-0% | Summer | Hero |  |
| 225 | 10000001 | 129 | Fall | 3/4 | Dark Moon | Deepening | 0% | Winter | Sage |  |
| 226 | 10000101 | 133 | Fall | 3/4 | Dark Moon | Emerging | 0-1% | Winter | Sage |  |
| 227 | 10001001 | 137 | Fall | 3/4 | New Moon | Birthing | 1-6% | Winter | Sage |  |
| 228 | 10001101 | 141 | Fall | 3/4 | New Moon | Strengthening | 6-12.5% | Fall | Monster |  |
| 229 | 10010001 | 145 | Fall | 3/4 | First Quarter | Challenging | 12.5-25% | Winter | Sage |  |
| 230 | 10010101 | 149 | Fall | 3/4 | First Quarter | Balancing | 25-37.5% | Fall | Monster |  |
| 231 | 10011001 | 153 | Fall | 3/4 | Waxing Gibbous | Building | 37.5-50% | Fall | Monster |  |
| 232 | 10011101 | 157 | Fall | 3/4 | Waxing Gibbous | Culminating | 50-62.5% | Fall | Monster |  |
| 233 | 10100001 | 161 | Fall | 3/4 | Full Moon | Illuminating | 62.5-75% | Spring | Fool |  |
| 234 | 10100101 | 165 | Fall | 3/4 | Full Moon | Revealing | 75-87.5% | Spring | Fool |  |
| 235 | 10101001 | 169 | Fall | 3/4 | Waning Gibbous | Sharing | 87.5-75% | Spring | Fool |  |
| 236 | 10101101 | 173 | Fall | 3/4 | Waning Gibbous | Integrating | 75-62.5% | Summer | Hero |  |
| 237 | 10110001 | 177 | Fall | 3/4 | Last Quarter | Releasing | 62.5-50% | Spring | Fool |  |
| 238 | 10110101 | 181 | Fall | 3/4 | Last Quarter | Resolving | 50-37.5% | Summer | Hero |  |
| 239 | 10111001 | 185 | Fall | 3/4 | Balsamic Moon | Distilling | 37.5-12.5% | Summer | Hero |  |
| 240 | 10111101 | 189 | Fall | 3/4 | Balsamic Moon | Surrendering | 12.5-0% | Summer | Hero |  |
| 241 | 11000001 | 193 | Fall | 4/4 | Dark Moon | Deepening | 0% | Spring | Fool |  |
| 242 | 11000101 | 197 | Fall | 4/4 | Dark Moon | Emerging | 0-1% | Spring | Fool |  |
| 243 | 11001001 | 201 | Fall | 4/4 | New Moon | Birthing | 1-6% | Spring | Fool |  |
| 244 | 11001101 | 205 | Fall | 4/4 | New Moon | Strengthening | 6-12.5% | Summer | Hero |  |
| 245 | 11010001 | 209 | Fall | 4/4 | First Quarter | Challenging | 12.5-25% | Spring | Fool |  |
| 246 | 11010101 | 213 | Fall | 4/4 | First Quarter | Balancing | 25-37.5% | Summer | Hero |  |
| 247 | 11011001 | 217 | Fall | 4/4 | Waxing Gibbous | Building | 37.5-50% | Summer | Hero |  |
| 248 | 11011101 | 221 | Fall | 4/4 | Waxing Gibbous | Culminating | 50-62.5% | Summer | Hero |  |
| 249 | 11100001 | 225 | Fall | 4/4 | Full Moon | Illuminating | 62.5-75% | Spring | Fool |  |
| 250 | 11100101 | 229 | Fall | 4/4 | Full Moon | Revealing | 75-87.5% | Spring | Fool |  |
| 251 | 11101001 | 233 | Fall | 4/4 | Waning Gibbous | Sharing | 87.5-75% | Spring | Fool |  |
| 252 | 11101101 | 237 | Fall | 4/4 | Waning Gibbous | Integrating | 75-62.5% | Summer | Hero |  |
| 253 | 11110001 | 241 | Fall | 4/4 | Last Quarter | Releasing | 62.5-50% | Spring | Fool |  |
| 254 | 11110101 | 245 | Fall | 4/4 | Last Quarter | Resolving | 50-37.5% | Summer | Hero |  |
| 255 | 11111001 | 249 | Fall | 4/4 | Balsamic Moon | Distilling | 37.5-12.5% | Summer | Hero |  |
| 256 | 11111101 | 253 | Fall | 4/4 | Balsamic Moon | Surrendering | 12.5-0% | Summer | Hero |  |
