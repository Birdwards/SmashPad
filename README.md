# SmashPad
Tool to compress and pad SSBU mods to the correct file size
by Birdwards and NyxTheShield

All files in Super Smash Bros. Ultimate are compressed using the zstd format. Any modded files need to be compressed to the same exact size as the game's original compressed file. This Python script can do that for you.

## Requirements

- [Python 3](https://www.python.org/) (or Python 2.7)
- [zstandard Python library](https://pypi.org/project/zstandard/) (can be installed with `pip install zstandard`; if you don't have pip, see [here](https://pip.pypa.io/en/stable/installing/))
- [CrossArc](https://github.com/Ploaj/ArcCross/) with updated hashes.txt from [here](https://github.com/ultimate-research/archive-hashes/)

## Instructions

### Compression

1. Install all of the above required software.
2. Download smashpad.py from this page.
3. Extract a game file using CrossArc and mod it to your liking (if you haven't already). Make note of what CrossArc says is the "Comp Size" of the file; you'll need it for step 5.
4. Place the modded file in the same folder as smashpad.py (or somewhere nearby).
5. In Command Prompt (Windows) or Terminal (macOS), navigate to the folder containing smashpad.py, then type the following:
   - `python smashpad.py [input] [size] [output]`
   - Replace `[input]` with the name of the modded file (or the path to the file if it's not in the same folder).
   - Replace `[size]` with the comp size of the file as shown in CrossArc (see step 3). Enter the comp size as you see it (in hexadecimal); don't convert it to a decimal number.
   - Replace `[output]` with the name you want your new compressed file to have. This is optional; if you don't care, leave it blank.
   - Example: `python smashpad.py ui_spirits_battle_db.prc 0x140CD 0x103B7D0B8.prc`
   - If you receive `Error: File cannot be compressed to the required size`, then your modded file is too large or complex to be compressed to the same size as the original file.
6. Look in the folder that contains your input file. You should see a compressed file, padded to your specified size, with the file name you specified in the previous step. If you didn't specify a file name, the compressed file will have the same name as your input file, but with `.pad` added to the end. 
7. Install the compressed file using your preferred install tools.
8. Have fun!

### Decompression

SmashPad can now decompress any file that was compressed with it (or that was compressed with any ZStandard implementation). To decompress, follow steps 1-6 for compression, except in step 5, replace `[size]` with the word `decomp`. If you don't specify an output file name, your decompressed file will have the same name as your input file, but with `.orig` added to the end.

Example: `python smashpad.py 0x103B7D0B8.prc decomp spirit_battles.prc`

