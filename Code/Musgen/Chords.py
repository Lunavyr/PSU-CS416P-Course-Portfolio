# Frank Claverie
# CS 416
# Chords and notes - transition module chords and notes for use in Musgen

from Envr import *

import random


major_scale = [0, 2, 4, 5, 7, 9, 11]
minor_scale = [0, 2, 3, 5, 7, 8, 10]
triad = [1, 3, 5]
sus_four = [1, 4, 5]
seven_chord = [1, 3, 5, 7]
nine_chord = [1, 3, 5, 9]

scales = [
    major_scale,
    minor_scale
    ]

chords = [
    triad,
    sus_four,
    seven_chord,
    nine_chord
]

loops = [
    [8, 5, 6, 4],
    [1, 4, 1, 6, 5, 4],
    [1, 5, 6, 1, 5, 6],
    [4, 1, 3, 6, 7, 8]
]

melody_root = args.root
harmony_root = melody_root - 24
bass_root = melody_root - 12 * args.bass_octave


# Given a scale note with root note 0, return a key offset
# from the corresponding root MIDI key.
def note_to_key_offset(note):
    scale_degree = note % 7
    return note // 7 * 12 + minor_scale[scale_degree]

# Given a position within a chord, return a scale note
# offset — zero-based.
def chord_to_note_offset(posn):
    chord_posn = posn % 3
    return posn // 3 * 7 + random.choice(chords)[chord_posn] - 1


position = 0
def pick_melody(chord_root:int, notes_per_beat:int=4) -> list:
    global position
    p = position

    notes = []
    for _ in range(notes_per_beat):
        chord_note_offset = chord_to_note_offset(p)
        chord_note = note_to_key_offset(chord_root + chord_note_offset)
        notes.append([chord_note, 1/notes_per_beat])

        if p > 12:
            p -= 1
        elif p < -12:
            p += 1
        else:
            if random.random() > 0.5:
                p = p + 1
            else:
                p = p - 1

    position = p 
    return notes


def pick_chord(chord_root:int, notes_per_beat:int=1) -> list:
    chord = random.choice(chords)
    chord_notes = []
    duration = 1.0/notes_per_beat

    for i in range(notes_per_beat):
        notes = [chord_root + interval for interval in chord]
        
        adjusted_chord_notes = [
            note_to_key_offset(chord_root + chord_to_note_offset(off)) 
            for off in range(len(notes))
        ]
        notes = adjusted_chord_notes
        if i > 0:
            random.shuffle([chord_root + note for note in chord])

        chord_notes.append([notes, duration])

    return chord_notes