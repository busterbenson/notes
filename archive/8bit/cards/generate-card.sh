#!/bin/bash
# generate-card.sh
# A shell script to generate 8-Bit Oracle cards

# Show usage if no arguments provided
if [ "$#" -eq 0 ]; then
  echo "Usage: ./generate-card.sh <binary_code>"
  echo "Example: ./generate-card.sh 10101010"
  exit 1
fi

# Validate that the input is an 8-digit binary code
if ! [[ "$1" =~ ^[0-1]{8}$ ]]; then
  echo "Error: The input must be an 8-digit binary code (e.g., 10101010)"
  exit 1
fi

BINARY_CODE=$1
SCRIPT_DIR=$(dirname "$0")

# Make the Python script executable
chmod +x "$SCRIPT_DIR/generate-card.py"

# Run the Python script
echo "Generating card for binary code: $BINARY_CODE..."
"$SCRIPT_DIR/generate-card.py" "$BINARY_CODE"

# If Python script was successful, display next steps
if [ $? -eq 0 ]; then
  echo ""
  echo "Card generation successful!"
  echo ""
  echo "To generate more cards, use one of these commands:"
  echo "  - For a specific binary code: ./generate-card.sh <binary_code>"
  echo "  - For a hexagram with all seasons: ./generate-hexagram.sh <6-bit_code>"
  echo ""
  echo "To enhance the generated card:"
  echo "  1. Review the generated YAML file in the 'generated' directory"
  echo "  2. Fill in the placeholder fields with meaningful content"
  echo "  3. Use the descriptions to craft an image prompt"
  echo "  4. Generate the card image using the prompt"
fi

exit 0