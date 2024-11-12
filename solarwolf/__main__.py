"""
Another Main module. So `python -m solarwolf` works
"""

import sys
import os
import solarwolf.cli

# Füge das übergeordnete Verzeichnis zum sys.path hinzu
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

if __name__ == "__main__":
    solarwolf.cli.main()
