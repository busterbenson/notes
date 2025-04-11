#!/bin/bash

# 8-Bit Oracle Card Generator Script
# Enhanced version with support for both raw associations and full card generation

# Display help information
function show_help {
    echo "8-Bit Oracle Card Generator"
    echo ""
    echo "Usage:"
    echo "  $0 [options] <binary_code>"
    echo ""
    echo "Options:"
    echo "  -h, --help              Show this help message and exit"
    echo "  -a, --associations      Generate raw associations only (requires 6-bit code)"
    echo "  -f, --full              Generate full card with interpretations (requires 8-bit code)"
    echo "  -g, --generate-all      Generate associations for all 64 hexagrams"
    echo ""
    echo "Examples:"
    echo "  $0 --associations 101010     # Generate raw associations for hexagram 101010"
    echo "  $0 --full 10101011           # Generate a full card for 10101011"
    echo "  $0 --generate-all            # Generate raw associations for all 64 hexagrams"
    echo "  $0 10101011                  # Default: Generate full card"
    echo ""
    exit 0
}

# Default mode
MODE="full"
BINARY_CODE=""

# Parse command-line arguments
if [ $# -eq 0 ]; then
    show_help
fi

while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -h|--help)
        show_help
        ;;
        -a|--associations)
        MODE="associations"
        shift
        ;;
        -f|--full)
        MODE="full"
        shift
        ;;
        -g|--generate-all)
        MODE="generate-all"
        shift
        ;;
        *)
        BINARY_CODE="$1"
        shift
        ;;
    esac
done

# Check for binary code if we're not in generate-all mode
if [ "$MODE" != "generate-all" ] && [ -z "$BINARY_CODE" ]; then
    echo "Error: Binary code is required"
    show_help
fi

# Execute the appropriate command based on the mode
case $MODE in
    associations)
        # Check if binary code has 6 bits
        if ! [[ $BINARY_CODE =~ ^[01]{6}$ ]]; then
            echo "Error: Association generation requires a 6-bit code (hexagram)"
            exit 1
        fi
        
        echo "Generating raw associations for hexagram: $BINARY_CODE"
        python association-generator.py "$BINARY_CODE"
        
        echo ""
        echo "Next steps:"
        echo "1. Review the generated files in compiled/$BINARY_CODE/"
        echo "2. Use these raw associations to help create the full card"
        ;;
        
    full)
        # Check if binary code has 8 bits
        if ! [[ $BINARY_CODE =~ ^[01]{8}$ ]]; then
            echo "Error: Full card generation requires an 8-bit code"
            exit 1
        fi
        
        # Create hexagram directory if it doesn't exist
        HEXAGRAM=${BINARY_CODE:0:6}
        mkdir -p completed/$HEXAGRAM
        
        # Run the Python description generator
        echo "Generating full card for: $BINARY_CODE"
        python create-description.py "$BINARY_CODE"
        
        # Enhance the card with additional content
        if [ -f "completed/$HEXAGRAM/$BINARY_CODE.md" ]; then
            python create-enhanced-card.py "$BINARY_CODE" "completed/$HEXAGRAM/$BINARY_CODE.md"
        fi
        
        # Create directory for card images
        mkdir -p ../card_images/completed/$HEXAGRAM
        
        # Create directories for image prompts
        mkdir -p image_prompts/$HEXAGRAM
        
        # Create a symbolic link from v3 to completed for backward compatibility
        if [ -d "v3/$HEXAGRAM" ]; then
            echo "Note: v3/$HEXAGRAM already exists"
        else
            mkdir -p v3
            ln -sf ../completed/$HEXAGRAM v3/$HEXAGRAM
            echo "Created symbolic link from v3/$HEXAGRAM to completed/$HEXAGRAM for backward compatibility"
        fi
        
        echo ""
        echo "Next steps:"
        echo "1. Edit the generated markdown file in completed/$HEXAGRAM/$BINARY_CODE.md and FILL IN ALL SECTIONS completely"
        echo "2. Once all sections are complete, run: python create-enhanced-card.py $BINARY_CODE completed/$HEXAGRAM/$BINARY_CODE.md"
        echo "3. Create a custom image prompt in image_prompts/$HEXAGRAM/$BINARY_CODE.md using examples in image_prompts/101010/ as templates"
        echo "4. Use the custom image prompt to create card artwork and save to:"
        echo "   ../card_images/completed/$HEXAGRAM/$BINARY_CODE-card-name.png"
        echo ""
        echo "IMPORTANT: Image generation should ALWAYS happen after both the narrative arc AND all card description"
        echo "           sections have been completed to ensure visual and thematic coherence."
        ;;
        
    generate-all)
        echo "Generating associations for all 64 hexagrams..."
        python generate-all-associations.py
        ;;
esac

exit 0