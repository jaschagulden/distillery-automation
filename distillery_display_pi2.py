
#!/usr/bin/env python3
"""
Palmeri Distillery Display - Pi #2
Pulls sensor data from Pi #1 and displays on round screen
"""

from PIL import Image, ImageDraw, ImageFont
from GC9A01 import GC9A01
import requests
import time

# Pi #1 data server
PI1_URL = "http://192.168.0.31:5000/sensors"

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

# Colors
BLACK = (0, 0, 0)
ORANGE = (255, 140, 0)
RED = (255, 0, 0)

def create_data_screen(label, value, unit):
    img = Image.new('RGB', (240, 240), color=BLACK)
    draw = ImageDraw.Draw(img)
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    label_bbox = draw.textbbox((0, 0), label, font=font_small)
    label_width = label_bbox[2] - label_bbox[0]
    draw.text(((240 - label_width) // 2, 40), label, fill=ORANGE, font=font_small)
    value_text = str(value)
    value_bbox = draw.textbbox((0, 0), value_text, font=font_large)
    value_width = value_bbox[2] - value_bbox[0]
    draw.text(((240 - value_width) // 2, 90), value_text, fill=ORANGE, font=font_large)
    unit_bbox = draw.textbbox((0, 0), unit, font=font_medium)
    unit_width = unit_bbox[2] - unit_bbox[0]
    draw.text(((240 - unit_width) // 2, 165), unit, fill=ORANGE, font=font_medium)
    return img

def create_error_screen():
    img = Image.new('RGB', (240, 240), color=BLACK)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()
    draw.text((60, 90), "NO DATA", fill=RED, font=font)
    draw.text((40, 130), "Pi #1 offline?", fill=RED, font=font)
    return img

def fade_transition(img1, img2, steps=10):
    for i in range(steps + 1):
        alpha = i / steps
        blended = Image.blend(img1, img2, alpha)
        disp.display(blended)
        time.sleep(0.05)

print("Palmeri Distillery Display - Pi #2")
print(f"Pulling data from: {PI1_URL}")
print("Press Ctrl+C to exit")

current_screen = Image.new('RGB', (240, 240), color=BLACK)
disp.display(current_screen)

screens = ['temp1', 'temp2', 'weight']
screen_index = 0

try:
    while True:
        try:
            response = requests.get(PI1_URL, timeout=3)
            data = response.json()
            temp1_f = round(data.get('temp1_f', 0))
            temp2_f = round(data.get('temp2_f', 0))
            weight_lb = data.get('weight_lb', 0)
            screen_map = {
                'temp1': create_data_screen("TEMP 1", temp1_f, "°F"),
                'temp2': create_data_screen("TEMP 2", temp2_f, "°F"),
                'weight': create_data_screen("WEIGHT", f"{weight_lb:.1f}", "LBS"),
            }
            new_screen = screen_map[screens[screen_index]]
        except Exception as e:
            print(f"Error fetching data: {e}")
            new_screen = create_error_screen()

        fade_transition(current_screen, new_screen)
        current_screen = new_screen

        start_time = time.time()
        while time.time() - start_time < 3:
            try:
                response = requests.get(PI1_URL, timeout=3)
                data = response.json()
                temp1_f = round(data.get('temp1_f', 0))
                temp2_f = round(data.get('temp2_f', 0))
                weight_lb = data.get('weight_lb', 0)
                screen_map = {
                    'temp1': create_data_screen("TEMP 1", temp1_f, "°F"),
                    'temp2': create_data_screen("TEMP 2", temp2_f, "°F"),
                    'weight': create_data_screen("WEIGHT", f"{weight_lb:.1f}", "LBS"),
                }
                current_screen = screen_map[screens[screen_index]]
                disp.display(current_screen)
            except:
                pass
            time.sleep(0.5)

        screen_index = (screen_index + 1) % len(screens)

except KeyboardInterrupt:
    print("\nExiting...")
    blank = Image.new('RGB', (240, 240), color=BLACK)
    disp.display(blank)
    print("Done!")
