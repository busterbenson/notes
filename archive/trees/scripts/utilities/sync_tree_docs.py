#!/usr/bin/env python3
"""
Tree Documentation Sync Tool

This script manages the synchronization between markdown files and XMind mind maps.
It provides a unified interface for generating and validating the tree documentation.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Constants
DEFAULT_PATH_DIR = "../../decision_trees/paths"
DEFAULT_XMIND_FILE = "../../decision_trees/paths/california_tree_guide_xmind_generated.xmind"
MAPPING_FILE = "node_mapping.json"

def generate_xmind(args):
    """Generate XMind file from markdown files."""
    cmd = [
        "python", 
        "markdown_to_xmind_zip.py", 
        "--path-dir", args.path_dir, 
        "--output", args.xmind,
        "--mapping", args.mapping
    ]
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout)
        print("XMind generation completed successfully!")
        return True
    else:
        print(f"Error generating XMind file: {result.stderr}")
        return False

def verify_correspondence(args):
    """Verify correspondence between markdown and XMind files."""
    cmd = [
        "python", 
        "verify_correspondence.py", 
        "--md-dir", args.path_dir, 
        "--xmind", args.xmind
    ]
    
    if args.detailed:
        cmd.append("--detailed")
    
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout)
        print("Verification completed successfully! 100% correspondence achieved.")
        return True
    else:
        print(result.stdout)
        print(f"Verification failed! Check the discrepancies above.")
        return False

def sync(args):
    """Sync markdown files to XMind and verify correspondence."""
    success = generate_xmind(args)
    if not success:
        print("Aborting sync due to XMind generation failure.")
        return False
    
    print("\n=== Verifying Correspondence ===\n")
    success = verify_correspondence(args)
    
    if success:
        print("\n✅ Sync completed successfully!")
    else:
        print("\n❌ Sync failed! Please check the verification results.")
    
    return success

def view_xmind(args):
    """Open the XMind file in the default application."""
    xmind_path = Path(args.xmind).resolve()
    
    if not xmind_path.exists():
        print(f"XMind file not found: {xmind_path}")
        return False
    
    try:
        if sys.platform == 'darwin':
            subprocess.run(['open', str(xmind_path)])
        elif sys.platform == 'win32':
            os.startfile(str(xmind_path))
        elif sys.platform == 'linux':
            subprocess.run(['xdg-open', str(xmind_path)])
        else:
            print(f"Unsupported platform: {sys.platform}")
            return False
        
        print(f"Opened XMind file: {xmind_path}")
        return True
    except Exception as e:
        print(f"Error opening XMind file: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Tree Documentation Sync Tool')
    parser.add_argument('--path-dir', default=DEFAULT_PATH_DIR, 
                        help=f'Directory containing path markdown files (default: {DEFAULT_PATH_DIR})')
    parser.add_argument('--xmind', default=DEFAULT_XMIND_FILE, 
                        help=f'XMind file path (default: {DEFAULT_XMIND_FILE})')
    parser.add_argument('--mapping', default=MAPPING_FILE, 
                        help=f'Mapping file name (default: {MAPPING_FILE})')
    parser.add_argument('--detailed', action='store_true', 
                        help='Show detailed verification results')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate XMind from markdown')
    gen_parser.set_defaults(func=generate_xmind)
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify correspondence')
    verify_parser.set_defaults(func=verify_correspondence)
    
    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Sync markdown to XMind and verify')
    sync_parser.set_defaults(func=sync)
    
    # View command
    view_parser = subparsers.add_parser('view', help='Open XMind file')
    view_parser.set_defaults(func=view_xmind)
    
    args = parser.parse_args()
    
    if not hasattr(args, 'func'):
        # Default to sync if no command specified
        args.func = sync
    
    success = args.func(args)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()