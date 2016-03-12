#!/usr/bin/env python
from __future__ import print_function

import argparse
import os
import textwrap

import numpy as np
import tifffile


def load_ge2(
    filename, image=0, shape=(2048,2048), dtype='uint16', byteoffset=8192,
    byteorder='=', bytegap=0, summed=False, **kwargs
    ):
    """reads a binary image from a file and returns a 3D numpy array"""

    # create a numpy dtype instance so we can inspect its width
    # and determine the image size
    dt = np.dtype(dtype)
    dt.newbyteorder(byteorder)
    bytes_per_image = dt.itemsize * np.prod(shape)

    with open(filename, 'rb') as f:
        f.seek(byteoffset + image * (bytes_per_image + bytegap))
        res = np.frombuffer(f.read(bytes_per_image), dtype=dt)
        if summed:
            res = res.astype('uint32')
            while 1:
                try:
                    res += np.frombuffer(f.read(bytes_per_image), dtype=dt)
                except ValueError:
                    break
    res.shape = shape
    return res


class AdeptFileIter(object):

    def __init__(self, obj):
        self._obj = obj
        self._index = -1
        self._stop = len(obj)

    def next(self):
        self._index += 1
        if self._index >= self._stop:
            raise StopIteration
        return self._obj[self._index]


class AdeptFile(object):

    def __init__(self, filename):
        self._fn = filename
        self._len = (os.path.getsize(filename) - 8192) / (2048 * 2048 * 2)

    def __iter__(self):
        return AdeptFileIter(self)

    def __getitem__(self, val):
        return load_ge2(self._fn, val)

    def __len__(self):
        return self._len

    @property
    def filename(self):
        return self._fn


def main(args):
    tiff_fileno = args.filenumber
    for arg in args.ge2:
        if not arg.endswith('.ge2'):
            if args.verbose:
                print('Skipping %s, file format not recognized.' % (arg))
                continue
        if args.dezing:
            raise NotImplementedError('dezinging has not been implemented')
            continue
        if args.summed:
            out = "%s.tif" % (arg.rsplit('.ge2', 1)[0])
            if os.path.exists(out):
                if args.verbose:
                    print('Skipping %s, %s already exists' % (arg,out))
                    continue
            if args.verbose:
                print('Converting %s to %s'% (arg, out), end='\n')
            tifffile.imsave(out, load_ge2(arg, summed=args.summed))
            if args.delete:
                os.remove(arg)
                if args.verbose:
                    print('Removed %s' % arg)
        else:
            stem = args.output if args.output else arg.rsplit('.ge2', 1)[0]
            for i, d in enumerate(AdeptFile(arg)):
                out = '%s_%05d.tif' % (stem, tiff_fileno)
                if args.verbose:
                    print("saving image %d from %s as %s" % (i+1, arg, out))
                tifffile.imsave(out, d)
                tiff_fileno += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='ge2tiff.py',
        description='Converts ge2 files to tiff.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
            example:

            $ ge2tiff.py -v -o output_file_stem input1.ge2 input2.ge2 ...
            ''')
        )
    parser.add_argument(
        'ge2', metavar='ge2', type=str, nargs='+',
        help='reads Adept .ge2 files and writes .tiff files'
        )
    parser.add_argument(
        '-S', '--summed', action='store_true',
        help='returns the sum of all images in file'
        )
    parser.add_argument(
        '-D', '--delete', action='store_true',
        help='deletes original .ge2 file after conversion'
        )
    parser.add_argument(
        '-o', '--output', type=str, help='output file stem'
        )
    parser.add_argument(
        '-n', '--filenumber', type=int, default = 1,
        help='starting file number for tiff output'
        )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='report progress in terminal'
        )
    parser.add_argument(
        '-z', '--dezing', action='store_true',
        help='return a dezinged summed image (not implemented, ha!)'
        )
    main(parser.parse_args())
