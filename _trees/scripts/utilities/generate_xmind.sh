#!/bin/bash

# Script to generate the XMind file for the California Tree Guide
# This script provides a simple way to regenerate the XMind file after making changes to markdown files.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON_SCRIPT="${SCRIPT_DIR}/markdown_to_xmind_complete.py"
OUTPUT_DIR="/Users/buster/projects/notes/_trees/decision_trees/paths/export"
OUTPUT_FILE="${OUTPUT_DIR}/california_tree_guide.xmind"

echo "Generating XMind file from markdown paths..."
echo "Using script: ${PYTHON_SCRIPT}"
echo "Output file will be: ${OUTPUT_FILE}"
echo

# Make backup of existing file if it exists
if [ -f "${OUTPUT_FILE}" ]; then
    BACKUP_FILE="${OUTPUT_FILE}.backup"
    echo "Making backup of existing XMind file to ${BACKUP_FILE}"
    cp "${OUTPUT_FILE}" "${BACKUP_FILE}"
fi

# Run the Python script
python3 "${PYTHON_SCRIPT}"

# Check if successful
if [ $? -eq 0 ]; then
    echo
    echo "✅ XMind file successfully generated at: ${OUTPUT_FILE}"
    echo "You can now open this file in XMind to visualize the decision tree."
else
    echo
    echo "❌ Error generating XMind file. Check the error messages above."
    if [ -f "${BACKUP_FILE}" ]; then
        echo "Restoring backup file..."
        cp "${BACKUP_FILE}" "${OUTPUT_FILE}"
    fi
fi