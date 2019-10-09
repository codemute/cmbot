import queue

from tests.isolated_testcase import IsolatedTestCase


class HelloWorldTest(IsolatedTestCase):

    def test_hello_world_callback(self):
        self.assertCommand('hello world', 'Welcome to codemute!')
        with self.assertRaises(queue.Empty):
            self.assertCommand('helloworld', 'Welcome to codemute!')
