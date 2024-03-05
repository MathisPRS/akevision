from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status


class UserRestTest(APITestCase):
    CREATE = 'Created'
    OK = 'OK'
    NO_CONTENT = 'No Content'
    NOT_ALLOWED = 'Method Not Allowed'

    def setUp(self):
        self.user = User.objects.create(username='akema')
        Token.objects.create(user_id=self.user.id, key='azerty123')
        self.token = Token.objects.get(user__username='akema')

    def add_permissions(self, model):
        content_type = ContentType.objects.get_for_model(model)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user.user_permissions.add(permission)

    def test_user_get_method(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        self.add_permissions(User)

        user = User.objects.get(username='akema')
        url = 'http://127.0.0.1:8000/controlequalite/users/' + str(user.id) + '/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_text, self.OK)
        self.assertEqual(len(response.data), 6)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['username'], 'akema')
        self.assertEqual(response.data['email'], '')
        self.assertEqual(response.data['firstName'], '')
        self.assertEqual(response.data['lastName'], '')
        self.assertEqual(response.data['groups'], [])

    def test_user_post_method(self):
        self.add_permissions(User)

        url = 'http://127.0.0.1:8000/controlequalite/users/'
        json_user = {
            'username': 'akemapost',
            'firstName': 'dg',
            'lastName': 'dg',
            'password': 'qgezsgh'
        }

        response = self.client.post(url, json_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_text, self.CREATE)
        self.assertEqual(len(response.data), 6)
        self.assertEqual(response.data['id'], 2)
        self.assertEqual(response.data['username'], 'akemapost')
        self.assertEqual(response.data['email'], '')
        self.assertEqual(response.data['firstName'], '')
        self.assertEqual(response.data['lastName'], '')
        self.assertEqual(response.data['groups'], [])

    def test_user_delete_method(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        self.add_permissions(User)

        User.objects.create(username='akema_delete')
        user = User.objects.get(username='akema_delete')

        url = 'http://127.0.0.1:8000/controlequalite/users/' + str(user.id) + '/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.status_text, self.NO_CONTENT)
        self.assertIsNone(response.data)

    def test_user_put_method(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        self.add_permissions(User)

        User.objects.create(username='akemaCreate', first_name='firstNameCreate', last_name='lastNameCreate')
        user = User.objects.get(username='akemaCreate')

        url = 'http://127.0.0.1:8000/controlequalite/users/' + str(user.id) + '/'
        json_user = {
            'username': 'akemaPut',
            'firstName': 'firstNamePut',
            'lastName': 'lastNamePut',
            'password': 'qgezsgh'
        }

        response = self.client.put(url, json_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_text, self.OK)
        self.assertEqual(len(response.data), 6)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['username'], 'akemaPut')
        self.assertEqual(response.data['email'], '')
        self.assertEqual(response.data['firstName'], 'firstNamePut')
        self.assertEqual(response.data['lastName'], 'lastNamePut')
        self.assertEqual(response.data['groups'], [])

    def test_user_patch_method(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        self.add_permissions(User)

        User.objects.create(username='akemaCreate', first_name='firstNameCreate', last_name='lastNameCreate',
                            email='emailCreate')
        user = User.objects.get(username='akemaCreate')

        url = 'http://127.0.0.1:8000/controlequalite/users/' + str(user.id) + '/'
        json_user = {
            'username': 'akemaPatch',
            'firstName': 'firstNamePatch',
        }

        response = self.client.patch(url, json_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_text, self.OK)
        self.assertEqual(len(response.data), 6)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['username'], 'akemaPatch')
        self.assertEqual(response.data['email'], 'emailCreate')
        self.assertEqual(response.data['firstName'], 'firstNamePatch')
        self.assertEqual(response.data['lastName'], 'lastNameCreate')
        self.assertEqual(response.data['groups'], [])
