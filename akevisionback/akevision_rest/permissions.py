from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


class HasPermission(permissions.BasePermission):
    def get_permission_action(self, action_view):
        """
        retourne la "permission action" qui correspond à l'action de la vue passée en paramètre
        :param action (string): l'action de la vue
        :return (string): la permission action
        """
        if action_view in ('list', 'retrieve'):
            return 'view_'
        if action_view in ('update', 'partial_update'):
            return 'change_'
        elif action_view == 'destroy':
            return 'delete_'
        elif action_view in ('create', 'process', 'send_mail'):
            return 'add_'
        else:
            return None

    def has_permission(self, request, view):
        """
        Test que l'utilisateur a la permission d'executer la requête en fonction des droits de l'utilisateur sur le model
        :param request: la requête http
        :param view: vue appelée
        :return (boolean) : True s'il a la permission sinon False
        """
        permission = None
        action_permission = self.get_permission_action(view.action)
        content_type = ContentType.objects.get_for_model(view.queryset.model)

        if action_permission:
            permission = Permission.objects.filter(content_type=content_type,
                                                   codename__startswith=action_permission).first()
        if permission:
            return request.user.has_perm(content_type.app_label + '.' + permission.codename)
        return False
