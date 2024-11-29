# Frank Claverie
# CS 416
# Sounds - defines sound wave types for use in Musegen

from  Envr import *


'''
For all sound generators:

Input: 
    key -> MIDI note num
    dur -> duration of note relative to beat
        1.0 = Quarter note,
        0.5 = Eigth note, etc...
'''

def bell(key: int, dur: float = 1.0) -> np.array:
    f = 440 * 2 ** ((key - 69) / 12)
    b = int(beat_samples * dur)
    t = np.linspace(0, dur, b, endpoint=False)

    sine_wave = np.sin(2 * np.pi * f * t)
    partial1 = 0.5 * np.sin(2 * np.pi * 1.5 * f * t)  
    partial2 = 0.3 * np.sin(2 * np.pi * 2.7 * f * t)  
    partial3 = 0.2 * np.sin(2 * np.pi * 3.9 * f * t)  
    combined_wave = sine_wave + partial1 + partial2 + partial3

    attack = int(b * 0.02) 
    decay = int(b * 0.8)   
    sustain = b - attack - decay
    envelope = np.concatenate([
        np.linspace(0, 1, attack),      
        np.linspace(1, 0, decay),        
        np.zeros(sustain)               
    ])

    bell_wave = combined_wave * envelope
    return bell_wave


def string(key: int, dur: float = 1.0) -> np.array:
    f = 440 * 2 ** ((key - 69) / 12)
    b = int(beat_samples * dur)
    t = np.linspace(0, dur, b, endpoint=False)

    sine_wave = np.sin(2 * np.pi * f * t)
    overtones = 0.4 * np.sin(2 * np.pi * 2 * f * t) + 0.2 * np.sin(2 * np.pi * 3 * f * t)
    combined_wave = sine_wave + overtones

    attack = int(b * 0.05)
    decay = int(b * 0.15)
    sustain = b - attack - decay
    envelope = np.concatenate([
        np.linspace(0, 1, attack),         
        np.linspace(1, 0.5, decay),        
        np.full(sustain, 0.5)             
    ])

    string_wave = combined_wave * envelope
    return string_wave


def flute(key: int, dur: float = 1.0) -> np.array:
    f = 440 * 2 ** ((key - 69) / 12)
    b = int(beat_samples * dur)
    t = np.linspace(0, dur, b, endpoint=False)

    sine_wave = np.sin(2 * np.pi * f * t)

    attack = int(b * 0.1)  
    decay = int(b * 0.1)   
    sustain = b - attack - decay
    envelope = np.concatenate([
        np.linspace(0, 1, attack),         
        np.linspace(1, 0.8, decay),        
        np.full(sustain, 0.8)             
    ])


    vibrato = 0.01 * np.sin(2 * np.pi * 7 * t)
    flute_wave = sine_wave * envelope + vibrato
    return flute_wave

