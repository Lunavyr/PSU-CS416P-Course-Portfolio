'''
Frank Claverie
CS 416P
Fall 2024
'''

# Documentation & inspiration found at:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html#scipy.io.wavfile.write

import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import matplotlib.pyplot as plot
import struct
import os

# Global data
samplerate = 96000
freq = 440
max_amplitude = 0.2 * np.iinfo(np.int16).max



# -----Main assignment functions-----

# Part 1:
def make_sine_wav_file():
    # Create sine data
    t = np.linspace(0., 1., samplerate)
    amplitude = .25 * max_amplitude
    data = amplitude * np.sin(2. * np.pi * freq * t)

    return data

# Part 2
def make_fuzzy_wav():
    # Create sine data
    t = np.linspace(0., 1., samplerate)
    amplitude = 0.5 * max_amplitude
    data = amplitude * np.sin(2. * np.pi * freq * t)

    # Clip all low and high data points past threshold
    high_clip = amplitude/2
    low_clip = -1*amplitude/2
    for i in range(len(data)):
        if data[i] > high_clip:
            data[i] = high_clip
        elif data[i] < low_clip:
            data[i] = low_clip

    return data

# Part 3
def play_sound_arr(np_arr: np.array):
    sd.play(np_arr, samplerate, blocking=True)
    return



# -----Analytic bonus content-----

# Useful because I was curious how smooth the data collection is.
def plot_sine_wave(sine_array):
    plot.plot(sine_array)
    plot.show()


# For my own curiosity - I wanted to see the structure of wav file.
# Source: 
# https://medium.com/@jatin.dhall7385/pythonic-wav-file-handling-a-guide-to-reading-wav-files-without-external-libraries-f5869b27b2e7
def extract_wav_header(wav_file_path):
    with open(wav_file_path, 'rb') as wav_file:
        header = wav_file.read(44)  # WAV header is 44 bytes long

        # File validation cause we cool like that
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
        
        # Encapsulating data 2bCool
        header_info = {
            'Header Chunk ID': header_chunk_id.decode(),
            'Header Chunk Size': header_chunk_size,
            'Header Format': header_chunk_format.decode(),
            'Format Chunk ID': format_chunk_id.decode(),
            'Format chunk Size': format_chunk_size,
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
    

def save_wav(sound_arr: np.array, file_path:str):
        write(file_path, samplerate, sound_arr.astype(np.int16))

# ===== mAiN =====
if __name__ == "__main__":
    # Main reqs.

    sine = make_sine_wav_file()
    clipped = make_fuzzy_wav()

    # plot_sine_wave(sine)
    # plot_sine_wave(clipped)

    play_sound_arr(sine)
    play_sound_arr(clipped)

    # save_wav(sine, "./sine.wav")
    # save_wav(clipped, "./clipped.wav")

    # Analytics for my own sanity.
    # print("\nWav file metadata:\n")
    # wav_file_path = './sine.wav'
    # header_info = extract_wav_header(wav_file_path)
    # for i in header_info:
    #     print(i, ': ', header_info[i])