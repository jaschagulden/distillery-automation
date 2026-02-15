#!/usr/bin/env python3
"""
Distillery Display - Shows real-time weight and temperature
on the GC9A01 1.28" round display
"""

import time
from PIL import Image, ImageDraw, ImageFont
from GC9A01 import GC9A01
from hx711 import HX711
import sm_tc

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

# Initialize HX711 load cells
hx = HX711(5, 6)
hx.reset()
hx.set_reading_format("MSB", "MSB")

# Load calibration data
TARE = -241007.50
CALIBRATION = -25651.61

try:
    with open('calibration_data.txt', 'r') as f:
        tare_line = f.readline().strip()
        cal_line = f.readline().strip()
        # Extract numbers from "Tare: -241007.50" format
        TARE = float(tare_line.split(':')[1].strip())
        CALIBRATION = float(cal_line.split(':')[1].strip())
    print("Calibration loaded successfully")
    print(f"Tare: {TARE}, Calibration: {CALIBRATION}")
except Exception as e:
    print(f"Warning: Using default calibration values: {e}")

# Initialize thermocouple
tc_hat = sm_tc.SMtc(0)  # Stack 0
tc_hat.set_sensor_type(1, 3)  # Channel 1 = K-type
tc_hat.set_sensor_type(2, 3)  # Channel 2 = K-type

print("Distillery Display Started!")
print("Press Ctrl+C to exit")

try:
    while True:
        # Create blank image
        img = Image.new('RGB', (240, 240), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw outer circle (blue)
        draw.ellipse((10, 10, 230, 230), outline=(0, 100, 255), width=3)
        
        # Get weight
        try:
            raw = hx.get_weight(5)
            weight_kg = (raw - TARE) / CALIBRATION
            weight_lb = weight_kg * 2.20462
            weight_text = f"{weight_lb:.1f} lb"
        except Exception as e:
            weight_text = "Error"

               # Get temperatures
        try:
            temp1_c = tc_hat.get_temp(1)
            temp1_f = (temp1_c * 9/5) + 32
            temp1_text = f"T1: {temp1_f:.0f}F"
        except:
            temp1_text = "T1: --"
        
        try:
            temp2_c = tc_hat.get_temp(2)
            temp2_f = (temp2_c * 9/5) + 32
            temp2_text = f"T2: {temp2_f:.0f}F"
        except:
            temp2_text = "T2: --"
        
        # Draw title
        draw.text((70, 40), "DISTILLERY", fill=(255, 255, 255))
        
        # Draw weight (large, center)
        draw.text((60, 100), weight_text, fill=(0, 255, 0))
        
        # Draw temperatures
        draw.text((60, 150), temp1_text, fill=(255, 200, 0))
        draw.text((60, 175), temp2_text, fill=(255, 200, 0))
        
        # Display the image
        disp.display(img)
        
        # Update every 1 second
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")
    # Clear display
    img = Image.new('RGB', (240, 240), color=(0, 0, 0))
    disp.display(img)
    print("Display cleared")
