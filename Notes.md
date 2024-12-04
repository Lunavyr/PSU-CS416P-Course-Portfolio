# Personal Notes
Quick reference to general topics

Project ideas: wavetable synthesizer with adjustable gain, attack, decay, delay. Maybe some wavetable modulation, too (this is the ideal)

## Digital/Background Concepts:
### Sound representation in computers:
Analog sound waves can be roughly approximated using an array of points that roughly draw the wave we want to encode, called PCM (pulse code modulation).  
When considering frequency, the Nyquist limit suggests that to adequately capture a particular frequency, f, the rate at which samples are generated for the wave should be at least 2f.  
For the human range of hearing, a sample rate of 44k is adequate - though good luck detecting really squeaky animals and such.

### Analog waves to digital:
A device called a ADC (analog to digital converter) samples analog electrical current relative to a sample rate (as previously stated) and a bit depth (16, 24, 32, 64 bits) to provide a range for representing amplitude. This ADC works by first filtering out frequencies above half the samplerate (Nyquist limit) also called anti-aliasing. The modified signal is sent to a sample and hold circuit, which effectively takes snapshots of the signals voltage, then sends that to an encoder which outputs binary representations of the voltage over time. 

### Wav files:
.wav (waveform audio file format) is a common file encoding for digital sound representation - it is comprised the following data and file meta-data:  
* Header: Chunk ID: RIFF - verifies that file is not corrupt; Chunk size: file size minus header; Format: encoding format.
* Format: Audio format: PCM, etc; Channels: 1,2, etc; Samplerate; Byterate: samplerate * channels * bits per sample / 8; Bits per sample.
* Data: Data: actual sound representation.
* Optional: Other meta-data segments, like artist, copyright, etc.

