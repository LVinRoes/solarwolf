"""
Another Main module. So `python -m solarwolf` works
"""

import sys
import os
import solarwolf.cli

# Fügen Sie das Elternverzeichnis zum sys.path hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("Python Path:", sys.path)
print("SolarWolf Module:", solarwolf)

if __name__ == "__main__":
    solarwolf.cli.main()
