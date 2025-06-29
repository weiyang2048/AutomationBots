#!/usr/bin/env python3
"""
Test script for the AutomationBots CLI
"""

import sys
from pathlib import Path

# Add the AutomationBots directory to the path
sys.path.insert(0, str(Path(__file__).parent / "AutomationBots"))

try:
    from cli import cli
    print("✅ CLI module imported successfully!")
    print("🚀 Available commands:")
    
    # Get the command list
    commands = cli.commands.keys()
    for cmd in sorted(commands):
        print(f"  - {cmd}")
        
except ImportError as e:
    print(f"❌ Failed to import CLI module: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)

print("\n🎉 CLI setup complete! You can now use:")
print("  python -m AutomationBots.cli --help")
print("  automationbots --help (after installation)") 