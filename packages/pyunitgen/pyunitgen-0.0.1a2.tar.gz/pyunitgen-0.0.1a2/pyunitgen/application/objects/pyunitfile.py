import ast
import collections
import os
from .pyunitexception import PyUnitExceptionNone


class PyUnitFile:

    def __init__(self, fileName, root):
        self.fileName = fileName
        self.root = root
        self.path = None
        self.module = None

    def getModule(self):
        return self.module

    def getRoot(self):
        if len(self.root) == 0:
            return self.module
        return self.root.strip("/")

    def getReloadPath(self):
        if len(self.root) > 0:
            return "{}.{}".format(self.getRoot(), self.getModule())
        return self.getModule()

    def getPath(self):
        # print(self.path.replace("/", ".").rstrip(".py"))
        return "from "+self.path.replace("/", ".").rstrip(".py")

    def getSourceTree(self):
       # Skip non-Python files
        if not self.fileName.endswith('.py') or "__init__" in self.fileName:
            raise PyUnitExceptionNone

        # Skip symlinks
        path = os.path.join(self.root, self.fileName)
        if os.path.islink(path):
            print('Symlink: %s' % path)
            raise PyUnitExceptionNone
        self.path = path

        # Get the parts of the filename
        pathParts = os.path.split(path)
        fileName = pathParts[-1]
        self.module, _ = os.path.splitext(fileName)

        # Load the file
        try:
            with open(path) as f:
                text = f.read()

        except UnicodeDecodeError as ude:
            print('Unicode decode error for %s: %s' % (path, ude))
            raise PyUnitExceptionNone

        # Parse it
        try:
            tree = ast.parse(text)
            return tree
        except Exception as e:  # @suppress warnings since this really does need to catch all
            print('Failed to parse %s' % path)
            print(e)
            raise PyUnitExceptionNone
