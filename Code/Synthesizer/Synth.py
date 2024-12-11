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

# System settings:
sample_rate = 96000
block_size = 32
#   Want to try and get stereo working eventually
channels = 1

# Sound settings:
base_freq = 437
max_amplitude = 0.5

# Oscillator settings:
global_fade = False # Change this to true for a really cool effect that scales with the number of notes
fade = 0
fade_rate = 0.002
fade_direction = 1

# Note settings:
#   ADR in ms, Sustain in scalar to max amplitude
attack = 0.002
decay = 0.004
sustain = 0.8
release = 0.05

# Buffers for managing Midi events and sound generation:
#   Queue allows us to gurantee atomic process for midi event and audio callback handling
midi_q = queue.SimpleQueue()
notes_to_play = dict()



''' Sound generation '''
# Waveform functions:
def string(freq):
    period = math.ceil(sample_rate/freq)

    time = np.linspace(0, (2 * np.pi), period, dtype=np.float32)
    phase_slice = np.sin(time) + 0.4 * np.sin(2 * time) + 0.2 * np.sin(3 * time) + 0.1 * np.sin(5 * time)
    return max_amplitude * phase_slice

# This function is begging for some filter implementation.
def saw(freq):
    period = math.ceil(sample_rate/freq)
    time = np.linspace(0, (2* np.pi), period, dtype=np.float32)
    phase_slice = time / (2 * np.pi)
    for i, t in enumerate(time):
        phase_slice[i] = t % 1
    return max_amplitude * phase_slice


string_table = dict()
saw_table = dict()

def note_to_freq(note):
    return base_freq * (2 ** ((note-69) / 12))

def populate_tables():
    for note in range(128):
        freq = note_to_freq(note)
        string_table[note] = string(freq)
        saw_table[note] = saw(freq)
    print("Loaded wavetables")   


# Controls the generation of sound frames
class Oscillator:
    def __init__(self):
        global string_table, saw_table
        self.string_table = string_table
        self.saw_table = saw_table

        # Tracks starting point in phases for wrapping around frame blocks
        self.string_phase_index = 0
        self.saw_phase_index = 0

        # Currently pans between the two wave types
        #   during block generation at the speed fade_rate
        self.fade = 0
        self.fade_rate = fade_rate
        self.fade_direction = 1

    # Dynamically fades between the two waves
    def __cross_fade(self, string_wave, saw_wave):
        global global_fade, fade, fade_rate, fade_direction
        if global_fade:
            output = (1 - fade) * string_wave + fade * saw_wave

            fade += fade_rate * fade_direction
            if fade >= 1 or fade <= 0:
                fade_direction *= -1
        else:
            output = (1 - self.fade) * string_wave + self.fade * saw_wave

            self.fade += self.fade_rate * self.fade_direction
            if self.fade >= 1 or self.fade <= 0:
                self.fade_direction *= -1

        return output

    # Generates waveforms of length frame_count for each wave type
    #   keeps track of what part of each phase the frame_block cutoff at
    #   then merges the two and returns output wave
    def __gen_waveform(self, note,  frame_count):
        string_phase = self.string_table[note]
        saw_phase = self.saw_table[note]
        string_len, saw_len = len(string_phase), len(saw_phase)

        string_wave = np.zeros(frame_count, dtype=np.float32)
        saw_wave = np.zeros(frame_count, dtype=np.float32)

        for i in range(frame_count):
            string_wave[i] = string_phase[self.string_phase_index]
            saw_wave[i] = saw_phase[self.saw_phase_index]

            self.string_phase_index = (self.string_phase_index + 1) % string_len
            self.saw_phase_index = (self.saw_phase_index + 1) % saw_len

        full_wave = self.__cross_fade(string_wave, saw_wave)
        return full_wave

    def gen_samples(self, note, frame_count):
        output = self.__gen_waveform(note, frame_count)
        return output



