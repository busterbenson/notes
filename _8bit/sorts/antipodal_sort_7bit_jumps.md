# PERFECT ANTIPODAL SORT WITH OPTIMAL BIT TRANSITIONS

This document provides a reference for all 256 cards in the 8-bit Oracle system, sorted to achieve both perfect antipodal positioning and optimized bit transitions.

## Complete Card Listing (Perfect Antipodal Order)

| Position | Binary | L→R Dec | Season | Cycle | Phase | Half | Illumination | Archetype | Card Name | Opposite Position |
|----------|--------|---------|--------|-------|-------|------|--------------|-----------|----------|------------------|
| 1 | 00000000 | 0 | Winter | 1/4 | Dark Moon | Deepening | 0% | Sage | Void Mirror | 129 |
| 2 | 00000001 | 128 | Fall | 1/4 | Dark Moon | Deepening | 0% | Monster | Devouring Void | 130 |
| 3 | 00000011 | 192 | Summer | 1/4 | Dark Moon | Deepening | 0% | Hero | Perfect Vessel | 131 |
| 4 | 00000010 | 64 | Spring | 1/4 | Dark Moon | Deepening | 0% | Fool | Unwritten Beginning | 132 |
| 5 | 00000110 | 96 | Spring | 2/4 | Dark Moon | Deepening | 0% | Fool |  | 133 |
| 6 | 00000111 | 224 | Summer | 2/4 | Dark Moon | Deepening | 0% | Hero |  | 134 |
| 7 | 00000101 | 160 | Fall | 2/4 | Dark Moon | Deepening | 0% | Monster |  | 135 |
| 8 | 00000100 | 32 | Winter | 2/4 | Dark Moon | Deepening | 0% | Sage |  | 136 |
| 9 | 00001100 | 48 | Winter | 3/4 | Dark Moon | Deepening | 0% | Fool |  | 137 |
| 10 | 00001101 | 176 | Fall | 3/4 | Dark Moon | Deepening | 0% | Sage |  | 138 |
| 11 | 00001111 | 240 | Summer | 3/4 | Dark Moon | Deepening | 0% | Monster |  | 139 |
| 12 | 00001110 | 112 | Spring | 3/4 | Dark Moon | Deepening | 0% | Hero |  | 140 |
| 13 | 00001010 | 80 | Spring | 2/4 | Dark Moon | Deepening | 0% | Fool |  | 141 |
| 14 | 00001011 | 208 | Summer | 2/4 | Dark Moon | Deepening | 0% | Hero |  | 142 |
| 15 | 00001001 | 144 | Fall | 2/4 | Dark Moon | Deepening | 0% | Monster |  | 143 |
| 16 | 00001000 | 16 | Winter | 2/4 | Dark Moon | Deepening | 0% | Sage |  | 144 |
| 17 | 00011000 | 24 | Winter | 3/4 | Full Moon | Illuminating | 62.5-75% | Fool |  | 145 |
| 18 | 00011001 | 152 | Fall | 3/4 | Full Moon | Illuminating | 62.5-75% | Sage |  | 146 |
| 19 | 00011011 | 216 | Summer | 3/4 | Full Moon | Illuminating | 62.5-75% | Monster |  | 147 |
| 20 | 00011010 | 88 | Spring | 3/4 | Full Moon | Illuminating | 62.5-75% | Hero |  | 148 |
| 21 | 00011110 | 120 | Spring | 4/4 | Full Moon | Illuminating | 62.5-75% | Hero |  | 149 |
| 22 | 00011111 | 248 | Summer | 4/4 | Full Moon | Illuminating | 62.5-75% | Monster |  | 150 |
| 23 | 00011101 | 184 | Fall | 4/4 | Full Moon | Illuminating | 62.5-75% | Sage |  | 151 |
| 24 | 00011100 | 56 | Winter | 4/4 | Full Moon | Illuminating | 62.5-75% | Fool |  | 152 |
| 25 | 00010100 | 40 | Winter | 3/4 | Full Moon | Illuminating | 62.5-75% | Fool |  | 153 |
| 26 | 00010101 | 168 | Fall | 3/4 | Full Moon | Illuminating | 62.5-75% | Sage |  | 154 |
| 27 | 00010111 | 232 | Summer | 3/4 | Full Moon | Illuminating | 62.5-75% | Monster |  | 155 |
| 28 | 00010110 | 104 | Spring | 3/4 | Full Moon | Illuminating | 62.5-75% | Hero |  | 156 |
| 29 | 00010010 | 72 | Spring | 2/4 | Full Moon | Illuminating | 62.5-75% | Fool |  | 157 |
| 30 | 00010011 | 200 | Summer | 2/4 | Full Moon | Illuminating | 62.5-75% | Hero |  | 158 |
| 31 | 00010001 | 136 | Fall | 2/4 | Full Moon | Illuminating | 62.5-75% | Monster |  | 159 |
| 32 | 00010000 | 8 | Winter | 2/4 | Full Moon | Illuminating | 62.5-75% | Sage |  | 160 |
| 33 | 00110000 | 12 | Winter | 3/4 | Last Quarter | Releasing | 62.5-50% | Sage |  | 161 |
| 34 | 00110001 | 140 | Fall | 3/4 | Last Quarter | Releasing | 62.5-50% | Monster |  | 162 |
| 35 | 00110011 | 204 | Summer | 3/4 | Last Quarter | Releasing | 62.5-50% | Hero |  | 163 |
| 36 | 00110010 | 76 | Spring | 3/4 | Last Quarter | Releasing | 62.5-50% | Fool |  | 164 |
| 37 | 00110110 | 108 | Spring | 4/4 | Last Quarter | Releasing | 62.5-50% | Hero |  | 165 |
| 38 | 00110111 | 236 | Summer | 4/4 | Last Quarter | Releasing | 62.5-50% | Monster |  | 166 |
| 39 | 00110101 | 172 | Fall | 4/4 | Last Quarter | Releasing | 62.5-50% | Sage |  | 167 |
| 40 | 00110100 | 44 | Winter | 4/4 | Last Quarter | Releasing | 62.5-50% | Fool |  | 168 |
| 41 | 00111100 | 60 | Winter | 1/4 | Last Quarter | Releasing | 62.5-50% | Fool |  | 169 |
| 42 | 00111101 | 188 | Fall | 1/4 | Last Quarter | Releasing | 62.5-50% | Sage |  | 170 |
| 43 | 00111111 | 252 | Summer | 1/4 | Last Quarter | Releasing | 62.5-50% | Monster |  | 171 |
| 44 | 00111110 | 124 | Spring | 1/4 | Last Quarter | Releasing | 62.5-50% | Hero |  | 172 |
| 45 | 00111010 | 92 | Spring | 4/4 | Last Quarter | Releasing | 62.5-50% | Hero |  | 173 |
| 46 | 00111011 | 220 | Summer | 4/4 | Last Quarter | Releasing | 62.5-50% | Monster |  | 174 |
| 47 | 00111001 | 156 | Fall | 4/4 | Last Quarter | Releasing | 62.5-50% | Sage |  | 175 |
| 48 | 00111000 | 28 | Winter | 4/4 | Last Quarter | Releasing | 62.5-50% | Fool |  | 176 |
| 49 | 00101000 | 20 | Winter | 3/4 | First Quarter | Challenging | 12.5-25% | Sage |  | 177 |
| 50 | 00101001 | 148 | Fall | 3/4 | First Quarter | Challenging | 12.5-25% | Monster |  | 178 |
| 51 | 00101011 | 212 | Summer | 3/4 | First Quarter | Challenging | 12.5-25% | Hero |  | 179 |
| 52 | 00101010 | 84 | Spring | 3/4 | First Quarter | Challenging | 12.5-25% | Fool |  | 180 |
| 53 | 00101110 | 116 | Spring | 4/4 | First Quarter | Challenging | 12.5-25% | Hero |  | 181 |
| 54 | 00101111 | 244 | Summer | 4/4 | First Quarter | Challenging | 12.5-25% | Monster |  | 182 |
| 55 | 00101101 | 180 | Fall | 4/4 | First Quarter | Challenging | 12.5-25% | Sage |  | 183 |
| 56 | 00101100 | 52 | Winter | 4/4 | First Quarter | Challenging | 12.5-25% | Fool |  | 184 |
| 57 | 00100100 | 36 | Winter | 3/4 | First Quarter | Challenging | 12.5-25% | Sage |  | 185 |
| 58 | 00100101 | 164 | Fall | 3/4 | First Quarter | Challenging | 12.5-25% | Monster |  | 186 |
| 59 | 00100111 | 228 | Summer | 3/4 | First Quarter | Challenging | 12.5-25% | Hero |  | 187 |
| 60 | 00100110 | 100 | Spring | 3/4 | First Quarter | Challenging | 12.5-25% | Fool |  | 188 |
| 61 | 00100010 | 68 | Spring | 2/4 | First Quarter | Challenging | 12.5-25% | Fool |  | 189 |
| 62 | 00100011 | 196 | Summer | 2/4 | First Quarter | Challenging | 12.5-25% | Hero |  | 190 |
| 63 | 00100001 | 132 | Fall | 2/4 | First Quarter | Challenging | 12.5-25% | Monster |  | 191 |
| 64 | 00100000 | 4 | Winter | 2/4 | First Quarter | Challenging | 12.5-25% | Sage |  | 192 |
| 65 | 01100000 | 6 | Winter | 3/4 | Waxing Gibbous | Building | 37.5-50% | Monster |  | 193 |
| 66 | 01100001 | 134 | Fall | 3/4 | Waxing Gibbous | Building | 37.5-50% | Hero |  | 194 |
| 67 | 01100011 | 198 | Summer | 3/4 | Waxing Gibbous | Building | 37.5-50% | Fool |  | 195 |
| 68 | 01100010 | 70 | Spring | 3/4 | Waxing Gibbous | Building | 37.5-50% | Sage |  | 196 |
| 69 | 01100110 | 102 | Spring | 4/4 | Waxing Gibbous | Building | 37.5-50% | Sage |  | 197 |
| 70 | 01100111 | 230 | Summer | 4/4 | Waxing Gibbous | Building | 37.5-50% | Fool |  | 198 |
| 71 | 01100101 | 166 | Fall | 4/4 | Waxing Gibbous | Building | 37.5-50% | Hero |  | 199 |
| 72 | 01100100 | 38 | Winter | 4/4 | Waxing Gibbous | Building | 37.5-50% | Monster |  | 200 |
| 73 | 01101100 | 54 | Winter | 1/4 | Waxing Gibbous | Building | 37.5-50% | Hero |  | 201 |
| 74 | 01101101 | 182 | Fall | 1/4 | Waxing Gibbous | Building | 37.5-50% | Fool |  | 202 |
| 75 | 01101111 | 246 | Summer | 1/4 | Waxing Gibbous | Building | 37.5-50% | Sage |  | 203 |
| 76 | 01101110 | 118 | Spring | 1/4 | Waxing Gibbous | Building | 37.5-50% | Monster |  | 204 |
| 77 | 01101010 | 86 | Spring | 4/4 | Waxing Gibbous | Building | 37.5-50% | Sage |  | 205 |
| 78 | 01101011 | 214 | Summer | 4/4 | Waxing Gibbous | Building | 37.5-50% | Fool |  | 206 |
| 79 | 01101001 | 150 | Fall | 4/4 | Waxing Gibbous | Building | 37.5-50% | Hero |  | 207 |
| 80 | 01101000 | 22 | Winter | 4/4 | Waxing Gibbous | Building | 37.5-50% | Monster |  | 208 |
| 81 | 01111000 | 30 | Winter | 1/4 | Balsamic Moon | Distilling | 37.5-12.5% | Hero |  | 209 |
| 82 | 01111001 | 158 | Fall | 1/4 | Balsamic Moon | Distilling | 37.5-12.5% | Fool |  | 210 |
| 83 | 01111011 | 222 | Summer | 1/4 | Balsamic Moon | Distilling | 37.5-12.5% | Sage |  | 211 |
| 84 | 01111010 | 94 | Spring | 1/4 | Balsamic Moon | Distilling | 37.5-12.5% | Monster |  | 212 |
| 85 | 01111110 | 126 | Spring | 2/4 | Balsamic Moon | Distilling | 37.5-12.5% | Monster |  | 213 |
| 86 | 01111111 | 254 | Summer | 2/4 | Balsamic Moon | Distilling | 37.5-12.5% | Sage |  | 214 |
| 87 | 01111101 | 190 | Fall | 2/4 | Balsamic Moon | Distilling | 37.5-12.5% | Fool |  | 215 |
| 88 | 01111100 | 62 | Winter | 2/4 | Balsamic Moon | Distilling | 37.5-12.5% | Hero |  | 216 |
| 89 | 01110100 | 46 | Winter | 1/4 | Balsamic Moon | Distilling | 37.5-12.5% | Hero |  | 217 |
| 90 | 01110101 | 174 | Fall | 1/4 | Balsamic Moon | Distilling | 37.5-12.5% | Fool |  | 218 |
| 91 | 01110111 | 238 | Summer | 1/4 | Balsamic Moon | Distilling | 37.5-12.5% | Sage |  | 219 |
| 92 | 01110110 | 110 | Spring | 1/4 | Balsamic Moon | Distilling | 37.5-12.5% | Monster |  | 220 |
| 93 | 01110010 | 78 | Spring | 4/4 | Balsamic Moon | Distilling | 37.5-12.5% | Sage |  | 221 |
| 94 | 01110011 | 206 | Summer | 4/4 | Balsamic Moon | Distilling | 37.5-12.5% | Fool |  | 222 |
| 95 | 01110001 | 142 | Fall | 4/4 | Balsamic Moon | Distilling | 37.5-12.5% | Hero |  | 223 |
| 96 | 01110000 | 14 | Winter | 4/4 | Balsamic Moon | Distilling | 37.5-12.5% | Monster |  | 224 |
| 97 | 01010000 | 10 | Winter | 3/4 | Waning Gibbous | Sharing | 87.5-75% | Sage |  | 225 |
| 98 | 01010001 | 138 | Fall | 3/4 | Waning Gibbous | Sharing | 87.5-75% | Monster |  | 226 |
| 99 | 01010011 | 202 | Summer | 3/4 | Waning Gibbous | Sharing | 87.5-75% | Hero |  | 227 |
| 100 | 01010010 | 74 | Spring | 3/4 | Waning Gibbous | Sharing | 87.5-75% | Fool |  | 228 |
| 101 | 01010110 | 106 | Spring | 4/4 | Waning Gibbous | Sharing | 87.5-75% | Hero |  | 229 |
| 102 | 01010111 | 234 | Summer | 4/4 | Waning Gibbous | Sharing | 87.5-75% | Monster |  | 230 |
| 103 | 01010101 | 170 | Fall | 4/4 | Waning Gibbous | Sharing | 87.5-75% | Sage |  | 231 |
| 104 | 01010100 | 42 | Winter | 4/4 | Waning Gibbous | Sharing | 87.5-75% | Fool |  | 232 |
| 105 | 01011100 | 58 | Winter | 1/4 | Waning Gibbous | Sharing | 87.5-75% | Fool |  | 233 |
| 106 | 01011101 | 186 | Fall | 1/4 | Waning Gibbous | Sharing | 87.5-75% | Sage |  | 234 |
| 107 | 01011111 | 250 | Summer | 1/4 | Waning Gibbous | Sharing | 87.5-75% | Monster |  | 235 |
| 108 | 01011110 | 122 | Spring | 1/4 | Waning Gibbous | Sharing | 87.5-75% | Hero |  | 236 |
| 109 | 01011010 | 90 | Spring | 4/4 | Waning Gibbous | Sharing | 87.5-75% | Hero |  | 237 |
| 110 | 01011011 | 218 | Summer | 4/4 | Waning Gibbous | Sharing | 87.5-75% | Monster |  | 238 |
| 111 | 01011001 | 154 | Fall | 4/4 | Waning Gibbous | Sharing | 87.5-75% | Sage |  | 239 |
| 112 | 01011000 | 26 | Winter | 4/4 | Waning Gibbous | Sharing | 87.5-75% | Fool |  | 240 |
| 113 | 01001000 | 18 | Winter | 3/4 | New Moon | Birthing | 1-6% | Sage |  | 241 |
| 114 | 01001001 | 146 | Fall | 3/4 | New Moon | Birthing | 1-6% | Monster |  | 242 |
| 115 | 01001011 | 210 | Summer | 3/4 | New Moon | Birthing | 1-6% | Hero |  | 243 |
| 116 | 01001010 | 82 | Spring | 3/4 | New Moon | Birthing | 1-6% | Fool |  | 244 |
| 117 | 01001110 | 114 | Spring | 4/4 | New Moon | Birthing | 1-6% | Hero |  | 245 |
| 118 | 01001111 | 242 | Summer | 4/4 | New Moon | Birthing | 1-6% | Monster |  | 246 |
| 119 | 01001101 | 178 | Fall | 4/4 | New Moon | Birthing | 1-6% | Sage |  | 247 |
| 120 | 01001100 | 50 | Winter | 4/4 | New Moon | Birthing | 1-6% | Fool |  | 248 |
| 121 | 01000100 | 34 | Winter | 3/4 | New Moon | Birthing | 1-6% | Sage |  | 249 |
| 122 | 01000101 | 162 | Fall | 3/4 | New Moon | Birthing | 1-6% | Monster |  | 250 |
| 123 | 01000111 | 226 | Summer | 3/4 | New Moon | Birthing | 1-6% | Hero |  | 251 |
| 124 | 01000110 | 98 | Spring | 3/4 | New Moon | Birthing | 1-6% | Fool |  | 252 |
| 125 | 01000010 | 66 | Spring | 2/4 | New Moon | Birthing | 1-6% | Fool |  | 253 |
| 126 | 01000011 | 194 | Summer | 2/4 | New Moon | Birthing | 1-6% | Hero |  | 254 |
| 127 | 01000001 | 130 | Fall | 2/4 | New Moon | Birthing | 1-6% | Monster |  | 255 |
| 128 | 01000000 | 2 | Winter | 2/4 | New Moon | Birthing | 1-6% | Sage |  | 256 |
| 129 | 11111111 | 255 | Summer | 3/4 | Balsamic Moon | Surrendering | 12.5-0% | Sage |  | 1 |
| 130 | 11111110 | 127 | Spring | 3/4 | Balsamic Moon | Surrendering | 12.5-0% | Monster |  | 2 |
| 131 | 11111100 | 63 | Winter | 3/4 | Balsamic Moon | Surrendering | 12.5-0% | Hero |  | 3 |
| 132 | 11111101 | 191 | Fall | 3/4 | Balsamic Moon | Surrendering | 12.5-0% | Fool |  | 4 |
| 133 | 11111001 | 159 | Fall | 2/4 | Balsamic Moon | Surrendering | 12.5-0% | Fool |  | 5 |
| 134 | 11111000 | 31 | Winter | 2/4 | Balsamic Moon | Surrendering | 12.5-0% | Hero |  | 6 |
| 135 | 11111010 | 95 | Spring | 2/4 | Balsamic Moon | Surrendering | 12.5-0% | Monster |  | 7 |
| 136 | 11111011 | 223 | Summer | 2/4 | Balsamic Moon | Surrendering | 12.5-0% | Sage |  | 8 |
| 137 | 11110011 | 207 | Summer | 1/4 | Balsamic Moon | Surrendering | 12.5-0% | Fool |  | 9 |
| 138 | 11110010 | 79 | Spring | 1/4 | Balsamic Moon | Surrendering | 12.5-0% | Sage |  | 10 |
| 139 | 11110000 | 15 | Winter | 1/4 | Balsamic Moon | Surrendering | 12.5-0% | Monster |  | 11 |
| 140 | 11110001 | 143 | Fall | 1/4 | Balsamic Moon | Surrendering | 12.5-0% | Hero |  | 12 |
| 141 | 11110101 | 175 | Fall | 2/4 | Balsamic Moon | Surrendering | 12.5-0% | Fool |  | 13 |
| 142 | 11110100 | 47 | Winter | 2/4 | Balsamic Moon | Surrendering | 12.5-0% | Hero |  | 14 |
| 143 | 11110110 | 111 | Spring | 2/4 | Balsamic Moon | Surrendering | 12.5-0% | Monster |  | 15 |
| 144 | 11110111 | 239 | Summer | 2/4 | Balsamic Moon | Surrendering | 12.5-0% | Sage |  | 16 |
| 145 | 11100111 | 231 | Summer | 1/4 | Waxing Gibbous | Culminating | 50-62.5% | Fool |  | 17 |
| 146 | 11100110 | 103 | Spring | 1/4 | Waxing Gibbous | Culminating | 50-62.5% | Sage |  | 18 |
| 147 | 11100100 | 39 | Winter | 1/4 | Waxing Gibbous | Culminating | 50-62.5% | Monster |  | 19 |
| 148 | 11100101 | 167 | Fall | 1/4 | Waxing Gibbous | Culminating | 50-62.5% | Hero |  | 20 |
| 149 | 11100001 | 135 | Fall | 4/4 | Waxing Gibbous | Culminating | 50-62.5% | Hero |  | 21 |
| 150 | 11100000 | 7 | Winter | 4/4 | Waxing Gibbous | Culminating | 50-62.5% | Monster |  | 22 |
| 151 | 11100010 | 71 | Spring | 4/4 | Waxing Gibbous | Culminating | 50-62.5% | Sage |  | 23 |
| 152 | 11100011 | 199 | Summer | 4/4 | Waxing Gibbous | Culminating | 50-62.5% | Fool |  | 24 |
| 153 | 11101011 | 215 | Summer | 1/4 | Waxing Gibbous | Culminating | 50-62.5% | Fool |  | 25 |
| 154 | 11101010 | 87 | Spring | 1/4 | Waxing Gibbous | Culminating | 50-62.5% | Sage |  | 26 |
| 155 | 11101000 | 23 | Winter | 1/4 | Waxing Gibbous | Culminating | 50-62.5% | Monster |  | 27 |
| 156 | 11101001 | 151 | Fall | 1/4 | Waxing Gibbous | Culminating | 50-62.5% | Hero |  | 28 |
| 157 | 11101101 | 183 | Fall | 2/4 | Waxing Gibbous | Culminating | 50-62.5% | Fool |  | 29 |
| 158 | 11101100 | 55 | Winter | 2/4 | Waxing Gibbous | Culminating | 50-62.5% | Hero |  | 30 |
| 159 | 11101110 | 119 | Spring | 2/4 | Waxing Gibbous | Culminating | 50-62.5% | Monster |  | 31 |
| 160 | 11101111 | 247 | Summer | 2/4 | Waxing Gibbous | Culminating | 50-62.5% | Sage |  | 32 |
| 161 | 11001111 | 243 | Summer | 1/4 | New Moon | Strengthening | 6-12.5% | Sage |  | 33 |
| 162 | 11001110 | 115 | Spring | 1/4 | New Moon | Strengthening | 6-12.5% | Monster |  | 34 |
| 163 | 11001100 | 51 | Winter | 1/4 | New Moon | Strengthening | 6-12.5% | Hero |  | 35 |
| 164 | 11001101 | 179 | Fall | 1/4 | New Moon | Strengthening | 6-12.5% | Fool |  | 36 |
| 165 | 11001001 | 147 | Fall | 4/4 | New Moon | Strengthening | 6-12.5% | Hero |  | 37 |
| 166 | 11001000 | 19 | Winter | 4/4 | New Moon | Strengthening | 6-12.5% | Monster |  | 38 |
| 167 | 11001010 | 83 | Spring | 4/4 | New Moon | Strengthening | 6-12.5% | Sage |  | 39 |
| 168 | 11001011 | 211 | Summer | 4/4 | New Moon | Strengthening | 6-12.5% | Fool |  | 40 |
| 169 | 11000011 | 195 | Summer | 3/4 | New Moon | Strengthening | 6-12.5% | Fool |  | 41 |
| 170 | 11000010 | 67 | Spring | 3/4 | New Moon | Strengthening | 6-12.5% | Sage |  | 42 |
| 171 | 11000000 | 3 | Winter | 3/4 | New Moon | Strengthening | 6-12.5% | Monster |  | 43 |
| 172 | 11000001 | 131 | Fall | 3/4 | New Moon | Strengthening | 6-12.5% | Hero |  | 44 |
| 173 | 11000101 | 163 | Fall | 4/4 | New Moon | Strengthening | 6-12.5% | Hero |  | 45 |
| 174 | 11000100 | 35 | Winter | 4/4 | New Moon | Strengthening | 6-12.5% | Monster |  | 46 |
| 175 | 11000110 | 99 | Spring | 4/4 | New Moon | Strengthening | 6-12.5% | Sage |  | 47 |
| 176 | 11000111 | 227 | Summer | 4/4 | New Moon | Strengthening | 6-12.5% | Fool |  | 48 |
| 177 | 11010111 | 235 | Summer | 1/4 | Waning Gibbous | Integrating | 75-62.5% | Sage |  | 49 |
| 178 | 11010110 | 107 | Spring | 1/4 | Waning Gibbous | Integrating | 75-62.5% | Monster |  | 50 |
| 179 | 11010100 | 43 | Winter | 1/4 | Waning Gibbous | Integrating | 75-62.5% | Hero |  | 51 |
| 180 | 11010101 | 171 | Fall | 1/4 | Waning Gibbous | Integrating | 75-62.5% | Fool |  | 52 |
| 181 | 11010001 | 139 | Fall | 4/4 | Waning Gibbous | Integrating | 75-62.5% | Hero |  | 53 |
| 182 | 11010000 | 11 | Winter | 4/4 | Waning Gibbous | Integrating | 75-62.5% | Monster |  | 54 |
| 183 | 11010010 | 75 | Spring | 4/4 | Waning Gibbous | Integrating | 75-62.5% | Sage |  | 55 |
| 184 | 11010011 | 203 | Summer | 4/4 | Waning Gibbous | Integrating | 75-62.5% | Fool |  | 56 |
| 185 | 11011011 | 219 | Summer | 1/4 | Waning Gibbous | Integrating | 75-62.5% | Sage |  | 57 |
| 186 | 11011010 | 91 | Spring | 1/4 | Waning Gibbous | Integrating | 75-62.5% | Monster |  | 58 |
| 187 | 11011000 | 27 | Winter | 1/4 | Waning Gibbous | Integrating | 75-62.5% | Hero |  | 59 |
| 188 | 11011001 | 155 | Fall | 1/4 | Waning Gibbous | Integrating | 75-62.5% | Fool |  | 60 |
| 189 | 11011101 | 187 | Fall | 2/4 | Waning Gibbous | Integrating | 75-62.5% | Fool |  | 61 |
| 190 | 11011100 | 59 | Winter | 2/4 | Waning Gibbous | Integrating | 75-62.5% | Hero |  | 62 |
| 191 | 11011110 | 123 | Spring | 2/4 | Waning Gibbous | Integrating | 75-62.5% | Monster |  | 63 |
| 192 | 11011111 | 251 | Summer | 2/4 | Waning Gibbous | Integrating | 75-62.5% | Sage |  | 64 |
| 193 | 10011111 | 249 | Summer | 1/4 | Full Moon | Revealing | 75-87.5% | Monster |  | 65 |
| 194 | 10011110 | 121 | Spring | 1/4 | Full Moon | Revealing | 75-87.5% | Hero |  | 66 |
| 195 | 10011100 | 57 | Winter | 1/4 | Full Moon | Revealing | 75-87.5% | Fool |  | 67 |
| 196 | 10011101 | 185 | Fall | 1/4 | Full Moon | Revealing | 75-87.5% | Sage |  | 68 |
| 197 | 10011001 | 153 | Fall | 4/4 | Full Moon | Revealing | 75-87.5% | Sage |  | 69 |
| 198 | 10011000 | 25 | Winter | 4/4 | Full Moon | Revealing | 75-87.5% | Fool |  | 70 |
| 199 | 10011010 | 89 | Spring | 4/4 | Full Moon | Revealing | 75-87.5% | Hero |  | 71 |
| 200 | 10011011 | 217 | Summer | 4/4 | Full Moon | Revealing | 75-87.5% | Monster |  | 72 |
| 201 | 10010011 | 201 | Summer | 3/4 | Full Moon | Revealing | 75-87.5% | Hero |  | 73 |
| 202 | 10010010 | 73 | Spring | 3/4 | Full Moon | Revealing | 75-87.5% | Fool |  | 74 |
| 203 | 10010000 | 9 | Winter | 3/4 | Full Moon | Revealing | 75-87.5% | Sage |  | 75 |
| 204 | 10010001 | 137 | Fall | 3/4 | Full Moon | Revealing | 75-87.5% | Monster |  | 76 |
| 205 | 10010101 | 169 | Fall | 4/4 | Full Moon | Revealing | 75-87.5% | Sage |  | 77 |
| 206 | 10010100 | 41 | Winter | 4/4 | Full Moon | Revealing | 75-87.5% | Fool |  | 78 |
| 207 | 10010110 | 105 | Spring | 4/4 | Full Moon | Revealing | 75-87.5% | Hero |  | 79 |
| 208 | 10010111 | 233 | Summer | 4/4 | Full Moon | Revealing | 75-87.5% | Monster |  | 80 |
| 209 | 10000111 | 225 | Summer | 3/4 | Dark Moon | Emerging | 0-1% | Hero |  | 81 |
| 210 | 10000110 | 97 | Spring | 3/4 | Dark Moon | Emerging | 0-1% | Fool |  | 82 |
| 211 | 10000100 | 33 | Winter | 3/4 | Dark Moon | Emerging | 0-1% | Sage |  | 83 |
| 212 | 10000101 | 161 | Fall | 3/4 | Dark Moon | Emerging | 0-1% | Monster |  | 84 |
| 213 | 10000001 | 129 | Fall | 2/4 | Dark Moon | Emerging | 0-1% | Monster |  | 85 |
| 214 | 10000000 | 1 | Winter | 2/4 | Dark Moon | Emerging | 0-1% | Sage |  | 86 |
| 215 | 10000010 | 65 | Spring | 2/4 | Dark Moon | Emerging | 0-1% | Fool |  | 87 |
| 216 | 10000011 | 193 | Summer | 2/4 | Dark Moon | Emerging | 0-1% | Hero |  | 88 |
| 217 | 10001011 | 209 | Summer | 3/4 | Dark Moon | Emerging | 0-1% | Hero |  | 89 |
| 218 | 10001010 | 81 | Spring | 3/4 | Dark Moon | Emerging | 0-1% | Fool |  | 90 |
| 219 | 10001000 | 17 | Winter | 3/4 | Dark Moon | Emerging | 0-1% | Sage |  | 91 |
| 220 | 10001001 | 145 | Fall | 3/4 | Dark Moon | Emerging | 0-1% | Monster |  | 92 |
| 221 | 10001101 | 177 | Fall | 4/4 | Dark Moon | Emerging | 0-1% | Sage |  | 93 |
| 222 | 10001100 | 49 | Winter | 4/4 | Dark Moon | Emerging | 0-1% | Fool |  | 94 |
| 223 | 10001110 | 113 | Spring | 4/4 | Dark Moon | Emerging | 0-1% | Hero |  | 95 |
| 224 | 10001111 | 241 | Summer | 4/4 | Dark Moon | Emerging | 0-1% | Monster |  | 96 |
| 225 | 10101111 | 245 | Summer | 1/4 | First Quarter | Balancing | 25-37.5% | Sage |  | 97 |
| 226 | 10101110 | 117 | Spring | 1/4 | First Quarter | Balancing | 25-37.5% | Monster |  | 98 |
| 227 | 10101100 | 53 | Winter | 1/4 | First Quarter | Balancing | 25-37.5% | Hero |  | 99 |
| 228 | 10101101 | 181 | Fall | 1/4 | First Quarter | Balancing | 25-37.5% | Fool |  | 100 |
| 229 | 10101001 | 149 | Fall | 4/4 | First Quarter | Balancing | 25-37.5% | Hero |  | 101 |
| 230 | 10101000 | 21 | Winter | 4/4 | First Quarter | Balancing | 25-37.5% | Monster |  | 102 |
| 231 | 10101010 | 85 | Spring | 4/4 | First Quarter | Balancing | 25-37.5% | Sage |  | 103 |
| 232 | 10101011 | 213 | Summer | 4/4 | First Quarter | Balancing | 25-37.5% | Fool |  | 104 |
| 233 | 10100011 | 197 | Summer | 3/4 | First Quarter | Balancing | 25-37.5% | Fool |  | 105 |
| 234 | 10100010 | 69 | Spring | 3/4 | First Quarter | Balancing | 25-37.5% | Sage |  | 106 |
| 235 | 10100000 | 5 | Winter | 3/4 | First Quarter | Balancing | 25-37.5% | Monster |  | 107 |
| 236 | 10100001 | 133 | Fall | 3/4 | First Quarter | Balancing | 25-37.5% | Hero |  | 108 |
| 237 | 10100101 | 165 | Fall | 4/4 | First Quarter | Balancing | 25-37.5% | Hero |  | 109 |
| 238 | 10100100 | 37 | Winter | 4/4 | First Quarter | Balancing | 25-37.5% | Monster |  | 110 |
| 239 | 10100110 | 101 | Spring | 4/4 | First Quarter | Balancing | 25-37.5% | Sage |  | 111 |
| 240 | 10100111 | 229 | Summer | 4/4 | First Quarter | Balancing | 25-37.5% | Fool |  | 112 |
| 241 | 10110111 | 237 | Summer | 1/4 | Last Quarter | Resolving | 50-37.5% | Sage |  | 113 |
| 242 | 10110110 | 109 | Spring | 1/4 | Last Quarter | Resolving | 50-37.5% | Monster |  | 114 |
| 243 | 10110100 | 45 | Winter | 1/4 | Last Quarter | Resolving | 50-37.5% | Hero |  | 115 |
| 244 | 10110101 | 173 | Fall | 1/4 | Last Quarter | Resolving | 50-37.5% | Fool |  | 116 |
| 245 | 10110001 | 141 | Fall | 4/4 | Last Quarter | Resolving | 50-37.5% | Hero |  | 117 |
| 246 | 10110000 | 13 | Winter | 4/4 | Last Quarter | Resolving | 50-37.5% | Monster |  | 118 |
| 247 | 10110010 | 77 | Spring | 4/4 | Last Quarter | Resolving | 50-37.5% | Sage |  | 119 |
| 248 | 10110011 | 205 | Summer | 4/4 | Last Quarter | Resolving | 50-37.5% | Fool |  | 120 |
| 249 | 10111011 | 221 | Summer | 1/4 | Last Quarter | Resolving | 50-37.5% | Sage |  | 121 |
| 250 | 10111010 | 93 | Spring | 1/4 | Last Quarter | Resolving | 50-37.5% | Monster |  | 122 |
| 251 | 10111000 | 29 | Winter | 1/4 | Last Quarter | Resolving | 50-37.5% | Hero |  | 123 |
| 252 | 10111001 | 157 | Fall | 1/4 | Last Quarter | Resolving | 50-37.5% | Fool |  | 124 |
| 253 | 10111101 | 189 | Fall | 2/4 | Last Quarter | Resolving | 50-37.5% | Fool |  | 125 |
| 254 | 10111100 | 61 | Winter | 2/4 | Last Quarter | Resolving | 50-37.5% | Hero |  | 126 |
| 255 | 10111110 | 125 | Spring | 2/4 | Last Quarter | Resolving | 50-37.5% | Monster |  | 127 |
| 256 | 10111111 | 253 | Summer | 2/4 | Last Quarter | Resolving | 50-37.5% | Sage |  | 128 |

