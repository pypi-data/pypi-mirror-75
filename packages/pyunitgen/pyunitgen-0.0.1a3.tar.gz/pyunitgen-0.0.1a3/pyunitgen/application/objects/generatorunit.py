
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

import ast
import collections
import os
from threading import Thread

from .templates import Templates
from .nodeparser import NodeFunction, Node
from .nodetype import NodeType
from .pyunitfile import PyUnitFile
from .pyunitreport import PyUnitReport
from .pyunitexception import PyUnitExceptionNone


class Generator:

    @staticmethod
    def generateUnitTest(root, fileName, includeInternal=False):
        """
        Generates a unit test, given a root directory and a subpath to a file.

        :param root: str
        :param fileName: str
        :return: str or None
        """
        try:
            pyunit_source = PyUnitFile(fileName, root)
            tree = pyunit_source.getSourceTree()
            module = pyunit_source.getModule()
            import_path = (pyunit_source.getPath())
            # TODO: add the file root and file name to the main node so it can be use as the import path
            # TODO: Replace all the '/' with '.' and remove the '.py' at the end of the file.
            # print(fileName)
            # print(root)
            # print("File is {} :".format(module))

            # Walk the AST
            node = Node(tree, includeInternal=includeInternal,
                        import_path=import_path)
            node.unit_file = pyunit_source
            node.module_name = module
            list_children = node.getChildren()

            unitreport = PyUnitReport()

            if node.has_class:
                while list_children:
                    my_node = list_children.pop(0)

                    generate_unit_test_data = my_node.getUnitTest(
                        module)
                    # print(my_node.getName())
                    # print(my_node.list_import)
                    if generate_unit_test_data:
                        unitreport.add(generate_unit_test_data)
            else:
                generate_unit_test_data = node.getUnitTest(
                    module)

                if generate_unit_test_data:
                    unitreport.add(generate_unit_test_data)

            if node.node_module:
                import_path += " import "
                import_path += ",".join(node.node_module)
            else:
                import_path = ""

            if node.node_import:
                import_path += "\n"+"\n".join(node.node_import)

            # print(import_path)

            return unitreport.getReport(import_path=import_path)
        except PyUnitExceptionNone as ex:
            # print(ex)
            return None