# Interface between midi and sound generation
class Note:
    def __init__(self, key, velocity):
        self.oscillator = Oscillator()
        self.note = key
        self.vel = velocity/127

        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self.release_start_amp = 0
        self.release_start_time = 0

        self.playing = True
        self.elapsed_time = 0.0
        self.fully_released = False


    # Calls generator in oscillator to generate a sound of length frame_count and 
    def gen_sound(self, frame_count):
        if self.fully_released:
            return None
        else:
            envelope = self.__get_adsr_envelope(frame_count)
            sound = self.oscillator.gen_samples(self.note, frame_count)
            return sound * envelope * self.vel

    def release_note(self):
        self.playing = False
        self.release_start_time = self.elapsed_time

    def __get_adsr_envelope(self, frame_count):
        envelope = np.ones(frame_count)
        time_per_frame = 1 / sample_rate

        for i in range(frame_count):
            current_time = self.elapsed_time + i * time_per_frame

            # Attack phase
            if current_time <= self.attack and self.playing:
                self.release_start_amp = (current_time / self.attack)
                envelope[i] *= self.release_start_amp

            # Decay phase
            elif current_time <= self.attack + self.decay and self.playing:
                decay_time = current_time - self.attack
                self.release_start_amp = (1 - (decay_time / self.decay) * (1 - self.sustain))
                envelope[i] *= self.release_start_amp

            # Sustain phase
            elif self.playing:
                self.release_start_amp = self.sustain
                envelope[i] *= self.sustain

            # Release phase
            elif not self.playing:
                release_time = current_time - self.release_start_time
                envelope[i] *= self.release_start_amp * max(0, 1 - release_time / self.release)
                if envelope[i] <= 0:
                    self.fully_released = True

            else:
                envelope[i] = 0

        self.elapsed_time += frame_count * time_per_frame

        # Compress envelope to range [0,1] since we will convolve it and the output sound
        envelope = np.clip(envelope, 0, 1)
        
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
    global midi_q, notes_to_play
    
    match message.type:

        # Default behavior for midi off is "note on vel=0"
        #   for Novation Launchkey - according to docs
        case "note_on":
            key = message.note
            velocity = message.velocity

            # Note actually on
            if message.velocity > 0:
                if log_events:
                    print(f"Note on: {key}")
                note = Note(key, velocity)
                notes_to_play[key] = note
                
            # Note actually off
            else:
                if log_events:
                    print(f"Note off: {key}")
                if key in notes_to_play:
                    notes_to_play[key].release_note()
                
                
        case "control_change":
            if log_events:
                print(f"Control channel: {message.value}, value = {message.value}")

        case _:
            if log_unhandled_events:
                print(f"\t*Command \"{message.type}\" not implemented")


# Audio callback - processes sound generation.
#   To be passed to sounddevice.OuputStream().
def audio_callback(out_data, frame_count, time_info, status):
    global midi_q, notes_to_play
    notes_to_remove = list()

    # Required - critical error involving underflow.
    #   Apparently due to slow sample generation.
    if status:
        print("output callback:", status)

    # Process midi events.
    while not midi_q.empty():
        msg = midi_q.get()
        _parse_midi(msg)

    # Generate sounds.
    # Start with base empty sound.
    output = np.zeros(frame_count, dtype = np.float32)

    # Add in all current notes.
    for key, note in notes_to_play.items():
        sound = note.gen_sound(frame_count)

        # Handle note buffers.
        if sound is None:
            notes_to_remove.append(key)
        else:
            output += sound

    # Remove finished notes so they can be played again.
    for key in notes_to_remove:
        del notes_to_play[key]

    num_notes = len(notes_to_play)
    if num_notes > 0:
        output *= 1 / np.sqrt(num_notes + 1)

    # Reshape because sounddevice is picky apparently
    out_data[:] = output.reshape(frame_count, 1)


''' MAAAAAAAAAIN '''
def main():
    populate_tables()
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