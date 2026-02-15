#!/usr/bin/env python3
"""
Calibrate HX711 Load Cell Platform
"""

import RPi.GPIO as GPIO
from hx711 import HX711
import time
import sys

GPIO.setmode(GPIO.BCM)

print("HX711 Calibration")
print("=" * 60)
print()

# Initialize HX711
hx = HX711(5, 6)  # DT, SCK
hx.set_reading_format("MSB", "MSB")
hx.reset()

print("Initializing... please wait")
time.sleep(2)

try:
    # Step 1: Tare (zero)
    print()
    print("STEP 1: TARE (Zero the scale)")
    print("-" * 60)
    input("Make sure platform is EMPTY, then press ENTER...")
    
    print("Reading empty platform...")
    hx.reset()
    time.sleep(1)
    
    tare_readings = []
    for i in range(10):
        val = hx.get_weight(5)
        tare_readings.append(val)
        print(f"  Reading {i+1}: {val:.1f}")
        time.sleep(0.3)
    
    tare_value = sum(tare_readings) / len(tare_readings)
    print(f"\nTare (zero) value: {tare_value:.1f}")
    
    # Step 2: Known weight
    print()
    print("STEP 2: KNOWN WEIGHT")
    print("-" * 60)
    print("You have: Two 10 lb dumbbells")
    print()
    print("Choose calibration weight:")
    print("  1) One dumbbell (10 lbs / 4.54 kg)")
    print("  2) Two dumbbells (20 lbs / 9.07 kg)")
    
    choice = input("\nEnter 1 or 2: ")
    
    if choice == "1":
        known_weight_lbs = 10.0
        known_weight_kg = 4.54
        print("\nUsing: 10 lbs (4.54 kg)")
    else:
        known_weight_lbs = 20.0
        known_weight_kg = 9.07
        print("\nUsing: 20 lbs (9.07 kg)")
    
    input(f"\nPlace {known_weight_lbs} lbs on platform, then press ENTER...")
    
    print("Reading with weight...")
    time.sleep(1)
    
    weight_readings = []
    for i in range(10):
        val = hx.get_weight(5)
        weight_readings.append(val)
        print(f"  Reading {i+1}: {val:.1f}")
        time.sleep(0.3)
    
    weight_value = sum(weight_readings) / len(weight_readings)
    print(f"\nWeighted value: {weight_value:.1f}")
    
    # Calculate calibration factor
    print()
    print("STEP 3: CALCULATE CALIBRATION")
    print("-" * 60)
    
    raw_change = weight_value - tare_value
    calibration_factor = raw_change / known_weight_kg
    
    print(f"Raw change: {raw_change:.1f}")
    print(f"Known weight: {known_weight_kg} kg ({known_weight_lbs} lbs)")
    print(f"Calibration factor: {calibration_factor:.2f} units/kg")
    print()
    print(f"SAVE THIS NUMBER: {calibration_factor:.2f}")
    
    # Test it
    print()
    print("STEP 4: TEST CALIBRATION")
    print("-" * 60)
    input("Remove weight from platform, then press ENTER...")
    
    print("Testing empty platform...")
    time.sleep(1)
    val = hx.get_weight(5)
    weight_kg = (val - tare_value) / calibration_factor
    weight_lbs = weight_kg * 2.20462
    print(f"Raw: {val:.1f}")
    print(f"Weight: {weight_kg:.2f} kg ({weight_lbs:.2f} lbs)")
    print("Should be close to 0 kg")
    
    print()
    input(f"Place {known_weight_lbs} lbs back on platform, press ENTER...")
    
    print("Testing with weight...")
    time.sleep(1)
    val = hx.get_weight(5)
    weight_kg = (val - tare_value) / calibration_factor
    weight_lbs = weight_kg * 2.20462
    print(f"Raw: {val:.1f}")
    print(f"Weight: {weight_kg:.2f} kg ({weight_lbs:.2f} lbs)")
    print(f"Should be close to {known_weight_kg} kg ({known_weight_lbs} lbs)")
    
    # Save to file
    print()
    print("=" * 60)
    print("CALIBRATION COMPLETE!")
    print()
    print("Save these values:")
    print(f"  Tare (offset): {tare_value:.2f}")
    print(f"  Calibration factor: {calibration_factor:.2f}")
    print()
    
    with open("calibration_data.txt", "w") as f:
        f.write(f"Tare: {tare_value:.2f}\n")
        f.write(f"Calibration: {calibration_factor:.2f}\n")
    
    print("Values saved to: calibration_data.txt")

except KeyboardInterrupt:
    print("\n\nCalibration cancelled")
except Exception as e:
    print(f"\n\nError: {e}")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up")
