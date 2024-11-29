# Frank Claverie
# CS 416
# Musical Phrase generator


from Envr import *
from Sounds import *
from Chords import *

import  wave
import sounddevice as sd



# Unit tests, driven by hidden `--test` argument.
def test():
    note_tests = [
        (-9, -15),
        (-8, -13),
        (-7, -12),
        (-6, -10),
        (-2, -3),
        (-1, -1),
        (0, 0),
        (6, 11),
        (7, 12),
        (8, 14),
        (9, 16),
    ]

    for n, k in note_tests:
        k0 = note_to_key_offset(n)
        assert k0 == k, f"{n} {k} {k0}"

    chord_tests = [
        (-3, -7),
        (-2, -5),
        (-1, -3),
        (0, 0),
        (1, 2),
        (2, 4),
        (3, 7),
        (4, 9),
    ]

    for n, c in chord_tests:
        c0 = chord_to_note_offset(n)
        assert c0 == c, f"{n} {c} {c0}"

    exit(0)


def generate_sound() -> np.array:
    sound = np.array([], dtype=np.float64)


    # Generate sound per measure (i.e. chord)
    for c in random.choice(loops):
        # Bass generated once per chord (sustains for the full measure)
        bass_note = note_to_key_offset(c - 1)
        bass = string(bass_note + bass_root, beats_per_bar)

        # Initialize melody and harmony arrays for the measure
        melody = np.array([], dtype=np.float64)
        harmony = np.array([], dtype=np.float64)

        # Generate melody and harmony for each beat in the measure
        for beat in range(beats_per_bar):
            # Melody
            mel_notes_per_beat = random.choice([2,3,4])
            melody_notes = pick_melody(c - 1, mel_notes_per_beat)
            melody = np.append(melody, np.concatenate([flute(note + melody_root, duration) for note, duration in melody_notes]))
            
            # Harmony
            har_notes_per_beat = 1 #random.choice([1,2])
            harmony_notes = pick_chord(c - 1, har_notes_per_beat)
            for notes, duration in harmony_notes:
                harmony_chunk = np.array([], dtype=np.float64)
                for i, note in enumerate(notes):
                    # Silence on beat 1
                    if beat == 0:
                        note = 0

                    if i == 0:
                        harmony_chunk = np.append(harmony_chunk, string(note + harmony_root, duration))
                    else:
                        harmony_chunk += string(note + harmony_root, duration)
                harmony_chunk *= 1/len(notes)
                harmony = np.append(harmony, harmony_chunk)


        # Gain stage
        melody_gain = args.balance
        bass_gain = 1 - melody_gain
        harmony_gain = 0.7


        # Pad melody with zeros if it's shorter
        if len(melody) < len(bass):
            melody = np.pad(melody, (0, len(bass) - len(melody)), 'constant')
        # Pad bass with zeros if it's shorter
        elif len(melody) > len(bass):
            melody = melody[:len(melody) - len(bass)]
            #bass = np.pad(bass, (0, len(melody) - len(bass)), 'constant')

        if len(harmony) < len(bass):
            harmony = np.pad(harmony, (0, len(bass) - len(harmony)), 'constant')
        # Pad bass with zeros if it's shorter
        elif len(harmony) > len(bass):
            harmony = harmony[:len(harmony) - len(bass)]


        # Combine melody, bass, and harmony for the entire measure
        sound = np.append(sound, melody_gain * melody + bass_gain * bass + harmony_gain * harmony)

    return sound


# Saves generated music to wav file
def output_wav(sound:np.array):
        output = wave.open(args.output, "wb")
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(samplerate)
        output.setnframes(len(sound))

        data = args.gain * 32767 * sound.clip(-1, 1)
        output.writeframesraw(data.astype(np.int16))

        output.close()


# Play the given sound waveform using `sounddevice`.
def play(sound):
    sd.play(sound, samplerate=samplerate, blocking=True)
        

def main():
    if args.test:
        test()
    
    # Generates musical pattern
    sound = generate_sound()
    notes = parse_note("C[4]")

    # Save or play the generated "music".
    if args.output:
        output_wav(sound)
    else:
        play(args.gain * sound)

if __name__ == "__main__":
    main()