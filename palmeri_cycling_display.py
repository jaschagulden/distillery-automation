#!/usr/bin/env python3
"""
Palmeri Distillery Cycling Display
Shows: Logo -> Temp 1 -> Temp 2 -> Weight -> Loop
With smooth fade transitions
"""

from PIL import Image, ImageDraw, ImageFont
from GC9A01 import GC9A01
from hx711 import HX711
import sm_tc
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

# Initialize HX711 load cells
hx = HX711(5, 6)
hx.reset()
hx.set_reading_format("MSB", "MSB")

# Load calibration
TARE = -241007.50
CALIBRATION = -25651.61
try:
    with open('calibration_data.txt', 'r') as f:
        tare_line = f.readline().strip()
        cal_line = f.readline().strip()
        TARE = float(tare_line.split(':')[1].strip())
        CALIBRATION = float(cal_line.split(':')[1].strip())
except:
    pass

# Initialize thermocouples
tc_hat = sm_tc.SMtc(0)
tc_hat.set_sensor_type(1, 3)  # K-type
tc_hat.set_sensor_type(2, 3)  # K-type

# Colors
BLACK = (0, 0, 0)
ORANGE = (255, 140, 0)  # Bright orange

def create_logo_screen():
    """Create logo screen"""
    logo = Image.open('palmeri_logo.png')
    orig_width, orig_height = logo.size
    scale = min(220/orig_width, 220/orig_height)
    new_width = int(orig_width * scale)
    new_height = int(orig_height * scale)
    logo = logo.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    img = Image.new('RGB', (240, 240), color=BLACK)
    x_offset = (240 - new_width) // 2
    y_offset = (240 - new_height) // 2
    img.paste(logo, (x_offset, y_offset))
    return img.convert('RGB')

def create_data_screen(label, value, unit):
    """Create data screen with large orange text"""
    img = Image.new('RGB', (240, 240), color=BLACK)
    draw = ImageDraw.Draw(img)
    
    # Try to use a larger font, fallback to default if not available
    try:
        # Use large font for value
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw label at top
    label_bbox = draw.textbbox((0, 0), label, font=font_small)
    label_width = label_bbox[2] - label_bbox[0]
    draw.text(((240 - label_width) // 2, 40), label, fill=ORANGE, font=font_small)
    
    # Draw value in center (large)
    value_text = str(value)
    value_bbox = draw.textbbox((0, 0), value_text, font=font_large)
    value_width = value_bbox[2] - value_bbox[0]
    draw.text(((240 - value_width) // 2, 90), value_text, fill=ORANGE, font=font_large)
    
    # Draw unit below value
    unit_bbox = draw.textbbox((0, 0), unit, font=font_medium)
    unit_width = unit_bbox[2] - unit_bbox[0]
    draw.text(((240 - unit_width) // 2, 165), unit, fill=ORANGE, font=font_medium)
    
    return img

def fade_transition(img1, img2, steps=10):
    """Smooth fade from img1 to img2"""
    for i in range(steps + 1):
        alpha = i / steps
        # Blend images
        blended = Image.blend(img1, img2, alpha)
        disp.display(blended)
        time.sleep(0.05)  # Fast fade

print("Palmeri Distillery Cycling Display Started!")
print("Press Ctrl+C to exit")

try:
    logo_screen = create_logo_screen()
    
    while True:
        # === LOGO - Static for 3 seconds ===
        disp.display(logo_screen)
        time.sleep(3)
        
        # === TEMP 1 - Live updates for 3 seconds ===
        start_time = time.time()
        temp1_screen = None
        while time.time() - start_time < 3:
            try:
                temp1_c = tc_hat.get_temp(1)
                temp1_f = int((temp1_c * 9/5) + 32)
            except:
                temp1_f = 0
            
            new_temp1 = create_data_screen("TEMP 1", temp1_f, "°F")
            if temp1_screen is None:
                # First time - fade from logo
                fade_transition(logo_screen, new_temp1)
            else:
                # Just update (no fade)
                disp.display(new_temp1)
            temp1_screen = new_temp1
            time.sleep(0.5)  # Update twice per second
        
        # === TEMP 2 - Live updates for 3 seconds ===
        start_time = time.time()
        temp2_screen = None
        while time.time() - start_time < 3:
            try:
                temp2_c = tc_hat.get_temp(2)
                temp2_f = int((temp2_c * 9/5) + 32)
            except:
                temp2_f = 0
            
            new_temp2 = create_data_screen("TEMP 2", temp2_f, "°F")
            if temp2_screen is None:
                # First time - fade from temp1
                fade_transition(temp1_screen, new_temp2)
            else:
                disp.display(new_temp2)
            temp2_screen = new_temp2
            time.sleep(0.5)
        
        # === WEIGHT - Live updates for 3 seconds ===
        start_time = time.time()
        weight_screen = None
        while time.time() - start_time < 3:
            try:
                raw = hx.get_weight(5)
                weight_kg = (raw - TARE) / CALIBRATION
                weight_lb = weight_kg * 2.20462
            except:
                weight_lb = 0
            
            new_weight = create_data_screen("WEIGHT", f"{weight_lb:.1f}", "LBS")
            if weight_screen is None:
                # First time - fade from temp2
                fade_transition(temp2_screen, new_weight)
            else:
                disp.display(new_weight)
            weight_screen = new_weight
            time.sleep(0.5)  # Update twice per second
        
        # Fade back to logo
        fade_transition(weight_screen, logo_screen)

except KeyboardInterrupt:
    print("\nExiting...")
    blank = Image.new('RGB', (240, 240), color=BLACK)
    disp.display(blank)
    print("Display cleared")
