from django.test import TestCase
from pgcomments.models import Thread


class BasicTestCase(TestCase):
    def setUp(self):
        thread = Thread.objects.create()
        thread.add_comment('', 'AnonymousUser', 'text 1')
        thread.add_comment('0', 'AnonymousUser', 'text 2')
        self.object = thread


    def test_create(self):
        self.assertNotEqual(self.object.pk, None)

    def test_threading(self):
        self.assertEqual(len(self.object.thread), 1)
        self.assertEqual(len(self.object.thread[0]['children']), 1)
