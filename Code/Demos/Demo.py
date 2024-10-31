'''
Frank Claverie
CS 416P
Fall 2024
'''

# Minor wizardry to include utility file
import sys, os, random
utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Utilities"))
sys.path.append(utils_path)

import BasicUtils as utils



if __name__ == "__main__":
    index, wav_file = random.choice(list(utils.wav_files.items()))
    print(wav_file)
    data = utils.load_wav(wav_file)
    utils.play_sound(data)
    utils.plot_sound(data)