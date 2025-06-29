#!/usr/bin/env python3
"""
Random Folder Opener Script

This script opens a random subfolder from a given directory path.
If no path is provided, it uses the current directory.
The script recursively searches through all subfolders and sub-subfolders.
"""

import os
import random
import sys
import subprocess
import platform
from pathlib import Path


def get_all_subfolders(root_path):
    """
    Recursively get all subfolders from the given root path.

    Args:
        root_path (str): The root directory path to search

    Returns:
        list: List of all subfolder paths
    """
    subfolders = []

    try:
        for root, dirs, files in os.walk(root_path):
            # Filter out directories named 'Lib'
            dirs[:] = [d for d in dirs if d[0] not in ['.', '_']]
            # Add all directories found in this level
            for dir_name in dirs:
                full_path = os.path.join(root, dir_name)
                subfolders.append(full_path)
    except PermissionError:
        print(f"⚠️  Permission denied accessing some folders in {root_path}")
    except Exception as e:
        print(f"❌ Error scanning folders: {e}")

    return subfolders


def open_folder(folder_path):
    """
    Open a folder using the system's default file explorer.

    Args:
        folder_path (str): Path to the folder to open
    """
    system = platform.system().lower()

    if system == "windows":
        subprocess.run(["explorer", folder_path])
    elif system == "darwin":  # macOS
        subprocess.run(["open", folder_path])
    elif system == "linux":
        subprocess.run(["xdg-open", folder_path])
    else:
        print(f"❌ Unsupported operating system: {system}")


def main():
    """Main function to handle the random folder opening logic."""
    # Get the target directory from command line argument or use current directory
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
        if not os.path.exists(target_path):
            print(f"❌ Path does not exist: {target_path}")
            sys.exit(1)
        if not os.path.isdir(target_path):
            print(f"❌ Path is not a directory: {target_path}")
            sys.exit(1)
    else:
        # get user folder
        target_path = os.getcwd()

    print(f"🔍 Searching for subfolders in: {target_path}")

    # Get all subfolders
    subfolders = get_all_subfolders(target_path)

    if not subfolders:
        print("📁 No subfolders found in the specified directory.")
        print("💡 The directory might be empty or contain only files.")
        sys.exit(0)

    print(f"📂 Found {len(subfolders)} subfolder(s)")

    # Select a random subfolder
    random_folder = random.choice(subfolders)

    print(f"🎲 Randomly selected: {random_folder}")

    # Open the random folder
    open_folder(random_folder)


if __name__ == "__main__":
    main()
