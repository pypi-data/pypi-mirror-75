#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import os
import subprocess

# Third-party modules

# Owned modules
from .Log import Log
from .Context import Context


class Job(object):
    _section = None
    _profile = None

    def __init__(self, section, profile):
        self._section = section
        self._profile = profile

    def _add_filter(self, key, value, in_name):
        #Log().get().debug('add_filter: [' + key + ',' +
        #                  os.path.expandvars(value) + ']')

        result = False
        shell_cmd = os.path.expandvars(value)

        env = Context().get_env()
        proc = subprocess.Popen([shell_cmd],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                env=env)
        out, err = proc.communicate()

        if b'' != out:
            Log().get().debug(err.decode('utf-8'))
        if b'' != err:
            Log().get().debug(out.decode('utf-8'))

        # grep returns 0 if line matches
        if proc.returncode == 0:
            result = True

        Context().add_filter_result(key, result)

    def _evaluate_filter(self, section, in_name):
        if "?" not in section:
            return True

        result = Context().get_filter_result(section)
        return result

    def _remove_extension_name(self, in_name):
        return in_name.rsplit('.', 1)[0]

    def _remove_filter_name(self, section):

        index = section.find('?')
        if index > 0:
            section = section[:index]

        return section

    def _resolve_filter_name(self, section):

        index = section.find('?')
        if index > 0:
            section = section[index:]

        return section

    def get_section(self):
        return self._section