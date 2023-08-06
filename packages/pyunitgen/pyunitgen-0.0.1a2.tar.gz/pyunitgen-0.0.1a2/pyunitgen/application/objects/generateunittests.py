#!/usr/bin/env python3

# Copyright (c) 2015-2020 Agalmic Ventures LLC (www.agalmicventures.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .generatorunit import Generator
import argparse
import os
import sys
from threading import Thread
from os import path
import autopep8

import inspect
_currentFile = os.path.abspath(inspect.getfile(inspect.currentframe()))
_currentDir = os.path.dirname(_currentFile)
_parentDir = os.path.dirname(_currentDir)
sys.path.insert(0, _parentDir)


def generate_unittest(root, fileName, arguments, footer, header):

    rootInit = os.path.join(root, '__init__.py')

    # print(rootInit)

    if not os.path.exists(rootInit):
        with open(rootInit, "w") as rootInitFile:
            rootInitFile.write('')

    unitTest = Generator.generateUnitTest(
        root, fileName, arguments.internal)

    if unitTest:
        # Replace tabs
        if arguments.tab_width is not None:
            unitTest = unitTest.replace('\t', ' ' * arguments.tab_width)

        # Add header and footer
        unitTest = header + unitTest + footer

        # Write it
        outFile = '%s%s' % (arguments.test_prefix, fileName)
        outFolder = arguments.test_module
        if not os.path.exists(outFolder):
            os.makedirs(outFolder)

        # TODO: do this at every level
        testInit = os.path.join(outFolder, '__init__.py')
        if not os.path.exists(testInit):
            with open(testInit, 'w') as testInitFile:
                testInitFile.write('')

        outPath = os.path.join(outFolder, outFile)
        if arguments.force or not os.path.exists(outPath) or os.stat(outPath).st_size == 0:
            # print('[%s] Writing...' % outPath)
            with open(outPath, 'w') as outFile:
                outFile.write(unitTest)
        else:
            print('[%s] Already exists' % outPath)


def generate_unittest_for(fileNames, arguments, root, footer, header):
    for fileName in fileNames:
        # Skip ignored directories
        _, childDirectory = os.path.split(root)
        if childDirectory in arguments.exclude:
            continue

        unittest_thread = Thread(target=generate_unittest, args=(
            root, fileName, arguments, footer, header))
        unittest_thread.start()


def main(arguments):

    header = ''
    footer = ''
    if arguments.header is not None:
        with open(arguments.header) as headerFile:
            header = headerFile.read()
    if arguments.footer is not None:
        with open(arguments.footer) as footerFile:
            footer = footerFile.read()

    # Walk the directory finding Python files
    # print(arguments.module)

    if isinstance(arguments.module, dict):
        for root, fileNames in arguments.module.items():
            unittest_thread = Thread(target=generate_unittest_for, args=(
                fileNames, arguments, root, footer, header))
            unittest_thread.start()
    else:
        for root, _, fileNames in os.walk(arguments.module):
            if "__pycache__" not in root:
                # print(root)
                unittest_thread = Thread(target=generate_unittest_for, args=(
                    fileNames, arguments, root, footer, header))
                unittest_thread.start()

    return 0
