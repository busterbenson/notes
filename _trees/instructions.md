# Instructions for Generating Tree Species Files

## Overview
You will generate individual tree species profile files using the standardized structure and feature IDs defined in `features.yml`. Each tree profile will categorize features as "always true," "sometimes true," or "never true" for that species, creating a comprehensive profile that supports the generation of a kid-friendly decision tree.

## How These Files Will Be Used
The generated files will form the foundation of a tree-identification decision tree that will help children without specialized botanical knowledge to identify California trees using visual cues. The system is designed to work year-round and for trees of all ages. These instructions focus solely on generating the tree profile files, not the decision tree itself.

## Features.yml Structure and IDs

The `features.yml` file contains a comprehensive taxonomy of tree identification features organized into categories, each with a standardized ID format (e.g., LEAF-TYPE-01, BARK-TEXT-03):

1. **Leaf features** - Type, complexity, arrangement, shape, edge, color, fall color
2. **Needle features** - Arrangement, shape, characteristics, markings
3. **Reproductive features** - Flowers, fruits, cones
4. **Bark features** - Texture, color, patterns
5. **Growth form** - Tree shape, trunk form, size classifications
6. **Branch features** - Angles, patterns, twig characteristics
7. **Winter features** - Buds, seasonal visibility, persistent features
8. **Habitat features** - Location preferences, water relationships
9. **Sensory features** - Smell, texture, secretions
10. **Geographic features** - California regions, elevation ranges
11. **Ecological features** - Wildlife relationships, adaptations, human uses, origin

Each feature in features.yml has:
- **Standardized ID** (e.g., "LEAF-TYPE-02" for evergreen)
- General description
- Reliability rating
- Seasonal visibility
- Age dependency
- Observation distance
- Safety information
- Kid-friendly notes

## Tree File Format - The Alaska Cedar Example

For each tree, create a YAML file in the `trees/` directory with the format `trees/[family-name].[common-tree-name].yml` (with all words in lower-case and kebab-case). For example: `cupressaceae.alaska-cedar.yml`. This naming convention groups trees by family and makes it easier to find related species. Follow this structure, illustrated with the Alaska Cedar example:

