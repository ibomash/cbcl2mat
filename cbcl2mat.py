#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Download the CBCL face image data set, and convert it to MATLAB format"""

import os
import sys
import glob
import time

import numpy as np
import scipy.io
import Image


def read_image(fn):
    """Read an image from file and return it as an array"""
    img = Image.open(fn)
    return np.asarray(img)


def main():
    ## Download the data file and unzip it
    print '** Downloading data set'
    os.system('wget http://cbcl.mit.edu/projects/cbcl/software-datasets/faces.tar.gz')

    print '** Uncompressing data set'
    os.system('tar xvzf faces.tar.gz')
    os.system('tar xvzf face.train.tar.gz')

    ## Read face and non-face filenames
    face_fns = glob.glob('train/face/*.pgm')
    nonface_fns = glob.glob('train/non-face/*.pgm')
    nfaces = len(face_fns)
    nnonfaces = len(nonface_fns)
    nexamples = nfaces + nnonfaces
    print 'Total images: {0} ({1} face, {2} non-face)'.format(nexamples, nfaces, nnonfaces)

    ## Make output arrays
    # We know that these examples are 19x19
    images = np.empty((19, 19, nexamples), dtype='uint8')
    labels = np.empty((nexamples,), dtype='bool')
    labels[:nfaces] = True
    labels[nfaces:] = False

    ## Read images
    t_start = time.time()
    for iimage, image_fn in enumerate(face_fns + nonface_fns):
        images[:, :, iimage] = read_image(image_fn)
    t_end = time.time()
    t_elapsed = t_end - t_start
    print 'Read {0} images in {1} second(s) ({2:.1f} images/sec)'.format(nexamples, int(t_elapsed),
                                                                         nexamples / t_elapsed)

    ## Write to MATLAB format
    scipy.io.savemat('images.mat', dict(images=images, labels=labels),
                     oned_as='column')

    return 0


if __name__ == '__main__':
    sys.exit(main())
