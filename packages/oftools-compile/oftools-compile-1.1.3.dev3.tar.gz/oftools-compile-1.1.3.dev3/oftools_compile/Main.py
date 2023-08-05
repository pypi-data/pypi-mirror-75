#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import os
import argparse
import traceback
import sys
import time
from configparser import ConfigParser
from collections import OrderedDict

# Third-party modules

# Owned modules
from . import __version__
from .JobFactory import JobFactory
from .CompileJob import CompileJob
from .SetupJob import SetupJob
from .DeployJob import DeployJob
from .Log import Log
from .Context import Context
from .ReportGenerator import ReportGenerator


def main():
    return Main().run()


class Main:

    def __init__(self):
        return

    def _create_jobs(self, profile):
        jobs = []
        job_factory = JobFactory(profile)
        for section in profile.sections():
            try:
                job = job_factory.create(section)
                jobs.append(job)
            except:
                traceback.print_exc()
                print('Unexpected error detected during the job creation')
                exit(-1)

        # analyze created jobs
        if job_factory.is_fine() is not True:
            print('Missing jobs found. abort!')
            exit(-1)

        return jobs

    def _parse_arg(self):
        # add parse arguments
        arg_parser = argparse.ArgumentParser()

        arg_parser.add_argument(
            '-p',
            '--profile',
            action='append',
            help='profile which contains description of the compilation target.',
            required=False)

        arg_parser.add_argument('-s',
                                '--source',
                                action='append',
                                help='name of the source which must be a file.',
                                required=False)

        arg_parser.add_argument('-v',
                                '--version',
                                action='store_true',
                                help='print version information.',
                                required=False)

        arg_parser.add_argument(
            '-t',
            '--tag',
            help='add tag to the name of report file and the listing directory.',
            required=False)

        arg_parser.add_argument(
            '-l',
            '--log',
            help='set log level (DEBUG|INFO|WARNING|ERROR|CRITICAL).',
            required=False)

        # deprecated args
        arg_parser.add_argument('-r',
                                '--recursive',
                                action='store_true',
                                help=argparse.SUPPRESS)
        arg_parser.add_argument('-e',
                                '--export',
                                action='store_true',
                                help=argparse.SUPPRESS)

        # do the parsing
        args = arg_parser.parse_args()

        # analyze parsing result
        if args.version is True:
            return args

        if args.profile is None:
            Log().get().critical('-p or --profile option is not specified')
            exit(-1)

        if args.source is None:
            Log().get().critical('-s or --source option is not specified')
            exit(-1)

        if len(args.profile) != len(args.source):
            Log().get().critical(
                'the number of profile and source pairs does not match. profile='
                + str(len(args.profile)) + ',source=' + str(len(args.source)))
            exit(-1)

        for profile in args.profile:
            if os.path.isfile(os.path.expandvars(profile)) is False:
                Log().get().critical('cannot access profile: ' + profile)
                exit(-1)

        for source in args.source:
            if os.path.exists(os.path.expandvars(source)) is False:
                Log().get().critical('cannot access source: ' + source)
                exit(-1)

        return args

    def _run_internal(self, profile, source, report_generator):

        source_list = []

        # read profile
        profile_parser = ConfigParser(dict_type=OrderedDict)
        profile_parser.optionxform = str
        profile_parser.read(os.path.expandvars(profile))

        Log().get().debug('profile path = ' + os.path.expandvars(profile))

        # build source list
        if os.path.isdir(source):
            directory = os.path.expandvars(source)

            for dirpath, _, filenames in os.walk(directory):
                if dirpath.startswith('.'):
                    continue
                for f in filenames:
                    if f.startswith('.'):
                        continue
                    source_list.append(os.path.abspath(os.path.join(dirpath,
                                                                    f)))
        else:
            source_list = [source]

        source_list.sort()

        last_job = None
        for source in source_list:
            start_time = time.time()
            Context().clear()
            Log().clear()

            in_name = ""
            out_name = source
            jobs = self._create_jobs(profile_parser)

            for job in jobs:
                last_job = job
                try:
                    in_name = out_name
                    out_name = job.run(in_name)
                    rc = 0
                except KeyboardInterrupt:
                    rc = -255
                    break
                except:
                    trace_list = traceback.format_exc().splitlines()
                    for trace in trace_list:
                        Log().get().error(trace)
                    rc = -3
                    break

            # stop looping when ctrl+c
            if rc == -255:
                break

            unit_time = time.time() - start_time

            success = 'Y'
            if rc < 0:
                success = 'N'

            last_section = last_job._remove_filter_name(last_job.get_section())
            if last_section.startswith('deploy'):
                if Context().is_mandatory_complete() is not True:
                    last_section = Context().get_mandatory_section()

            report_generator.add(source,
                                 Context().get_cur_workdir(), last_section,
                                 success, unit_time)

        return rc

    def run(self):
        # initialize
        rc = 0

        # parse inline command
        args = self._parse_arg()

        if args.version is True:
            version = 'oftools-compile ' + __version__
            print(version)
            return 0

        # set log level
        Log().set_level(args.log)

        # run jobs through sources
        Context().set_const_tag(args.tag)
        report_generator = ReportGenerator()

        for i in range(len(args.source)):
            Log().clear()
            Context().clear()
            rc = self._run_internal(args.profile[i], args.source[i],
                                    report_generator)
            if rc is not 0:
                break

        report_generator.generate()

        # need to clear context to run pytest
        Log().clear()
        Context().clear()

        return rc
