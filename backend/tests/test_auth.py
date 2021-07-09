from backend.database import db_session, User
from flask.testing import FlaskClient
from backend import utils
from .base import BaseTestCase

class HomePageTest(BaseTestCase):
    def test_login(self, client: FlaskClient ):
        name="testuser"
        password="password"
        email="testemail@gmail.com"
        u = User(name=name, email=email, password=utils.hash_password(password))
        db_session.add(u)
        db_session.commit()
        response = self.post(
            '/auth/login/', 
            data={'email': email, 'password': password},
        )
        data = response.json
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Login successful.")

    def test_signup(self, *args, **kwargs):
        response = self.post('/auth/signup/', {'name': "SomeUser", "email": "Someemail@gmail.com", "password": "somepassword"})
        data = response.json
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(User.query.first(), None)
    
    