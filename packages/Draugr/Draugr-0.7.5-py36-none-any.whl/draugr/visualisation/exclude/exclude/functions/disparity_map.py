#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'

import cv2
from matplotlib import pyplot as plt


def disparity_map():
  imgL = cv2.imread('/home/heider/Datasets/disparity/tsukuba_l.png', 0)
  imgR = cv2.imread('/home/heider/Datasets/disparity/tsukuba_r.png', 0)

  stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
  disparity = stereo.compute(imgL, imgR)
  pyplot.imshow(disparity, 'gray')
  pyplot.show()


if __name__ == '__main__':
  disparity_map()
