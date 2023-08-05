from abc import ABCMeta

import numpy as np

import dask.array as da
from ..stategies import SingleLabelIndexQuery
from ...core.misc import randperm

__all__ = ['QueryInstanceRandom']


# ----------------------------------------------------------------------------------------------------------------------
# Random Sampling Strategy
# ----------------------------------------------------------------------------------------------------------------------
class QueryInstanceRandom(SingleLabelIndexQuery, metaclass=ABCMeta):
    """
    Randomly sample a batch of indexes from the unlabeled indexes.
    """

    @property
    def query_function_name(self):
        return "InstanceRandom"

    def select(self, X, y, label_index, unlabel_index, batch_size=1):
        """
        Select indexes randomly

        Parameters
        ----------
        :param X: array
            The [n_samples, n_features] training samples with n-features per instance.
        :param y: array
            The The [n_samples] label vector.
        :param label_index: object
            Add this parameter to ensure the consistency of api of strategies.
            Please ignore it.
        :param unlabel_index: collections.abc.Iterable
            The indexes of unlabeled set.
        :param batch_size:

        Return
        -------
        :return selected_idx: list
            The selected indexes which is a subset of unlabel_index.
        """

        super().select(X, y, label_index, unlabel_index, batch_size=batch_size)

        if len(unlabel_index) <= batch_size:
            return np.array(unlabel_index)

        tpl = da.from_array(unlabel_index.index)
        return tpl[randperm(len(unlabel_index) - 1, batch_size)].compute()

    def _select_by_prediction(self, unlabel_index, predict, batch_size=1, **kwargs):
        pass