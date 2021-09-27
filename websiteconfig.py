
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SECRET_KEY = 'taskuptestkey'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'db.sqlite3')
DATABASE_URI = SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}
ADMINS = frozenset(['http://taskup.com'])

if os.environ.get('DATABASE_URI'):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']

del os