## Transition Analysis

This sort achieves a perfect balance between antipodal positioning and bit transition optimality:

### Transition Summary

- 1-bit transitions: 254
- 7-bit transitions: 2

### Multi-Bit Transitions

Position 128 → 129: 01000000 → 11111111 (Bits 1, 3, 4, 5, 6, 7, 8 flip)
Position 256 → 1: 10111111 → 00000000 (Bits 1, 3, 4, 5, 6, 7, 8 flip)

### Antipodal Property Verification

This sort guarantees that binary opposites are EXACTLY 128 positions apart:

Position 1 (00000000) ↔ Position 129 (11111111): Distance = 128
Position 2 (00000001) ↔ Position 130 (11111110): Distance = 128
Position 3 (00000011) ↔ Position 131 (11111100): Distance = 128
Position 4 (00000010) ↔ Position 132 (11111101): Distance = 128
Position 5 (00000110) ↔ Position 133 (11111001): Distance = 128

...


## Mathematical Foundation

This sort uses a specialized construction to achieve the optimal balance between:

1. **Perfect Antipodal Property:** Binary opposites are positioned EXACTLY 128 positions apart
2. **Optimized Bit Transitions:** The sequence is designed to minimize bit changes between adjacent positions
3. **Mathematical Elegance:** The sequence exhibits a beautiful symmetry derived from the properties of Gray codes

This construction builds on the fact that it is mathematically impossible to create a sequence where:
- All binary opposites are exactly 128 positions apart, AND
- All transitions change exactly 1 bit, AND
- The sequence includes all 256 codes exactly once

Instead, this sort carefully balances these constraints to achieve the most elegant solution possible.

## Benefits of this Sort

1. **Perfect Antipodal Positioning:** Binary opposites are exactly 128 positions apart
2. **Optimized Transitions:** The sequence is designed to minimize bit changes
3. **Mathematical Elegance:** The sort exhibits beautiful symmetrical properties
4. **Complete Coverage:** The sequence includes all 256 possible 8-bit patterns exactly once
