# pylint: disable=missing-class-docstring, missing-function-docstring
import os
import unittest
import json
import magic
from werkzeug.datastructures import FileStorage

from app.test.base import BaseTestCase
from app.test.helper import register_user, login_user
from app.main.service.media_helper import MediaHelper
from app.main.model.user import User

def create_post(client, description, token, filename=None):
    data = {'description': description}
    if filename:
        filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
        file = open(filepath, 'rb')
        mime = magic.from_buffer(file.read(1024), mime=True)
        file.seek(0)
        data['media'] = FileStorage(
            stream=file,
            filename=filename,
            content_type=mime
        )

    return client.post(
        '/posts',
        data=data,
        content_type='multipart/form-data',
        headers={'Authorization': token}
    )

# pylint: disable=dangerous-default-value
# pylint: disable=too-many-arguments
def search_post(client, token, user_ids=[], page_size=20, page_num=0, order='desc'):
    url = '/posts?filters[user_ids]={}&page[size]={}&page[number]={}&order={}'.format(
        ','.join([str(u) for u in user_ids]),
        page_size,
        page_num,
        order
    )
    return client.get(url, headers={'Authorization': token})

def delete_file_from_post(post):
    for med in post['medias']:
        MediaHelper.del_file(med['path'].rsplit('/')[1])

class TestPostBlueprint(BaseTestCase):
    token = ''
    def setUp(self):
        super(TestPostBlueprint, self).setUp()
        register_user(self.client)
        resp = login_user(self.client)
        data = json.loads(resp.data.decode())
        self.token = 'Bearer ' + data['Authorization']

    def test_create_post_non_auth(self):
        with self.client:
            resp = create_post(self.client, 'whatever', '', 'fixture/favicon.ico')
            self.assert401(resp)

    def test_create_post_without_file(self):
        resp = create_post(self.client, 'test_create_post_without_file', self.token)
        data = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 201)
        post = data['data']
        self.assertEqual(post['description'], 'test_create_post_without_file')
        self.assertEqual(len(post['medias']), 0)

    def test_create_post_with_image(self):
        with self.client:
            resp = create_post(self.client, 'whatever', self.token, 'fixture/favicon.ico')
            data = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 201)
            post = data['data']
            self.assertEqual(post['description'], 'whatever')
            self.assertEqual(len(post['medias']), 1)
            self.assertEqual(post['medias'][0]['media_type'], 'image')
            delete_file_from_post(post)

    def test_create_post_with_video(self):
        with self.client:
            resp = create_post(self.client, 'whatever', self.token, 'fixture/small.mp4')
            data = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 201)
            post = data['data']
            self.assertEqual(post['description'], 'whatever')
            self.assertEqual(len(post['medias']), 1)
            self.assertEqual(post['medias'][0]['media_type'], 'video')
            delete_file_from_post(post)

    def test_create_post_with_txt(self):
        with self.client:
            resp = create_post(self.client, 'whatever', self.token, 'fixture/temp.txt')
            data = json.loads(resp.data.decode())
            self.assert400(resp)
            self.assertEqual(data['errors']['media'], 'Media can only be image / video')
            self.assertEqual(data['message'], 'Invalid request')

    def test_create_post_too_short(self):
        with self.client:
            resp = create_post(self.client, '', self.token)
            data = json.loads(resp.data.decode())
            self.assert400(resp)
            self.assertEqual(data['errors']['description'], 'Description too short (<1 characters)')
            self.assertEqual(data['message'], 'Invalid request')


    def test_list_post_non_auth(self):
        with self.client:
            resp = search_post(self.client, '')
            self.assert401(resp)

    def test_list_post(self):
        with self.client:
            create_post(self.client, 'aaaa', self.token)

            resp = search_post(self.client, self.token)
            data = json.loads(resp.data.decode())
            self.assert200(resp)
            self.assertGreater(len(data['data']), 0)
            self.assertIn('aaaa', [p['description'] for p in data['data']])

    def test_list_post_desc_order(self):
        with self.client:
            create_post(self.client, 'a', self.token)
            create_post(self.client, 'b', self.token)

            resp = search_post(self.client, self.token, order='desc')
            data = json.loads(resp.data.decode())
            self.assert200(resp)
            self.assertGreater(len(data['data']), 0)
            self.assertEqual(['b', 'a'], [p['description'] for p in data['data']])

    def test_list_post_asc_order(self):
        with self.client:
            create_post(self.client, 'a', self.token)
            create_post(self.client, 'b', self.token)

            resp = search_post(self.client, self.token, order='asc')
            data = json.loads(resp.data.decode())
            self.assert200(resp)
            self.assertGreater(len(data['data']), 0)
            self.assertEqual(['a', 'b'], [p['description'] for p in data['data']])

    def test_list_post_filter_user_ids(self):
        with self.client:
            current_user = User.decode_auth_token(self.token[len('Bearer '):])
            create_post(self.client, 'test_list_post_filter_user_ids', self.token)
            resp = search_post(self.client, self.token, user_ids=[current_user])
            data = json.loads(resp.data.decode())
            self.assert200(resp)
            self.assertGreater(len(data['data']), 0)
            self.assertIn(
                'test_list_post_filter_user_ids',
                [p['description'] for p in data['data']]
            )

    def test_list_post_filter_other_user(self):
        with self.client:
            create_post(self.client, 'test_list_post_filter_other_user', self.token)

            resp = search_post(self.client, self.token, user_ids=[99999999])
            data = json.loads(resp.data.decode())
            self.assert200(resp)
            self.assertEqual(len(data['data']), 0)
            self.assertNotIn(
                'test_list_post_filter_other_user',
                [p['description'] for p in data['data']]
            )


if __name__ == '__main__':
    unittest.main()
