#!/usr/bin/env python3
"""
Real-time weight display
Press Ctrl+C to exit
"""

import RPi.GPIO as GPIO
from hx711 import HX711
import time
import sys

GPIO.setmode(GPIO.BCM)

# Your calibration values
TARE = -241007.50
CALIBRATION = -25651.61

print("Real-Time Weight Monitor")
print("=" * 60)
print("Press Ctrl+C to exit")
print()

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.reset()

time.sleep(1)

try:
    while True:
        # Read raw value
        raw = hx.get_weight(5)
        
        # Convert to kg
        weight_kg = (raw - TARE) / CALIBRATION
        
        # Convert to lbs
        weight_lbs = weight_kg * 2.20462
        
        # Display
        print(f"\rWeight: {weight_kg:7.2f} kg  ({weight_lbs:7.2f} lbs)  [Raw: {raw:9.1f}]", end='', flush=True)
        
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n\nStopped")
finally:
    GPIO.cleanup()
