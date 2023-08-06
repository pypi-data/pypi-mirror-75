#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 01/03/2020
           """

from abc import abstractmethod
from typing import Dict, Tuple

from torch.utils.data import Dataset

__all__ = ["SupervisedDataset"]

from draugr.torch_utilities.datasets.supervised.splitting import Split, SplitByPercentage
from warg import drop_unused_kws


class SupervisedDataset(Dataset):
  """

"""

  @drop_unused_kws
  def __init__(self):
    pass

  @property
  def split_names(self) -> Dict[Split, str]:
    """

:return:
:rtype:
"""
    return SplitByPercentage.default_split_names

  @property
  @abstractmethod
  def response_shape(self) -> Tuple[int, ...]:
    """

"""
    raise NotImplementedError

  @property
  @abstractmethod
  def predictor_shape(self) -> Tuple[int, ...]:
    """

"""
    raise NotImplementedError

  @abstractmethod
  def __len__(self):
    raise NotImplementedError

  @abstractmethod
  def __getitem__(self, index):
    raise NotImplementedError


if __name__ == "__main__":
  print(SplitByPercentage(521))
  print(SplitByPercentage(2512).unnormalised(123))
