import ast
from collections import namedtuple
import re
from .nodetype import NodeType, AssertUnitTestCase
from .templates import Templates
from faker import Faker
from .pyunitreport import PyUnitReport, PyUnitReportValidation
from .pyunittype import PyUnitObject
from random import choice
import autopep8


Import = namedtuple("Import", ["module", "name", "alias"])

# TODO: When generating the unittest file make sure to compare existing generate unittest
#      file so you don't overwrite the existing one. When comparing and there are some
#      missing function or method, just create those missing one.


# TODO: Allow the user to use 'self' instead the lower case letter for the class as '@apiReturn {apiParam.user_name} [person.get_name(0)]'
#       change that to @apiReturn {apiParam.user_name} [self.get_name(0)]

# TODO: There is issue using the following return parameter in python simple function
#      @apiReturn {Object} [Pet(apiParam.name,apiParam.species,apiParam.age)]
#       not easy to import for example the class Pet showing above


# TODO: When generating the parameter check whether the parameter is a positional parameter or not

class AstNode:
    def __init__(self, node):
        self.name = node.name

    def __new__(self, node):
        return node


class Node:
    def __init__(self, node, parent=None, includeInternal=None, import_path=None):
        self.node = AstNode(node)
        self.list_children = []
        self.parent = parent
        self.includeInternal = includeInternal
        self.name = None
        self.report = PyUnitReportValidation()
        self.module_name = None
        self.list_import = []
        self.node_module = []
        self.has_class = False
        self.init_method = None
        self.import_path = import_path
        self.node_import = []
        # print(ast.dump(node, annotate_fields=True))
        self.init_children()
        self.unit_file = None

    def getParentName(self):
        if isinstance(self.parent, ast.ClassDef):
            if hasattr(self.parent, "name"):
                return self.parent.name
        else:
            if self.parent == None or self.parent.getName() == None:
                return self.parent.module_name
            return self.parent.getName()

    def get_imports(self, node):

        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module.split('.')
        else:
            return

        for n in node.names:
            if Import(module, n.name.split('.'), n.asname) not in self.list_import:
                self.list_import.append(
                    Import(module, n.name.split('.'), n.asname))

    def init_children(self):
        # TODO: At this stage we are ignoring all the ast.FunctionDef that start with '__'
        for child in self.node.body:
            nodeType = type(child)
            node = None
            # print(nodeType)
            self.get_imports(child)
            if nodeType is ast.ClassDef:
                if not child.name.startswith('_') or self.includeInternal:
                    node = NodeClass(child, parent=self,
                                     includeInternal=self.includeInternal, import_path=self.import_path)
                    self.node_module.append(node.getName())
                    self.has_class = True
                    # node.import_path = self.import_path
            elif nodeType is ast.FunctionDef:
                if not child.name.startswith('_') or self.includeInternal:
                    node = NodeFunction(
                        child, parent=self, includeInternal=self.includeInternal)
                    if self.parent == None:
                        # print(child.name)
                        self.node_module.append(node.getName())
                elif child.name.startswith('__init__'):
                    init_node = NodeFunction(
                        child, parent=self, includeInternal=self.includeInternal)
                    init_node.parent.init_method = init_node

            self.get_imports(child)
            if node:
                node.list_import = self.list_import
                self.list_children.append(node)

    def getChildren(self):
        return self.list_children

    def getName(self):
        if hasattr(self.node, "name"):
            return self.node.name

    def getType(self):
        return type(self)

    def hasChildren(self):
        return len(self.list_children)

    def isClass(self):
        return False

    def isFunction(self):
        return False

    def getUnitTest(self, module=None):

        methodTests = ""
        classTestComment = ""
        # print('Tests for functions in the "{}" file.=> {}'.format(
        #     module, len(self.getChildren())))
        if self.hasChildren():
            classTestComment = 'Tests for functions in the "%s" file.' % module
            list_method = []
            for method in self.getChildren():
                if method.isFunction():
                    if method.getName()[0] != '_':
                        func_data = None
                        func_data = method.getFuncAssertTest()
                        if func_data:
                            list_method.append(func_data)

            # print(self.list_import)
            if self.list_import:

                for node_module, name, alias in self.list_import:
                    module_import = "from "
                    module_import += ".".join(node_module)
                    module_import += " import " + ",".join(name)
                    if alias:
                        module_import += " as " + alias
                    self.node_import.append(module_import)

            # print(method.getName())

            # print(self.list_import[0].module)
            if list_method:
                methodTests = '\n'.join(list_method)

        return Templates.classTest % (
            module, classTestComment,
            methodTests,
        )


