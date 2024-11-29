# Frank Claverie
# CS 416
# Environment - parses command line and establishes basis for musical generation

import re, argparse
import numpy as np


# 11 canonical note names.
names = [ "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B", ]
note_names = { s : i for i, s in enumerate(names) }

# Turn a note name into a corresponding MIDI key number.
# Format is name with optional bracketed octave, for example
# "D" or "Eb[5]". Default is octave 4 if no octave is
# specified.
note_name_re = re.compile(r"([A-G]b?)(\[([0-8])\])?")
def parse_note(s):
    m = note_name_re.fullmatch(s)
    if m is None:
        raise ValueError
    s = m[1]
    s = s[0].upper() + s[1:]
    q = 4
    if m[3] is not None:
        q = int(m[3])
    return note_names[s] + 12 * q


# Given a string representing a knob setting between 0 and
# 10 inclusive, return a linear gain value between 0 and 1
# inclusive. The input is treated as decibels, with 10 being
# 0dB and 0 being the specified `db_at_zero` decibels.
def parse_log_knob(k, db_at_zero=-40):
    v = float(k)
    if v < 0 or v > 10:
        raise ValueError
    if v < 0.1:
        return 0
    if v > 9.9:
        return 10
    return 10**(-db_at_zero * (v - 10) / 200)

# Given a string representing a knob setting between 0 and
# 10 inclusive, return a linear gain value between 0 and 1
# inclusive.
def parse_linear_knob(k):
    v = float(k)
    if v < 0 or v > 10:
        raise ValueError
    return v / 10

# Given a string representing an gain in decibels, return a
# linear gain value in the interval (0,1]. The input gain
# must be negative.
def parse_db(d):
    v = float(d)
    if v > 0:
        raise ValueError
    return 10**(v / 20)

ap = argparse.ArgumentParser()
ap.add_argument('--bpm', type=int, default=90)
ap.add_argument('--beats-per-bar', type=int, default=3)
ap.add_argument('--samplerate', type=int, default=96000)
ap.add_argument('--root', type=parse_note, default="C[5]")
ap.add_argument('--bass-octave', type=int, default=2)
ap.add_argument('--balance', type=parse_linear_knob, default="5")
ap.add_argument('--gain', type=parse_db, default="-3")
ap.add_argument('--output')
ap.add_argument("--test", action="store_true", help=argparse.SUPPRESS)
args = ap.parse_args()

# Tempo in beats per minute.
bpm = args.bpm

# Audio sample rate in samples per second.
samplerate = args.samplerate

# Samples per beat.
beat_samples = int(np.round(samplerate / (bpm / 60)))

beats_per_bar = 3