#!/usr/bin/env python3

import argparse
import json
import os
from pydoc import TextRepr
import queue
import re
import sounddevice as sd
import vosk
import sys
import pyttsx3
#sintese de voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')    #getting details of current voice

def speak(text):
    engine.say(text)
    engine.runAndWait()

q = queue.Queue()

def int_or_str(text):
    """Função auxiliar para análise de argumentos."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    "" "Isso é chamado (de um tópico separado) para cada bloco de áudio." ""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "model"

    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # O SoundFile espera um int, Sounddevice fornece um float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
        

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    result = json.loads(result)

                    if result is not None:
                        text = result['text']
                        print(text)
                        speak(text)

                    print(result)
                
                if dump_fn is not None:
                    dump_fn.write(data)
                    print(rec)

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
    