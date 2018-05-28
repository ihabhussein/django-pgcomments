from django.test import TestCase
from pgcomments.models import Thread


class DeleteTestCase(TestCase):
    def setUp(self):
        thread = Thread.objects.create()
        thread.add_comment('', 'AnonymousUser', 'text 1')
        thread.add_comment('0', 'AnonymousUser', 'text 2')
        self.object = thread


    def test_set_delete(self):
        (path, name, value) = ('0', 'text', '')
        get_value = self.object.get_attribute(path, name)
        self.assertNotEqual(get_value, value)

        self.object.delete_comment(path, False)
        get_value = self.object.get_attribute(path, name)
        self.assertEqual(get_value, value)

    def test_set_delete_comment(self):
        (path, name, value) = ('0', 'children', [])
        get_value = self.object.get_attribute(path, name)
        self.assertNotEqual(get_value, value)

        self.object.delete_comment(path, False)
        get_value = self.object.get_attribute(path, name)
        self.assertNotEqual(get_value, value)

    def test_set_delete_recursive(self):
        (path, name, value) = ('0', 'children', [])
        get_value = self.object.get_attribute(path, name)
        self.assertNotEqual(get_value, value)

        self.object.delete_comment(path, True)
        get_value = self.object.get_attribute(path, name)
        self.assertEqual(get_value, value)
