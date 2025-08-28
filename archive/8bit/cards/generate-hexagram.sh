#!/bin/bash
# generate-hexagram.sh
# A shell script to generate all four seasonal cards for a hexagram

# Show usage if no arguments provided
if [ "$#" -eq 0 ]; then
  echo "Usage: ./generate-hexagram.sh <6-bit_code>"
  echo "Example: ./generate-hexagram.sh 101010"
  exit 1
fi

# Validate that the input is a 6-digit binary code
if ! [[ "$1" =~ ^[0-1]{6}$ ]]; then
  echo "Error: The input must be a 6-digit binary code (e.g., 101010)"
  exit 1
fi

HEXAGRAM_CODE=$1
SCRIPT_DIR=$(dirname "$0")

# Make the Python script executable
chmod +x "$SCRIPT_DIR/generate-card.py"

echo "Generating all four seasonal cards for hexagram: $HEXAGRAM_CODE"
echo ""

# Generate Winter card (00)
echo "Generating Winter card: ${HEXAGRAM_CODE}00"
"$SCRIPT_DIR/generate-card.py" "${HEXAGRAM_CODE}00"
echo ""

# Generate Spring card (10)
echo "Generating Spring card: ${HEXAGRAM_CODE}10"
"$SCRIPT_DIR/generate-card.py" "${HEXAGRAM_CODE}10"
echo ""

# Generate Summer card (11)
echo "Generating Summer card: ${HEXAGRAM_CODE}11"
"$SCRIPT_DIR/generate-card.py" "${HEXAGRAM_CODE}11"
echo ""

# Generate Fall card (01)
echo "Generating Fall card: ${HEXAGRAM_CODE}01"
"$SCRIPT_DIR/generate-card.py" "${HEXAGRAM_CODE}01"
echo ""

echo "All four seasonal cards for hexagram $HEXAGRAM_CODE have been generated!"
echo "The cards are saved in the 'generated' directory."
echo ""
echo "To review each card:"
echo "  1. Open the YAML files in the 'generated' directory"
echo "  2. Fill in the placeholder fields with meaningful content"
echo "  3. Use the descriptions to craft image prompts"
echo "  4. Generate the card images using the prompts"

exit 0