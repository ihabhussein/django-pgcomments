SECRET_KEY = '-dummy-key-'

INSTALLED_APPS = [
    'pgcomments',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    },
}