```yaml
tree:
  common_name: "Alaska-cedar"
  scientific_name: "Callitropsis nootkatensis"
  family: "Cupressaceae"
  
  # Basic summary (2-3 sentences of most distinctive features)
  summary: "A tall, narrow conifer with distinctive drooping branch tips and scale-like leaves in flattened sprays. The bark is thin, stringy, and grayish-brown."
  
  # Identification path guides the decision tree
  identification_path:
    primary_markers: "Drooping branch tips that give a weeping appearance; strong cedar scent when foliage is crushed"
    secondary_markers: "Scale-like blue-green leaves in flat sprays; stringy gray-brown bark on mature trees"
    seasonal_markers: "Minimal seasonal change; small round cones visible on mature trees"
    similar_species_differentiation: "Unlike Port Orford-cedar, has distinctive drooping branch tips; unlike Western Redcedar, has rounder cones and bluer foliage"
  
  # Core features section
  features:
    always_true:
      # Reference features.yml IDs with tree-specific notes
      - feature_id: "LEAF-TYPE-02"  # Evergreen
        notes: "Retains foliage year-round with minimal seasonal changes"
      
      - feature_id: "LEAF-FORM-05"  # Scale-like leaves
        notes: "Tiny overlapping scales forming flat sprays"
      
      - feature_id: "TREE-FORM-03"  # Weeping form
        notes: "Distinctive drooping branch tips create a weeping appearance"
      
    sometimes_true:
      # Include age, seasonal, or condition-dependent features
      - feature_id: "BARK-TEXT-01"  # Smooth bark
        conditions: "Young trees before bark develops texture"
        notes: "Bark is relatively smooth when young"
      
      - feature_id: "BARK-TEXT-03"  # Peeling bark
        conditions: "Mature trees"
        notes: "Stringy, shredding bark in gray to brown color"
      
    never_true:
      # Features explicitly absent that help differentiation
      - feature_id: "LEAF-TYPE-01"  # Deciduous
        notes: "Never drops all leaves seasonally"
      
      - feature_id: "FLOWER-SIZE-01"  # Showy flowers
        notes: "Produces only small, inconspicuous cones, not showy flowers"
  
  # Kid-friendly identification section
  kid_friendly_identification:
    primary_identifier: "Drooping branch tips that look sad or sleepy"
    memorable_comparison: "Looks like a Christmas tree that's tired and droopy"
    touch_tip: "The leaves feel like tiny overlapping fish scales"
    smell_tip: "Crush a small bit of foliage to smell a spicy cedar scent, like a wooden chest"
    fun_fact: "Alaska-cedar's wood is so resistant to rot that fallen trees can stay intact for over 100 years!"
    
    # Detective steps walk children through identification
    detective_steps:
      - step: 1
        instruction: "First, look at the overall shape. Does it have droopy branch tips like it's tired?"
        yes_next: 2
        no_next: "Not an Alaska-cedar - try Western Redcedar or Port Orford-cedar"
      - step: 2
        instruction: "Look closely at the leaves. Are they tiny scales that overlap like fish scales?"
        yes_next: 3
        no_next: "Not an Alaska-cedar - check if it has needles instead"
      - step: 3
        instruction: "Carefully crush a small bit of foliage and smell. Does it have a spicy cedar smell?"
        yes_next: "You found an Alaska-cedar!"
        no_next: "Might be Port Orford-cedar - check for more upright branches"
  
  # Seasonal changes - separate entry for each season
  seasonal_timeline:
    - season: "Spring"
      visual_changes: "New growth appears at branch tips with slightly lighter color"
      reproductive_activity: "Pollen cones release yellow pollen"
      identification_tips: "Look for the contrast between new growth and older foliage"
      kid_friendly_tip: "Look for tiny yellow pollen cones at branch tips"
    
    - season: "Summer" 
      visual_changes: "Consistent blue-green color throughout"
      reproductive_activity: "Seed cones develop and begin maturing"
      identification_tips: "Blue-green color stands out compared to other conifers"
      kid_friendly_tip: "Notice the blue-green color of the foliage against other trees"
    
    - season: "Fall"
      visual_changes: "No color change as it remains evergreen"
      reproductive_activity: "Mature cones release seeds"
      identification_tips: "Distinctive among trees that are changing color"
      kid_friendly_tip: "While other trees change color, Alaska-cedar stays the same dark green"
    
    - season: "Winter"
      visual_changes: "Foliage remains but growth is dormant"
      reproductive_activity: "Dormant, no reproductive activity"
      identification_tips: "Easier to identify when deciduous trees are bare"
      kid_friendly_tip: "Still has its green scale-like leaves when other trees are bare"
      
  # Additional required sections 
  confirmation_checklist:
    - feature: "Scale-like leaves in flattened sprays"
      reliability: "High"
      visibility: "Medium - need to look closely"
    - feature: "Strong, spicy cedar scent when foliage is crushed"
      reliability: "Very high"
      visibility: "Requires interaction"
    
  look_alike_species:
    - species: "Port Orford-cedar (Chamaecyparis lawsoniana)"
      differences: "Port Orford-cedar has more upright branches and foliage that is more bluish; cones are slightly larger"
      identification_tip: "If the branches point up instead of drooping down, it's likely Port Orford-cedar"
    
  cultural_ecological_notes:
    - "Wood is highly valued by Indigenous peoples of the Pacific Northwest for its durability and carving qualities"
    - "Used traditionally for canoe paddles, tool handles, and ceremonial items"
    
  range_within_california:
    - "Not native to California but cultivated in northern parts of the state"
    - "Prefers cool, moist environments with adequate rainfall"
    
  # Decision tree mapping section - algorithmic support
  decision_tree_placement:
    primary_split_features:
      - "feature_id: LEAF-TYPE-02"  # Evergreen
      - "feature_id: LEAF-FORM-05"  # Scale-like leaves
      - "feature_id: TREE-FORM-03"  # Weeping form
    confirmation_features:
      - "feature_id: SENSORY-SMELL-01"  # Aromatic leaves
      - "feature_id: BARK-TEXT-03"  # Peeling bark
    observation_sequence:
      - distance: "from_far_away"
        features_to_check: ["TREE-FORM-03", "LEAF-TYPE-02"]  # Weeping form, evergreen
      - distance: "from_nearby"
        features_to_check: ["LEAF-FORM-05", "LEAF-COLOR-03"]  # Scale-like leaves, blue-green
      - distance: "close_inspection"
        features_to_check: ["SENSORY-SMELL-01", "LEAF-ARRANGE-02"]  # Cedar scent, leaf arrangement
    seasonal_identification:
      spring:
        reliability: "High"
        key_features: ["LEAF-TYPE-02", "LEAF-FORM-05", "TREE-FORM-03"]
        notes: "New growth and pollen cones provide additional confirmation"
      summer:
        reliability: "High"
        key_features: ["LEAF-TYPE-02", "LEAF-FORM-05", "LEAF-COLOR-03"]
        notes: "Blue-green color more visible against other conifers"
      fall:
        reliability: "High" 
        key_features: ["LEAF-TYPE-02", "LEAF-FORM-05", "TREE-FORM-03"]
        notes: "Evergreen nature stands out as deciduous trees change color"
      winter:
        reliability: "Very high"
        key_features: ["LEAF-TYPE-02", "TREE-FORM-03", "SENSORY-SMELL-01"]
        notes: "Easier to spot the distinctive form when deciduous trees are bare"
```

