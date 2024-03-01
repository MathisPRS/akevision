from django.contrib.auth import login, logout

from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from django.utils import timezone
from .serializers import UserSerializer


class AuthAPIView(ObtainAuthToken):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        for field in 'username', 'password':
            if field not in request.data:
                # logger.warning("Missing field '%s' for authentication", field, extra={'request': request})
                return Response({'detail': "Field '%s' is mandatory for authentication." % field},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        if user and user.is_active:
            user.last_login = timezone.now()
            user.save()
            login(request, user)
            return Response(
                data={
                    "user": UserSerializer(
                        request.user, context={"request": request}
                    ).data,
                    "token": token.key,
                },
                status=status.HTTP_201_CREATED,
            )
        raise AuthenticationFailed

    def delete(self, request, *args, **kwargs):
        user = getattr(request, 'user', None)
        logout(request)
        created = Token.objects.filter(user_id=user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'POST':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]