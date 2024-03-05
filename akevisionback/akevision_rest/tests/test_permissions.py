from unittest.mock import MagicMock

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from ..models import Caracteristique
from ..permissions import HasPermission


class PermissionsTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='akema')
        Token.objects.create(user_id=self.user.id, key='azerty123')
        self.token = Token.objects.get(user__username='akema')

    def test_get_permission_action_view_list(self):
        # given
        action_view = 'list'

        # when
        action_permission = HasPermission().get_permission_action(action_view)

        # then
        self.assertEqual(action_permission, 'view_')

    def test_get_permission_action_view_retrieve(self):
        # given
        action_view = 'retrieve'

        # when
        action_permission = HasPermission().get_permission_action(action_view)

        # then
        self.assertEqual(action_permission, 'view_')

    def test_get_permission_action_view_update(self):
        # given
        action_view = 'update'

        # when
        action_permission = HasPermission().get_permission_action(action_view)

        # then
        self.assertEqual(action_permission, 'change_')

    def test_get_permission_action_view_partial_update(self):
        # given
        action_view = 'partial_update'

        # when
        action_permission = HasPermission().get_permission_action(action_view)

        # then
        self.assertEqual(action_permission, 'change_')

    def test_get_permission_action_view_destroy(self):
        # given
        action_view = 'destroy'

        # when
        action_permission = HasPermission().get_permission_action(action_view)

        # then
        self.assertEqual(action_permission, 'delete_')

    def test_get_permission_action_view_create(self):
        # given
        action_view = 'create'

        # when
        action_permission = HasPermission().get_permission_action(action_view)

        # then
        self.assertEqual(action_permission, 'add_')

    def test_get_permission_action_view_None(self):
        # given
        action_view = None

        # when
        action_permission = HasPermission().get_permission_action(action_view)

        # then
        self.assertEqual(action_permission, None)

    def test_get_permission_action_view_Empty(self):
        # given
        action_view = ''

        # when
        action_permission = HasPermission().get_permission_action(action_view)

        # then
        self.assertEqual(action_permission, None)

    def test_has_permission_user_no_permission(self):
        # given
        self.request = MagicMock(user=self.user)
        self.queryset = MagicMock(model=Caracteristique)
        self.view = MagicMock(action='list', queryset=self.queryset)

        # when
        result = HasPermission().has_permission(self.request, self.view)

        # then
        self.assertEqual(result, False)

    def test_has_permission_user_one_good_permission(self):
        # given
        self.request = MagicMock(user=self.user)
        self.queryset = MagicMock(model=Caracteristique)
        self.view = MagicMock(action='list', queryset=self.queryset)

        content_type = ContentType.objects.get_for_model(Caracteristique)
        permission = Permission.objects.filter(content_type=content_type, codename__startswith='view_').first()
        self.user.user_permissions.add(permission)

        # when
        result = HasPermission().has_permission(self.request, self.view)

        # then
        self.assertEqual(result, True)

    def test_has_permission_user_one_bad_permission(self):
        # given
        self.request = MagicMock(user=self.user)
        self.queryset = MagicMock(model=Caracteristique)
        self.view = MagicMock(action='list', queryset=self.queryset)

        content_type = ContentType.objects.get_for_model(Caracteristique)
        permission = Permission.objects.filter(content_type=content_type, codename__startswith='add_').first()
        self.user.user_permissions.add(permission)

        # when
        result = HasPermission().has_permission(self.request, self.view)

        # then
        self.assertEqual(result, False)
