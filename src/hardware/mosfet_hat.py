#!/usr/bin/env python3
"""
Test script for Sequent Microsystems 8-MOSFET HAT
Stack 0 - Controls relays/solid-state switches
"""

import lib8mosind as mosfet
import time

def test_mosfet_hat():
    """Test all 8 MOSFET channels on Stack 0"""
    
    stack = 0  # DIP switch setting
    
    print("=" * 60)
    print("8-MOSFET HAT Test - Stack 0")
    print("=" * 60)
    print(f"Testing all 8 channels with 2 second intervals")
    print("Watch your test load on channel 5!")
    print("-" * 60)
    
    try:
        # Turn all channels OFF first
        print("Turning all channels OFF...")
        for channel in range(1, 9):
            mosfet.set(stack, channel, 0)
        time.sleep(1)
        
        # Test each channel individually
        for channel in range(1, 9):
            print(f"\nChannel {channel}: ON", end="", flush=True)
            if channel == 5:
                print(" <-- YOUR TEST LOAD!", end="", flush=True)
            mosfet.set(stack, channel, 1)
            time.sleep(2)
            
            print(f" -> OFF")
            mosfet.set(stack, channel, 0)
            time.sleep(0.5)
        
        print("\n" + "=" * 60)
        print("Test complete! All channels cycled successfully.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError during test: {e}")
        print("Turning all channels OFF for safety...")
        for channel in range(1, 9):
            try:
                mosfet.set(stack, channel, 0)
            except:
                pass

if __name__ == "__main__":
    test_mosfet_hat()