class NodeClass(Node):

    def isClass(self):
        return (type(self) == NodeClass)

    def get_init_method_arg(self):
        if self.init_method:
            if self.init_method.getParameter():
                init_argument = self.init_method.generateParameterData(
                    self.init_method.getParameter())
                # print(ast.dump(self.init_method.node))
                arg_str = ",".join(init_argument)
                return re.sub("[a-zA-Z0-9]+=", "", arg_str)
        return ""

    def getUnitTest(self, module=None):
        if self.hasChildren():
            classTestComment = 'Tests for methods in the %s class.' % self.getName()
            list_method = []
            for method in self.getChildren():
                if method.isFunction():
                    if method.getName()[0] != '_':
                        list_method.append(
                            method.getAssertTest())
                elif method.isClass():
                    class_children = method.getUnitTest(module)
                    if class_children:
                        list_method.extend(class_children)

            methodTests = '\n'.join(list_method)

            return Templates.classTest % (
                self.getName(), classTestComment,
                methodTests,
            )


class NodeDecoration:
    pass


class NodeFunction(NodeClass):
    def __init__(self, node, parent=None, includeInternal=None):
        super(NodeFunction, self).__init__(
            node=node, parent=parent, includeInternal=includeInternal)
        self.list_parameter = {}
        self.return_type = None
        self.return_value = None
        # print(node.name)
        # print(ast.dump(node))

    def isFunction(self):
        return (type(self) == NodeFunction)

    def getDecorationList(self):
        if self.node.decorator_list:
            for deco in self.node.decorator_list:
                yield deco
        return None

    def getFuncUnitTest(self, module):
        functionTests = Templates.functionTest.format(
            self.getName(), NodeType.re_none % (self.getName()))
        return functionTests

    def getUnitTest(self, module=None):

        moduleTestComment = 'Tests for functions in the %s module.' % module
        functionTests = Templates.functionTest.format(
            self.getName(), NodeType.re_none % (self.getName()))
        functionTests += "\n"

        # print(self.parent)

        return Templates.classTest % (
            module, moduleTestComment,
            functionTests)

    def getDecoration(self):
        return next(self.getDecorationList())

    def getComment(self):
        return ast.get_docstring(self.node, clean=True)

    def getFunctionType(self, res):
        _, k, v = res[0]
        value = v.strip("[ ]")
        key = k.strip("{ }")
        if "," in value and key.lower() != "object":
            value = value.split(",")

        if key.lower() == "boolean":
            if value:
                return True, value
            return True, None

        if key.lower() == "number":
            if value:
                return 1, value
            return 1, None

        if key.lower() == "string":
            if value:
                return "", "'{}'".format(value)
            return "", None

        if key.lower() == "list":
            if value:
                return "", value
            return [], None

        if key.lower() == "dict":
            if value:
                return "", value
            return {}, None

        if key.lower() == "object":
            if value:
                if "apiparam" in value.lower():
                    key = re.sub(
                        "([a-zA-Z0-9\(\)\[\] ]+)?apiParam.", "", value).strip("( )").split(",")
                    self.return_type = PyUnitObject(key)
                    return self.return_type, value
                return object, value
            return object, None

        if "apiparam" in key.lower():
            self.return_type = PyUnitObject(key)
            if value:
                return self.return_type, value
            return None, None

    def getReturnType(self):
        comment = self.getComment()
        # print(dir(self.node))
        if comment:
            res = re.findall(
                r"(\@apiReturn)[ ]+(?P<type>[a-zA-Z0-9\{\}\._ ]+)(?P<arg>[a-zA-Z0-9\[\]\{\}\.'\":, _\(\)]+)", comment)
            # print(res)
            if res:

                return self.getFunctionType(res)

        return None, None

    def getParameter(self):
        comment = self.getComment()
        list_param = None

        if comment:
            res = re.findall(
                r"(\@apiParam)[ ]+(?P<type>[a-zA-Z0-9=_\{\} ]+)[ ]+(?P<arg>[a-zA-Z0-9\[\]:=_\"]+)", comment)
            # print(res)
            if res:
                list_param = {v.strip("[ ]"): k.strip("{ }")
                              for _, k, v in res}
        return list_param

    def _getFakeDataBy(self, type_of_data=None, default="name"):
        if default is None:
            default = "name"
        faker = Faker()
        if type_of_data == None:
            type_of_data = default

        try:
            return getattr(faker, type_of_data.lower())()
        except AttributeError:
            return default

    def generateParameterData(self, list_param):
        arg_body = []
        faker = Faker()
        # print(list_param)
        boolean_value = choice([True, False])
        for arg_name, arg_type in list_param.items():
            type_of_data = None
            default = None
            value = None
            if "=" in arg_type:
                arg_type, type_of_data = arg_type.split("=")
            if "=" in arg_name:
                arg_name, default = arg_name.split("=")
            if arg_type.lower() == "string":

                if default:
                    default = default.strip("'\"")
                value = self._getFakeDataBy(type_of_data, default=default)
                arg_body.append("{}='{}'".format(
                    arg_name, value))
                self.list_parameter[arg_name] = {
                    "value": value, "type": arg_type.lower()}
            elif arg_type.lower() == "number":
                if default is None:
                    default = "random_number"
                value = self._getFakeDataBy(type_of_data, default=default)
                arg_body.append("{}={}".format(
                    arg_name, value))
                self.list_parameter[arg_name] = {
                    "value": value, "type": arg_type.lower()}
            elif arg_type.lower() == "boolean":
                arg_body.append("{}={}".format(
                    arg_name, boolean_value))
                self.list_parameter[arg_name] = boolean_value
                self.list_parameter[arg_name] = {
                    "value": boolean_value, "type": arg_type.lower()}
            else:
                pass
                # value = getattr(faker, arg_type.lower())()
                # arg_body.append("{}={}".format(
                #     arg_name, value))

        return arg_body

    def _get_object_name(self):
        return self.getParentName().lower()

    def method_initialization_name(self):
        return "{}_{}".format(self.getParentName().lower(), self.getName())

    def getAssertTest(self):

        r_type, r_value = self.getReturnType()
        list_param = self.getParameter()
        # print(list_param)
        func_body = None
        faker = Faker()

        if r_value and ("self" in r_value):
            r_value = r_value.replace("self", self._get_object_name())

        init_arg = self.parent.get_init_method_arg()

        # if self.parent:
        #     print(self.getParentName())

        arg_body = []
        # TODO: Change all the return name of the class method for example {}={}.{}({})
        if self.node.decorator_list:
            if self.getDecoration().id in ["classmethod", "staticmethod"]:
                if list_param:
                    arg_body = self.generateParameterData(list_param)
                    func_body = '''
        {}={}.{}({})'''.format(self.method_initialization_name(), self.getParentName(), self.getName(), ",".join(arg_body))

                else:
                    func_body = '''
        {}={}.{}()'''.format(self.method_initialization_name(), self.getParentName(), self.getName())
        else:
            if list_param:

                arg_body = self.generateParameterData(list_param)
                func_body = '''
        {0} = {1}({5})
        {4}={0}.{2}({3}) '''.format(self.getParentName().lower(), self.getParentName(), self.getName(), ",".join(arg_body), self.method_initialization_name(), init_arg)
            else:
                func_body = '''
        {0} = {1}({4})
        {3} = {0}.{2}() '''.format(self.getParentName().lower(), self.getParentName(), self.getName(), self.method_initialization_name(), init_arg)

        if self.parent.init_method:
            try:
                import_path = self.parent.import_path
                import_path += " import "
                # print("node module")
                # print(self.parent.parent.node_module)
                import_path += ",".join(self.parent.parent.node_module)
                code_str = import_path + "\n"+func_body
                func_body_format = (autopep8.fix_code(code_str))
                # print(func_body)
                codeObejct = compile(func_body_format, 'test', "exec")
                Vars = {}
                exec(codeObejct, globals(), Vars)

                if r_value.strip() == "'}'":
                    r_value = "'{}'".format(
                        Vars.get(self.method_initialization_name()))
            except ModuleNotFoundError:
                pass
            except TypeError:
                pass
            except ImportError:
                pass

        # print(type(r_type))
        # print(self.list_parameter)

        if isinstance(r_type, bool):
            if r_value == "True":
                return Templates.methodTest.format(
                    self.getName(), func_body, AssertUnitTestCase.assert_true.format(self.method_initialization_name(), r_value))
            return Templates.methodTest.format(
                self.getName(), func_body, AssertUnitTestCase.assert_false.format(self.method_initialization_name(), r_value))

        if isinstance(r_type, int) or isinstance(r_type, str) or isinstance(r_type, list) or isinstance(r_type, dict):
            # print(func_body)
            # print("start")
            # print(self.method_initialization_name())
            # print(r_value)
            # print("end")
            return Templates.methodTest.format(
                self.getName(), func_body, AssertUnitTestCase.assert_equal.format(self.method_initialization_name(), r_value))

        if isinstance(r_type, PyUnitObject):
            parameter = self.list_parameter.get(
                r_type.get_return_object_name())
            value = parameter.get("value")
            if parameter.get("type") == "string":
                value = "'{}'".format(value)

            return Templates.methodTest.format(
                self.getName(), func_body, AssertUnitTestCase.assert_equal.format(value, r_value))

        if r_type is None:
            return Templates.methodTest.format(
                self.getName(), func_body, AssertUnitTestCase.assert_is_none.format(self.method_initialization_name()))

    def run_test(self, func_body):
        # This is only will be used by function unit test implementation
        unit_file = self.parent.unit_file
        exec_import_path = "\nfrom importlib import reload\n"

        # import_path += "import {}".format(self.parent.module_name)
        import_path = self.parent.import_path
        import_path += " import "
        # print("node module")
        # print(self.parent.parent.node_module)
        import_path += ",".join(self.parent.node_module)

        exec_import_path += "import {}\n".format(unit_file.getRoot())

        unit_file = self.parent.unit_file

        # print("===>{}==>{}".format(unit_file.getModule(), unit_file.getRoot()))

        # print(import_path)

        exec_import_path += "\nreload({})\n".format(
            unit_file.getReloadPath())

        code_str = import_path + exec_import_path + "\n"+func_body
        func_body_format = (autopep8.fix_code(code_str))

        # print(func_body_format)
        codeObejct = compile(func_body_format, 'test', "exec")
        Vars = {}
        exec(codeObejct, globals(), Vars)
        return Vars

    def getFuncAssertTest(self):

        try:

            # print(self.getReturnType())
            r_type, r_value = self.getReturnType()
            list_param = self.getParameter()
            # print(list_param)
            func_body = None
            faker = Faker()

            # if self.parent:
            #     print(self.getParentName())

            arg_body = []

            if self.node.decorator_list:
                if self.getDecoration().id in ["classmethod", "staticmethod"]:
                    if list_param:
                        arg_body = self.generateParameterData(list_param)
                        func_body = '''
        {}={}({})'''.format(self.method_initialization_name(), self.getName(), ",".join(arg_body))

                    else:
                        func_body = '''
        {}={}()'''.format(self.method_initialization_name(), self.getName())
            else:
                if list_param:
                    arg_body = self.generateParameterData(list_param)
                    func_body = '''
        {} = {}({}) '''.format(self.getParentName().lower(), self.getName(), ",".join(arg_body))
                else:
                    func_body = '''
        {} = {}() '''.format(self.getParentName().lower(), self.getName())

            body = func_body
            # print(isinstance(r_type, bool))

            # print(func_body)

            test_result = self.run_test(func_body)
            # print(self.getParentName().lower())
            # print(test_result)
            # print(self.getName())
            # print(test_result.get(self.getParentName().lower()))
            # print(r_value.strip())
            if (r_value is not None) and (r_value.strip() == "'}'" or r_value.strip() == "}"):
                # print(self.getName())
                # print(test_result)
                test_ret = test_result.get(self.getParentName().lower())
                r_value = test_ret
                if isinstance(test_ret, str):
                    r_value = "'{}'".format(test_ret)

            if isinstance(r_type, bool):
                if r_value == "True":
                    return Templates.methodTest.format(
                        self.getName(), body, AssertUnitTestCase.assert_true.format(self.getParentName().lower(), r_value))
                return Templates.methodTest.format(
                    self.getName(), body, AssertUnitTestCase.assert_false.format(self.getParentName().lower(), r_value))

            if isinstance(r_type, int) or isinstance(r_type, str) or isinstance(r_type, list) or isinstance(r_type, dict):
                # print(func_body)
                return Templates.methodTest.format(
                    self.getName(), body, AssertUnitTestCase.assert_equal.format(self.getParentName().lower(), r_value))

            # print(self.getName())

            # if type(r_type) == object:
            #     print("in object")
            #     print(self.list_parameter)
            #     return Templates.methodTest.format(
            #         self.getName(), func_body, AssertUnitTestCase.assert_equal.format(self.getParentName().lower(), r_value))
            res_type = str
            if type(r_type) == PyUnitObject:
                # print(self.list_parameter)
                # print("in PyUnitObject")
                # print(self.list_parameter)

                value = None
                if isinstance(r_type.get_return_object_name(), list):
                    list_new_value = []

                    for param in r_type.get_return_object_name():
                        return_value, type_value = self.list_parameter.get(
                            param).values()
                        func_param = "{}".format(return_value)

                        if type_value == "string":
                            func_param = "'{}'".format(return_value)

                        list_new_value.append(func_param)

                    # print(list_new_value)
                    r_value = (re.sub("\([a-zA-Z0-9 _,\.]+\)",
                                      "({})".format(",".join(list_new_value)), r_value))

                    value = self.getParentName().lower()

                    # New code start here
                    # import_path = self.parent.import_path
                    # import_path += " import "

                    # # print("node module")
                    # # print(self.parent.parent.node_module)
                    # import_path += ",".join(self.parent.node_module)
                    # # print(import_path)
                    # code_str = import_path + "\n"+func_body
                    # func_body_format = (autopep8.fix_code(code_str))
                    # # print(func_body_format)
                    # codeObejct = compile(func_body_format, 'test', "exec")
                    # Vars = {}
                    # exec(codeObejct, globals(), Vars)
                    # # print(Vars)
                    # # print(self.getParentName().lower())
                    # res_type = type(Vars.get(self.getParentName().lower()))
                    # if r_value.strip() == "'}'":
                    #     r_value = "'{}'".format(
                    #         Vars.get(self.method_initialization_name()))

                else:
                    parameter = self.list_parameter.get(
                        r_type.get_return_object_name())

                    value = parameter.get("value")
                    if parameter.get("type") == "string":
                        value = "'{}'".format(value)

                # if not isinstance(res_type, (str, int, bool)):
                #     r_value = res_type.__name__
                #     return Templates.methodTest.format(
                #         self.getName(), func_body, AssertUnitTestCase.assert_is_instance.format(value, r_value))

                return Templates.methodTest.format(
                    self.getName(), func_body, AssertUnitTestCase.assert_equal.format(value, r_value))

            # print(self.getName())
            # print(type(r_type))
            if type(r_type) == type:

                Vars = self.run_test(func_body)
                # print(Vars)
                # print(self.getParentName().lower())
                res_type = type(Vars.get(self.getParentName().lower()))

                # print(Vars.get("pet_main"))
                # print(self.getName())
                # # print("{}".format(Vars.get(self.getParentName().lower())))
                # print(r_value)

                # if r_value.strip() == "'}'":
                #     r_value = "'{}'".format(
                #         Vars.get(self.method_initialization_name()))

                if not isinstance(res_type, (str, int, bool)):
                    r_value = res_type.__name__
                    return Templates.methodTest.format(
                        self.getName(), body, AssertUnitTestCase.assert_is_instance.format(self.getParentName().lower(), r_value))

            if r_type is None:
                return Templates.methodTest.format(
                    self.getName(), body, AssertUnitTestCase.assert_is_none.format(self.getParentName().lower()))

        except ModuleNotFoundError as ex:
            print(ex)

        except ImportError as ex:
            print(ex)

        except AttributeError as ex:
            print(ex)

        except Exception as ex:
            print(ex)
