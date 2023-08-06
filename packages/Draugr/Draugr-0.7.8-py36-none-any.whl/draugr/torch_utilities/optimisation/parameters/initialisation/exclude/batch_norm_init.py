#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 28/07/2020
           '''

__all__ = []

from torch import nn
from torch.nn import Module


def batch_norm_init(model:Module)->None:
  for m in model.modules():
    if isinstance(m, nn.BatchNorm2d):
      nn.init.constant_(m.weight, 1)
      nn.init.constant_(m.bias, 0)


if __name__ == '__main__':
    bn= nn.BatchNorm2d(3)
    print(bn.weight,bn.bias)
    batch_norm_init(bn)
    print(bn.weight,bn.bias)
