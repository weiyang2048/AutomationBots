"""
LinkedIn Job Tracker

A tool to track and manage saved LinkedIn jobs.
"""

__version__ = "0.1.0"

from . import scraper
from . import cli

__all__ = ['scraper', 'cli']