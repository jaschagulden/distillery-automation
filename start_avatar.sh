#!/bin/bash
export HOME=/home/pi
export XDG_RUNTIME_DIR=/run/user/1000

cage -- bash -c 'wlr-randr --output HDMI-A-2 --transform 90 && python3 /home/pi/palmeri-ai/avatar_display.py'
```

Save with `Ctrl+O`, `Enter`, `Ctrl+X`. Then make it executable:
```
chmod +x ~/palmeri-ai/start_avatar.sh
