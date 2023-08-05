#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pathlib
from contextlib import suppress

import numpy
from matplotlib import pyplot

from draugr import PROJECT_APP_PATH
from draugr.writers.writer import Writer

__author__ = "Christian Heider Nielsen"
__doc__ = """
Created on 27/04/2019

@author: cnheider
"""
__all__ = ["TensorBoardXWriter"]

from warg import passes_kws_to


class TensorBoardXWriter(Writer):
    """

    """

    def _open(self):
        with suppress(FutureWarning):
            from torch.utils.tensorboard import SummaryWriter

            self.writer = SummaryWriter(str(self._log_dir), self._comment)
            return self

    def _close(self, exc_type=None, exc_val=None, exc_tb=None):
        self.writer.close()

    @passes_kws_to(Writer.__init__)
    def __init__(
        self, path=pathlib.Path.home() / "Models", comment: str = "", **kwargs
    ):
        super().__init__(**kwargs)

        self._log_dir = path
        self._comment = comment

    def _scalar(self, tag: str, value: float, step: int):
        self.writer.add_scalar(tag, value, step)

    def _graph(self, model, input_to_model):
        self.writer.add_graph(model, input_to_model)

    def histogram(self, tag: str, values: list, step: int):
        """

        :param tag:
        :type tag:
        :param values:
        :type values:
        :param step:
        :type step:
        """
        self.writer.add_histogram(tag, values, step, bins="auto")

    def bar(
        self,
        tag: str,
        values: list,
        step: int,
        yerr=None,
        x_labels=None,
        y_label="Probs",
        title="Action Categorical Distribution",
    ):
        """

        :param tag:
        :type tag:
        :param values:
        :type values:
        :param step:
        :type step:
        :param yerr:
        :type yerr:
        :param x_labels:
        :type x_labels:
        :param y_label:
        :type y_label:
        :param title:
        :type title:
        """
        fig = pyplot.figure()
        ind = numpy.arange(len(values))
        pyplot.bar(ind, values, yerr=yerr)
        if x_labels:
            pyplot.xticks(ind, labels=x_labels)
        else:
            pyplot.xticks(ind)

        pyplot.ylabel(y_label)
        pyplot.title(title)

        self.writer.add_figure(tag, fig, global_step=step, close=True)


if __name__ == "__main__":

    with TensorBoardXWriter(PROJECT_APP_PATH.user_log / "test") as w:
        w.scalar("What", 4)
