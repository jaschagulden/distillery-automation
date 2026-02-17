#!/usr/bin/env python3
"""
Palmeri Assistant Avatar Display - Fullscreen
"""

import time
import subprocess
from PIL import Image

AVATARS = {
    'neutral': '/home/pi/distillery-automation/avatar_neutral.png',
    'happy': '/home/pi/distillery-automation/avatar_happy.png',
    'casual': '/home/pi/distillery-automation/avatar_casual.png',
    'pointing': '/home/pi/distillery-automation/avatar_pointing.png',
}

def resize_for_screen(img_path, output_path):
    """Resize image to fill 1024x600 screen"""
    img = Image.open(img_path)
    
    # Calculate scaling to fill screen while maintaining aspect ratio
    screen_w, screen_h = 1024, 600
    img_ratio = img.width / img.height
    screen_ratio = screen_w / screen_h
    
    if img_ratio > screen_ratio:
        # Image is wider - scale by height
        new_h = screen_h
        new_w = int(new_h * img_ratio)
    else:
        # Image is taller - scale by width
        new_w = screen_w
        new_h = int(new_w / img_ratio)
    
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Center crop to exact screen size
    left = (new_w - screen_w) // 2
    top = (new_h - screen_h) // 2
    img = img.crop((left, top, left + screen_w, top + screen_h))
    
    img.save(output_path, 'PNG')

def show_avatar(avatar_name):
    if avatar_name not in AVATARS:
        avatar_name = 'neutral'
    
    avatar_path = AVATARS[avatar_name]
    resized_path = f'/tmp/avatar_{avatar_name}_fullscreen.png'
    
    # Resize if not already done
    resize_for_screen(avatar_path, resized_path)
    
    try:
        subprocess.run(['pkill', '-f', 'feh'], stderr=subprocess.DEVNULL)
        time.sleep(0.1)
        
        subprocess.Popen(
            ['sudo', '-u', 'pi', 'feh', '--fullscreen', '--no-menus', resized_path],
            env={'DISPLAY': ':0', 'XAUTHORITY': '/home/pi/.Xauthority'}
        )
        print(f"Showing: {avatar_name} (fullscreen)")
    except Exception as e:
        print(f"Error: {e}")

print("Palmeri Assistant Avatar - Fullscreen Mode")
print("Press Ctrl+C to exit")

expressions = ['neutral', 'happy', 'casual', 'pointing']

try:
    while True:
        for expr in expressions:
            show_avatar(expr)
            time.sleep(3)
except KeyboardInterrupt:
    print("\nExiting...")
    subprocess.run(['pkill', '-f', 'feh'], stderr=subprocess.DEVNULL)
    print("Done!")
