#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 07/07/2020
           '''

import torch
import torch.nn as nn


class SomeArch(nn.Module):
  def __init__(self):
    super().__init__()
    self.conv = nn.Conv2d(3, 10, 2, stride=2)
    self.relu = nn.ReLU()
    self.flatten = lambda x:x.view(-1)
    self.fc1 = nn.Linear(160, 5)
    self.seq = nn.Sequential(nn.Linear(5, 3), nn.Linear(3, 2))

  def forward(self, x):
    return self.seq(self.fc1(self.flatten(self.relu(self.conv(x)))))


model = SomeArch()
#loss_fn = torch.nn.CrossEntropyLoss()
loss_fn = torch.nn.MSELoss()
input1 = torch.randn(1, 3, 8, 8)
target = torch.randn(2)
#target = torch.empty(1, dtype=torch.long).random_(2)


def a():
  visualisation = {}

  def hook_fn(m, i, o):
    visualisation[m] = o

  def get_all_layers(net):
    for name, layer in net._modules.items():
      # If it is a sequential, don't register a hook on it
      # but recursively register hook on all it's module children
      if isinstance(layer, nn.Sequential):
        get_all_layers(layer)
      else:
        # it's a non sequential. Register a hook
        layer.register_forward_hook(hook_fn)

  get_all_layers(model)

  out = model(input1)

  # Just to check whether we got all layers
  print(visualisation.keys())  # output includes sequential layers


def forward():
  def printnorm(self, input, output):
    # input is a tuple of packed inputs
    # output is a Tensor. output.data is the Tensor we are interested
    print('Inside ' + self.__class__.__name__ + ' forward')
    print('')
    print('input: ', type(input))
    print('input[0]: ', type(input[0]))
    print('output: ', type(output))
    print('')
    print('input size:', input[0].size())
    print('output size:', output.data.size())
    print('output norm:', output.data.norm())

  model.fc1.register_forward_hook(printnorm)

  out = model(input1)


def backward():
  def printgradnorm(self, grad_input, grad_output):
    print('Inside ' + self.__class__.__name__ + ' backward')
    print('Inside class:' + self.__class__.__name__)
    print('')
    print('grad_input: ', type(grad_input))
    print('grad_input[0]: ', type(grad_input[0]))
    print('grad_output: ', type(grad_output))
    print('grad_output[0]: ', type(grad_output[0]))
    print('')
    print('grad_input size:', grad_input[0].size())
    print('grad_output size:', grad_output[0].size())
    print('grad_input norm:', grad_input[0].norm())

  model.fc1.register_backward_hook(printgradnorm)

  out = model(input1)
  err = loss_fn(out, target)
  err.backward()

if __name__ == '__main__':

  a()
  forward()
  backward()
