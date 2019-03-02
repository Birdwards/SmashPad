import sys

byte_data = open(sys.argv[1] , 'rb').read()

if ord(byte_data[0]) != 40 or ord(byte_data[1]) != 181 or ord(byte_data[2]) != 47 or ord(byte_data[3]) != 253:
    sys.exit("Error: The file you are trying to pad does not appear to have been compressed with zstd. Please compress it with zstd before using this tool.")

target_size = int(sys.argv[2], 16)
pad_size =  target_size - len(byte_data)

if pad_size < 0:
    sys.exit("Error: Your file is larger than the size you want it to be. Compress it to a smaller size first.")
elif pad_size == 0:
    sys.exit("Error: Your file is already the right size!")
elif pad_size == 1 or pad_size == 2 or pad_size == 5:
    sys.exit("Error: Sorry, but this technique doesn't work on files that are exactly 1, 2, or 5 bytes smaller than they need to be. Try compressing it to a smaller size first.")

start_index = 6
if ord(byte_data[4]) >= 192:
    start_index = 13
elif ord(byte_data[4]) >= 128:
    start_index = 9
elif ord(byte_data[4]) >= 64:
    start_index = 7

out = open(sys.argv[1] + ".pad", 'w+b')
out.write(byte_data[0:start_index])

if pad_size % 3 == 0:
    for x in range(pad_size):
        out.write("\x00")
elif pad_size % 3 == 1:
    for x in range(pad_size-4):
        out.write("\x00")
    out.write("\x02\x00\x00\x00")
elif pad_size % 3 == 2:
    for x in range(pad_size-8):
        out.write("\x00")
    out.write("\x02\x00\x00\x00\x02\x00\x00\x00")
    
out.write(byte_data[start_index:])
out.close()

print "File successfully padded to " + hex(target_size) + " bytes!"
