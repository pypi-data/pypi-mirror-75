#!/usr/bin/env python3
import io
from nutcracker.utils.funcutils import grouper, flatten

def descumm(data: bytes):
    print(data)

if __name__ == '__main__':
    import argparse
    import os
    import glob

    from .preset import sputm

    parser = argparse.ArgumentParser(description='read smush file')
    parser.add_argument('files', nargs='+', help='files to read from')
    args = parser.parse_args()


    files = set(flatten(glob.iglob(r) for r in args.files))
    print(files)
    for filename in files:

        print(filename)

        with open(filename, 'rb') as res:
            resource = res.read()[8:]

        descumm(resource)
