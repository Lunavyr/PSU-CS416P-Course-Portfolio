# Frank Claverie
# CS 358 Fall 2024
# Wavetable Synthesizer. 



import mido
import sounddevice as sd
import numpy as np
import math
import queue



''' Globals '''
log_events = False
log_unhandled_events = True
debug = True

# System settings
sample_rate = 96000
block_size = 32
#   Want to try and get stereo working eventually
channels = 1

# Sound settings
base_freq = 437
max_amplitude = 0.5
attack = 0.5
decay = 0.5
sustain = 0.5
release = 0.5

# Buffers for managing Midi events and sound generation
#   Queue allows us to gurantee atomic process for midi event and audio callback handling
midi_q = queue.SimpleQueue()
note_buffer = dict()
notes_to_play = dict()
notes_to_remove = dict()


''' Sound generation '''
# Waveform functions:
def string(freq):
    period = math.ceil(sample_rate/freq)
    time = np.linspace(0, 1, period, dtype=np.float32)
    phase_slice = np.sin(2 * np.pi * freq * time) + 0.4 * np.sin(2 * np.pi * 2 * freq * time) + 0.2 * np.sin(2 * np.pi * 3 * freq * time) + 0.1 * np.sin(2 * np.pi * 4 * freq * time)
    return max_amplitude * phase_slice

# We like amount of freq transients (will oscillate filter around this)
def saw(freq):
    period = math.ceil(sample_rate/freq)
    time = np.linspace(0, 1, period, dtype=np.float32)
    phase_slice = 2 * (time * freq - np.floor(0.5 + time * freq))
    return max_amplitude * phase_slice


# Wavetables for string and saw (populated with midi note values between 0-127)
string_table = dict()
saw_table = dict()

# Controls the generation of sound frames
class Oscillator:
    def __init__(self):
        self._populate_tables()
        self.wavetables = [
            string_table,
            saw_table
        ]
        self.fade_params = [
            0 # between 0 and 1
        ]
    def _populate_tables(self):
        pass
    def _init_wavetable(self):
        pass

    def get_samples(self):
        # _gen_waveform()
        pass
    def _gen_waveform(self):
        pass

    def cross_fade(self):
        pass


oscillator = Oscillator()


# Interface between midi and sound generation
class Note:
    def __init__(self, key, osc, attack=0.02, decay=0.1, sustain=0.7, release=0.1):
        global oscillator

        self.frequency = self._key_to_freq(key)
        self.attack_remaining = attack
        self.decay_remaining = decay
        self.sustain = sustain
        self.release_remaining = None
        self.attack_complete = False
        self.playing = True
        self.out_osc = oscillator

    def _key_to_freq(self, key):
        pass

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



''' Midi connection/input functions '''
# Presently connects to first listed midi device
#   Might add dynamic processing, but this works for me for now
def connect_device():
    port_names = mido.get_input_names()
    if not port_names:
        print("No MIDI input ports found.")
        exit()
    port = port_names[0]

    try:
        midi_device = mido.open_input(port)
        print(f"Listening to MIDI input: {midi_device}")
        print("   * Press \"Stop\" button on midi controller to exit.")
    except Exception as e:
        print(f"error: {e}")
        exit()

    return midi_device

# Listens for midi events and passes it to midi queue for processing
def process_midi(device_port):
    global midi_q
    for msg in device_port:
        if log_events:
            print(msg)
        if msg.type == "stop":
            print("\t=== Stop entered: shutting down. ===")
            return False
        else:
            midi_q.put(msg)
            return True

            


''' Audio functions '''
# Pulls midi from queue and parses
#   Helper function for audio_callback()
def _parse_midi(message):
    global midi_q, note_buffer, notes_to_play, notes_to_remove
    
    msg_type = message.type
    # Handles midi encoding for note_off = note_on: vel=0
    if msg_type == "note_on" and message.velocity ==0:
        msg_type = "note_off"

    match msg_type:
        case "note_on":
            print("on")
        case "note_off":
            print("off")
        case "control_change":
            print("control")

        case _:
            if log_unhandled_events:
                print(f"\t*Command \"{msg_type}\" not implemented")

# Audio callback - processes sound generation
#   To be passed to sounddevice.OuputStream()
def audio_callback(out_data, frame_count, time_info, status):
    global midi_q, note_buffer, notes_to_play, notes_to_remove

    # Required - critical error involving underflow
    #   Apparently due to slow sample generation
    if status:
        print("output callback:", status)

    # Process midi events
    while not midi_q.empty():
        msg = midi_q.get()
        _parse_midi(msg)

    # Generate sounds



def main():
    midi_device = connect_device()

    # Start output stream and loop through 
    with sd.OutputStream(
        samplerate=sample_rate,
        channels=channels,
        blocksize=block_size,
        callback=audio_callback
    ) as stream:
        stream.start()

        # Open port connection to midi device and start trying to read in midi events
        #with mido.open_input(midi_device) as inport:
        try:
            while process_midi(midi_device):
                pass

        except Exception as e:
            print(f"error: {e}")


if __name__ == "__main__":
    main()

