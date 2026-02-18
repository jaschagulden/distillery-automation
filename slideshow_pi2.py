#!/usr/bin/env python3
import requests
import random
import time
import threading
import subprocess
import os
from PIL import Image
from GC9A01 import GC9A01
from io import BytesIO

# Wait for desktop to be ready on boot
time.sleep(15)

BASE_IMAGES = [
    "https://static.wixstatic.com/media/9f3037c83ca048ddb0485e3badb0a6a3.jpg",
    "https://static.wixstatic.com/media/b48252_7f03fc74080c412da82778e270ef053a~mv2.jpg",
    "https://static.wixstatic.com/media/d0b656e8f10a40b696305e49240d773c.jpg",
    "https://static.wixstatic.com/media/b48252_54a8f3b80bbd478897043b7d5c063ef0~mv2.png",
    "https://static.wixstatic.com/media/b48252_538e7cd7de2f424a9c80503f1887cdfe~mv2.png",
    "https://static.wixstatic.com/media/b48252_af7ef6a2b3c94556a03f5d32005f1104~mv2.jpg",
]

disp = GC9A01(port=0, cs=0, dc=25, rst=24, backlight=None,
              spi_speed_hz=80000000, width=240, height=240)
disp.begin()

def download_image(url):
    try:
        base_url = url.split('/v1/')[0]
        high_res_url = base_url + "/v1/fill/w_1200,h_800,al_c,q_90/image.jpg"
        response = requests.get(high_res_url, timeout=10)
        if response.status_code != 200:
            response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content)).convert('RGB')
        return img
    except Exception as e:
        print(f"Download error: {e}")
        return None

def prepare_round(img):
    w, h = img.size
    size = min(w, h)
    left = (w - size) // 2
    top = (h - size) // 2
    img = img.crop((left, top, left + size, top + size))
    return img.resize((240, 240), Image.Resampling.LANCZOS)

def prepare_hdmi(img, sw, sh):
    ir = img.width / img.height
    sr = sw / sh
    if ir > sr:
        nh = sh
        nw = int(nh * ir)
    else:
        nw = sw
        nh = int(nw / ir)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - sw) // 2
    top = (nh - sh) // 2
    return img.crop((left, top, left + sw, top + sh))

def show_hdmi(path):
    try:
        subprocess.Popen(
            ['feh', '--fullscreen', '--auto-zoom', '--hide-pointer', '--no-menus', '--reload', '1', path],
            env={
                'DISPLAY': ':0',
                'XAUTHORITY': '/home/pi/.Xauthority',
                'HOME': '/home/pi',
                'PATH': '/usr/bin:/bin'
            }
        )
    except Exception as e:
        print(f"HDMI error: {e}")

def fade(img1, img2, steps=15):
    for i in range(steps + 1):
        alpha = i / steps
        blended = Image.blend(img1, img2, alpha)
        disp.display(blended)
        time.sleep(0.05)

os.makedirs('/tmp/distillery_images', exist_ok=True)

print("Palmeri Slideshow - Pi #2")

current = Image.new('RGB', (240, 240), (0, 0, 0))
disp.display(current)

hdmi_path = '/tmp/distillery_images/current_pi2.jpg'
blank = Image.new('RGB', (800, 480), (0, 0, 0))
blank.save(hdmi_path, 'JPEG')
show_hdmi(hdmi_path)
time.sleep(1)

print("Pre-loading first images...")
url_round = random.choice(BASE_IMAGES)
url_hdmi = random.choice([u for u in BASE_IMAGES if u != url_round])
next_round = download_image(url_round)
next_hdmi = download_image(url_hdmi)

while True:
    img_round = next_round
    img_hdmi = next_hdmi

    next_round = [None]
    next_hdmi = [None]
    next_url_round = random.choice(BASE_IMAGES)
    next_url_hdmi = random.choice([u for u in BASE_IMAGES if u != next_url_round])

    def prefetch(ur=next_url_round, uh=next_url_hdmi):
        next_round[0] = download_image(ur)
        next_hdmi[0] = download_image(uh)

    prefetch_thread = threading.Thread(target=prefetch, daemon=True)
    prefetch_thread.start()

    if img_round and img_hdmi:
        round_img = prepare_round(img_round)
        hdmi_img = prepare_hdmi(img_hdmi, 800, 480)
        hdmi_img.save(hdmi_path, 'JPEG', quality=90)

        fade(current, round_img)
        current = round_img
        print("Displaying 30s...")
        time.sleep(30)
    else:
        time.sleep(5)

    prefetch_thread.join(timeout=5)
    next_round = next_round[0] or download_image(random.choice(BASE_IMAGES))
    next_hdmi = next_hdmi[0] or download_image(random.choice(BASE_IMAGES))