### Frequency/Period/Samples/Sound Frames
Given a sample rate, s; a frequency, f where:
$$ s = (samples/second) $$ 
and 
$$ f = (1 second/period) = (cycles/1 second) $$
* Number of samples per cycle: 
$$ s/f = (samples/second)/(cycles/second) = (samples/second)*(second/cycles) = (samples/cycles) $$
* Cycles per sound frame (Use ceiling function to make sure it's big enough): 
$$ (cycles/samples) * (samples/frame) = (cycles/frame) $$
* Adjusted frame size (to make sure the passed back wave is big enough - use round or ceiling):
$$ (cycles/frame) * (samples/cylces) = (samples/frame) $$

## MIDI
### Musical Instrument Digital Interface.  
This data encoding is (for MIDI 1.0) comprised of messages that take the shape [[status], [data1], [data2]], where each group is a byte.  
The status indicates what sort of message it is: note_on, note_off, control_change, Polyphonic Aftertouch, ..., etc.  
The data bytes have information pertaining to each of these message types, and allow us to pass in super lightweight information for use in a synthesizer, which can scale this information to a musical domain.



## Sound Manipulation
### Fourier transforms:
Discrete Fourier Transform: $$ X[k] = \sum_{n=0}^{N-1} x[n] e^{-i k n / N} $$

Allows us to represent a sequence of amplitude values over time as a function returning amplitudes at particular frequencies and their relative phase.  
This analysis lends itself well to manipulating sounds - such as determining the dominate frequencies present in a particular sound.  
Doing so can allow us to hone in those frequencies, adjusting them or even outright ignoring them - which can have the byproduct effect of smaller file sizes and getting rid of ambient noises.  
EQ is also done in this paramaterized view - allowing us to dynamically control which frequency ranges we want to either boost or cut.

* Idea: this can be used to effectively parse random samples and use additive synthesis to create arbitrarilly based synthesizers. Probably how sampling works these days...

## Music theory:
Notes are arbitrary divisions of ranges of frequencies into roughly equally sized partitions relative to a particular frequency.  
For western music, A4(440hz) is considered the basis, and all notes between (440, 880) are divied up into 12 by: $$ \textrm{note}_i(f) = f \cdot 2^{i/12} $$

# Applied Concepts
## Filters (FIR and IIR):
FIR EQ: $$ y(n) = \sum_{k=0}^{N}a(k)*x(n-k) $$
* y(n) - filtered signal
* x(n-k) - input samples
* a(k) - attenuation coefficient
* N - number of previous samples

A Finite Impulse Response filter is a type of digital wave transformation that operates in the time domain (allowing us to bypass potentially costly FFTs). It works by summing an arbitrary number of previous sample values and multiplying these by arbitrary coefficients. N values dictate the steepness of the cutoff - lower N, more gradual cutoff; higher N, sharper cutoff. 

Additionally, a(k) values can be computed using minor wizardry using DFTs and windowing functions. Performing this process also typically introduces a phase delay in the resulting wave representation - which makes sense, as we are only normalizing by historic values, instead of future waves, which constitute the local area. This delay is also impacted by the size of N.

IIR EQ: $$ y(n) = \sum_{k=0}^{N}a(k)*x(n-k) + \sum_{j=0}^{P}b(j)*y(n-j)$$
* P - number of historic outputs
* b(j) - attenuation coefficient of historic output

Infinite IRs work similarly to FIRs - except that they add in some amount of attenuation generated by previous outputs. This filter tends to have a sharper cutoff for fewer terms than FIRs do - but they also have variable phase delay, and will oscillate between 0 and some amplitude for high frequency values; unlike FIRs. 

One way to alleviate filter delay is by performing the same filtering from the back of the newly generated attenuated wave. Of course, this will also modify the resulting shape of the wave.

* Idea: filtering (anti-aliasing low pass [brick wall sytle]) can be a potent way to perform samplerate transforms. If we want s/2, then we can apply a filter at half the desired sampling rate (or 1/4 of start sample rate) then cut every other sample. Likewise for doubling, we first double the number of samples (either duplicate each original, or insert 0s), then apply a filter at 1/2 the original sample freq. (For very conservative scaling, we probably want to use FIRs to conserve phase data)

### Resampling:
Technique used to adapt a given sound array into an array with a different sample rate
* Useful for ensuring consistency across sounds in a program
* Especially useful for pitch and time shifting as an effect.  
However, this requires care: interpolation required when up/down sampling; and filtering can help reduce artifacting.


## Effects:
Digital music effects are generally of two classes - those that perform transformations on a time-domain signal, and those on a frequency domain (and some, like convolution reverb in both).  
For live performance, we want data throughput high and latency low - for production, this doesn't matter so much.  

The following is a rough breakdown of common effects and their function:
### Time-domain:
***Delay Types***  
Delay: 
* Achieved by storing signal in a buffer and playing it back after some period of time.
* Commonly implemented with circular buffers
* Useful Params: Delay, Feedback, Mix

Reverb:
* Uses a similar priciple as delay, but adds in the functionality of comingling various versions of the buffered signal to simulate natural reverb.
* Requires a deeper understanding of physical acoustics.
* Useful Params: Room Size (likely affects how signals are combined), Decay, Mix

Chorus/Flanger:
* Similar to delay, but slightly pitch-modulates the repeated signal.
* Flanger is basically a faster chorus.
* Both commonly modulated with sythesis of an LFO
* Useful Params: Delay, Mod Depth/Rate, Mix, Feedback

***Amplitude Types***  
Compressor:
* Attenuates signal amplitude above a certain threshold.
* Useful Params: Threshold, Ratio (reduction coefficient), Attack/Release(how quickly the compressor engages/disengages), Gain

Tremolo:
* Varies the amplitude of a signal with additive synthesis of a LFO.
* Params: Depth (amplitude of LFO), Rate (freq of LFO)

Limiter:
* EXTREME COMPRESSOR

Gate:
* Filters out signals below a threshold amplitude (kind of an inverse compressor).
* Ideal for Djent. Much chug. Small buzz.
* Params: Threshold, Attack (how quickly the gate opens), Hold (how long to keep the gate open if noises dip below), Release, Range (how strongly the signal is attenuated)

***Distortion Types***  
Distortion/Overdrive:
* In basic form, this amplifies and clips the signal above a certain threshold. Less extreme -> Distortion; More extreme -> Overdrive.
* Params: Gain, Tone (filters), Mix

Bitcrush:
* Reduces bit depth/sampling rate to introduce weird transients.
* Params: Bit Depth, Sample Rate

***Modulation Types***
Phaser:
* Uses series of filters to shift the phase of signal, resulting in some frequencies being enhanced or squashed
* Params: Stages, LFO rate/depth

Vibrato:
* Similar to tremolo, but modulates the frequency with an LFO instead.
* Params: Depth, Rate

### Frequency-Domain:  
EQ:
* Boosts/Attenuates specific freq ranges - can be done either with filters or via FFT bins
* Params: Gain, Bandwidth

Wah:
* Dynamic bandpass filter sweeps across the FFT bins with an LFO.
* Params: Sweep Freq, Resonance (bandwidth)

Pitch Shifting:
* Shifts frequency values higher or lower while maintaining harmonic relationships.

Spectral Morphing:
* Form of convolution between two signals spectra. 
* Maps freq bins from source onto target using something like interpolation or direct convolution.

### Hybrid:  
Convolution Reverb:
* Convolves a signal with an impulse response generated from a real environment.
* More accurate, but also more expensive.

Time Stretching:
* Changes duration by manipulating phase and magnitude of FFT bins.

Noise Reduction:
* Squashes certain frequency ranges that are not strongly present (probably done via a threshold or something like a gradient) to help reduce noise.

Pooling:
* This is a fascinating technique. Essentially the idea is to use a window of arbitrary size to propogate across a signal and average (or min or max) data points along the length of the signal with steps in the size of the window.  
* Kinda feels like convolution meets filtering. This could be an effective way to downsample audio or compress its size while maintaining key characteristics of sound.  
* Additionally, this might be of use in sampling an arbitrary sound using FFT analysis, as it would allow peak values (thus the fundamental note and overtone response) to more easily discovered.  
* Idea: use pooling to help create a function that provides the mathematical relationship of frequencies up to some arbitrary number of frequencies and given a particular cutoff amplitude.  
e.g.
```python
def get_sample_equation_coefficients(fft_data, window_len, amp_cutoff)
    pool_size = window_len
    fft_data = avg_pool(fft_data, pool_size)
    # fft_data = avg_pool_backwards(fft_data, pool_size) <- Maybe useful. Maybe not.

    peaks = get_peaks(fft_data, amp_cutoff) # Get list of peak values
    coefs = get_musical_rel(peaks)
    return coefs
```
* Could then use this idea to generate sounds of this pattern but at any given frequency and use it as a carrier wave, in a wavetable, or in additive/subtractive synthesis


# Python Notes:

## Useful Libraries:
### Numpy:
* Affords the usage of vectorized arrays and access to a great deal of predefined, easy access math functions.
* Used to hard encode digital representation of sound waves.

### Scipy:
* Gives us the signal library, useful for creating filters.
* Also gives us the fft and ifft, which is useful for frequency analysis and manipulation
* Honestly the GOAT for pythonic DSP
* Likewise has libraries for wavfile manipulation and many other goodies

### Sounddevice:
* Allows us to interface with our machines native sound system.
* wE cAN hEaR nUmbErs.
* Output stream expects dtype in the set {float32(High quality), int16, int8}
* Requires defined callback function that fills "frames" (read: sound buffer) with sound data.

### Mido:
* Python wrapper for python-rtmidi (which is a wrapper for C's rtmidi) {Can also use other midi libraries as backend, like pygame.midi}
* Allows for the structured use and manipulation of midi in so called MIDI Objects.
* Super handy. 
* Fascinatingly (examples for which are annoyingly missing the documentation), mido.open_input accepts a callback function as a parameter, which can asynchronously process midi events.
* Not sure if inport.receive() is a better option here, though. Needs more research.

* Ideas on race condition prevention: 
* inport polling + snapshotting sound buffer
* callback functions for both and using a thread on input and send messages directly to a shared queue
* Real solution -> use queue.put() for capturing and queue.get() for thread-safe processing

### Pyo:
* Prebuilt DSP components. Might be worth a look, or could be similar to scipy.signals

### Numba (PyPy, Cython, JAX):
* Just in time compiler for compiling often reused code into machine code (versus the normal byte code). Can drastically improve performance of filters (and probably everything else in synths)
* Can utilize gpu processing. Which is saucy.
* Requires more research and is probably agressively beyond the scope of this class.
* Apparently pairs extremely well with numpy and CUDA
* Evidently this is also similar to tensorflow

* Nevermind I hate this idea. Apparently it isn't supported on Python 3.13. Rude...
* JAX might be a suitable replacement though...

### Jupyter:
* Strange webpage based environment for running python snippets. Could be useful for iterative programming.
