#!/usr/bin/env python3
"""
CLI interface for AutomationBots

Provides command-line access to various automation tools.
"""

import click
import os
import sys
from pathlib import Path
from loguru import logger

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from random_folder_opener import get_all_subfolders, open_folder


@click.group()
@click.version_option(version="0.1.0", prog_name="AutomationBots")
def cli():
    """
    AutomationBots CLI
    
    A collection of automation tools accessible via command line.
    """
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True), 
                default=os.getcwd(), required=False)
@click.option('--count', '-c', default=1, help='Number of random folders to open (default: 1)')
@click.option('--exclude', '-e', multiple=True, help='Patterns to exclude from search (can be used multiple times)')
@click.option('--include', '-i', multiple=True, help='Patterns to include in search (can be used multiple times)')
@click.option('--max-depth', '-d', type=int, help='Maximum depth to search for subfolders')
@click.option('--dry-run', is_flag=True, help='Show what would be opened without actually opening folders')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def random_folder(path, count, exclude, include, max_depth, dry_run, verbose):
    """
    Open random 🎲 subfolder(s) from a directory
    
    Opens one or more random subfolders from the specified directory.
    If no directory is specified, uses the current working directory.
    
    Examples:
        automationbots random-folder                    # Open 1 random folder from current directory
        automationbots random-folder /path/to/dir      # Open 1 random folder from specified path
        automationbots random-folder -c 3              # Open 3 random folders
        automationbots random-folder -e "node_modules" # Exclude node_modules folders
        automationbots random-folder --dry-run         # Show what would be opened
    """
    if verbose:
        logger.info(f"🔍 Searching for subfolders in: {path}")
    
    # Get all subfolders
    subfolders = get_all_subfolders(path)
    
    if not subfolders:
        click.echo("📁 No subfolders found in the specified directory.")
        click.echo("💡 The directory might be empty or contain only files.")
        return
    
    # Apply filters
    filtered_subfolders = subfolders
    
    # Apply exclude patterns
    if exclude:
        for pattern in exclude:
            filtered_subfolders = [f for f in filtered_subfolders if pattern not in f]
    
    # Apply include patterns
    if include:
        for pattern in include:
            filtered_subfolders = [f for f in filtered_subfolders if pattern in f]
    
    # Apply max depth filter
    if max_depth:
        filtered_subfolders = [
            f for f in filtered_subfolders 
            if f.count(os.sep) - path.count(os.sep) <= max_depth
        ]
    
    if not filtered_subfolders:
        click.echo("📁 No subfolders match the specified filters.")
        return
    
    click.echo(f"📂 Found {len(filtered_subfolders)} subfolder(s) after filtering")
    
    # Determine how many folders to open
    actual_count = min(count, len(filtered_subfolders))
    
    if actual_count < count:
        click.echo(f"⚠️  Only {actual_count} folders available, opening {actual_count} instead of {count}")
    
    # Select random folders
    import random
    selected_folders = random.sample(filtered_subfolders, actual_count)
    
    if dry_run:
        click.echo("🔍 Dry run mode - would open the following folders:")
        for i, folder in enumerate(selected_folders, 1):
            click.echo(f"  {i}. {folder}")
        return
    
    # Open the selected folders
    for i, folder in enumerate(selected_folders, 1):
        click.echo(f"🎲 Opening folder {i}/{actual_count}: {folder}")
        open_folder(folder)
        
@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True), 
                default=os.getcwd(), required=False)
@click.option('--max-depth', '-d', type=int, help='Maximum depth to search')
@click.option('--count', '-c', type=int, default=10, help='Number of folders to list (default: 10)')
def list_folders(path, max_depth, count):
    """
    📋 List subfolders in a directory
    
    Lists subfolders in the specified directory, optionally limited by depth.
    
    Examples:
        automationbots list-folders                    # List folders in current directory
        automationbots list-folders /path/to/dir      # List folders in specified path
        automationbots list-folders -d 2              # Limit to 2 levels deep
        automationbots list-folders -c 20             # Show 20 folders
    """
    click.echo(f"🔍 Scanning subfolders in: {path}")
    
    subfolders = get_all_subfolders(path)
    
    if not subfolders:
        click.echo("📁 No subfolders found.")
        return
    
    # Apply max depth filter
    if max_depth:
        subfolders = [
            f for f in subfolders 
            if f.count(os.sep) - path.count(os.sep) <= max_depth
        ]
    
    click.echo(f"📂 Found {len(subfolders)} subfolder(s)")
    
    # Show folders (limited by count)
    for i, folder in enumerate(subfolders[:count], 1):
        relative_path = os.path.relpath(folder, path)
        click.echo(f"  {i:2d}. {relative_path}")
    
    if len(subfolders) > count:
        click.echo(f"  ... and {len(subfolders) - count} more folders")


@cli.command()
def info():
    """
    ℹ️  Show information about AutomationBots
    
    Displays version information and available commands.
    """
    click.echo("🚀 AutomationBots CLI")
    click.echo("=" * 40)
    click.echo("Version: 0.1.0")
    click.echo("A collection of automation tools for various tasks.")
    click.echo()
    click.echo("Available commands:")
    click.echo("  random-folder  - Open random subfolder(s) from a directory")
    click.echo("  list-folders   - List subfolders in a directory")
    click.echo("  info          - Show this information")
    click.echo()
    click.echo("For help with a specific command, use: automationbots <command> --help")


if __name__ == "__main__":
    cli()