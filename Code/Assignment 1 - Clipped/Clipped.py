'''
Frank Claverie
CS 416P
Fall 2024
'''
# Documentation & inspiration found at:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html#scipy.io.wavfile.write


import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plot
import struct

# Globals for 
samplerate = 48000
freq = 440

# Part 1:
def make_sine_wav_file():
    t = np.linspace(0., 1., samplerate)
    amplitude = .25 * np.iinfo(np.int16).max
    data = amplitude * np.sin(2. * np.pi * freq * t)
    write("./sine.wav", samplerate, data.astype(np.int16))
    #plot_sine_wave(data)
    return

# Part 2
def make_fuzzy_wav():
    # Create sine data
    t = np.linspace(0., 1., samplerate)
    amplitude = np.iinfo(np.int16).max
    data = amplitude * np.sin(2. * np.pi * freq * t)

    # Clip all low and high data points past threshold
    high_clip = amplitude/2
    low_clip = -1*amplitude/2
    for i in range(len(data)):
        if data[i] > high_clip:
            data[i] = high_clip
        elif data[i] < low_clip:
            data[i] = low_clip


    write("./clipped.wav", samplerate, data.astype(np.int16))

    plot_sine_wave(data)
    print("Amps:", amplitude, high_clip, low_clip)
    for i in data[:50:]:
        print(i)

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
        
        # Read the data from the file
        wav_file.seek(44)
        data = wav_file.read(data_chunk_size)

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
    



if __name__ == "__main__":
    make_sine_wav_file()
    make_fuzzy_wav()

    print("\nWav file metadata:\n")
    wav_file_path = './example.wav'  # Replace with your WAV file path
    header_info = extract_wav_header(wav_file_path)
    for i in header_info:
        print(i, ': ', header_info[i])