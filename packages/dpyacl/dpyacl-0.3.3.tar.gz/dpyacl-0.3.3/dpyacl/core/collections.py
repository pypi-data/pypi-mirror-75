"""
The container to store indexes in active learning.
Serve as the basic type of 'set' operation.

Added distributed processing capabilities with Dask
"""
# Authors: Alfredo Lorie extended from Ying-Peng Tang version


import collections
import copy
import warnings
from abc import ABCMeta, abstractmethod

import numpy as np

from dpyacl.core.misc import randperm

__all__ = ['BaseCollection', 'IndexCollection', 'MultiLabelIndexCollection']


class BaseCollection(metaclass=ABCMeta):
    """
    The basic container of indexes.

    Functions include:
    1. Update new indexes.
    2. Discard existed indexes.
    3. Validity checking. (Repeated element, etc.)
    """
    _innercontainer = None
    _element_type = None

    def __contains__(self, other):
        return other in self._innercontainer

    def __iter__(self):
        return iter(self._innercontainer)

    def __len__(self):
        return len(self._innercontainer)

    def __repr__(self):
        return self._innercontainer.__repr__()

    @abstractmethod
    def add(self, *args):
        """Add element to the container."""
        pass

    @abstractmethod
    def discard(self, *args):
        """Discard element in the container."""
        pass

    @abstractmethod
    def update(self, *args):
        """Update multiple elements to the container."""
        pass

    @abstractmethod
    def difference_update(self, *args):
        """Discard multiple elements in the container"""
        pass

    def remove(self, value):
        """Remove an element. If not a member, raise a KeyError."""
        self.discard(value)

    def clear(self):
        """Clear the container."""
        self._innercontainer.clear()


class IndexCollection(BaseCollection, metaclass=ABCMeta):
    """
    Index Collection.

    Index Collection class is a basic data type of setting operation.
    Multiple different type of element is supported for Active learning.
    Also check the validity of given operation.
    Note that:
    1. The types of elements should be same
    1. If multiple elements to update, it should be a list, numpy.ndarray or IndexCollection
        object, otherwise, it will be cheated as one single_label element. (If single_label element
        contains multiple values, take tuple as the type of element.)
    Parameters
    ----------
    data : list or np.ndarray or object, optional (default=None)
        shape [n_element].  Element should be int or tuple.
        The meaning of elements can be defined by users.
        Some examples of elements:
        (example_index, label_index) for instance-label pair strategies.
        (example_index, feature_index) for feature strategies,
        (example_index, example_index) for active clustering;
        If int, it may be the index of an instance, for example.
    Attributes
    ----------
    index: list, shape (1, n_elements)
        A list contains all elements in this container.
    Examples
    --------
    >>> a = IndexCollection([1, 2, 3])
    >>> a.update([4,5])
    [1, 2, 3, 4, 5]
    >>> a.difference_update([1,2])
    [3, 4, 5]
    """

    def __init__(self, data=None):
        if data is None or len(data) == 0:
            self._innercontainer = []
        else:
            if isinstance(data, IndexCollection):
                self._innercontainer = copy.deepcopy(data.index)
                self._element_type = data.get_elementType()
                return
            if not isinstance(data, (list, np.ndarray)):
                data = [data]
            self._innercontainer = list(np.unique([i for i in data], axis=0))
            if len(self._innercontainer) != len(data):
                warnings.warn("There are %d same elements in the given data" % (len(data) - len(self._innercontainer)),
                              stacklevel=3)
            datatype = collections.Counter([type(i) for i in self._innercontainer])
            if len(datatype) != 1:
                raise TypeError("Different types found in the given _indexes.")
            tmp_data = self._innercontainer[0]
            if isinstance(tmp_data, np.generic):
                # self._element_type = type(np.asscalar(tmp_data))    # deprecated in numpy v1.16
                self._element_type = type(tmp_data.item())
            else:
                self._element_type = type(tmp_data)

    @property
    def index(self):
        """
        Get the index of data.
        """
        return copy.deepcopy(self._innercontainer)

    def __getitem__(self, item):
        return self._innercontainer.__getitem__(item)

    def get_elementType(self):
        """
        Return the type of data.
        """
        return self._element_type

    def pop(self):
        """
        Return the popped value. Raise KeyError if empty.
        """
        return self._innercontainer.pop()

    def add(self, value):
        """
        Add element.
        It will warn if the value to add is existent.
        Parameters
        ----------
        value: object
            same type of the element already in the set.
            Raise if unknown type is given.
        Returns
        -------
        self: object
            return self.
        """
        if self._element_type is None:
            self._element_type = type(value)
        # check validation
        if isinstance(value, np.generic):
            # value = np.asscalar(value)  # deprecated in numpy v1.16
            value = value.item()
        if not isinstance(value, self._element_type):
            raise TypeError(
                "A %s parameter is expected, but received: %s" % (str(self._element_type), str(type(value))))
        if value in self._innercontainer:
            warnings.warn("Adding element %s has already in the collection, skip." % (value.__str__()),
                          stacklevel=3)
        else:
            self._innercontainer.append(value)
        return self

    def discard(self, value):
        """Remove an element.
        It will warn if the value to discard is inexistent.
        Parameters
        ----------
        value: object
            Value to discard.
        Returns
        -------
        self: object
            Return self.
        """
        if value not in self._innercontainer:
            warnings.warn("Element %s to discard is not in the collection, skip." % (value.__str__()),
                          stacklevel=3)
        else:
            self._innercontainer.remove(value)
        return self

    def difference_update(self, other):
        """Remove all elements of another array from this container.
        Parameters
        ----------
        other: object
            Elements to discard. Note that, if multiple indexes are contained,
            a list, numpy.ndarray or IndexCollection should be given. Otherwise,
            it will be cheated as an object.
        Returns
        -------
        self: object
            Return self.
        """
        if not isinstance(other, (list, np.ndarray, IndexCollection)):
            other = [other]
        for item in other:
            self.discard(item)
        return self

    def update(self, other):
        """Update self with the union of itself and others.
        Parameters
        ----------
        other: object
            Elements to add. Note that, if multiple indexes are contained,
            a list, numpy.ndarray or IndexCollection should be given. Otherwise,
            it will be cheated as an object.
        Returns
        -------
        self: object
            Return self.
        """
        if not isinstance(other, (list, np.ndarray, IndexCollection)):
            other = [other]
        for item in other:
            self.add(item)
        return self

    def random_sampling(self, rate=0.3):
        """Return a random sampled subset of this collection.
        Parameters
        ----------
        rate: float, optional (default=None)
            The rate of sampling. Must be a number in [0,1].
        Returns
        -------
        array: IndexCollection
            The sampled index collection.
        """
        assert (0 < rate < 1)
        perm = randperm(len(self) - 1, round(rate * len(self)))
        return IndexCollection([self.index[i] for i in perm])


