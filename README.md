Frank Claverie  
CS 416P  
Fall 2024

# CS 416P Programming Portfolio
This repository is the accumulation of all projects done in CS416p.  
Content is organized in subfolders according to the assignments, and a detailed log can be found in the Notebook.md

# Main Projects
## Assignment 1: Clipped Audio
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


## Adaptive tone control
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

Getting the program to work in the first place was challenging, but once all the pieces were properly in place, it simply became a matter of adjusting the function determining the gain. Presently I am calculating it by dividing the average energy by the absolute difference of band and average energies, then multiplying it by the index of the current band (1, 2, ..., etc) - THEN finally taking the square root. This seems to work pretty well, only introduces minor clipping, and I feel satisfied with my work!


## Wavetable Synthesizer
This project's objective is to create a wavetable synthesizer that is controllable with a USB MIDI controller.  
Presently, this program is configured to run with a Novation Launchkey mk4.  


Features:
* Wavetable Generation - program generates single phase arrays for each note in the midi sequence and saves them to a dictionary indexable with a midi note number.  
* Oscillator Class - using the generated wavetables, this class generates frame_count sized arrays of sounds that oscillates between the two generated wave types.
* Note Class - this is the functional interface between MIDI, sound, and output. This class handles note on and off events and applies an adjustable ADSR envelope to the sound generated in the Oscillator class.
* MIDI parsing function - for use in the output callback function; processes available notes and schedules notes to be played or finished.  
This method will also allow for dynamic control over the various global paramaters and feature integration with a sustain pedal... eventually...
* MIDI event listener using the "mido" package: this listens for midi events sent from controller and passes it to a queue for later processing in the audio callback function.
* Audio callback routine: this feature pulls midi events from the midi_queue and leverages all of the above to create sweet, sweet music.  

This project was a BEAST. I learned a lot and struggled A LOT. Im decently satisfied with it's functionality thus far. The sound generation is reasonably balanced, and the ADSR envelope functions well.  
Though, I get the feeling I'm gonna be working on this more in my free time. And I'd really like to introduce stereo output, filters on the saw waves (probably dynamic), compression, and delay eventually.

Also - a fun little consequence of the way I've structured this code: if the setting "global_fade" is set to True, the oscillator will manipulate a single variable set for an arbitrary number of notes, which means that the speed at which the sound oscillates between wave types increases for each consecutive note. It's kinda fun, and makes me significantly less annoyed that this fade effect isn't synchronized across notes.



# Auxillary Work
### Demos
A loose collection of tests for various ideas that help calcify various class topics.

Current content:
* Demo.py - learned some quick cool, painful lessons about how to make importable modules for use in programs outside of a given directory.
* FFT.py - a short program that analyzes the waveform vs frequency responses in a graphical format.
* MidiDemo.py - primarilly an attempt to wrangle midi data that turned into a barebones synthesizer.  
Provides a solid foundation for building a fully fledged synth, which is the next project!

### Utilites
Collection of importable modules that serve basic functions (such as reading in a wav file) so that I don't have to keep writing the same lines of code.

### Future
*Pending: student's tears
