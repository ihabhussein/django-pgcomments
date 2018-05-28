import json
from django.db import models, connection
from django.contrib.postgres.fields import JSONField


RESERVED_KEYS = [
    'author', 'text', 'created_at', 'children',
]


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
            cursor.execute(
                "SELECT pgcomments_add_comment(%s, %s, %s, %s)",
                (self.pk, self._fix_path(path), user, text)
            )
        self.refresh_from_db()

    def delete_comment(self, path, recursive):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT pgcomments_delete_{0}(%s, %s)".format('thread' if recursive else 'comment'),
                (self.pk, self._fix_path(path))
            )
        self.refresh_from_db()

    def set_attribute(self, path, name, value):
        if name in RESERVED_KEYS:
            raise ValueError("""
                Can not change any of the reserved keys: {0}
            """.format(RESERVED_KEYS))

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT pgcomments_set_attribute(%s, %s, %s, %s::jsonb)",
                (self.pk, self._fix_path(path), name, json.dumps(value))
            )
        self.refresh_from_db()

    def get_attribute(self, path, name):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT pgcomments_get_attribute(%s, %s, %s)",
                (self.pk, self._fix_path(path), name)
            )
            row = cursor.fetchone()
            return row[0]