class MultiLabelIndexCollection(IndexCollection):
    """
    Class for managing multi-label indexes.

    This class stores indexes in multi-label. Each element should be a tuple.
    A single_label index should only have 1 element (example_index, ) to strategies all labels or
    2 elements (example_index, [label_indexes]) to strategies specific labels.

    Some examples of valid multi-label indexes include:
    queried_index = (1, [3,4])
    queried_index = (1, [3])
    queried_index = (1, 3)
    queried_index = (1, (3))
    queried_index = (1, (3,4))
    queried_index = (1, )   # strategies all labels

    Several validity checking are implemented in this class.
    Such as repeated elements, Index out of bound.

    Parameters
    ----------
    data : list or np.ndarray of a single_label tuple, optional (default=None)
        shape [n_element]. All elements should be tuples.

    label_size: int, optional (default=None)
        The number of classes. If not provided, an infer is attempted, raise if fail.

    Attributes
    ----------
    index: list, shape (1, n_elements)
        A list contains all elements in this container.

    Examples
    --------
    >>> multi_lab_ind1 = MultiLabelIndexCollection([(0, 1), (0, 2), (0, (3, 4)), (1, (0, 1))], label_size=5)
    {(0, 1), (1, 1), (0, 4), (1, 0), (0, 2), (0, 3)}
    >>> multi_lab_ind1.update((0, 0))
    {(0, 1), (0, 0), (1, 1), (0, 4), (1, 0), (0, 2), (0, 3)}
    >>> multi_lab_ind1.update([(1, 2), (1, (3, 4))])
    {(0, 1), (1, 2), (0, 0), (1, 3), (1, 4), (1, 1), (0, 4), (1, 0), (0, 2), (0, 3)}
    >>> multi_lab_ind1.update([(2,)])
    {(0, 1), (1, 2), (0, 0), (1, 3), (2, 2), (1, 4), (2, 1), (2, 0), (1, 1), (2, 3), (2, 4), (0, 4), (1, 0), (0, 2), (0, 3)}
    >>> multi_lab_ind1.difference_update([(0,)])
    {(1, 2), (1, 3), (2, 2), (1, 4), (2, 1), (2, 0), (1, 1), (2, 3), (2, 4), (1, 0)}
    """

    def __init__(self, data=None, label_size=None):
        if data is None or len(data) == 0:
            self._innercontainer = set()
            if label_size is None:
                warnings.warn("This collection does not have a label_size value, set it manually or "
                              "it will raise when decomposing indexes.",
                              stacklevel=3)
            self._label_size = label_size
        else:
            if isinstance(data, MultiLabelIndexCollection):
                self._innercontainer = copy.deepcopy(data.index)
                self._label_size = data._label_size
                return
            # check given indexes
            data = self.__check_index_multilabel(data)
            if label_size is None:
                self._label_size = self.__infer_label_size_multilabel(data, check_arr=False)
            else:
                self._label_size = label_size

            # decompose all label queries.
            decomposed_data = self.__flattern_multilabel_index(data, self._label_size, check_arr=False)

            self._innercontainer = set(decomposed_data)
            if len(self._innercontainer) != len(decomposed_data):
                warnings.warn(
                    "There are %d same elements in the given data" % (len(data) - len(self._innercontainer)),
                    stacklevel=3)

    @property
    def index(self):
        """
        Get the index of data.
        """
        return list(self._innercontainer)

    def add(self, value):
        """Add element.

        It will warn if the value to add is existent. Raise if
        invalid type of value is given.

        Parameters
        ----------
        value: tuple
            Index for adding. Raise if index is out of bound.

        Returns
        -------
        self: object
            return self.
        """
        # check validation
        assert (isinstance(value, tuple))
        if len(value) == 1:
            value = [(value[0], i) for i in range(self._label_size)]
            return self.update(value)
        elif len(value) == 2:
            if isinstance(value[1], collections.Iterable):
                for item in value[1]:
                    if item >= self._label_size:
                        raise ValueError("Index %s is out of bound %s" % (str(item), str(self._label_size)))
            else:
                if value[1] >= self._label_size:
                    raise ValueError("Index %s is out of bound %s" % (str(value[1]), str(self._label_size)))
        else:
            raise ValueError("A tuple with 1 or 2 elements is expected, but received: %s" % str(value))
        if value in self._innercontainer:
            warnings.warn("Adding element %s has already in the collection, skip." % (value.__str__()),
                          stacklevel=3)
        else:
            self._innercontainer.add(value)
        return self

    def discard(self, value):
        """Remove an element.

        It will warn if the value to discard is inexistent. Raise if
        invalid type of value is given.

        Parameters
        ----------
        value: tuple
            Index for adding. Raise if index is out of bound.

        Returns
        -------
        self: object
            return self.
        """
        assert (isinstance(value, tuple))
        if len(value) == 1:
            value = [(value[0], i) for i in range(self._label_size)]
            return self.difference_update(value)
        if value not in self._innercontainer:
            warnings.warn("Element %s to discard is not in the collection, skip." % (value.__str__()),
                          stacklevel=3)
        else:
            self._innercontainer.discard(value)
        return self

    def difference_update(self, other):
        """Remove all elements of another array from this container.

        Parameters
        ----------
        other: object
            Elements to discard. Note that, if multiple indexes are contained,
            a list, numpy.ndarray or MultiLabelIndexCollection should be given. Otherwise,
            a tuple should be given.

        Returns
        -------
        self: object
            Return self.
        """
        if isinstance(other, (list, np.ndarray, MultiLabelIndexCollection)):
            label_ind = self.__flattern_multilabel_index(other, self._label_size)
            for j in label_ind:
                self.discard(j)
        elif isinstance(other, tuple):
            self.discard(other)
        else:
            raise TypeError(
                "A list or np.ndarray is expected if multiple indexes are "
                "contained. Otherwise, a tuple should be provided")
        return self

    def update(self, other):
        """Update self with the union of itself and others.

        Parameters
        ----------
        other: object
            Elements to add. Note that, if multiple indexes are contained,
            a list, numpy.ndarray or MultiLabelIndexCollection should be given. Otherwise,
            a tuple should be given.

        Returns
        -------
        self: object
            Return self.
        """
        if isinstance(other, (list, np.ndarray, MultiLabelIndexCollection)):
            label_ind = self.__flattern_multilabel_index(other, self._label_size)
            for j in label_ind:
                self.add(j)
        elif isinstance(other, tuple):
            self.add(other)
        else:
            raise TypeError(
                "A list or np.ndarray is expected if multiple indexes are "
                "contained. Otherwise, a tuple should be provided")
        return self

    def get_onedim_index(self, order='C', ins_num=None):
        """Get the 1d index.

        Parameters
        ----------
        order : {'C', 'F'}, optional (default='C')
            Determines whether the indices should be viewed as indexing in
            row-major (C-style) or column-major (Matlab-style) order.

        ins_num: int, optional
            The total number of instance. Must be provided if the order is 'F'.

        Examples
        --------
        >>> b = [1, 4, 11]
        >>> mi = MultiLabelIndexCollection.construct_by_1d_array(array=b, label_mat_shape=(3, 4))
        >>> print(mi)
        {(1, 0), (2, 3), (1, 1)}
        >>> print('col major:', mi.get_onedim_index(order='F', ins_num=3))
        col major: [1, 11, 4]
        >>> print('row major:', mi.get_onedim_index(order='C'))
        row major: [4, 11, 5]
        """
        if order == 'F':
            if ins_num is None:
                raise ValueError("The ins_num must be provided if the order is 'F'.")
            return [tup[0] + tup[1] * ins_num for tup in self._innercontainer]
        elif order == 'C':
            return [tup[0] * self._label_size + tup[1] for tup in self._innercontainer]
        else:
            raise ValueError("The value of order must be one of {'C', 'F'}")

    def get_instance_index(self):
        """Get the index of instances contained in this object.
        If it is a labeled set, it is equivalent to the indexes of fully and partially labeled instances.

        Returns
        -------
        partlab: list
            The indexes of partially labeled instances.
        """
        return np.unique([tp[0] for tp in self._innercontainer])

    def _get_cond_instance(self, cond):
        """Return the indexes of instances according to the cond.

        cond = 0: return the instances which are unbroken.
        cond = 1: return the instances which have missing entries.
        """
        tmp = self.__integrate_multilabel_index(self.index, label_size=self._label_size, check_arr=False)
        if cond == 0:
            return [tp[0] for tp in tmp if len(tp) == 1]
        else:
            return [tp[0] for tp in tmp if len(tp) > 1]

    def get_unbroken_instances(self):
        """Return the indexes of unbroken instances whose entries are all known."""
        return self._get_cond_instance(cond=0)

    def get_break_instances(self):
        """Return the indexes of break instances which have missing entries."""
        return self._get_cond_instance(cond=1)

    def get_matrix_mask(self, mat_shape, fill_value=1, sparse=True, sparse_format='lil_matrix'):
        """Return an array which has the same shape with the label matrix.
        If an entry is known, then, the corresponding value in the mask is 1, otherwise, 0.

        Parameters
        ----------
        mat_shape: tuple
            The shape of label matrix. [n_samples, n_classes]

        fill_value: int
            The value filled in the mask when the entry is in the container.

        sparse: bool
            Whether to return a sparse matrix or a dense matrix (numpy.ndarray).

        sparse_format: str
            The format of the returned sparse matrix. Only available if sparse==True
            should be one onf [bsr_matrix, coo_matrix, csc_matrix, csr_matrix, dia_matrix, dok_matrix, lil_matrix].
            Please refer to https://docs.scipy.org/doc/scipy-0.18.1/reference/sparse.html
            for the definition of each sparse format.

        Returns
        -------
        mask: {scipy.sparse.csr_matrix, scipy.sparse.csc_matrix}
            The mask of the label matrix.
        """
        assert isinstance(mat_shape, tuple)
        if sparse:
            try:
                exec("from scipy.sparse import " + sparse_format)
            except:
                raise ValueError(
                    "sparse format " + sparse_format + "is not defined. Valid format should be one of "
                                                       "[bsr_matrix, coo_matrix, csc_matrix, csr_matrix, "
                                                       "dia_matrix, dok_matrix, lil_matrix].")
            mask = eval(sparse_format + '(mat_shape)')
        else:
            if fill_value == 1 or fill_value == True:
                mask = np.zeros(mat_shape, dtype=bool)
                for item in self._innercontainer:
                    mask[item] = True
            else:
                mask = np.zeros(mat_shape)
                for item in self._innercontainer:
                    mask[item] = fill_value
        return mask

    @classmethod
    def construct_by_1d_array(cls, array, label_mat_shape, order='F'):
        """Construct a MultiLabelIndexCollection object by providing a
        1d array, and the number of classes.

        Parameters
        ----------
        array: {list, np.ndarray}
            An 1d array of indexes.

        label_mat_shape: tuple of ints
            The shape of label matrix. The 1st element is the number of instances,
            and the 2nd element is the total classes.

        order : {'C', 'F'}, optional
            Determines whether the indices should be viewed as indexing in
            row-major (C-style) or column-major (Matlab-style) order.

        Returns
        -------
        multi_ind: MultiLabelIndexCollection
            The MultiLabelIndexCollection object.

        Examples
        --------
        >>> b = [1, 4, 11]
        >>> mi = MultiLabelIndexCollection.construct_by_1d_array(array=b, label_mat_shape=(3, 4))
        >>> print(mi)
        {(1, 0), (2, 3), (1, 1)}
        >>> print('col major:', mi.get_onedim_index(order='F', ins_num=3))
        col major: [1, 11, 4]
        >>> print('row major:', mi.get_onedim_index(order='C'))
        row major: [4, 11, 5]
        """
        assert len(label_mat_shape) == 2
        row, col = np.unravel_index(array, dims=label_mat_shape, order=order)
        return cls(data=[(row[i], col[i]) for i in range(len(row))], label_size=label_mat_shape[1])

    @classmethod
    def construct_by_element_mask(cls, mask):
        """Construct a MultiLabelIndexCollection object by providing a
        2d array whose shape should be the same as the matrix shape.

        Parameters
        ----------
        mask: {list, np.ndarray}
            The 2d mask matrix of elements.
            There must be only 1 and 0 in the matrix, in which,
            1 means the corresponding element is known, and will be
            added to the MultiLabelIndexCollection container.
            Otherwise, it will be cheated as an unknown element.

        Examples
        --------
        >>> import numpy as np
        >>> mask = np.asarray([
            [0, 1],
            [1, 0],
            [1, 0]
        ]) # 3 rows, 2 lines
        >>> mi = MultiLabelIndexCollection.construct_by_element_mask(mask=mask)
        >>> print(mi)
        {(0, 1), (2, 0), (1, 0)}

        """
        mask = np.asarray(mask)
        ue = np.unique(mask)
        if not (len(mask.shape) == 2 and len(ue) == 2 and 0 in ue and 1 in ue):
            raise ValueError("The mask matrix should be a 2d array, and there must be only "
                             "1 and 0 in the matrix, in which, 1 means the corresponding "
                             "element is known, and will be added to the MultiLabelIndexCollection container.")

    def __check_index_multilabel(self, index):
        """check if the given indexes are legal.

        Parameters
        ----------
        index: list or np.ndarray
            index of the data.
        """
        if isinstance(index, BaseCollection):
            return index
        if not isinstance(index, (list, np.ndarray)):
            index = [index]
        datatype = collections.Counter([type(i) for i in index])
        if len(datatype) != 1:
            raise TypeError("Different types found in the given indexes.")
        if not datatype.popitem()[0] == tuple:
            raise TypeError("Each index should be a tuple.")
        return index

    def __infer_label_size_multilabel(self, index_arr, check_arr=True):
        """Infer the label size from a set of index arr.

        raise if all index are example index only.

        Parameters
        ----------
        index_arr: list or np.ndarray
            index array.

        Returns
        -------
        label_size: int
        the inferred label size.
        """
        if check_arr:
            index_arr = self.__check_index_multilabel(index_arr)
        data_len = np.array([len(i) for i in index_arr])
        if np.any(data_len == 2):
            label_size = np.max([i[1] for i in index_arr if len(i) == 2]) + 1
        elif np.all(data_len == 1):
            raise Exception(
                "Label_size can not be induced from fully labeled set, label_size must be provided.")
        else:
            raise ValueError(
                "All elements in indexes should be a tuple, with length = 1 (example_index, ) "
                "to strategies all labels or length = 2 (example_index, [label_indexes]) to strategies specific labels.")
        return label_size


    def __flattern_multilabel_index(self, index_arr, label_size=None, check_arr=True):
        """
        Falt the multilabel_index to one-dimensional.

        Parameters
        ----------
        index_arr: list or np.ndarray
            index array.

        label_size: int
            the inferred label size.

        check_arr: bool
            if True,check the index_arr is a legal multilabel_index.

        Returns
        -------
        decomposed_data: list
            the decomposed data after falting.
        """
        if check_arr:
            index_arr = self.__check_index_multilabel(index_arr)
        if label_size is None:
            label_size = self.__infer_label_size_multilabel(index_arr)
        else:
            assert (label_size > 0)
        decomposed_data = []
        for item in index_arr:
            if len(item) == 1:
                for i in range(label_size):
                    decomposed_data.append((item[0], i))
            else:
                if isinstance(item[1], collections.Iterable):
                    label_ind = [i for i in item[1] if 0 <= i < label_size]
                else:
                    assert (0 <= item[1] < label_size)
                    label_ind = [item[1]]
                for j in range(len(label_ind)):
                    decomposed_data.append((item[0], label_ind[j]))
        return decomposed_data