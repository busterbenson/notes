#!/usr/bin/env python3
"""
Generate association files for all 64 possible hexagrams.

This script runs the association-generator.py script for every possible 6-bit pattern
to generate all 256 card association files (64 hexagrams × 4 seasonal variations).

The enhanced script:
1. Sets up a virtual environment with required dependencies
2. Processes all 64 hexagrams (6-bit patterns)
3. Shows a progress bar during generation
4. Provides detailed error reporting
5. Validates the number of files generated

Usage:
    python generate-all-associations.py
"""

import os
import sys
import subprocess
import itertools
import platform
import time

# Configuration
VENV_DIR = "venv"
REQUIRED_PACKAGES = ["pyyaml"]
OUTPUT_DIR = "compiled"

def setup_environment():
    """Set up a virtual environment with required packages."""
    # Check if venv exists
    venv_path = os.path.join(os.getcwd(), VENV_DIR)
    if not os.path.exists(venv_path):
        print(f"Creating virtual environment in {VENV_DIR}...")
        subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)
    
    # Determine activation script and python path based on OS
    if platform.system() == "Windows":
        activate_script = os.path.join(venv_path, "Scripts", "activate")
        python_path = os.path.join(venv_path, "Scripts", "python")
    else:
        activate_script = os.path.join(venv_path, "bin", "activate")
        python_path = os.path.join(venv_path, "bin", "python")
    
    # Install required packages
    for package in REQUIRED_PACKAGES:
        # Check if package is installed
        result = subprocess.run(
            f"{python_path} -c 'import {package}' 2>/dev/null", 
            shell=True, 
            executable="/bin/bash" if platform.system() != "Windows" else None
        )
        
        if result.returncode != 0:
            print(f"Installing {package}...")
            if platform.system() == "Windows":
                subprocess.run(
                    f"{python_path} -m pip install {package}", 
                    shell=True,
                    check=True
                )
            else:
                subprocess.run(
                    f"source {activate_script} && pip install {package}", 
                    shell=True, 
                    executable="/bin/bash", 
                    check=True
                )
    
    return activate_script, python_path

def generate_all_hexagrams(activate_script, python_path):
    """Generate all 64 possible 6-bit patterns and run association-generator.py for each."""
    # Make sure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate all possible 6-bit patterns
    all_bits = list(itertools.product(['0', '1'], repeat=6))
    total = len(all_bits)
    
    print(f"Generating association files for all {total} hexagrams...")
    print(f"This will create {total * 4} card files (64 hexagrams × 4 seasonal variations)")
    
    success_count = 0
    error_count = 0
    errors = []
    
    start_time = time.time()
    
    # Process each hexagram
    for i, bits in enumerate(all_bits):
        hexagram = ''.join(bits)
        
        # Show progress
        progress = (i / total) * 100
        print(f"[{progress:.1f}%] Processing hexagram {i+1}/{total}: {hexagram}", end='', flush=True)
        
        # Run the association generator script for this hexagram
        if platform.system() == "Windows":
            cmd = f"{python_path} association-generator.py {hexagram}"
        else:
            cmd = f"source {activate_script} && python association-generator.py {hexagram}"
            
        result = subprocess.run(
            cmd, 
            shell=True, 
            executable="/bin/bash" if platform.system() != "Windows" else None,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            success_count += 1
            print(" ✓")
        else:
            error_count += 1
            errors.append((hexagram, result.stderr))
            print(" ✗")
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    # Print summary
    print("\n--- Generation Summary ---")
    print(f"Successfully processed: {success_count} hexagrams")
    if error_count > 0:
        print(f"Errors encountered: {error_count} hexagrams")
        print("\nError details:")
        for hexagram, error in errors:
            print(f"- Hexagram {hexagram}: {error}")
    
    # Count files generated
    file_count = 0
    for root, _, files in os.walk(OUTPUT_DIR):
        for file in files:
            if file.endswith(".yml"):
                file_count += 1
    
    print(f"\nTotal files generated: {file_count} (expected: {success_count * 4})")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

def main():
    """Main function to set up environment and generate associations."""
    # Set up the virtual environment
    activate_script, python_path = setup_environment()
    
    # Generate all hexagrams
    generate_all_hexagrams(activate_script, python_path)
    
    print("\nAll association files have been generated!")

if __name__ == "__main__":
    main()