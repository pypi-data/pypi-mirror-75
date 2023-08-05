"""
Regex replacement class
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import os
from pykrete.calls import CheckedCall


class File:
    """Used to handle text files

    Properties:
    path (string): the file's path
    """

    def __init__(self, path):
        """Initialize this instance to handle the file at the specified path

        :param path: file path
        """
        self.path = path
        self.__contents = None

    def update(self, test, *replacements):
        """If the specified file's contents pass the test, preforms replacements and updates the
         file

        :param test: (function accepting a string and returning bool) a test on the file's contents
        :param replacements: (Replacement) replacement object(s)

        :return: (bool) True if test passed and file was updated, False if test failed (file won't
         be updated)
        """
        contents = self.__contents if self.__contents else self.read()
        if not test(contents):
            return False

        for replacement in replacements:
            contents = replacement.replace(contents)
        self.write(contents)

        if self.__contents:
            self.__contents = contents
        return True

    def write(self, contents):
        """Write contents to a file

        :param contents: (string) contents to be written
        """
        self.__write(lambda file: file.write(contents))

    def write_doc(self, doc):
        """Write XML document to a file

        :param doc: (Document) XML to be written
        """
        self.__write(doc.writexml)

    def read_contents(self):
        """Read file's contents and keep them in memory
        """
        self.__contents = self.read()

    def forget_contents(self):
        """Clear this object's contents memory
        """
        self.__contents = None

    def get_contents(self):
        """Get this object's contents memory
        """
        return self.__contents

    def read(self):
        """Read file's contents into a string

        :return: (string) contents read
        """
        with open(self.path, 'r', encoding='utf-8') as file:
            return file.read()

    def __write(self, writer):
        if os.path.exists(self.path):
            CheckedCall(f'attrib -R {self.path}')
        with open(self.path, 'w', encoding='utf-8') as file:
            writer(file)