## Feature Classification Guidelines

### 1. Tree File Feature Structure
In tree files, include **only** the following for each feature:
- **feature_id**: Standardized ID from features.yml (e.g., "LEAF-TYPE-02")
- **notes**: Tree-specific description of the feature
- **conditions**: For "sometimes_true" features, specify when the feature applies
- **exceptions**: For "usually_true" features, describe situations where exceptions occur

### 2. Classification of Features
There are now four levels of feature certainty in tree files:

#### a. Always True Features
- Features consistently present in normal, healthy specimens with no exceptions
- Focus on structural, year-round features that are definitive
- Include applicable features that have no known exceptions for the species
- Use these for primary identification in decision trees
- IMPORTANT: Avoid putting trunk form features (TREE-TRUNK-01, TREE-TRUNK-02) in this category as they often have exceptions

#### b. Usually True Features
- Features that are primarily true but have documented exceptions
- The exceptions shouldn't immediately rule out the species during identification
- Include the **exceptions** field to explain situations where feature may not be present
- Example: A tree that typically has a single trunk but may occasionally have multiple trunks
- Trunk form features (single vs. multi-trunked) generally belong in this category

#### c. Sometimes True Features
- Features that vary by:
  - Age (young vs. mature trees)
  - Season
  - Growing conditions
  - Regional variation
- Always specify the **conditions** field
- Group related features (e.g., bark textures at different ages)

#### d. Never True Features
- Features explicitly absent that aid in differentiation
- Focus on features that might be expected in similar species
- Include features whose absence is distinctive
- Add notes explaining why the feature never occurs

## Comprehensive Coverage Requirements

Each tree file must cover features from ALL of these categories:

1. **Basic Morphology**:
   - Leaf/needle type (LEAF-TYPE-xx or equivalent)
   - Growth form (TREE-FORM-xx)
   - Bark characteristics (BARK-TEXT-xx, BARK-COLOR-xx)
   - Size classification (TREE-SIZE-xx)

2. **Structural Traits**:
   - Trunk form (TREE-TRUNK-xx)
   - Branch patterns (BRANCH-xx)
   - Leaf/needle arrangement (LEAF-ARRANGE-xx or NEEDLE-ARRANGE-xx)

3. **Reproductive Features** (as applicable):
   - Cone or fruit characteristics
   - Flower features (or note their absence)

