#!/usr/bin/env python3
"""
Display Palmeri Distillery logo on round display
"""

from PIL import Image
from GC9A01 import GC9A01
import time

# Initialize display
disp = GC9A01(
    port=0,
    cs=0,
    dc=25,
    rst=24,
    backlight=None,
    spi_speed_hz=80000000,
    width=240,
    height=240
)
disp.begin()

print("Loading logo...")

# Load and resize the logo
logo = Image.open('palmeri_logo.png')

# Resize to fit the 240x240 display
logo = logo.resize((240, 240), Image.Resampling.LANCZOS)

# Convert to RGB (in case it's RGBA or other format)
logo = logo.convert('RGB')

print("Displaying logo...")
disp.display(logo)

print("Logo displayed! Press Ctrl+C to clear and exit.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nClearing display...")
    # Clear to black
    blank = Image.new('RGB', (240, 240), color=(0, 0, 0))
    disp.display(blank)
    print("Done!")
