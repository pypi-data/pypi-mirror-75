#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import shutil
import os
import subprocess

# Third-party modules

# Owned modules
from .Job import Job
from .Log import Log
from .Context import Context


class DeployJob(Job):

    def _analyze(self, in_name):

        # check if any compile job was a success
        if Context().is_mandatory_complete() is False:
            Log().get().error(
                'mandatory section [' + Context().get_mandatory_section() +
                '] did not ran successfully. aborting the deploy job')
            exit(-1)

        # check if given section is already completed
        if Context().is_section_complete(self._section):
            Log().get().debug('section has already been processed. skipping [' +
                              self._section + '] section.')
            return -1

        # evaluate filter to decide whether this section should run or not
        if self._evaluate_filter(self._section, in_name) is False:
            Log().get().debug('[' + self._section + '] ' +
                              self._resolve_filter_name(self._section) +
                              ' is False. skipping section.')
            return -1

        return 0

    def _process_region(self, out_name):

        if self._profile.has_option(self._section, 'region') is False:
            return

        regions = self._profile.get(self._section, 'region').split(':')
        for region in regions:
            shell_cmd = 'cp ' + out_name + ' ' + os.path.join(
                '$OPENFRAME_HOME/osc/region',
                os.path.expandvars(region) + '/tdl/mod')
            shell_cmd += '; '
            shell_cmd += 'osctdlupdate'
            shell_cmd += ' ' + region
            shell_cmd += ' ' + self._remove_extension_name(out_name)

            Log().get().info('[' + self._section + '] ' + shell_cmd)
            proc = subprocess.Popen([shell_cmd],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
            out, err = proc.communicate()

            # handle resultget
            if proc.returncode != 0:
                Log().get().error(err.decode('utf-8'))
                Log().get().error(out.decode('utf-8'))
                exit(proc.returncode)

        return

    def _process_tdl(self, out_name):
        if self._profile.has_option(self._section, 'tdl') is False:
            return

        tdls = self._profile.get(self._section, 'tdl').split(':')
        for tdl in tdls:
            shell_cmd = 'cp ' + out_name + ' ' + os.path.join(
                os.path.expandvars(tdl) + '/tdl/mod')
            shell_cmd += '; '
            shell_cmd += 'tdlupdate'
            shell_cmd += ' -m ' + self._remove_extension_name(out_name)
            shell_cmd += ' -r ' + os.path.join(
                os.path.expandvars(tdl) + '/tdl/mod')

            Log().get().info('[' + self._section + '] ' + shell_cmd)
            proc = subprocess.Popen([shell_cmd],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
            out, err = proc.communicate()

            # handle result
            if proc.returncode != 0:
                Log().get().error(err.decode('utf-8'))
                Log().get().error(out.decode('utf-8'))
                exit(proc.returncode)

        return

    def _process_dataset(self, out_name):
        out = ""
        err = ""

        if self._profile.has_option(self._section, 'dataset') is False:
            return

        datasets = self._profile.get(self._section, 'dataset').split(':')
        for dataset in datasets:
            shell_cmd = 'dlupdate ' + os.path.join(os.getcwd(),
                                                   out_name) + ' ' + dataset
            Log().get().info('[' + self._section + '] ' + shell_cmd)
            proc = subprocess.Popen([shell_cmd],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
            out, err = proc.communicate()

            # handle result
            if proc.returncode != 0:
                Log().get().error(err.decode('utf-8'))
                Log().get().error(out.decode('utf-8'))
                exit(proc.returncode)

        return

    def _process_file(self, in_name):
        out_name = in_name

        try:
            out_name = self._profile.get(self._section, 'file')
            out_name = out_name.replace("$OF_COMPILE_BASE",
                                        self._remove_extension_name(in_name))

            if in_name != out_name:
                Log().get().info('[' + self._section + '] ' + 'cp ' + in_name +
                                 ' ' + out_name)
                shutil.copy(in_name, out_name)

        except:
            Log().get().error('[' + self._section + '] failed to copy ' +
                              in_name)
            exit(-1)

        return out_name

    def run(self, in_name):
        # analyze section
        if self._analyze(in_name) < 0:
            return in_name

        # start section
        Log().get().debug("[" + self._section + "] start section")

        # update predefined environment variable
        base_name = self._remove_extension_name(in_name)
        out_name = base_name + '.' + self._remove_filter_name(self._section)
        Context().add_env('$OF_COMPILE_IN', in_name)
        Context().add_env('$OF_COMPILE_OUT', out_name)
        Context().add_env('$OF_COMPILE_BASE', base_name)

        # add environment variables
        for key in self._profile.options(self._section):
            value = self._profile.get(self._section, key)

            if key.startswith('$'):
                Context().add_env(key, value)

        # process others
        out_name = self._process_file(in_name)
        self._process_dataset(out_name)
        self._process_tdl(out_name)
        self._process_region(out_name)

        # set section as completed
        Context().set_section_complete(self._remove_filter_name(self._section))

        # end section
        Log().get().debug("[" + self._section + "] end section")

        return out_name
