# This module contains the voice recorder for Nick

from pvrecorder import PvRecorder
import wave
import struct
import os



def record():
    recorder = PvRecorder(device_index=-1, frame_length=512)
    audio = []

    try:
        recorder.start()
        dead_frames = []
        while True:
            frame = recorder.read()
            if max(frame) > 9999:
                print(int(max(frame)/5000) * "*")
                dead_frames = []
            else:
                dead_frames.append(frame)
                if len(dead_frames)> 50:
                    recorder.stop()
                    # audio = [i for i in audio if i not in dead_frames]
                    with wave.open("output.mp3", 'w') as f:
                        f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
                        f.writeframes(struct.pack("h" * len(audio), *audio))
                        break  
            audio.extend(frame)      
            
    finally:
        recorder.delete()



