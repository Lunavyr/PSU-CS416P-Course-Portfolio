# Frank Claverie
# CS 416p
# Midi Demo


# Note: mido requires installing python-rtmidi controller
#       Which is a wrapper for the C library rtmidi
import mido
import numpy as np
import sounddevice as sd

# Change this to match you system spec
sample_rate = 96000
max_amplitude = np.iinfo(np.int16).max

def generate_sine_wave(freq:int = 440, duration:float = 1, samplerate:int=sample_rate):
    t = np.linspace(0, duration, int(samplerate * duration))
    wave = 0.5 * max_amplitude * np.sin(2 * np.pi * freq * t)
    return wave

def play_sound(sound:np.array, samplerate:int = sample_rate, duration:float=0.5):
    sd.play(sound, samplerate)

def midi_to_freq(midi_note:int):
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))

def main():
    port_names = mido.get_input_names()
    if not port_names:
        print("No MIDI input ports found.")
        exit()
    
    print("List of available ports:")
    for i, port in enumerate(port_names):
        print(f"{i}: {port}")
    choice = int(input("Enter the number of your choice:\n>"))

    if port_names[choice] not in port_names:
        print("I'm sorry dave, I'm afraid you can't select that port...")
        exit()
    port = port_names[choice]
        

    with mido.open_input(port) as inport:
        print(f"Listening to MIDI input: {port}")
        print("   * Press ctrl-c to end.")
        try:
            for msg in inport:
                if msg.type == 'note_on' and msg.velocity > 0:
                    frequency = midi_to_freq(msg.note)
                    wave = generate_sine_wave(frequency)
                    print(f"Note ON: {msg.note}, Frequency: {frequency} Hz")
                    play_sound(wave)
                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    print(f"Note OFF: {msg.note}")

        except KeyboardInterrupt:
            print("Exiting...")
                

if __name__ == "__main__":
    main()