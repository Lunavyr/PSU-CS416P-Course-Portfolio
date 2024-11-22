# Frank Claverie
# CS 358 Fall 2024
# Full Fledged Synthesizer. 
'''
Future Features:
Wavetable synth (that eventually will modulate between wave types)
Some kind of effects (reverb would be a good start)
    Compression? - easy and uses filters
Adjustable attack and decay
Adjustable gain
'''

import mido
import sounddevice as sd
import numpy as np

'''
Plan:
* Global sound buffer
* Generate base wavetable for sound generation.
* Wavetable crossfade function
*   Maybe wavetable as a class (could generate a dict of predefined wave phases for each wave type)
*   Maybe crossfade with osc num of params and use them to control filters applied to all waves
        then add together
*   Maybe choose between two 

* Abstract a Note as a class
    Holds info about note_on, note_off, freq, phase, gain, attack, release
        and functions to manipulate them
        * maybe also data and functions for pitch bending and modulation - we'll see

    Maybe I can also include functions to establish delay, but might be easier in 
        output callback function or as logic in the note class

* Midi handler function (maybe pass as a callback func?)
* Midi to freq function
* Audio output callback function
'''
# Globals
sample_rate = 96000
block_size = 32


# Waveform functions:
#   *Must all have same interface

def sine():
    pass
def square():
    pass
def additive_wave():
    pass
def tbd():
    pass
# Samples parts from the above to make some funky biz
def wavetable():
    pass
def sample_time():
    pass

# This might allow me to parallelize for stereo use
class Oscillator:
    def __init__(self):
        self.waves = [
            sine #, etc
        ]
        self.fade_params = [
            0 # between 0 and 1
        ]
    def _init_wavetable():
        pass
    def get_samples():
        # _gen_waveform()
        pass
    def _gen_waveform():
        pass


    def cross_fade():
        pass


oscillator = Oscillator()


def key_to_freq(key):
    pass

class Note:
    def __init__(self, key, osc, attack=0.02, decay=0.1, sustain=0.7, release=0.1):
        self.frequency = key_to_freq(key)
        self.attack_remaining = attack
        self.decay_remaining = decay
        self.sustain = sustain
        self.release_remaining = None
        self.attack_complete = False
        self.playing = True
        self.out_osc = oscillator

    def gen_samples(self, t, frame_count):
        pass   

    def release(self):
        pass

    def apply_adsr_envelope(self, t, frame_count):
        envelope = np.ones(frame_count)  # Default to full volume
        
        if not self.attack_complete:
            pass
        elif self.attack_complete and self.decay_time_remaining > 0:
            pass
        elif self.decay_time_remaining <= 0 and self.release_time_remaining is None:
            pass
        elif self.release_time_remaining is not None:
            pass

        return envelope


def midi_handler():
    pass



def audio_callback():
    pass



def main():
    pass

if __name__ == "__main__":
    main

