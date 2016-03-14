#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

from PIL import Image
from numpy import *

__author__ = 'Aklis'


def convert2b(pixel_data):
    for i in pixel_data:
        for j in i:
            yield j & 1

def main(imagefile):
    with Image.open(imagefile) as f:
        t = array(f.convert('L'))
        print "".join([str(x) for x in convert2b(t)])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Error!"
    else:
        main(sys.argv[1])
