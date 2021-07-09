from backend.tests import base
from backend.database import Project
from backend import schema

class TestProject(base.BaseTestCase):
    def test_create_project(self, *args, **kwargs):
        user = base.create_random_user()
        self.login(user=user)
        response = self.post('/project/', data={'name': "Test Project"})
        data = response.json

        self.assertTrue(data['success'])
        self.assertIsInstance(data['result'], dict)
        self.assertEqual(data['result']['name'], "Test Project")
        self.assertEqual(data['result']['manager'], schema.UserSchema().dump(user))
        self.logout()