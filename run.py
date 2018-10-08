#!/usr/bin/env python

''' run.py: convert screenshots into a long image '''

__author__ = '-T.K.-'

import os
import cv2
import numpy as np

folder_name = 'imgs'

def read_files():
    ''' sort the imgs according to the time last modified '''
    files = []
    for file in list(os.walk(folder_name))[0][-1]:
        filename = os.path.join(folder_name, file)
        stats = os.stat(filename)
        files.append((stats.st_ctime_ns, filename))
    files.sort()
    return files

def crop_top(img):
    crop_height = 128
    for i in range(1, img.shape[0]):
        if (img[i, :, :] == (235, 235, 235)).all():
            crop_height = i
            break
    img = img[crop_height:, :, :]
    return img


def crop_bottom(img):
    crop_height = 100
    for i in range(1, img.shape[0]):
        if (img[-i, :, :] == (235, 235, 235)).all():
            crop_height = i
            break
    img = img[:-crop_height, :, :]
    return img

def run():
    files = read_files()

    res_img = crop_bottom(cv2.imread(files[0][1]))
    files.remove(files[0])
    
    for t, filepath in files:
        img = cv2.imread(filepath)
        img = crop_top(img)
        img = crop_bottom(img)
        res_img = np.append(res_img, img, axis=0)

    cv2.imwrite('result.png', res_img)

if __name__ == '__main__':
    run()
