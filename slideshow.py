#!/usr/bin/env python3
"""
Palmeri Distillery Website Slideshow - Pi #1
"""

import requests
import random
import time
import re
import threading
from PIL import Image
from GC9A01 import GC9A01
from io import BytesIO
from flask import Flask, send_file, jsonify
import subprocess
import os

app = Flask(__name__)

disp = GC9A01(port=0, cs=0, dc=25, rst=24, backlight=None, 
              spi_speed_hz=80000000, width=240, height=240)
disp.begin()

current_image_path = None
current_image_lock = threading.Lock()
feh_process = None

BASE_IMAGES = [
    "https://static.wixstatic.com/media/9f3037c83ca048ddb0485e3badb0a6a3.jpg",
    "https://static.wixstatic.com/media/b48252_7f03fc74080c412da82778e270ef053a~mv2.jpg",
    "https://static.wixstatic.com/media/d0b656e8f10a40b696305e49240d773c.jpg",
    "https://static.wixstatic.com/media/b48252_54a8f3b80bbd478897043b7d5c063ef0~mv2.png",
    "https://static.wixstatic.com/media/b48252_538e7cd7de2f424a9c80503f1887cdfe~mv2.png",
    "https://static.wixstatic.com/media/b48252_af7ef6a2b3c94556a03f5d32005f1104~mv2.jpg",
]

def fetch_fresh_images():
    try:
        response = requests.get("https://www.palmeridistillery.com", timeout=10)
        urls = re.findall(r'https://static\.wixstatic\.com/media/[a-zA-Z0-9_~]+(?:~mv2)?\.(?:jpg|jpeg|png|webp)', response.text)
        unique = list(set(urls))
        if len(unique) > 3:
            print(f"Refreshed: {len(unique)} images")
            return unique
    except:
        pass
    return BASE_IMAGES

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
    global feh_process
    try:
        if feh_process:
            try:
                feh_process.terminate()
            except:
                pass
        
        subprocess.run(['pkill', '-f', 'feh.*current.jpg'], stderr=subprocess.DEVNULL)
        time.sleep(0.1)
        
        feh_process = subprocess.Popen(
            ['sudo', '-u', 'pi', 'feh', '--fullscreen', '--auto-zoom', 
             '--hide-pointer', '--no-menus', '--reload', '1', path],
            env={'DISPLAY': ':0', 'XAUTHORITY': '/home/pi/.Xauthority'}
        )
    except Exception as e:
        print(f"HDMI error: {e}")

def fade(img1, img2, steps=15):
    for i in range(steps + 1):
        alpha = i / steps
        blended = Image.blend(img1, img2, alpha)
        disp.display(blended)
        time.sleep(0.05)

@app.route('/current_image')
def current_image():
    with current_image_lock:
        if current_image_path and os.path.exists(current_image_path):
            return send_file(current_image_path, mimetype='image/jpeg')
    return jsonify({"error": "no image"}), 404

@app.route('/status')
def status():
    return jsonify({"status": "online", "pi": "distillery-pi-1"})

def run_flask():
    app.run(host='0.0.0.0', port=5001, use_reloader=False)

def run_slideshow():
    global current_image_path
    os.makedirs('/tmp/distillery_images', exist_ok=True)
    
    print("Palmeri Slideshow - Pi #1")
    image_urls = fetch_fresh_images()
    print(f"Found {len(image_urls)} images")
    
    current = Image.new('RGB', (240, 240), (0, 0, 0))
    disp.display(current)
    last_refresh = time.time()
    
    # Start feh once at beginning
    hdmi_path = '/tmp/distillery_images/current.jpg'
    blank = Image.new('RGB', (1024, 600), (0, 0, 0))
    blank.save(hdmi_path, 'JPEG')
    show_hdmi(hdmi_path)
    time.sleep(1)
    
    while True:
        if time.time() - last_refresh > 600:
            image_urls = fetch_fresh_images()
            last_refresh = time.time()
        
        url_round = random.choice(image_urls)
        url_hdmi = random.choice([u for u in image_urls if u != url_round])
        
        print("Loading...")
        img_round = download_image(url_round)
        img_hdmi = download_image(url_hdmi)
        
        if img_round and img_hdmi:
            round_img = prepare_round(img_round)
            hdmi_img = prepare_hdmi(img_hdmi, 1024, 600)
            
            # Save HDMI image - feh will auto-reload it
            hdmi_img.save(hdmi_path, 'JPEG', quality=90)
            
            with current_image_lock:
                current_image_path = hdmi_path
            
            # Round display fade
            fade(current, round_img)
            current = round_img
            
            print("Displaying 30s...")
            time.sleep(30)
        else:
            time.sleep(5)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("Image server: port 5001")
    
    try:
        run_slideshow()
    except KeyboardInterrupt:
        print("\nExiting...")
        blank = Image.new('RGB', (240, 240), (0, 0, 0))
        disp.display(blank)
        if feh_process:
            feh_process.terminate()
