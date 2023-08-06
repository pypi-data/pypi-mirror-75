#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 07/07/2020
           '''

if __name__ == '__main__':
  # helper function
  def select_n_random(data, labels, n=100):
    '''
    Selects n random datapoints and their corresponding labels from a dataset
    '''
    assert len(data) == len(labels)

    perm = torch.randperm(len(data))
    return data[perm][:n], labels[perm][:n]

  # select random images and their target indices
  images, labels = select_n_random(trainset.data, trainset.targets)

  # get the class labels for each image
  class_labels = [classes[lab] for lab in labels]

  # log embeddings
  features = images.view(-1, 28 * 28)
  writer.add_embedding(features,
                       metadata=class_labels,
                       label_img=images.unsqueeze(1))
  writer.close()
