# Engineering notebook
Frank Claverie<br>
CS 416P<br>
Fall 2024
## Purpose:
To document my progress and process throughout the term.

## Entries:

### 10/1/2024
Established github repository and prepared body for term-long suffering =')

### 10/8/2024
Started on assignment 1.

This assignment seeks to have us create sine audio data and export it as a wav.
Additionally, the program must also play back the created audio data.

I began by creating the two required audio datum. 
I also created two helper functions to analyze the waveform and extract meta-data from the wav files for my own amusement.

### 10/29/2024
Began compiling personal notes in my own terms from the course (mostly for quick access for use in projects)

### 10/30/2024
Continued compiling notes to date and began structuring code directory to create some general utilites relating to analyzing and playing .wav files. Also added some stock of sample sounds generated with Ableton. Also making a file in a different directory able to be imported to another file in python is kinda tricky. BUT! I got it working, and VSCode even gives me that sweet juicy syntax highlighting for my own code =D

Also also - started work on the adaptive tone control project. With the utils in place, I should have the basic boilerplate ready to go!

### 10/31/2024
Made a program "FFT.py" to import an arbitrary wav file and analyze the resulting waveform array with an array corresponding to it's frequency responses. Plotted both against time in seconds and frequency in hz, respectively.