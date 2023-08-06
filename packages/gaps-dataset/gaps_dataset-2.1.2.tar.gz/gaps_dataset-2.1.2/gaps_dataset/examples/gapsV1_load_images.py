"""
Created on 2017/08/15
Last update 2019/09/11

@author: Markus Eisenbach, Ronny Stricker
Example for downloading images of GAPs v1 dataset and usage.
"""

from gaps_dataset import gaps
import zipfile
import os
import numpy as np
import cv2

# change these parameters:
destination_directory = '/your/download/destination/directory'
login = 'yourlogin'

# download images and patch references
gaps.download(login=login,
              output_dir=destination_directory,
              version=1,
              patchsize='images',
              debug_outputs=True)

# unzip images
basedir = os.path.join(destination_directory, 'v1', 'images')

zip_filename = os.path.join(basedir, 'images.zip')
zip_ref = zipfile.ZipFile(zip_filename, 'r')
zip_ref.extractall(basedir)
zip_ref.close()

# load patch references for training subset
ref_filename = os.path.join(basedir, 'patch_references_train.npz')
patch_ref = np.load(ref_filename)['data'].astype(int)

# get patches from images
n_patches = patch_ref.shape[0]    # number of patches
image_template = os.path.join(basedir, 'images', 'train_{:04d}.jpg')

for patch_index, patch_info in enumerate(patch_ref):
    # get information for this patch
    image_index, row, col, mirror_state, binary_label, class_label = patch_info
    # load image containing this patch
    image_filename = image_template.format(image_index)
    image = cv2.imread(image_filename)
    # extract patch from image
    patch = image[row:row + 64, col:col + 64]
    # mirroring
    if mirror_state == 0:    # flip rows
        patch = patch[::-1, :]
    elif mirror_state == 1:    # flip cols
        patch = patch[:, ::-1]
    # binary_label:
    #    0 = intact road,
    #    1 = distress
    # class_label:
    #    0 = intact road,
    #    1 = applied patch,
    #    2 = pothole,
    #    3 = inlaid patch,
    #    4 = open joint,
    #    5 = crack

# replace train with valid or test respectively to extract patches of the other subsets
