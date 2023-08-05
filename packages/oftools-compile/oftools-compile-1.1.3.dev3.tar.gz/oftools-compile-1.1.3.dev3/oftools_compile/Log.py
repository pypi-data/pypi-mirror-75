#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import logging
import os
import time
import datetime

# Third-party modules

# Owned modules


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Log(object, metaclass=SingletonType):
    _logger = None
    _file_handler = None
    _stream_handler = None
    _formatter = None

    def __init__(self):
        self._logger = logging.getLogger("Logger")
        self._logger.setLevel(logging.INFO)
        #self._formatter = logging.Formatter(
        #    "%(asctime)-15s [%(levelname)8s] %(message)-100s (%(filename)s:%(lineno)s)",
        #    "%Y-%m-%d %H:%M:%S")
        self._formatter = logging.Formatter(
            "%(asctime)-8s [%(levelname)8s] %(message)s", "%H:%M:%S")

    def __del__(self):
        if self._file_handler is not None:
            self._file_handler.close()

    def set_file(self, cwd):
        if self._file_handler is not None:
            return

        self._file_handler = logging.FileHandler(
            os.path.join(cwd, "oftools_compile.log"))
        self._file_handler.setFormatter(self._formatter)
        self._logger.addHandler(self._file_handler)

    def set_level(self, level):

        if level == "DEBUG":
            self._formatter = logging.Formatter(
                "%(asctime)-8s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
                "%H:%M:%S")
            self._logger.setLevel(logging.DEBUG)
        elif level == "INFO":
            self._logger.setLevel(logging.INFO)
        elif level == "WARNING":
            self._logger.setLevel(logging.WARNING)
        elif level == "ERROR":
            self._logger.setLevel(logging.ERROR)
        elif level == "CRITICAL":
            self._logger.setLevel(logging.CRITICAL)

        if self._stream_handler is None:
            self._stream_handler = logging.StreamHandler()
            self._stream_handler.setFormatter(self._formatter)
            self._logger.addHandler(self._stream_handler)

    def get(self):
        return self._logger

    def clear(self):
        # oftools_compile.log
        if self._file_handler is not None:
            self._logger.removeHandler(self._file_handler)
            self._file_handler.close()
            self._file_handler = None
