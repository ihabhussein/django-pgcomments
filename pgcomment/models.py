import json
from django.db import models, connection
from django.contrib.postgres.fields import JSONField


class Thread(models.Model):
    thread = JSONField(default=list)

    def __str__(self):
        return json.dumps(self.thread)

    def __iter__(self):
        return iter(self.thread)

    @classmethod
    def _fix_path(self, path):
        try:
            return list(map(int, path.strip(',').split(',')))
        except:
            return []

    def add_comment(self, path, user, text):
        with connection.cursor() as cursor:
            cursor.execute("SELECT pgcomment_add_comment(%s, %s, %s, %s);", (
                self.pk, self._fix_path(path), user.username, text,
            ))

    def set_comment_attributes(self, path, new_value):
        with connection.cursor() as cursor:
            cursor.execute("SELECT pgcomment_set_comment_attributes(%s, %s, %s);", (
                self.pk, self._fix_path(path), json.dumps(new_value),
            ))
