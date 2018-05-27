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
            cursor.execute("SELECT pgcomments_add_comment(%s, %s, %s, %s)", (
                self.pk, self._fix_path(path), user.username, text,
            ))

    def set_attribute(self, path, name, value):
        with connection.cursor() as cursor:
            cursor.execute("SELECT pgcomments_set_attribute(%s, %s, %s, %s::jsonb)", (
                self.pk, self._fix_path(path), name, json.dumps(value),
            ))

    def get_attribute(self, path, name):
        with connection.cursor() as cursor:
            cursor.execute("SELECT pgcomments_get_attribute(%s, %s, %s)", (
                self.pk, self._fix_path(path), name,
            ))
            row = cursor.fetch_one()
            return json.loads(row[0])
