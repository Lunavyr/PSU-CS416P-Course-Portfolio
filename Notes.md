# Personal Notes
Quick reference to general topics

Project ideas: dynamic grain distortion with octaver

## Sound representation in computers:
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

### Fourier transforms:
Discrete Fourier Transform: $$ X[k] = \sum_{n=0}^{N-1} x[n] e^{-i k n / N} $$


Allows us to represent a sequence of amplitude values over time as a function returning amplitudes at particular frequencies and their relative phase.  
This analysis lends itself well to manipulating sounds - such as determining the dominate frequencies present in a particular sound.  
Doing so can allow us to hone in those frequencies, adjusting them or even outright ignoring them - which can have the byproduct effect of smaller file sizes and getting rid of ambient noises.  
EQ is also done in this paramaterized view - allowing us to dynamically control which frequency ranges we want to either boost or cut.

* Idea: this can be used to effectively parse random samples and use additive synthesis to create arbitrarilly based synthesizers. Probably how sampling works these days...

### Music theory:
Notes are arbitrary divisions of ranges of frequencies into roughly equally sized partitions relative to a particular frequency.  
For western music, A4(440hz) is considered the basis, and all notes between (440, 880) are divied up into 12 by: $$ \textrm{note}_i(f) = f \cdot 2^{i/12} $$


### Filters (FIR and IIR):

### Effects: