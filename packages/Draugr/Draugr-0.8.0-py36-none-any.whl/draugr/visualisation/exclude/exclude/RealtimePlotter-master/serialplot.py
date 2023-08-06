#!/usr/bin/env python3
'''
Real-time plot demo using serial input

Copyright (C) 2015 Simon D. Levy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
'''

from threading import Thread

import serial
from realtime_plot import RealtimePlotter

# Change these to suit your needs
PORT = '/dev/ttyACM0'
BAUD = 115200
RANGE = (-1, +1)


class SerialPlotter(RealtimePlotter):

  def __init__(self):
    RealtimePlotter.__init__(self, [RANGE],
                             window_name='Serial input',
                             yticks=[RANGE],
                             styles=['b-'])

    self.xcurr = 0
    self.ycurr = 0

  def getValues(self):
    return (self.ycurr,)


def _update(port, plotter):
  msg = ''

  while True:

    c = port.read().decode()

    if c == '\n':
      try:
        plotter.ycurr = float(msg)
      except:
        pass
      msg = ''
    else:
      msg += c

    plotter.xcurr += 1


if __name__ == '__main__':

  try:
    port = serial.Serial(PORT, BAUD)
  except serial.SerialException:
    print('Unable to access device on port %s' % PORT)
    exit(1)

  plotter = SerialPlotter()

  thread = Thread(target=_update, args=(port, plotter))
  thread.daemon = True
  thread.start()

  plotter.start()
