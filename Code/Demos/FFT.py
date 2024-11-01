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


def main():
    # Load waveform data from wav file
    index, wav_file = random.choice(list(wav_files.items()))
    # wav_file = wav_files[13] # Used to select particular wav file
    data, samplerate = load_wav(wav_file)
    print(f"Analysis of {wav_file}")

    # *** Want to get to work with stereo data...
    # if data.ndim > 1:
    #     fftdata = fft.rfft2(data)
    # else:
    #     fftdata = fft.rfft(data)

    # Workaround - only analyzes one channel for stereo input.
    if data.ndim > 1:
        data = data[:,0]
    
    # Creates an x axis corresponding time to each sample in the waveform array
    duration = len(data)/samplerate
    t = np.linspace(0, duration, len(data), endpoint=False)
    
    # Converts waveform data to frequency data, normalizes to positive values, 
    # and defines a range of frequencies to plot against
    fftdata = fft.rfft(data)
    fftdata = np.abs(fftdata)/len(fftdata)
    freqs = fft.rfftfreq(len(data), d=1/samplerate)


    # Plotting goodies
    # Reference: https://www.geeksforgeeks.org/matplotlib-pyplot-subplots-in-python/
    fig, (p1, p2) = plot.subplots(1,2, figsize = (10,5))
    fig.suptitle(f"Waveform vs Frequencies for {wav_file}")

    p1.plot(t, data, c='green')
    p1.set_title("Wave Form")
    p1.set_xlabel("Time (seconds)")
    p1.set_ylabel("Amplitude (voltage?)")
    p1.grid(True)

    p2.plot(freqs, fftdata, c='purple')
    p2.set_title("Frequency Form")
    p2.set_xlabel("Frequency (hz)")
    p2.set_ylabel("Amplitude (power?)")
    p2.grid(True)

    plot.tight_layout()
    plot.show()

    # Single plot method:

    # plot.title(f"Real FFT of {wav_file}")
    # plot.xlabel("Frequency")
    # plot.ylabel("Amplitude")
    # plot.grid()

    # plot.subplot(1,2,1)
    # plot.plot(data)

    # plot.subplot(1,2,2)
    # plot.plot(fftdata)
    # plot.show()

if __name__ == "__main__":
    main()