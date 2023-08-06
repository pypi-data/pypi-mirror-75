#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @autor: Ramón Invarato Menéndez
# @version 1.0

import os
import time

try:
    import cPickle as pickle
except ImportError:
    import pickle


__test__ = {'import_test': """
                           >>> from easy_binary_file_pkg.easy_binary_file import *

                           """}


def dump_ensure_space(file, value, fun_err=None):
    """
    Only dump value if space enough in disk.
    If is not enough space, then it retry until have space
    Note: this method is less efficient and slowly than simple dump

    >>> with open("test_ensure_space.tmp", "wb") as f:
    ...     dump_ensure_space(f, "test_value")

    :param file: file where dump
    :param value: value to dump
    :param fun_err: event previous to sleep if error, with params:
        times_waiting: times retrying until now
        time_to_retry: time to next retry in seconds
        err: msg error
    :return: None
    """
    if fun_err is None:
        def fun_err_default(_, __, ___):
            return None
        fun_err = fun_err_default

    times_waiting = 0
    retry = True
    while retry:
        try:
            pickle.dump(value, file, pickle.HIGHEST_PROTOCOL)
            retry = False
        except IOError as err:
            if "No space left on device" in str(err):
                retry = True
                times_waiting += 1
                time_to_retry = 0.1 * times_waiting

                if time_to_retry > 3600:
                    time_to_retry = 3600

                fun_err(times_waiting, time_to_retry, err)

                time.sleep(time_to_retry)
            else:
                raise


