#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Set of functions useful in any module.

This module gathers a set of functions that are useful in many other modules. When a 
function is widely used in different modules, a general version of it is created and 
can be found here.

  Typical usage example:

  Context = Context()
"""

# Generic/Built-in modules
import os
from datetime import datetime

# Third-party modules

# Owned modules
from .Log import Log


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Context(metaclass=SingletonMeta):
    _env = None
    _init_env = None
    _total_time = 0
    _init_pwd = None
    _mandatory = ""
    _cur_workdir = ""
    _root_workdir = ""
    _filter_dict = {}
    _const_tag = ""

    _section_complete_dict = {}

    def __init__(self):
        self._init_env = os.environ.copy()
        self._env = self._init_env
        self._init_pwd = os.getcwd()
        self.set_time_stamp()
        return

    def add_env(self, key, value):
        if key.startswith('$') is False:
            #warning
            return

        self._env[key[1:]] = os.path.expandvars(value)
        os.environ.update(self._env)

    def get_env(self):
        return self._env

    def set_section_complete(self, section):
        self._section_complete_dict[section] = True

    def is_section_complete(self, section):
        if section in self._section_complete_dict:
            return True
        return False

    def is_mandatory_complete(self):
        if self._mandatory in self._section_complete_dict:
            return True

        return False

    def set_time_stamp(self):
        self._time_stamp = datetime.now().strftime("_%Y%m%d_%H%M%S")

    def get_time_stamp(self):
        return self._time_stamp

    def set_root_workdir(self, workdir):
        self._root_workdir = workdir

    def get_root_workdir(self):
        return self._root_workdir

    def set_cur_workdir(self, cur_workdir):
        self._cur_workdir = cur_workdir

    def get_cur_workdir(self):
        return self._cur_workdir

    def set_mandatory_section(self, mandatory):
        index = mandatory.find('?')
        if index > 0:
            mandatory = mandatory[:index]

        self._mandatory = mandatory

    def get_mandatory_section(self):
        return self._mandatory

    def add_filter_result(self, key, value):
        self._filter_dict[key] = value

    def get_filter_result(self, key):
        result = False
        index = key.find('?')
        if index > 0:
            key = key[index:]

        if key in self._filter_dict:
            result = self._filter_dict[key]

        return result

    def set_const_tag(self, tag):
        """tag information should be erased"""
        if tag is not None:
            self._const_tag = "_" + tag

    def get_const_tag(self):
        return self._const_tag

    def clear(self):
        self._env = self._init_env
        os.environ.update(self._init_env)

        self._cur_workdir = ""
        self._mandatory = ""

        self.set_time_stamp()

        self._section_complete_dict.clear()
        self._filter_dict.clear()

        os.chdir(self._init_pwd)
