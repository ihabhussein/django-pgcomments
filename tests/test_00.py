from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from pgcomments.models import Thread


class BasicTestCase(TestCase):
    def setUp(self):
        thread = Thread.objects.create()
        thread.add_comment('', AnonymousUser, 'text 1')
        thread.add_comment('0', AnonymousUser, 'text 2')
        self.pk = thread.pk


    def test_create(self):
        self.assertNotEqual(self.pk, None)

    def test_threading(self):
        object = Thread.objects.get(pk=self.pk)
        self.assertEqual(len(object.thread), 1)
        self.assertEqual(len(object.thread[0]['children']), 1)
