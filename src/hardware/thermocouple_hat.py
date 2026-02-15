#!/usr/bin/env python3
"""
Test script for Sequent Microsystems 8-Thermocouple HAT
Stack 0 - Reads temperature from thermocouples
"""

from sm_tc import SMtc
import time

def test_thermocouple_hat():
    """Test all 8 thermocouple channels on Stack 0"""
    
    stack = 0  # DIP switch setting
    
    print("=" * 60)
    print("8-Thermocouple HAT Test - Stack 0")
    print("=" * 60)
    print("Reading all 8 channels...")
    print("K-type thermocouples on channels 1 and 2")
    print("-" * 60)
    
    try:
        # Create thermocouple object
        tc = SMtc(stack)
        
        # Set channels 1 and 2 to K-type
        # _TC_TYPE_K = 3 (from the library constants)
        tc.set_sensor_type(1, 3)  # Channel 1 = K-type
        tc.set_sensor_type(2, 3)  # Channel 2 = K-type
        
        time.sleep(0.5)  # Wait for settings to apply
        
        # Read each channel
        for channel in range(1, 9):
            try:
                temp_c = tc.get_temp(channel)
                temp_f = (temp_c * 9/5) + 32
                
                if channel in [1, 2]:
                    print(f"Channel {channel} (K-type): {temp_c:.2f}°C ({temp_f:.2f}°F)")
                else:
                    print(f"Channel {channel}: {temp_c:.2f}°C (not configured)")
            except Exception as e:
                print(f"Channel {channel}: Error - {e}")
            
            time.sleep(0.2)
        
        print("\n" + "=" * 60)
        print("Test complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError during test: {e}")

if __name__ == "__main__":
    test_thermocouple_hat()
