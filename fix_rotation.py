#!/usr/bin/env python3
import subprocess
import time

while True:
    result = subprocess.run(['wlr-randr'], capture_output=True, text=True)
    if 'HDMI-A-2' in result.stdout:
        lines = result.stdout.split('\n')
        for i, line in enumerate(lines):
            if 'HDMI-A-2' in line:
                for j in range(i, min(i+20, len(lines))):
                    if 'Transform:' in lines[j]:
                        if 'Transform: 90' not in lines[j]:
                            subprocess.run(['wlr-randr', '--output', 'HDMI-A-2', '--transform', '90'])
                        break
    time.sleep(3)
