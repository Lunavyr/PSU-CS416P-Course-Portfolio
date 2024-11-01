Frank Claverie  
CS 416P  
Fall 2024

# CS 416P Programming Portfolio
This repository is the accumulation of all projects done in CS416p.  
Content is organized in subfolders according to the assignments, and a detailed log can be found in the Notebook.md

# Content:
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

Things to consider: how wide of an FFT window should we use? how fast should the tone be adjusted? peak or avg band energy?

* Useful libs: scipy.fft, nnumpy.fft, scipy.signal (filters)

### Demos
A loose collection of tests for various ideas that help calcify various class topics.

Current content:
* Demo.py - learned some quick cool, painful lessons about how to make importable modules for use in programs outside of a given directory.
* FFT.py - a short program that analyzes the waveform vs frequency responses in a graphical format.

### Utilites
Collection of importable modules that serve basic functions (such as reading in a wav file) so that I don't have to keep writing the same lines of code.

### Future
*Pending: student's tears
