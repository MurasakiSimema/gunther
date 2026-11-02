"""
Root entry point for the Duck Sprite Builder.
Usage:
    python duck_sprite_builder.py
    python duck_sprite_builder.py --preview
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gunther.duck_sprite_builder import main

if __name__ == "__main__":
    main()
