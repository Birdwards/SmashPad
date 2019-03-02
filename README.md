# SmashPad
Tool to compress and pad SSBU mods to the correct file size
by Birdwards and NyxTheShield

All files in Super Smash Bros. Ultimate are compressed using the zstd format. Any modded files need to be compressed to the same exact size as the game's original compressed file. This Python script can do that for you.

## Requirements

- [Python 3](https://www.python.org/) (or Python 2.7)
- [zstandard Python library](https://pypi.org/project/zstandard/) (can by installed with `pip install zstandard`; if you don't have pip, see [here](https://pip.pypa.io/en/stable/installing/))
- [CrossArc](https://github.com/Ploaj/ArcCross/) with updated hashes.txt from [here](https://github.com/ultimate-research/archive-hashes/)

## Instructions

1. Install all of the above required software.
2. Download smashpad.py from this page.
3. Extract a game file using CrossArc and mod it to your liking (if you haven't already). Make note of what CrossArc says is the "Comp Size" of the file; you'll need it for step 5.
4. Place the modded file in the same folder as smashpad.py (or somewhere nearby).
5. In Command Prompt (Windows) or Terminal (macOS), navigate to the folder containing smashpad.py, then type the following:
   - `python smashpad.py [input] [size]`
   - Replace `[input]` with the name of the modded file (or the path to the file if it's not in the same folder).
   - Replace `[size]` with the comp size of the file as shown in CrossArc (see step 3). Enter the comp size as you see it (in hexadecimal); don't convert it to a decimal number.
   - If you receive `Error: File cannot be compressed to the required size`, then your modded file is too large or complex to be compressed to the same size as the original file.
6. Install the modded file using your preferred install tools.
7. Have fun!
