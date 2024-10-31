'''
Frank Claverie
CS 416P
Fall 2024
'''

# Minor wizardry to include utility file
import sys, os, random
utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Utilities"))
sys.path.append(utils_path)

from BasicUtils import *

# Global variables
freq_bands = {
    "low": (0,300),
    "mid": (300, 2000),
    "high": (2000, sample_rate/2)
}


# Function to analyze energy in band
def band_enery(fft_data, band):
    pass

# Adjust energy in band
def control_tone(fft_data, band, energy):
    pass


def main():
    # State variables
    freq_bands = {
        "low": (0,300),
        "mid": (300, 2000),
        "high": (2000, sample_rate/2)
    }

    index, wav_file = random.choice(list(wav_files.items()))
    data = load_wav(wav_file)

if __name__ == "__main__":
    main()