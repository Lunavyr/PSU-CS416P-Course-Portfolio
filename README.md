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

### Future
*Pending: student's tears
