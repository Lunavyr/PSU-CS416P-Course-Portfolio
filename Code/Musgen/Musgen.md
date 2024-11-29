# Popgen
Document Highlighting the improvements made.


## Setup:
I opted to break apart individual components of this program to help me be able to focus on a single part at a time.  
Additionally, this improves readability and modularity. Plus I like classes and abstraction!

## Improvements:
1. Added harmony part (comprised of chords relative to root and can play inversions on non-beat rythms) which plays on all beats after 1

2. Different sound for melody and harmony and bass (flute, bell, string) with added filter for each sound generator made with additive synthesis

3. Added functionality to change number of beats per par as an argument that can be passed to the command line (default = 3)

4. Allowed all sounds to generate array segments relative to number of notes per beat (allows for quarter, eight, triplet, and technically arbitrary n-tuplets)

5. Added various chord types and progression patterns