# django-pgcomments

A simple Django app to store comment threads in PostgreSQL using a `jsonb`
field.

## Features

- Nested comment threading

- Comment author (string) and time stamp

- Setting and getting extra comment attributes (for "likes", "votes", "links",
  ..., etc)

## Installation

The app can be installed using `pip`:

    pip3 install django-pgcomments

## Usage

Add `pgcomments` to your Django project's `INSTALLED_APPS`. In `settings.py`:

    INSTALLED_APPS = [
        ...
        'pgcomments',
        ...
    ]

then migrate the database to create the needed tables and functions. From the
command line:

    manage.py migrate


Include a `OneToOneField` in your model for the comments:

    class BlogPost(models.Model):
        ...
        comments = models.OneToOneField(Thread, on_delete=models.CASCADE)
        ...

To display the comments, there is a template included in the app to recursively
render the nested comment threads. In your template:

    {% include "pgcomments/thread.html" with list=object.comments prefix=',' %}

## License

The code is released under the 2-clause BSD license.
