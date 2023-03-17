# raw_head_extractor.raw_head_reader created by bathy at 1/3/2023
from zlib import adler32
import struct

BLOCKSIZE=10485760-152


def calc_adler32(filename):
    asum = 0
    with open(filename,'rb') as f:
        header=f.read(152)
        header_list=list(header)
        header_list[-4:]=[0,0,0,0]
        header=bytearray(header_list)
        asum = adler32(header, asum)
        data = f.read(BLOCKSIZE)
        asum = adler32(data, asum)
        if asum < 0:
            asum += 2**32
    rev_asum=struct.unpack('<L',struct.pack('>L',asum))[0]
    return hex(rev_asum)[2:10].zfill(8).upper()


def read_adler32_checksum(raw_file):
    with open(raw_file, 'rb') as file_raw:
        file_header = file_raw.read(152)
        signature = file_header[:18]
        checksum = file_header[-4:]
    if signature == b'\x01\xA1\x46\x00\x69\x00\x6E\x00\x6E\x00\x69\x00\x67\x00\x61\x00\x6E\x00':
        return ''.join(format(n, '02X') for n in checksum)
    else:
        return 'Not Thermo Raw File'


def extract_header(raw_file):
    with open(raw_file, 'rb') as file_raw:
        file_header = file_raw.read(20000)
    file_info = file_header[1420:1600]
    print(file_info.hex())
    print(file_info.find(b'\x03\x00\x00\x00\x42\x00\x44\x00\x33\x00'))


if __name__ == '__main__':
    import sys, os

    if len(sys.argv)<2:
        print("Usage python3 raw_head_reader.py [path_to_raw_file]")
    else:
        file_path = str(sys.argv[1])
        if os.path.exists(file_path):
            print("Your input file checksum tag is: %s" % read_adler32_checksum(file_path))
            print("The checksum of your file is: %s" % calc_adler32(file_path))
            print(extract_header(file_path))