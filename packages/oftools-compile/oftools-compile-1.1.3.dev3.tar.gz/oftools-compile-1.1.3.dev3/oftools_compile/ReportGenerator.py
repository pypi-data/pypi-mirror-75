#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import os
import subprocess
import logging

# Third-party modules

# Owned modules
from .Log import Log
from .Context import Context


class Record(object):
    _rc = 0
    _source = ""
    _section = ""
    _unit_time = 0

    def __init__(self, source, list_dir, section, success, unit_time):
        self._source = source
        self._section = section
        self._success = success
        self._list_dir = list_dir
        self._unit_time = unit_time
        pass

    def to_csv(self):
        return str(self._source + ',' + self._list_dir + ',' + self._section +
                   ',' + self._success + ',' + str(round(self._unit_time, 4)))


class ReportGenerator(object):

    _total_time = 0
    _success_count = 0
    _fail_count = 0
    _records = []

    def __init__(self):
        return

    def add(self, source, list_dir, section, success, time):

        record = Record(source, list_dir, section, success, time)
        self._records.append(record)

        if success == 'Y':
            self._success_count += 1
        else:
            self._fail_count += 1

        self._total_time += time

        if success == 'Y':
            Log().get().info('BUILD SUCCESS (' + str(round(time, 4)) + ' sec)')
        else:
            Log().get().info('BUILD FAILED (' + str(round(time, 4)) + ' sec)')
        Log().get().info('')

        return

    def generate(self):

        results = []
        results.append("source,list_dir,section,success,time")

        Log().get().info(
            '= SUMMARY ==================================================')
        Log().get().info('TOTAL TIME: ' + str(round(self._total_time, 4)) +
                         ' sec')
        Log().get().info('TOTAL     : ' +
                         str(self._success_count + self._fail_count))
        Log().get().info('SUCCESS   : ' + str(self._success_count))
        Log().get().info('FAILED    : ' + str(self._fail_count))

        for record in self._records:
            results.append(record.to_csv())

        # export the report file
        file_name = 'report/oftools_compile' + Context().get_const_tag(
        ) + Context().get_time_stamp() + '.csv'
        file_name = os.path.expandvars(
            os.path.join(Context().get_root_workdir(), file_name))

        with open(file_name, 'w') as f:
            for result in results:
                f.write("%s\n" % result)
        f.close()

        Log().get().info('csv report has been generated: ' + file_name)

        return