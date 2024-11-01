'''
Frank Claverie
CS 416P
Fall 2024
'''


'''
This was a weird lesson to learn. 
Basically I needed to create a .env in the root directory for this project containing
    the line "UTILPATH=./Code/Utilities", which allowed the python interpreter to recognize
    Utilites as a module directory.
    Additionally I needed to created an empty file called "__init__.py" to specifically
    flag this info.

Likewise, to make VSCode recognize and give me context for my modules I had to 
    include the following lines in my settings.json:
    "python.analysis.extraPaths": ["./Code/Utilities"],
    "python.envFile": "${workspaceFolder}/.env"
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