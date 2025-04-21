# Converting the California Tree Guide to XMind Format

This document provides instructions for converting the California Tree Guide mind map to a format that can be opened with XMind.

## Method 1: Direct Import in XMind

XMind supports importing FreeMind (.mm) files directly:

1. **Open XMind**: Launch the XMind application
2. **Import File**: 
   - Click "File" > "Import" 
   - Select "FreeMind" from the import options
   - Navigate to and select `california_tree_guide.mm` (not the .xml file)
   - Click "Open" or "Import"

If you don't have the .mm file or experience issues with it:

## Method 2: Convert XML to MM Format

1. **Download and install FreeMind**: If you don't already have it, get it from http://freemind.sourceforge.net/
2. **Open XML in FreeMind**:
   - Launch FreeMind
   - Open the `california_tree_guide_complete.xml` file
3. **Save as MM format**:
   - Click "File" > "Save As"
   - Save the file with the extension `.mm`
4. **Import to XMind**:
   - Open XMind
   - Click "File" > "Import" > "FreeMind"
   - Select the newly saved `.mm` file

## Method 3: Online Conversion

If you're having trouble with direct imports:

1. **Use Online Converter**: 
   - Visit https://www.xmind.net/zen/ (XMind's online version)
   - Sign up/Log in if required
   - Click "Import" and select your `.mm` file
2. **Download and Use Locally**:
   - After successful import to XMind Zen online
   - Click "File" > "Export" > "XMind" to download an XMind format file
   - Open this file in your desktop XMind application

## Method 4: Manual Export from FreeMind to XMind

If other methods fail:

1. **Open in FreeMind**:
   - Launch FreeMind
   - Open `california_tree_guide_complete.xml`
2. **Export to specific format**:
   - Click "File" > "Export" > "Using XSLT"
   - Select an output format that XMind can read (try HTML or another structured format)
3. **Import to XMind**:
   - In XMind, try importing the exported file
   - If direct import doesn't work, copy-paste the structure manually

## Troubleshooting Tips

If you experience issues with the import:

1. **Simplify First**: Try importing a small subset of the mind map first to test compatibility
2. **Check XMind Version**: Newer versions of XMind have better import capabilities
3. **Try XMind Zen**: The online version sometimes handles imports differently than the desktop version
4. **Remove Complex Formatting**: If the mind map has custom formatting or features, these might cause import issues
5. **Use Intermediate Format**: If direct conversion doesn't work, try exporting to an intermediate format (like HTML) first

## Expected Results

After successful import to XMind:

1. The complete tree structure should be visible
2. The "California Tree Identification Guide" should appear as the central/root topic
3. "What Catches Your Eye?" should be the main branch
4. All identification paths should be preserved
5. All tree species should be included as leaf nodes

## Alternative Suggestion

If you continue to have difficulties with the conversion, XMind has the ability to create mind maps from scratch relatively quickly. Given the structured nature of our decision tree, recreating the high-level structure in XMind might be an option if automated conversion proves challenging.