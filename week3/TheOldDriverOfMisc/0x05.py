#!/usr/bin/env python
# -*- coding:utf-8 -*-
import base64
import zlib

from PIL import Image
from numpy import *

__author__ = 'Aklis'
Flag = 'hctf{erg0uzhenbang!!!POIIII!!!}'
Mi_Message = '1111111111111111111111111111111111110000000110110011010011001100000001101111101011001101101000001011111011010001010000000110010110010100010110100010110001011101000100101000101101000101011111110111010001010001011011111010010100011101011110111110110000000101010101010101010100000001111111111001101011010100111111111111001011001101111000011100010001001111111111111001100110100010100100101111010001000110000110101101111011011001111110111101011111010110110101111101010111110110110111101000111001101000011010000101000101110010101011001111000011010000110010001101001111011111010010110100000001110011011110111100100010100000010001000111011001000111001111010111010011111111111000000000111100010111111100100001101001011111010100101100011011110011100111001000010010110101001010111111010101010100100001111110000111001100100000101000010100101101110011011101000101000011001010001001000100110110110111101100010100110000011111111111111011010000010000101110101011000000010110100010111001010100101110111110111001000101100010111011011101000101100100100100001100000111111010001010111000010011001000100110110100010110000100010100110011000101101111101001101100011101001000111111000000010111011010100001010001101111111111111111111111111111111111111'


def main(origin, message, output):
    compressed = zlib.compress(message, 2)
    encode_compressed = base64.b64encode(compressed)
    # print encode_compressed
    with Image.open(origin) as f:
        assert f.width * f.height * 3 > len(encode_compressed) * 8
        img_size = f.size
        img_data = f.tobytes('raw', 'RGB')
        # img_arr = array(f)
        # print img_arr

    merge = ''.join(chr(i) for i in distribute(encode_compressed, img_data))
    output_data = merge + img_data[len(encode_compressed) * 8:]
    output_img = Image.frombytes(mode='RGB', size=img_size, data=output_data)
    # print array(output_img)
    output_img.save(output)


def distribute(message, img_data):
    start = -8
    for character in message:
        start += 8
        for offset in xrange(8):
            bit = (ord(character) >> (7 - offset)) & 1
            yield ((ord(img_data[start + offset]) & 0xFE) | bit)


def lsb_decode(img):
    with Image.open(img) as f:
        img_data = f.tobytes()
    for i in img_data:
        yield (ord(i) & 1)


def get_the_message(img):
    message = ''.join([str(i) for i in lsb_decode(img)])
    encode = tostr(message)
    result = zlib.decompress((base64.b64decode(encode)))
    if result.endswith(Mi_Message):
        print "Yes"
    else:
        print "Something Happened!"


def tostr(message_string):
    res = ''
    for i in xrange(0, len(message_string), 8):
        res += chr(int(message_string[i:i + 8], 2))
    return res


if __name__ == '__main__':
    main('ergou.png', Flag + Mi_Message, 'output.png')
    get_the_message('output.png')
