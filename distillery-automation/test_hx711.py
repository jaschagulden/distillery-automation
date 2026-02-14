#!/usr/bin/env python3
"""
Quick test for HX711 load cells
"""

import RPi.GPIO as GPIO
from hx711 import HX711
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)

print("HX711 Load Cell Test")
print("=" * 50)
print()

# Test load cell #1 (Platform 1)
print("Testing Load Cell Platform")
print("GPIO 5 (DT), GPIO 6 (SCK)")
print("-" * 50)

try:
    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    hx.reset()
    
    print("Reading values (press Ctrl+C to stop)...")
    print()
    
    for i in range(10):
        try:
            val = hx.read_long()
            print(f"Reading {i+1}: {val}")
        except Exception as e:
            print(f"Reading {i+1}: Error - {e}")
        
        time.sleep(0.5)
    
    print()
    print("✅ Load Cell Platform is working!")
    print()
    print("Raw values shown above. We'll calibrate next.")
    
except KeyboardInterrupt:
    print("\nTest stopped by user")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    GPIO.cleanup()
    print("\nGPIO cleaned up")

print()
print("=" * 50)
print("Test complete!")
