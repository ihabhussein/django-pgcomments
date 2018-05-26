from django.db import models
from pgcomments.models import Thread


class Post(models.Model):
    content = models.TextField(default='')
    comments = models.OneToOneField(Thread, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.comments_id is None:
            t = Thread()
            t.save()
            self.comments = t
        return super().save(*args, **kwargs)
