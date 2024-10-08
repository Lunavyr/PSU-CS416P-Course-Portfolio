'''
Frank Claverie
CS 416P
Fall 2024
'''

import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plot

# Documentation & inspiration found at:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html#scipy.io.wavfile.write
samplerate = 48000
freq = 440
t = np.linspace(0., 1., samplerate)
amplitude = np.iinfo(np.int16).max
data = amplitude * np.sin(2. * np.pi * freq * t)
write("./example.wav", samplerate, data.astype(np.int16))
print(amplitude, "\n", amplitude/4)
print(t)
print("\n", data)
print('\n', len(data))

plot.plot(data)
plot.show()

import struct

def extract_wav_header(wav_file_path):
    with open(wav_file_path, 'rb') as wav_file:
        header = wav_file.read(44)  # WAV header is 44 bytes long

        # Unpack header information
        chunk_id, chunk_size, format = struct.unpack('<4s4s4s', header[:12])
        subchunk1_id, subchunk1_size, audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample = struct.unpack('<4s4sHHIIHH', header[12:40])
        subchunk2_id, subchunk2_size = struct.unpack('<4s4s', header[40:])

        header_info = {
            'Chunk ID': chunk_id.decode(),
            'Chunk Size': chunk_size,
            'Format': format.decode(),
            'Subchunk1 ID': subchunk1_id.decode(),
            'Subchunk1 Size': subchunk1_size,
            'Audio Format': audio_format,
            'Num Channels': num_channels,
            'Sample Rate': sample_rate,
            'Byte Rate': byte_rate,
            'Block Align': block_align,
            'Bits Per Sample': bits_per_sample,
            'Subchunk2 ID': subchunk2_id.decode(),
            'Subchunk2 Size': subchunk2_size
        }

        return header_info

if __name__ == "__main__":
    wav_file_path = './example.wav'  # Replace with your WAV file path
    header_info = extract_wav_header(wav_file_path)
    print(header_info)