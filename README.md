Frank Claverie  
CS 416P  
Fall 2024

# CS 416P Programming Portfolio
This repository is the accumulation of all projects done in CS416p.  
Content is organized in subfolders according to the assignments, and a detailed log can be found in the Notebook.md

## Main Projects
### Assignment 1: Clipped Audio
This assignment saw us creating raw audio data and both exporting it as a wav file and playing it within our program.  
The raw audio was created and exported following the boilerplate found in the scipy.io.wavfile.write documentation.  
Additionally, the clipped audio was achieved by iteratively comparing each index in the created array to the threshold.
I suspect this is a naive way to achieve this - as a more mathematical approach could cut down on runtime complexity.

Requirements:
* Channels: 1  
* Sample bit size: 16 bits  
* Amplitude: 1/4 of maximum sample size & 1/2 with 1/4 hard clipping for each part, respectively.
* Duration: 1 sec
* Frequency: 440 Hz
* Sample Rate: 48000 sps

I chose to complete this assignment using Python and its libraries: numpy, scipy, matplotlib, and sounddevice.  
The program Clipped.py in the Assignment 1 subdirectory can be run using VSCode or via command line.  
The wav files will be output to the current working directory.


### Adaptive tone control
Our objective is to create a program that allows us to control tones across arbitrary frequency bands. 

Requirements:
* Band divisions: low(0-300hz), mid(300-2000hz), high(2000+hz).
* Use FFT to analyze amplitude of particular frequencies.

This program was a bit of a beast to complete... lots of digging through scipy docs.
However, it works decently as an "across the board" equalizer. In its current state it reasonably averages out the total energies of each of the bands above.

The implementation for this project is as follows:
* Load one of the wav files saved in the ./Code/Wavs at random.
* For each channel: convert the PCM into a frequency spectrum, convert that into an array of frequency bins, apply the core algorithm (control_tone), convert back to PCM.

The control_tone function is as follows:
* For each band, find the total energy for that range of frequencies.
* Take the average energy of all bands and use that to establish a gain setting for each frequency band.
* Apply the gain to the data at each band.

Getting the program to work in the first place was challenging, but once all the pieces were properly in place, it simply became a matter of adjusting the function determining the gain. Presently I am calculating it by dividing the average energy by the absolute difference of band and average energies. This seems to work ok, but I'd really like for the gain to increase decently over the span of frequency bands. I might come back and find an equation to achieve this, but the core lessons seem to have been learned!

## Auxillary Work
### Demos
A loose collection of tests for various ideas that help calcify various class topics.

Current content:
* Demo.py - learned some quick cool, painful lessons about how to make importable modules for use in programs outside of a given directory.
* FFT.py - a short program that analyzes the waveform vs frequency responses in a graphical format.

### Utilites
Collection of importable modules that serve basic functions (such as reading in a wav file) so that I don't have to keep writing the same lines of code.

### Future
*Pending: student's tears
