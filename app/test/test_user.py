# pylint: disable=missing-class-docstring, missing-function-docstring
import unittest
import json

from app.main import db
from app.test.base import BaseTestCase
from app.main.model.user import User
from app.test.helper import register_user, login_user

def create_user(username):
    new_user = User(
        username=username,
        password='123456'
    )
    db.session.add(new_user)
    db.session.flush()
    return new_user

class TestUserBlueprint(BaseTestCase):
    token = ''
    def setUp(self):
        super(TestUserBlueprint, self).setUp()
        register_user(self.client)
        resp = login_user(self.client)
        data = json.loads(resp.data.decode())
        self.token = 'Bearer ' + data['Authorization']

    def test_search_user_not_auth(self):
        with self.client:
            resp = self.client.get('/users')
            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Provide a valid auth token.')
            self.assertEqual(resp.status_code, 401)

    def test_search_user_basic(self):
        with self.client:
            create_user('abcabc')
            db.session.commit()
            resp = self.client.get('/users', headers={
                'Authorization': self.token,
            })
            data = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(len(data) <= 5)
            self.assertIn('abcabc', [d['username'] for d in data['data']])

    def test_search_user_able_to_search(self):
        with self.client:
            create_user('zombie')
            db.session.commit()
            resp = self.client.get('/users?username=zom', headers={
                'Authorization': self.token,
            })
            data = json.loads(resp.data.decode())
            self.assert200(resp)
            self.assertIn('zombie', [d['username'] for d in data['data']])

    def test_search_user_for_start_with_only(self):
        with self.client:
            create_user('kokookok')
            db.session.commit()
            resp = self.client.get('/users?username=ok', headers={
                'Authorization': self.token,
            })
            data = json.loads(resp.data.decode())
            self.assert200(resp)
            self.assertNotIn('abcabc', [d['username'] for d in data['data']])

if __name__ == '__main__':
    unittest.main()
