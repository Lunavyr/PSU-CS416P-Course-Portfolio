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


# Function to analyze energy in band
def band_energy(fft_data:np.array, freqs:np.array, low: int, high: int) -> np.array:
    energy = {}
    band_mask = (freqs >= low) & (freqs < high)
    return np.sum(np.abs(fft_data[band_mask]) ** 2)
    

# Normalizes the given frequency bands relative to one another
def control_tone(fft_data:np.array, bands:np.array, freqs:np.array) -> np.array:
    attenuation_arr = []
    energy = []

    # Accumulate the energy in each band
    for band in bands:
        low, high = bands[band]
        energy.append(band_energy(fft_data, freqs, low, high))
    
    # Find average energy and set gain relative to ratio of average and each band
    avg_energy = sum(energy)/len(energy)
    for i, band in enumerate(bands):
        # This guy is a finicky one - I've tried lots of different stuff
        #   but this seems to work subtly for now.
        gain = np.sqrt((avg_energy / np.abs(avg_energy - energy[i]) * np.int16(i + 1)))
        print(band, "gain", gain)
        attenuation_arr.append(gain)

    # GAINZZZ
    for i, band in enumerate(bands):
        low, high = bands[band]
        band_mask = (freqs >= low) & (freqs < high)
        fft_data[band_mask] *= attenuation_arr[i]

    return fft_data


def main():
    index, wav_file = random.choice(list(wav_files.items()))
    data, samplerate = load_wav(wav_file)
    save_wav(data, "Before.wav", samplerate)

    # EQ bands
    freq_bands = {
        "Low": (0,300),
        "Mid": (300, 2000),
        "High": (2000, samplerate/2)
    }
    print(f"\nAdapting tone for file: {wav_file}\n")
    print(f"Before processing: min {np.min(data):0.5f}, max {np.max(data):0.5f}")

    # Mono Channel equalization
    if len(data.shape) == 1:
        print()
        fft_data = fft.rfft(data)
        freqs = fft.rfftfreq(len(data), 1 / samplerate)

        fft_data = control_tone(fft_data, freq_bands, freqs)
        data = fft.irfft(fft_data)

    # Stereo
    else:
        num_channels = data.shape[1]
        for channel in range(num_channels):
            print("\nChannel", channel + 1)
            fft_data = fft.rfft(data[:, channel])
            freqs = fft.rfftfreq(len(data[:, channel]), 1 / samplerate)
            
            fft_data = control_tone(fft_data, freq_bands, freqs)

            # Due to the black magic of using ffts on stereo arrays...
            #   My inverse fft was giving back an array of mismatched size
            #   Might investigate this fix I found...
            #   Maybe.....
            temp_data = fft.irfft(fft_data)
            if len(temp_data) > len(data[:, channel]):
                temp_data = temp_data[:-1]
            elif len(temp_data) < len(data[:, channel]):
                temp_data = np.pad(temp_data, (0, 1), mode='constant')

            data[:, channel] = temp_data


    print(f"\nBefore processing: min {np.min(data):0.5f}, max {np.max(data):0.5f}")    
    save_wav(data, "After.wav", samplerate)

if __name__ == "__main__":
    main()