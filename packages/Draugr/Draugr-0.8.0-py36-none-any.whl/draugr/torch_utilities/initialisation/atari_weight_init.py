#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import torch

from draugr.torch_utilities.initialisation.ortho_weight_init import ortho_weights

__author__ = "Christian Heider Nielsen"

import numpy

__all__ = ["atari_initializer", "initialize_parameters"]


def atari_initializer(module: torch.nn.Module):
    """ Parameter initializer for Atari models

Initializes Linear, Conv2d, and LSTM weights.
"""
    classname = module.__class__.__name__

    if classname == "Linear":
        module.weight.data = ortho_weights(
            module.weight.data.size(), scale=numpy.sqrt(2.0)
        )
        module.bias.data.zero_()

    elif classname == "Conv2d":
        module.weight.data = ortho_weights(
            module.weight.data.size(), scale=numpy.sqrt(2.0)
        )
        module.bias.data.zero_()

    elif classname == "LSTM":
        for name, param in module.named_parameters():
            if "weight_ih" in name:
                param.data = ortho_weights(param.data.size(), scale=1.0)
            if "weight_hh" in name:
                param.data = ortho_weights(param.data.size(), scale=1.0)
            if "bias" in name:
                param.data.zero_()


def initialize_parameters(m: torch.nn.Module) -> None:
    """

    :param m:
    :type m:
    """
    classname = m.__class__.__name__
    if classname.find("Linear") != -1:
        m.weight.data.normal_(0, 1)
        m.weight.data *= 1 / torch.sqrt(m.weight.data.pow(2).sum(1, keepdim=True))
        if m.bias is not None:
            m.bias.data.fill_(0)
