
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SECRET_KEY = 'taskuptestkey'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'db.sqlite3')
DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'db.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}
ADMINS = frozenset(['http://taskup.com'])


del os