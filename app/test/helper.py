# pylint: disable=missing-class-docstring, missing-function-docstring
import json

def login_user(client):
    return client.post(
        '/auth/login',
        data=json.dumps(dict(
            username='joe@gmail.com',
            password='123456'
        )),
        content_type='application/json'
    )
def register_user(client):
    return client.post(
        '/users',
        data=json.dumps(dict(
            username='joe@gmail.com',
            password='123456'
        )),
        content_type='application/json'
    )
