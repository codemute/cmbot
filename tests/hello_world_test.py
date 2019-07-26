from tests.isolated_testcase import IsolatedTestCase


class HelloWorldTest(IsolatedTestCase):

    def test_hello_world_callback(self):
        self.assertCommand('hello world', 'Welcome to codemute!')
        self.assertCommand('Hello World', 'Welcome to codemute!')
        self.assertCommand('hello, world', 'Welcome to codemute!')
