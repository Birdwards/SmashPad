# SmashPad v0.1
# by Birdwards and NyxTheShield

import sys
import zstandard as zstd

if len(sys.argv) != 3:
    sys.exit("Error: Wrong number of arguments\n\nHow to use this tool:\npython smashpad.py [input] [size]\n[input] = Name of the file to compress and/or pad\n[size] = Desired size of the compressed file, in hexadecimal\n\nExample:\npython smashpad.py ui_spirits_battle_db.prc 0x140CD")

uncomp_file = open(sys.argv[1] , 'rb').read()
target_size = int(sys.argv[2], 16)
lvl = 1

# Compress uncomp_file to smaller than target_size
print("Finding small enough compression level...")
while True:
    cctx = zstd.ZstdCompressor(level=lvl)
    byte_data = cctx.compress(uncomp_file)
    comp_size = len(byte_data)

    pad_size =  target_size - comp_size

    print("Level " + str(lvl) + ": file compressed to " + hex(comp_size) + " bytes")
    if pad_size < 0 or pad_size == 1 or pad_size == 2 or pad_size == 5:
        lvl+=1
        if lvl > 22:
            sys.exit("Error: File cannot be compressed to the required size")
    else:
        break
print("Padding file at compression level " + str(lvl) +  "...")

# Get the Frame_Header_Descriptor from the compressed file's first Frame_Header
# This is the only step that differs between Python 2 and 3
# For more info on how Frame_Header_Descriptor works, see:
# https://tools.ietf.org/html/rfc8478#section-3.1.1.1
if sys.version_info[0] >= 3:
    fhd = byte_data[4]
else:
    fhd = ord(byte_data[4])

# Read Frame_Content_Size_Flag to find the length of the Frame_Header
start_index = 6
if fhd >= 192:
    start_index = 13
elif fhd >= 128:
    start_index = 9
elif fhd >= 64:
    start_index = 7

# Dictionary_ID_Flag also affects Frame_Header length. I think this is always 0 by default, but I'm including it just in case
if fhd % 4 == 1:
    start_index += 1
elif fhd % 4 == 2:
    start_index += 2
elif fhd % 4 == 3:
    start_index += 4

# Create output file and write entire Frame_Header to file
out = open(str(sys.argv[1] + ".pad"), 'w+b')
out.write(byte_data[0:start_index])

# Insert empty data blocks of 3-byte or 4-byte lengths to make up the difference between the compressed size and our target size 
if pad_size % 3 == 0:
    for x in range(pad_size):
        out.write(b"\x00")
elif pad_size % 3 == 1:
    for x in range(pad_size-4):
        out.write(b"\x00")
    out.write(b"\x02\x00\x00\x00")
elif pad_size % 3 == 2:
    for x in range(pad_size-8):
        out.write(b"\x00")
    out.write(b"\x02\x00\x00\x00\x02\x00\x00\x00")

# Write the rest of the data from the compressed file
out.write(byte_data[start_index:])
out.close()

print("File successfully padded to " + hex(target_size) + " bytes!")