4. **Geographic & Ecological**:
   - Origin status (native/introduced)
   - Regional presence
   - Elevation range
   - Habitat preferences
   - Wildlife relationships

5. **Sensory Features**:
   - Smell characteristics
   - Texture traits
   - Any distinctive secretions

## Seasonal Considerations

1. **Distinct Seasons**: Create separate entries for each season (Spring, Summer, Fall, Winter)
2. **No Combined Seasons**: Never combine seasons (e.g., "Fall/Winter")
3. **Year-Round Identification**: Ensure each season has distinctive identification characteristics
4. **Consistent Fields**: Include all required fields for each season

## Additional Requirements

1. **Kid-Friendly Language THROUGHOUT ALL SECTIONS**: 
   - All descriptions in EVERY section must be accessible to children (age 8-10) without specialized knowledge
   - Avoid botanical jargon throughout the entire file - replace technical terms with everyday language
   - Use simple, concrete comparisons (e.g., "as big as your thumb" rather than measurements in inches)
   - Keep sentences short and simple
   - For size comparisons, use familiar objects like "as tall as a 10-story building" or "as wide as a car tire"
   - Explain concepts in relation to familiar experiences
   - Replace technical terms throughout ALL sections, not just kid-friendly sections:
     - Replace "conifer" with "evergreen tree" or "tree that stays green all year"
     - Replace "foliage" with "leaves" or "needles"
     - Replace "mature" with "grown" or "older"
     - Replace "deciduous" with "trees that lose their leaves in fall"
     - Replace "fibrous" with "stringy" or "spongy"
     - Replace "pyramidal" with "triangle-shaped" or "Christmas tree shaped"
     - Replace "columnar" with "tall and straight"
     - Replace "furrowed" with "grooved" or "bumpy"

2. **Clear Differentiation with Kid-Friendly Comparisons**: 
   - Emphasize features that distinguish from similar-looking species using simple language
   - Use visual comparisons that children can understand like "hugging the branch" or "looks like a bottle brush"
   - Focus on obvious differences rather than subtle botanical distinctions
   - Use memorable analogies that relate to children's experiences (e.g., "bark feels like puzzle pieces" or "needles like tiny green fingers")

3. **Observation Distance in Simple Terms**: 
   - Group features by how close you need to be to observe them
   - Use clear, simple language for viewing instructions like "look from far away" or "check up close"
   - Provide kid-friendly guidance like "stand back to see the whole tree shape" or "look closely at the needles"

4. **Kid-Friendly Safety Notes**: 
   - Include clear cautions for any features requiring interaction (smelling, touching)
   - Explicitly state when something should not be tasted or touched in simple terms
   - Explain why in kid-friendly language (e.g., "it's sticky and hard to clean off" rather than "contains resin")
   - Use positive direction when possible (e.g., "only touch the bark gently" rather than a list of what not to do)
   - Make safety messages clear without being scary

5. **Kid-Friendly Cultural Context and Significance**: 
   - Structure the cultural_significance section by culture first, then by physical uses and symbolic meanings:
     ```yaml
     cultural_significance:
       # Organized by culture
       - culture: "[Cultural Group Name]"
         physical_uses:
           - "[Specific physical use in simple, concrete language]"
           - "[Additional uses with how/why explanations a child can understand]"
         symbolic_meaning:
           - "[Specific symbolic meaning connected to observable features in simple terms]"
           - "[Additional symbolic associations explained in child-friendly language]"
     ```
   - Include specific, well-researched information about cultural significance in simple language
   - Name specific cultural groups rather than using generic terms (e.g., "Tlingit and Haida peoples" rather than "Indigenous tribes")
   - For physical uses, be specific and concise with kid-friendly explanations:
     - For medicinal uses: "Used sticky sap to help heal cuts" instead of "Resin was utilized as a topical antiseptic"
     - For craft uses: "Made canoe paddles from this wood because it doesn't rot in water" instead of "Wood utilized for maritime implements due to its decay-resistant properties"
     - For food uses: "Collected the seeds and ground them into flour for bread" instead of "Seeds were processed into meal for culinary applications"
   - For symbolic meanings, focus on concrete connections kids can understand:
     - Connect physical traits to meaning: "Straight, tall growth showed reaching to the sky world"
     - Simplify spiritual concepts: "Tree was seen as connecting earth and sky" instead of "Tree symbolized cosmological axis mundi"
     - Make stories relatable: "Stories taught how the tree showed strength by standing tall in storms"
   - Include sensory details in simple language (e.g., "smells like Christmas with a hint of orange" rather than "aromatic terpene profile")
   - For cultural_significance sections: provide historically accurate, respectful information in language 8-10 year olds can understand
   - When noting symbolic meanings, connect them to observable features kids can see
   - Be concise but specific, using concrete examples rather than abstract concepts