def dump_single_value(path_and_file, value, append=False):
    """
    Open a file in the binary mode, dump a single value and close file

    >>> dump_single_value("test_file_single.tmp", "test_value")

    :param path_and_file: path to file
    :param value: value to dump
    :param append: True to open file in "ab" mode, False to open in "rb" mode.
                    By default: False (rb)
    :return: None
    """
    with open(path_and_file, mode='ab' if append else 'wb') as f:
        pickle.dump(value, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_single_value(path_and_file):
    """
    Open a file in the binary mode, load a single value, return it and close file

    Load the binary value:
    >>> value = load_single_value("test_file_single.tmp")
    >>> print(value)
    test_value

    :param path_and_file: path to file
    :return: value in file
    """
    with open(path_and_file, mode='rb') as f:
        return pickle.load(f)


def dump_items(file, iter_to_save, ensure_space=False, fun_err_space=None):
    """
    Serialize one iterable in a single file

    >>> with open("test_items.tmp", "wb") as f:
    ...     dump_items(f, ["a", "b", "c"])

    :param file: file where dump
    :param iter_to_save: iterable with items to save
    :param ensure_space: True to dump value if space enough in disk,
                         False raise exception. By default: False
    :param fun_err_space: event previous to sleep if error. By default: None
    :return: None
    """
    if ensure_space:
        for value in iter_to_save:
            dump_ensure_space(file, value, fun_err_space)
    else:
        for value in iter_to_save:
            pickle.dump(value, file, protocol=pickle.HIGHEST_PROTOCOL)


def load_items(file):
    """
    Deserialize item by item in one stream generator

    >>> with open("test_items.tmp", "rb") as f:
    ...     gen = load_items(f)
    ...     print(list(gen))
    ['a', 'b', 'c']

    :return: generator
    """
    try:
        while True:
            yield pickle.load(file)
    except EOFError:
        return


def quick_dump_items(path_to_file,
                     iter_to_save,
                     ensure_space=False,
                     fun_err_space=None,
                     append=False):
    """
    Quick open a file in ab or wb mode and dump items one by one from iterator,
    when generator is exhausted then close the file.

    >>> quick_dump_items("test_q_items.tmp", ["a", "b", "c"])

    :param path_to_file: path to file to open
    :param iter_to_save: iterable with items to save
    :param ensure_space: True to dump value if space enough in disk,
                         False raise exception. By default: False
    :param fun_err_space: event previous to sleep if error. By default: None
    :param append: True to open in ab mode, False to open in rb mode.
                   By defatult: False
    :return: None
    """
    with open(path_to_file, mode='ab' if append else 'wb') as f:
        dump_items(f, iter_to_save, ensure_space, fun_err_space)


def quick_load_items(path_to_file):
    """
    Quick open a file in rb mode and load items in one generator,
    when generator is exhausted then close the file.

    >>> gen = quick_load_items("test_q_items.tmp")
    >>> print(list(gen))
    ['a', 'b', 'c']

    :param path_to_file: path to file to open
    :return: generator of file
    """
    with open(path_to_file, mode='rb') as f:
        for v in load_items(f):
            yield v


class EasyBinaryFile(object):

    def __init__(self, path_and_file, mode='wb'):
        """
        Open (or create if not exist) a new binary file.

        Note: it is necesary close this file in end use.

        >>> ebf = EasyBinaryFile("test_ebf_object.tmp")
        >>> ebf.close()

        or more easy:
        >>> with EasyBinaryFile("test_ebf_object.tmp") as ebf:
        ...     pass  # Use ebf

        :param path_and_file: path to file to open or create
        :param mode: wb, rb or ab. By defatul: wb
        """
        self.path_and_file = path_and_file
        self.mode = mode
        self.file = open(path_and_file, mode)

    def close(self):
        """
        Close the binary file
        :return: None
        """
        self.file.close()
        self.file = None

    def __enter__(self):
        if self.file is None:
            self.file = open(self.path_and_file, self.mode)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def dump(self, value, ensure_space=False, fun_err_space=None):
        """
        Dump in file one single value

        >>> with EasyBinaryFile("test_ebf_object.tmp") as ebf:
        ...     ebf.dump("Value test")

        :param value: Value to dump in file
        :param ensure_space: True to dump value if space enough in disk,
                             False raise exception. By default: False
        :param fun_err_space: event previous to sleep if error. By default: None
        :return: None
        """
        if ensure_space:
            pickle.dump(value, self.file, pickle.HIGHEST_PROTOCOL)
        else:
            dump_ensure_space(self.file, value, fun_err_space)

    def load(self):
        """
        Load from file one single value

        >>> with EasyBinaryFile("test_ebf_object.tmp", "rb") as ebf:
        ...     print(ebf.load())
        Value test

        :return: value loaded from file
        """
        return pickle.load(self.file)

    def get_cursor_position(self):
        """
        Get last position of cursor in file

        >>> with EasyBinaryFile("test_ebf_object.tmp") as ebf:
        ...     ebf.dump("Test value")
        ...     print(ebf.get_cursor_position())
        25

        :return: cursor position
        """
        cursor_pos = self.file.tell()

        # Check tell
        if cursor_pos == 0:
            filesize = os.fstat(self.file.fileno()).st_size
            if filesize > 0:
                pickle.dump(None, self.file, pickle.HIGHEST_PROTOCOL)
                return self.file.tell()

        return cursor_pos

    def seek(self, cursor_pos):
        """
        Seek file in position

        :param cursor_pos: cursor position
        :return: None
        """
        self.file.seek(cursor_pos)

    def get_by_cursor_position(self, cursor_pos):
        """
        Get value by cursor position in file

        >>> with EasyBinaryFile("test_ebf_object.tmp") as ebf:
        ...     ebf.dump("Test value1")
        ...     pos = ebf.get_cursor_position()
        ...     ebf.dump("Value to get by position")
        ...     ebf.dump("Test value2")
        >>> with EasyBinaryFile("test_ebf_object.tmp", "rb") as ebf:
        ...     print(ebf.get_by_cursor_position(pos))
        Value to get by position

        :param cursor_pos: cursor position
        :return: value in this cursor position
        """
        self.seek(cursor_pos)
        return pickle.load(self.file)

    def dump_items(self, iter_to_save, ensure_space=False, fun_err_space=None):
        """
        Serialize one iterable in a file.

        >>> with EasyBinaryFile("test_ebf_object.tmp") as ebf:
        ...     ebf.dump_items(["a", "b", "c"])

        :param iter_to_save: iterable with items to save
        :param ensure_space: True to dump value if space enough in disk,
                             False raise exception. By default: False
        :param fun_err_space: event previous to sleep if error. By defatult: None
        :return: None
        """
        return dump_items(self.file, iter_to_save, ensure_space, fun_err_space)

    def load_items(self):
        """
        Deserialize item by item in one stream generator

        >>> with EasyBinaryFile("test_ebf_object.tmp", "rb") as ebf:
        ...     list(ebf.load_items())
        ['a', 'b', 'c']

        :return: generator
        """
        return load_items(self.file)

    def __iter__(self):
        """
        Iterate all items

        >>> with EasyBinaryFile("test_ebf_object.tmp", "rb") as ebf:
        ...     for item in ebf.load_items():
        ...         print(item)
        a
        b
        c

        :return: generator to iterate in all items
        """
        return self.load_items()

    __test__ = {
        'clean_test_files_obj': """
                        >>> from pathlib import Path
                        >>> Path("test_ebf_object.tmp").unlink()

                        """}


__test__ = {
    'clean_test_files': """
                        >>> from pathlib import Path
                        >>> Path("test_file_single.tmp").unlink()
                        >>> Path("test_ensure_space.tmp").unlink()
                        >>> Path("test_items.tmp").unlink()
                        >>> Path("test_q_items.tmp").unlink()

                        """}
