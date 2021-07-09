import os

import flask_unittest
from backend import app
from backend.database import User,db_session, init_db, clean_db
from backend import utils
import json

BASE_DIR = os.path.abspath(os.path.curdir)

test_user_name = "name"
test_user_email = "email@email.com"
test_user_password = "password"

def create_random_user() -> User:
    u = User(name=test_user_name, email=test_user_email, password=utils.hash_password(test_user_password))
    db_session.add(u)
    db_session.commit()
    return u

class BaseTestCase(flask_unittest.ClientTestCase):
    app = app
    app_client = app.test_client()
    _headers = {
        "Content-Type": 'application/json'
    }

    def setUp(self, *args, **kwargs) -> None:
        init_db()
        return super().setUp(*args, **kwargs)

    
    

    def tearDown(self, *args, **kwargs):
        clean_db()
        return super().tearDown(*args, **kwargs)
    
    def login(self,user: User,  url='/auth/login/'):
        print(user)
        if user is None:
            user = create_random_user()        
        
        token = user.encode_auth_token(user.id)
        self._headers['Authorization'] = f"Bearer {token}"
        return True

    def logout(self):
        self._headers.pop('Authorization')
        return True

    def get(self, url,  data={}):
        payload = json.dumps(data)
        return self.app_client.get(url, headers=self._headers, data=payload)
    
    def post(self, url,   data={}):
        payload = json.dumps(data)
        return self.app_client.post(url, headers=self._headers, data=payload)
    
    def put(self, url,   data={}):
        payload = json.dumps(data)
        return self.app_client.put(url, headers=self._headers, data=payload)
    
    def delete(self, url,   data={}):
        payload = json.dumps(data)
        return self.app_client.delete(url, headers=self._headers, data=payload)
