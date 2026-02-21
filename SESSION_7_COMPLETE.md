# Session 7 Complete - February 20, 2026

## Status: Voice AI Pipeline Built, Integration In Progress

---

## Pi 3 (palmeri-ai - 192.168.0.33) - AI Avatar Kiosk

### Hardware Confirmed Working
- Raspberry Pi 5 (8GB)
- AI HAT+ (13 TOPS Hailo-8L)
- 10.1" portrait touchscreen (HDMI-A-2, 1024x600, rotated 90 degrees)
- USB PnP Audio Device (card 2) - mic and speaker both working
- PipeWire audio server managing audio

### Software Installed
- Ollama + gemma2:2b model (1.6GB, running on CPU)
- faster-whisper (base.en model, speech to text)
- piper-tts (text to speech)
- sounddevice + numpy (audio recording)
- Amy voice: ~/piper-voices/en_US-amy-medium.onnx (woman/farm)
- Norman voice: ~/piper-voices/en_US-norman-medium.onnx (man/distillery)

### Files on Pi 3
- ~/palmeri-ai/avatar_display.py - pygame kiosk display (working)
- ~/palmeri-ai/voice_pipeline.py - full voice AI pipeline (working)
- ~/.bash_profile - auto-starts cage + avatar + voice on boot
- ~/piper_test.py - TTS test script
- ~/whisper_test.py - STT test script

### Avatar Display
- Two American Gothic avatars side by side
- Woman (left) = Farm/Garden, speaks with Amy voice
- Man (right) = Distillery, speaks with Norman voice
- Runs via cage/Wayland with wlr-randr rotation
- Auto-restarts if cage crashes (while loop in bash_profile)

### Voice Pipeline (voice_pipeline.py)
- Continuously listens for speech
- Records until silence (2 second silence timeout)
- Transcribes with faster-whisper
- Sends to gemma2:2b via Ollama with Palmeri persona
- Amy says "Let me think about that" while LLM processes
- Norman speaks the response
- Loops back to listening

### Palmeri AI Persona (System Prompt)
- Amy knows: farm, agave, botanicals, garden
- Norman knows: distilling, whiskey, rum, gin, spirits
- Answers in 2-3 sentences for spoken delivery
- No bullet points or markdown (speech optimized)

### Current bash_profile
```bash
if [ "$(tty)" = "/dev/tty1" ]; then
    export XDG_RUNTIME_DIR=/run/user/1000
    sleep 10 && python3 /home/pi/palmeri-ai/voice_pipeline.py >> /tmp/voice.log 2>&1 &
    while true; do
        cage -- bash -c 'wlr-randr --output HDMI-A-2 --transform 90 && sleep 0.5 && python3 /home/pi/palmeri-ai/avatar_display.py'
        sleep 2
    done
fi
```

### Known Issue - Display Rotation
- Plugging in USB devices can disrupt cage and rotate display
- Fix: sudo reboot (auto-restores on boot)
- Voice pipeline has SDL_VIDEODRIVER=dummy to prevent display conflicts

### Audio Device Reference
- Card 2: USB PnP Audio Device
- Use pw-play for playback (PipeWire)
- Use pw-record for recording
- Speaker volume: 80%, Mic capture: 100%

---

## Next Steps for Session 8

1. Verify voice pipeline + display run stably together after reboot
2. Add avatar expression states (listening/thinking/speaking visual feedback)
3. Add wake word detection (so it only listens when triggered)
4. Connect to Pi 1 sensor data (voice can answer "what is the temperature?")
5. Push all Pi 3 files to GitHub

---

## Quick Reference - Pi 3

**SSH:**
```bash
ssh pi@192.168.0.33
```

**Check voice pipeline running:**
```bash
ps aux | grep voice_pipeline
cat /tmp/voice.log
```

**Restart voice pipeline manually:**
```bash
python3 ~/palmeri-ai/voice_pipeline.py
```

**Fix rotated display:**
```bash
sudo reboot
```

**Test audio:**
```bash
pw-play /tmp/amy_test.wav
pw-record --target=alsa_input.usb-Generic_USB_PnP_Audio_Device-00.mono-fallback /tmp/test.wav
```

---

**For Next Session say:**
Claude - Palmeri Distillery project.
Read https://jaschagulden.github.io/distillery-automation/SESSION_7_COMPLETE
Pi 3 (192.168.0.33, palmeri-ai) has voice AI pipeline built.
Ready to test stable boot and add avatar expression states.

---

**Project Owner:** Jascha Gulden
**Date:** February 20, 2026
**Project Progress:** ~70% complete
**Next Milestone:** Stable voice AI kiosk with animated avatar expressions
