# SmashPad v0.2
# by Birdwards and NyxTheShield

import sys
import zstandard as zstd

def comp(input_name, output_name, target_size):
    input = open(input_name, 'rb').read()
    
    # Compress uncomp_file to smaller than target_size
    print("Finding small enough compression level...")
    lvl = 1
    while True:
        cctx = zstd.ZstdCompressor(level=lvl)
        byte_data = cctx.compress(input)
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
        
    # Handle edge case for large files with Single_Segment_Flag unset
    if start_index > 6 and fhd % 64 < 32:
        start_index += 1

    # Dictionary_ID_Flag also affects Frame_Header length. I think this is always 0 by default, but I'm including it just in case
    if fhd % 4 == 1:
        start_index += 1
    elif fhd % 4 == 2:
        start_index += 2
    elif fhd % 4 == 3:
        start_index += 4

    # Create output file and write entire Frame_Header to file
    output = open(output_name, 'w+b')
    output.write(byte_data[0:start_index])

    # Insert empty data blocks of 3-byte or 4-byte lengths to make up the difference between the compressed size and our target size 
    if pad_size % 3 == 0:
        for x in range(pad_size):
            output.write(b"\x00")
    elif pad_size % 3 == 1:
        for x in range(pad_size-4):
            output.write(b"\x00")
        output.write(b"\x02\x00\x00\x00")
    elif pad_size % 3 == 2:
        for x in range(pad_size-8):
            output.write(b"\x00")
        output.write(b"\x02\x00\x00\x00\x02\x00\x00\x00")

    # Write the rest of the data from the compressed file
    output.write(byte_data[start_index:])
    output.close()

    print("File successfully padded to " + hex(target_size) + " bytes!")

def decomp(input_name, output_name):
    o = open(output_name, 'w+b')
    i = open(input_name, 'rb').read()
    dctx = zstd.ZstdDecompressor()
    
    for chunk in dctx.read_to_iter(i):
        o.write(chunk)
    
    n = o.tell()
    o.close()
    
    print("File successfully decompressed to " + hex(n) + " bytes!")

howto = "How to use this tool:\npython smashpad.py [input] [size] [output]\n[input] = Name of the file to be compressed/decompressed\n[size] = (if compressing) Desired size of the compressed file, in hexadecimal\n(if decompressing, just type \"decomp\" instead of [size])\n[output] = (optional) New name for the compressed/decompressed file\n\nExamples:\npython smashpad.py ui_spirits_battle_db.prc 0x140CD 0x103B7D0B8.prc\npython smashpad.py 0x103B7D0B8.prc decomp spirit_battles.prc"

# Main stuff
if len(sys.argv) <= 1:
    sys.exit("SmashPad 0.2\n\n" + howto)
elif len(sys.argv) == 3:    
    if sys.argv[2] == "decomp":
        decomp(sys.argv[1], str(sys.argv[1] + ".orig"))
    else:
        comp(sys.argv[1], str(sys.argv[1] + ".pad"), int(sys.argv[2], 16))
elif len(sys.argv) == 4:
    if sys.argv[2] == "decomp":
        decomp(sys.argv[1], sys.argv[3])
    else:
        comp(sys.argv[1], sys.argv[3], int(sys.argv[2], 16))
else:
    sys.exit("Error: Wrong number of arguments\n\n" + howto)

