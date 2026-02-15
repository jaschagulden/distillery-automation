#!/usr/bin/env python3
"""
Test script for GC9A01 1.28" Round Display
Displays colored circles and text
"""

import time
from PIL import Image, ImageDraw, ImageFont
from GC9A01 import GC9A01

# Create display instance
# Your wiring:
# DC = GPIO 25
# RST = GPIO 24
# SPI port 0, device 0 (CE0)
disp = GC9A01(
    port=0,           # SPI port 0
    cs=0,             # CE0 (chip select 0)
    dc=25,            # DC pin
    rst=24,           # Reset pin
    backlight=None,   # No backlight control
    spi_speed_hz=80000000,
    width=240,
    height=240
)

# Initialize display
disp.begin()

print("Display initialized!")
print("Drawing test pattern...")

# Create blank image (240x240, RGB mode)
img = Image.new('RGB', (240, 240), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw colored circles
draw.ellipse((20, 20, 220, 220), fill=(255, 0, 0))      # Red outer circle
draw.ellipse((60, 60, 180, 180), fill=(0, 255, 0))      # Green middle circle
draw.ellipse((100, 100, 140, 140), fill=(0, 0, 255))    # Blue inner circle

# Draw text in center
draw.text((80, 110), "HELLO!", fill=(255, 255, 255))

# Display the image
disp.display(img)

print("Test pattern displayed!")
print("Display should show red, green, blue circles with 'HELLO!' text")
