import websiteconfig
import time
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(BASE_DIR, 'db_test.sqlite3')
websiteconfig.DATABASE_URI = 'sqlite:///' + database_path
websiteconfig.SQLALCHEMY_DATABASE_URI = websiteconfig.DATABASE_URI
from backend import app
from backend.tests import *

if __name__ == "__main__":
    import unittest
    unittest.main()
    time.sleep(2)
    os.remove(database_path)