#!/bin/bash
export XDG_RUNTIME_DIR=/run/user/1000
export WAYLAND_DISPLAY=wayland-0

# Fix display rotation
wlr-randr --output HDMI-A-2 --transform 90

# Start voice pipeline after delay
(sleep 30 && nohup python3 -u /home/pi/palmeri-ai/voice_pipeline.py >> /tmp/voice.log 2>&1 < /dev/null) &

# Loop avatar display
while true; do
    python3 /home/pi/palmeri-ai/avatar_display.py >> /tmp/avatar.log 2>&1
    sleep 2
done
