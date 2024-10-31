'''
Frank Claverie
CS 416P
Fall 2024
'''

import numpy as np
from scipy.io.wavfile import write, read
import sounddevice as sd
import matplotlib.pyplot as plot
import struct
import os

# Useful data
sample_rate = 96000
max_amplitude = np.iinfo(np.int16).max

# List of personal .wav files so I don't have to keep typing them
wav_files = {
    1: "7 Chords (mono).wav",
    2: "7 Chords.wav",
    3: "Fifth Sine (mono).wav",
    4: "Fifth Sine.wav",
    5: "Maj7 Step (mono).wav",
    6: "Maj7 Step.wav",
    7: "Sine Arp (mon).wav",
    8: "Sine Arp.wav",
    9: "TOTTF - bass.wav",
    10: "TOTTF - dulci (mono).wav",
    11: "TOTTF - dulci.wav",
    12: "TOTTF - wurli.wav"
}

# Uses sounddevice to play a given sound array
def play_sound(np_arr: np.array):
    sd.play(np_arr, sample_rate, blocking=True)
    return

# Plots data points
def plot_sound(np_arr: np.array):
    plot.plot(np_arr)
    plot.show()
    return

# Unpacks wav file info
def extract_wav_header(wav_file_path):
    with open(wav_file_path, 'rb') as wav_file:
        header = wav_file.read(44)

        if header[:4] != b'RIFF' or header[8:12] != b'WAVE' or header[12:16] != b'fmt ':
            raise ValueError("Invalid WAV file")
            
        # Extract relevant information from the header
        header_chunk_id = struct.unpack('4s', header[0:4])[0]
        header_chunk_size = struct.unpack('<I', header[4:8])[0]
        header_chunk_format = struct.unpack('4s', header[8:12])[0]
        format_chunk_id = struct.unpack('4s', header[12:16])[0]
        format_chunk_size = struct.unpack('<I', header[16:20])[0]
        format_code = struct.unpack('<H', header[20:22])[0]
        channels = struct.unpack('<H', header[22:24])[0]
        sample_rate = struct.unpack('<I', header[24:28])[0]
        byte_rate = struct.unpack('<I', header[28:32])[0]
        block_align = struct.unpack('<H', header[32:34])[0]
        sample_width = struct.unpack('<H', header[34:36])[0]
        data_chunk_id = struct.unpack('4s', header[36:40])[0]
        data_chunk_size = struct.unpack('<I', header[40:44])[0]
        
        # Encapsulating data in dictionary 2bCool
        header_info = {
            'Header Chunk ID': header_chunk_id.decode(),
            'Header Chunk Size': header_chunk_size,
            'Header Format': header_chunk_format.decode(),
            'Format Chunk ID': format_chunk_id.decode(),
            'Format Chunk Size': format_chunk_size,
            'Audio Format': format_code,
            'Channels': channels,
            'Sample Rate': sample_rate,
            'Byte Rate': byte_rate,
            'Block Align': block_align,
            'Bits Per Sample': sample_width,
            'Data Chunk ID': data_chunk_id.decode(),
            'Data Chunk Size': data_chunk_size,
        }

        return header_info

# Allows for saving a sound wave as a .wav file
def save_wav(sound_arr: np.array, file_path:str):
        write(file_path, sample_rate, sound_arr.astype(np.int16))

# Loads the data from a given .wav file
def load_wav(file_name):
    wav_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../Wavs/{file_name}"))
    samplerate, data = read(wav_path)
    return data