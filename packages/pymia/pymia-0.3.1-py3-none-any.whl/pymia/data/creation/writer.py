import abc
import os

import numpy as np
import h5py

import pymia.data.indexexpression as expr


class Writer(abc.ABC):
    """Represents the abstract dataset writer defining an interface for the writing process."""

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    @abc.abstractmethod
    def close(self):
        """Close the writer."""
        pass

    @abc.abstractmethod
    def open(self):
        """Open the writer."""
        pass

    @abc.abstractmethod
    def reserve(self, entry: str, shape: tuple, dtype=None):
        """Reserve space in the dataset for later writing.

        Args:
            entry(str): The dataset entry to be created.
            shape(tuple): The shape to be reserved.
            dtype: The dtype.
        """
        pass

    @abc.abstractmethod
    def fill(self, entry: str, data, index: expr.IndexExpression = None):
        """Fill parts of a reserved dataset entry.

        Args:
            entry(str): The dataset entry to be filled.
            data(object): The data to write.
            index(.IndexExpression): The slicing expression.
        """
        pass

    @abc.abstractmethod
    def write(self, entry: str, data, dtype=None):
        """Create and write entry.

        Args:
            entry(str): The dataset entry to be written.
            data(object): The data to write.
            dtype: The dtype.
        """
        pass


class Hdf5Writer(Writer):
    str_type = h5py.special_dtype(vlen=str)

    def __init__(self, file_path: str) -> None:
        """Writer class for HDF5 file type.

        Args:
            file_path(str): The path to the dataset file to write.
        """
        self.h5 = None  # type: h5py.File
        self.file_path = file_path

    def close(self):
        """see :meth:`.Writer.close`"""
        if self.h5 is not None:
            self.h5.close()
            self.h5 = None

    def open(self):
        """see :meth:`.Writer.open`"""
        self.h5 = h5py.File(self.file_path, mode='a', libver='latest')

    def reserve(self, entry: str, shape: tuple, dtype=None):
        """see :meth:`.Writer.reserve`"""
        # special string handling (in order not to use length limited strings)
        if dtype is str or dtype == 'str' or (isinstance(dtype, np.dtype) and dtype.type == np.str_):
            dtype = self.str_type
        self.h5.create_dataset(entry, shape, dtype=dtype)

    def fill(self, entry: str, data, index: expr.IndexExpression = None):
        """see :meth:`.Writer.fill`"""
        # special string handling (in order not to use length limited strings)
        if self.h5[entry].dtype is self.str_type:
            data = np.asarray(data, dtype=object)

        if index is None:
            index = expr.IndexExpression()

        self.h5[entry][index.expression] = data

    def write(self, entry: str, data, dtype=None):
        """see :meth:`.Writer.write`"""
        # special string handling (in order not to use length limited strings)
        if dtype is str or dtype == 'str' or (isinstance(dtype, np.dtype) and dtype.type == np.str_):
            dtype = self.str_type
            data = np.asarray(data, dtype=object)
        if entry in self.h5:
            del self.h5[entry]
        self.h5.create_dataset(entry, dtype=dtype, data=data)


def get_writer(file_path: str) -> Writer:
    """Get the dataset writer corresponding to the file extension.

        Args:
            file_path(str): The path of the dataset file to be written.

        Returns:
            .creation.writer.Writer: Writer corresponding to dataset file extension.
        """
    extension = os.path.splitext(file_path)[1]
    if extension not in writer_registry:
        raise ValueError('unknown dataset file extension "{}"'.format(extension))

    return writer_registry[extension](file_path)


writer_registry = {'.h5': Hdf5Writer, '.hdf5': Hdf5Writer}
"""Registry defining the mapping between file extension and :class:`.Writer` class. 
    Alternative writers need to be added to this registry in order to use :func:`.get_writer`."""
