import signal
import time
import subprocess
import os
import hashlib
import argparse
# from .application.objects.generator import Generator
from os import sys
from argparse import ArgumentParser

from .application.unittestgenerator import watch


def main(argv=None):

    try:
        parser = ArgumentParser()

        # parser.add_argument('-o', '--output', default=None,
        #                     help='Directory to generate the unittest to')

        parser.add_argument('module',
                            help='The module directory')

        parser.add_argument('-F', '--footer',
                            help='File to use as a footer.')
        parser.add_argument('-H', '--header',
                            help='File to use as a header.')
        parser.add_argument('-X', '--exclude', action='append', default=[],
                            help='Add a child directory name to exclude.')

        parser.add_argument('-f', '--force', action='store_true',
                            help='Force files to be generated, even if they already exist.')
        parser.add_argument('-i', '--internal', action='store_true',
                            help='Include internal classes and methods starting with a _.')
        parser.add_argument('-m', '--test-module', default='test',
                            help='The path of the test module to generate.')
        parser.add_argument('-p', '--test-prefix', default='test_',
                            help='The prefix for test files.')
        parser.add_argument('-t', '--tab-width', type=int,
                            help='The width of a tab in spaces (default actual tabs).')

        parser.add_argument('-nw', '--no-watch', default=False, action='store_true',
                            help='Do not watch the directory. When the file been modified.')

        if argv is None:
            argv = sys.argv

        argument = parser.parse_args(argv[1:])

        # print(argument)

        watch(argument)

    except Exception as ex:
        print(ex)
    except KeyboardInterrupt:
        pass