## Required Sections for Each Tree File

Each tree file must include ALL of the following sections in this order:

1. **Basic Information**
   - common_name
   - scientific_name
   - family

2. **Summary**
   - Concise overview focused on most distinctive features

3. **Identification Path**
   - primary_markers
   - secondary_markers
   - seasonal_markers
   - similar_species_differentiation

4. **Features**
   - always_true (fundamental traits with no exceptions)
   - usually_true (primary traits that may have exceptions; include exceptions field)
   - sometimes_true (variable traits with conditions; include conditions field)
   - never_true (explicitly absent features important for differentiation)

5. **Kid-Friendly Identification**
   - primary_identifier (most obvious feature for children)
   - memorable_comparison (vivid, relatable comparison)
   - touch_tip (tactile description with simile)
   - smell_tip (simple sensory instruction with cautions if needed)
   - fun_fact (engaging, memorable information with child-friendly context)
   - detective_steps (3+ steps for identification with decision branches)

6. **Seasonal Timeline**
   - All four seasons separately (Spring, Summer, Fall, Winter)
   - For each season: visual_changes, reproductive_activity, identification_tips, kid_friendly_tip

7. **Confirmation Checklist**
   - Multiple distinctive features with reliability and visibility ratings

8. **Look-Alike Species**
   - Similar species with specific differences and identification tips

9. **Cultural/Ecological Notes**
    - Brief ecological role information

10. **Cultural Significance**
   - Organized by cultural group, each with physical_uses and symbolic_meaning subsections
   - Specific, well-researched information

11. **Range Within California**
    - Geographic distribution details

12. **Physical Characteristics**
    - height_range, growth_rate, crown_spread, lifespan, trunk_diameter, root_system, toxicity

13. **Conservation Status**
    - status, threats, protection_efforts

14. **Decision Tree Placement**
    - primary_split_features, confirmation_features, observation_sequence, seasonal_identification
    - misidentification_risks (list of potential confusion species)

15. **Other Optional Sections** (as appropriate)
    - propagation_information (for garden-suitable species)
    - wildlife_value (details on habitat and food provided)

## Quality Checklist

Before completing each tree profile, verify:

