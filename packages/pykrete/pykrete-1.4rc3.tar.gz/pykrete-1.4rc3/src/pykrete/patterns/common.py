"""
Common module
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import os
import argparse
from pykrete.args import exiting_file


def assert_true(target, error):
    """Assert success of target

    :param target: target with bool success attribute
    :param error: error message in case of failure
    """
    if not target:
        raise AssertionError(error)


def first_or_error(vector, error):
    """Gets the first value in a vector, or throws an exception if the vector is empty

    :param vector: the target vector
    :param error: the error message
    :return: the first value in the vector
    """
    if vector:
        return vector[0]
    raise KeyError(error)


def existing_file_environment_cache(variable, path_maker):
    """Gets an existing file whose path is created once and kept in an environment variable

    :param variable: environment variable name
    :param path_maker: path maker lambda
    :return: path of existing file
    :exception: file doesn't exist
    """
    try:
        return exiting_file(os.environ[variable])
    except (KeyError, argparse.ArgumentTypeError):
        path = exiting_file(path_maker())
        os.environ[variable] = path
        return path


def pykrete_root():
    """
    :return: this package's installation root
    """
    package = 'pykrete'
    this_file = str(__file__)
    root = this_file[0:this_file.rfind(package)+len(package)]
    return root
