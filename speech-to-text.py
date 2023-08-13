#!/usr/bin/env python3

import sounddevice as sd
import queue
import json
import logging
import argparse

from vosk import Model, KaldiRecognizer, SetLogLevel

SAMPLE_RATE=44100
CHANNELS=1


def transcribe(device, language):    
    q = queue.Queue()
    def write_callback(data, frames, time, status):
        q.put(bytes(data))

    model = Model(lang=language)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)

    try:
        with sd.RawInputStream(device=device,channels=CHANNELS,samplerate=SAMPLE_RATE,dtype="int16",callback=write_callback):
            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result["text"]
                    if "" != text:
                        print(text)
    except KeyboardInterrupt:
        pass

def main():
    SetLogLevel(-1)

    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--device", type=int, required=False, default=None)
    parser.add_argument("-l","--language", type=str, required=False, default="de")
    args = parser.parse_args()
    transcribe(args.device, args.language)

if __name__ == "__main__":
    main()
