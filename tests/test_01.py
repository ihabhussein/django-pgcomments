from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from pgcomments.models import Thread


class AttributesTestCase(TestCase):
    def setUp(self):
        thread = Thread.objects.create()
        thread.add_comment('', AnonymousUser, 'text 1')
        thread.add_comment('0', AnonymousUser, 'text 2')
        self.pk = thread.pk


    def test_set_attr(self):
        object = Thread.objects.get(pk=self.pk)
        object.set_attribute('0', 'votes', 3)

        object = Thread.objects.get(pk=self.pk)
        self.assertEqual(object.get_attribute('0', 'votes'), 3)

    def test_set_complex_attr(self):
        object = Thread.objects.get(pk=self.pk)
        object.set_attribute('0,0', 'meta', {'this': 1, 'that': 2})

        object = Thread.objects.get(pk=self.pk)
        value = object.get_attribute('0,0', 'meta')
        self.assertEqual(value['this'], 1)
        self.assertEqual(value['that'], 2)

    def test_set_reserved_keys(self):
        object = Thread.objects.get(pk=self.pk)
        with self.assertRaises(ValueError):
            object.set_attribute('0', 'author', 'new_value')
