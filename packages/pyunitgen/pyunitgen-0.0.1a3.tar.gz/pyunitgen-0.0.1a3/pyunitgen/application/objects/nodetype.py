

class NodeType:

    re_bool = "bool"
    re_none = '''
      raise NotImplementedError() #TODO: test %s'''


class AssertUnitTestCase:

    assert_none = '''raise NotImplementedError() #TODO: test %s'''

    assert_true = """
        self.assertTrue({},{})"""

    assert_false = '''
        self.assertFalse({},{})'''

    assert_equal = """
        self.assertEqual({}, {}) """

    assert_not_equal = """
        self.assertNotEqual({}, {}) """

    assert_is = """
        self.assertIs({}, {}) """

    assert_is_not = """
        self.assertIsNot({}, {}) """

    assert_is_none = """
        self.assertIsNone({}) """

    assert_is_not_none = """
        self.assertIsNotNone({},{})"""

    assert_in = """
        self.assertIn({}, {}) """

    assert_not_in = """
        self.assertNotIn({}, {}) """

    assert_is_instance = """
        self.assertIsInstance({}, {}) """

    assert_not_is_instance = """
        self.assertNotIsInstance({},{})"""
