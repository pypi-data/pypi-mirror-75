#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 28/06/2020
           '''


def icnr_initialization(tensor):
  """ICNR initializer for checkerboard artifact free sub pixel convolution.

  Originally presented in
  `Checkerboard artifact free sub-pixel convolution: A note on sub-pixel convolution, resize convolution and convolution resize <https://arxiv.org/abs/1707.02937>`__
  Initializes convolutional layer prior to `torch.nn.PixelShuffle`.
  Weights are initialized according to `initializer` passed to to `__init__`.

  Parameters
  ----------
  tensor: torch.Tensor
          Tensor to be initialized using ICNR init.

  Returns
  -------
  torch.Tensor
          Tensor initialized using ICNR.

  """

  if self.upsample.upscale_factor == 1:
    return self.initializer(tensor)

  new_shape = [int(tensor.shape[0] / (self.upsample.upscale_factor ** 2))] + list(
    tensor.shape[1:]
    )

  subkernel = self.initializer(torch.zeros(new_shape)).transpose(0, 1)

  kernel = subkernel.reshape(subkernel.shape[0], subkernel.shape[1], -1).repeat(
    1, 1, self.upsample.upscale_factor ** 2
    )

  return kernel.reshape([-1, tensor.shape[0]] + list(tensor.shape[2:])).transpose(
    0, 1
    )
