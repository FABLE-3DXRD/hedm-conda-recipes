#!/usr/bin/env python

import argparse
import os
import shutil
import sys
import textwrap

import numpy as np
from scipy import ndimage

from ImageD11.connectedpixels import blobproperties, connectedpixels, s_1
import fabio

def filter_image(im, args):
    labels = np.zeros(im.data.shape, np.int)
    # determine which pixels in which peaks, how many peaks
    peaks = connectedpixels(im.data, labels, args.intensity_threshold, 0)
    # determine properties of each peak
    props = blobproperties(im.data, labels, peaks, 0)

    # don't understand how this next block works, and can't understand
    # the original comment:
    # number of pixels in peaks
    # labels go from 1->n with 0 being not in a peak...
    # ... so add an empty peak at zero to get match up
    npx = np.array([0,]+list(props[:, s_1]), np.int)
    npximage = np.take(npx, labels.ravel())
    npximage.shape = labels.shape
    data = np.where(
        npximage>args.pixel_threshold,
        args.max_intensity if args.max_intensity > 0 else im.data,
        0
        )

    #smoothing, why is this done three times?
    for j in range(args.gaussian_iterations):
        data = ndimage.gaussian_filter(data, args.gaussian_filter)
    im.data = data.astype('uint16')


def filter_images(args):
    fmtstr = '%s%0' + str(args.ndigits) + 'd' + args.extension
    for i in range(0, args.images):
	in_file = fmtstr % (args.stem, i+args.nstart)
	out_file = ('%s/' + fmtstr) % \
                   (args.output_dir,
                    os.path.split(args.stem)[-1],
                    i+args.nstart)
        im = fabio.open(in_file)
        if args.background:
            bg = fabio.open(args.background)
            im.data = im.data - bg.data
        if args.verbose:
            print('filtering %s' % in_file)
	filter_image(im, args)
        if os.path.exists(out_file) and not args.force:
            raise RuntimeError('Output file %s already exists' % out_file)
        im.write(out_file)


def main(args):
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    if args.images < 1:
        raise RuntimeError(
            'Number of images must be >= 1, %s specified' % args.images
            )
    if args.intensity_threshold < 0:
        raise RuntimeError(
            'Threshold must be > 0, %s specified' % args.intensity_threshold
            )
    if args.pixel_threshold < 0:
        raise RuntimeError(
            'Threshold must be > 0, %s specified' % args.pixel_threshold
            )

    # identify the file naming convention:
    ndigits = None
    for i in range(7):
        fmtstr = '%s%0' + str(i) + 'd.tif'
        first_tif_name = fmtstr % (args.stem, args.nstart)
        first_tiff_name = first_tif_name + 'f'
        if os.path.exists(first_tif_name):
            args.ndigits = i
            args.extension = '.tif'
            break
        elif os.path.exists(first_tiff_name):
            args.ndigits = i
            args.extension = '.tiff'
            break
    else:
        raise RuntimeError(
            'File name convention not recognized. Expected %s%0Nd.tif'
            )

    if args.verbose:
        print('Saving directory: %s/' % args.output_dir)
        print('Background file name: %s' % args.background)
        print('Number of images to filter: %i' % args.images)

    filter_images(args)


if __name__=='__main__':

    parser = argparse.ArgumentParser(
        prog='filter_images.py',
        description='Filters images according to provided threshold.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
            example:

            $ filter_images.py NF_data/a 20 750 -v
            ''')
        )
    parser.add_argument(
        'stem', type=str, help='image file stem'
        )
    parser.add_argument(
        'nstart', type=int, help='number of first image to filter'
        )
    parser.add_argument(
        'images', type=int, help='number of images to filter'
        )
    parser.add_argument(
        '-f', '--force', action='store_true',
        help='force overwriting existing data'
        )
    parser.add_argument(
        '-i', '--intensity-threshold', type=int, default=25,
        help='intensity threshold'
        )
    parser.add_argument(
        '-p', '--pixel-threshold', type=int, default=25,
        help='number of pixels for signal'
        )
    parser.add_argument(
        '-m', '--max-intensity', type=int, default=10,
        help='truncate output intensity if >= 1'
        )
    parser.add_argument(
        '-o', '--output-dir', type=str, default='filtered',
        help='output directory'
        )
    parser.add_argument(
        '-g', '--gaussian-filter', type=float, default=1,
        help='Gaussian filter threshold'
        )
    parser.add_argument(
        '--gaussian-iterations', type=int, default=3, choices=range(1,10),
        help='number of gaussian filter iterations'
        )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='report progress in terminal'
        )
    parser.add_argument(
        '-b', '--background', type=str, help='background file and directory'
        )
    args = parser.parse_args()
    main(args)
