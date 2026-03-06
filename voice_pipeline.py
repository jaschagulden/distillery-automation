#!/usr/bin/env python3
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['DISPLAY'] = ''
import sounddevice as sd
import numpy as np
import subprocess
import time
from faster_whisper import WhisperModel
from elevenlabs.client import ElevenLabs
from elevenlabs import save

SAMPLE_RATE = 16000
SILENCE_THRESHOLD = 0.01
SILENCE_SECONDS = 2
MAX_RECORD_SECONDS = 15

ELEVENLABS_API_KEY = 'sk_3db5fdeb8cd4066a8df61af1b75877bc8c3e46bf2e5a7027'
NAN_VOICE_ID = 'd3MFdIuCfbAIwiu7jC4a'
DOC_VOICE_ID = '0dPqNXnhg2bmxQv1WKDp'

SYSTEM_PROMPT = """You are the Palmeri Distillery and Agave Farm assistant.
Nan knows about the farm, agave, botanicals, and garden.
Doc knows about distilling, whiskey, rum, gin, and spirits.
Keep answers to 2-3 sentences for spoken delivery.
Never use bullet points or markdown. You are speaking aloud."""

import ollama

print("Loading Whisper...")
whisper = WhisperModel("base.en", device="cpu", compute_type="int8")
print("Connecting to ElevenLabs...")
eleven = ElevenLabs(api_key=ELEVENLABS_API_KEY)
print("All models loaded!")

def speak(text, voice_id):
    print("SPEAK: calling ElevenLabs API...")
    audio = eleven.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id="eleven_turbo_v2"
    )
    print("SPEAK: saving MP3...")
    save(audio, '/tmp/palmeri_speech.mp3')
    print("SPEAK: playing audio...")
    subprocess.run(['mpg123', '-q', '-a', 'hw:2,0', '/tmp/palmeri_speech.mp3'])
    print("SPEAK: done.")

def record_until_silence():
    print("Listening...")
    chunks = []
    silent_chunks = 0
    chunk_size = int(SAMPLE_RATE * 0.1)
    max_chunks = int(MAX_RECORD_SECONDS / 0.1)
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32') as stream:
        for _ in range(max_chunks):
            chunk, _ = stream.read(chunk_size)
            chunks.append(chunk.copy())
            volume = np.abs(chunk).mean()
            if volume < SILENCE_THRESHOLD:
                silent_chunks += 1
            else:
                silent_chunks = 0
            if silent_chunks > int(SILENCE_SECONDS / 0.1) and len(chunks) > 10:
                break
    return np.concatenate(chunks).flatten()

def transcribe(audio):
    segments, _ = whisper.transcribe(audio, beam_size=5)
    return " ".join([seg.text for seg in segments]).strip()

def ask_llm(question):
    response = ollama.chat(
        model='gemma2:2b',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': question}
        ]
    )
    return response['message']['content']

def main():
    speak("Hello! I'm Nan. Doc and I are here to help with anything on the farm or in the distillery.", NAN_VOICE_ID)
    while True:
        print("\nListening... (Ctrl+C to exit)")
        audio = record_until_silence()
        if len(audio) < SAMPLE_RATE:
            continue
        print("Transcribing...")
        text = transcribe(audio)
        if not text or len(text.strip()) < 3:
            continue
        print(f"You said: {text}")
        subprocess.run(['mpg123', '-q', '-a', 'hw:2,0', '/home/pi/palmeri-ai/thinking.mp3'])
        print("Asking LLM...")
        response = ask_llm(text)
        print(f"Response: {response}")
        speak(response, DOC_VOICE_ID)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
