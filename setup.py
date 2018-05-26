from distutils.core import setup
setup(
    name = 'django_pgcomments',
    packages = ['pgcomments'],
    version = '0.1',
    description = 'A simple package for comment threads',
    author = 'Ihab Hussein',
    author_email = 'ihab@ihabhussein.com',
    license = 'BSD',
    url = 'https://github.com/ihabhussein/django-pgcomments',
    keywords = ['postgresql', 'comments',],
    classifiers = [
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Topic :: Communications :: Chat',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
    ]
)