1. **Structure and Format**
   - Filename follows the correct format: `[family-name].[common-tree-name].yml` in lower case
   - All required sections are present and properly formatted
   - YAML structure is valid with consistent indentation
   - Feature IDs match the current standardized format (CATEGORY-TYPE-##)

2. **Scientific Accuracy with Kid-Friendly Language**
   - Features are properly categorized in appropriate categories
   - Trunk form features (TREE-TRUNK-01, TREE-TRUNK-02) are in usually_true category with exceptions field
   - Seasonal information is accurate and distinctive for all four seasons
   - Range, habitat, and ecological information is current and accurate
   - Conservation status includes specific threats and protection efforts
   - All information is presented in language an 8-10 year old can understand

3. **Consistently Kid-Friendly Content Throughout**
   - EVERY section uses concrete, engaging language appropriate for 8-10 year olds
   - ALL technical terms are replaced with simpler alternatives throughout the entire file
   - Fun facts are truly interesting and connect to observable features
   - Metaphors and similes use objects familiar to children
   - Safety cautions are clear but not frightening
   - No section (even "technical" ones like range or physical characteristics) uses botanical jargon

4. **Vividness and Engagement**
   - Sensory descriptions engage multiple senses in simple language
   - Size comparisons use familiar objects or body parts for scale (buildings, school buses, etc.)
   - Notable or unique features are highlighted with vivid, simple descriptions
   - Cultural information is specific, respectful, and presented in kid-friendly terms
   - Wildlife interactions are included and explained in simple language

5. **Clear Differentiation with Simple Language**
   - Clear distinctions from similar species in language kids understand
   - Similar species comparisons use simple, concrete differences ("needles are flat not round")
   - Misidentification risks section covers likely confusion species with simple explanations
   - Decision tree placement is logical and uses kid-friendly terminology
   - Features at multiple observation distances are included with simple viewing instructions
   - Features in always_true do not have contradictory features in any other section
   - Comparisons use relatable analogies ("hugs the branch" vs. "sticks straight out")

6. **Track which trees are complete and which still need to be generated**
   - After every tree file is created, updated, moved, or deleted, reflect the change in tree-tracking.md as well

## Maintaining Consistency Between Tree-tracking.md and Path Files

Tree-tracking.md serves as the master list and source of truth for all trees included in this project. This is critical for maintaining consistency across all identification paths.

### Key Guidelines:

1. **Source of Truth**: tree-tracking.md is the definitive reference for:
   - Which trees are included in the project (total count)
   - How trees are categorized (broadleaf, conifer, etc.)
   - Which trees should appear in each path

2. **Path File Structure**:
   - Each path file (e.g., broadleaf-path.md) must account for ALL trees in its category as listed in tree-tracking.md
   - The tree count in each path file must match the corresponding count in tree-tracking.md
   - If a tree is listed in tree-tracking.md but lacks a detailed description in the path file, note this in the path file's "Notes About Tree Classifications" section

3. **Count Verification Process**:
   - When updating any path file, verify the tree counts match tree-tracking.md
   - If there's a discrepancy, assume tree-tracking.md is correct unless specifically determined otherwise
   - NEVER remove trees from the path files to make counts match - instead, add the missing trees or note which trees need future detailed descriptions

4. **Resolving Inconsistencies**:
   - If a discrepancy is found, document it in the "Notes About Tree Classifications" section of the path file
   - If a tree appears to be incorrectly classified, confirm with botanical references before making changes
   - Any changes to tree classification should be updated in both tree-tracking.md and the appropriate path files

5. **Genus-First Approach**:
   - For rare species or those with subtle distinctions, use a genus-level approach
   - Group similar species at the genus level when they meet these criteria:
     a) Rarely encountered in California
     b) Difficult to distinguish at the species level (especially for children)
     c) Share distinctive genus-level characteristics
   - When using genus-level groupings:
     a) List all included species in both tree-tracking.md and path files
     b) Focus on genus-level identification characteristics
     c) Add detailed genus description sections to path files
     d) Update tree counts throughout all related files
     
   - **Implemented Genus Groups**:
     - **Broadleaf Trees**:
       - Birch Genus (Betula spp.) - 9 species
       - Less Common Alder Species (Alnus spp.) - 6 species
       - Elm Genus (Ulmus spp.) - 7 species
       - Less Common Maple Species (Acer spp.) - 2 species
     
     - **Conifer Trees**:
       - Common Cypress Genus (Cupressus spp.) - 6 species
       - Less Common Fir Species (Abies spp.) - 8 species
       - Less Common Pine Species (Pinus spp.) - 2 species
       - Less Common Spruce Species (Picea spp.) - 7 species
       - True Cedar Genus (Cedrus spp.) - 3 species
       
   - **Genus Description Format**:
     Each genus group should include:
     a) Common characteristics shared by all species in the genus
     b) Complete list of included species with brief distinguishing features
     c) Identification tips focusing on genus-level recognition
     d) Notes on where these species are most likely to be encountered

By following these comprehensive guidelines, you'll create standardized, accurate tree profiles that support the generation of an effective, kid-friendly decision tree for California tree identification.