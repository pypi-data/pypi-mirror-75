#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.animation as animation
from matplotlib import pyplot
import numpy
from matplotlib.mlab import window_none
from matplotlib.pyplot import specgram

__author__ = 'Christian Heider Nielsen'


def main7():
  ############### Constants ###############
  SAMPLES_PER_FRAME = 20

  overlap = 2
  delta = 0.01
  nfft = 32
  # freq_center = 4
  low = -10
  high = 10
  sampling_frequency = int(1.0 / delta)  # the sampling frequency
  window_length = 1

  def get_sample(t):
    nse = numpy.random.random_integers(low=low, high=high, size=nfft)

    data = nse  # the signal
    return data

  def get_specgram(signal, rate):
    arr2D, freqs, bins, *_ = specgram(signal,
                                      window=window_none,
                                      Fs=rate,
                                      NFFT=nfft,
                                      noverlap=overlap,
                                      scale='linear',
                                      # Fc=freq_center,
                                      sides='twosided',
                                      cmap=pyplot.cm.bone
                                      )
    return arr2D, freqs, bins

  '''
  update_fig:
  updates the image, just adds on samples at the start until the maximum size is
  reached, at which point it 'scrolls' horizontally by determining how much of the
  data needs to stay, shifting it left, and appending the new data. 
  inputs: iteration number
  outputs: updated image
  '''

  def update_fig(n):
    data = get_sample(n)
    arr2D, freqs, bins = get_specgram(data, sampling_frequency)
    im_data = im.get_array()
    if n < SAMPLES_PER_FRAME:
      im_data = numpy.hstack((im_data, arr2D))
      im.set_array(im_data)
    else:
      keep_block = arr2D.shape[1] * (SAMPLES_PER_FRAME - 1)
      im_data = numpy.delete(im_data, numpy.s_[:-keep_block], 1)
      im_data = numpy.hstack((im_data, arr2D))
      im.set_array(im_data)
    return im

  fig = pyplot.figure()
  data = get_sample(0)
  arr2D, freqs, bins = get_specgram(data, sampling_frequency)
  extent = (bins[0],
            bins[-1] * SAMPLES_PER_FRAME,
            freqs[-1],
            freqs[0])

  im = pyplot.imshow(arr2D,
                     aspect='auto',
                     extent=extent,
                     interpolation="none",
                     cmap=pyplot.cm.bone,
                     # norm=LogNorm(vmin=.01, vmax=1)
                     )

  pyplot.xlabel('Step')
  pyplot.ylabel('Action Index')
  pyplot.title('Episode')
  # pyplot.gca().invert_yaxis()
  # pyplot.colorbar()

  anim = animation.FuncAnimation(fig,
                                 update_fig,
                                 blit=False,
                                 fargs=(),
                                 interval=delta * SAMPLES_PER_FRAME)

  try:
    pyplot.show()
  except:
    print("Plot Closed")


if __name__ == '__main__':
  main7()
