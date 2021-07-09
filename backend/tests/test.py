from backend.database import User
from backend import app
from flask.testing import FlaskClient
import os
import json
import pprint
from werkzeug.datastructures import Headers
import flask_unittest
BASE_DIR = os.path.abspath(os.path.curdir)
print(BASE_DIR)
class BaseTestCase(flask_unittest.ClientTestCase):
    app = app
    app_client = app.test_client()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'db_test.sqlite3')
    def setUp(self, client: FlaskClient) -> None:
        return super().setUp(client)
    
    def get(self, url,  data={}):
        payload = json.dumps(data)
        return self.app_client.get(url, headers={'Content-Type': 'application/json'}, data=payload)
    
    def post(self, url,   data={}):
        payload = json.dumps(data)
        return self.app_client.post(url, headers={'Content-Type': 'application/json'}, data=payload)
    
    def put(self, url,   data={}):
        payload = json.dumps(data)
        return self.app_client.put(url, headers={'Content-Type': 'application/json'}, data=payload)
    
    def delete(self, url,   data={}):
        payload = json.dumps(data)
        return self.app_client.delete(url, headers={'Content-Type': 'application/json'}, data=payload)

class HomePageTest(BaseTestCase):
    def test_login(self, client: FlaskClient ):
        
        
        response = self.post(
            '/auth/login/', 
            data={'email': 'otiboatengjoe@gmail.com', 'password': 'password'},
        )
        data = response.json
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Login successful.")

    def test_signup(self, *args, **kwargs):
        response = self.post('/auth/signup/', {'name': "SomeUser", "email": "Someemail@gmail.com", "password": "somepassword"})
        data = response.json
        self.assertEqual(data['success'], True)
        pprint.pprint(data)
        self.assertIsNotNone(User.query.first(), None)