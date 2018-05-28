from django.test import TestCase
from pgcomments.models import Thread


class AttributesTestCase(TestCase):
    def setUp(self):
        thread = Thread.objects.create()
        thread.add_comment('', 'AnonymousUser', 'text 1')
        thread.add_comment('0', 'AnonymousUser', 'text 2')
        self.object = thread


    def test_set_attr(self):
        (path, name, value) = ('0', 'votes', 3)
        self.object.set_attribute(path, name, value)
        get_value = self.object.get_attribute(path, name)
        self.assertEqual(get_value, value)

    def test_set_complex_attr(self):
        (path, name, value) = ('0,0', 'meta', {'this': 1, 'that': 2})
        self.object.set_attribute(path, name, value)
        get_value = self.object.get_attribute(path, name)
        self.assertEqual(get_value, value)

    def test_set_reserved_keys(self):
        (path, name, value) = ('0', 'author', 'new_value')
        with self.assertRaises(ValueError):
            self.object.set_attribute(path, name, value)
