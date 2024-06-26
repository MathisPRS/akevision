import logging
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from rest_framework import viewsets, pagination, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Compagnie, Client, AccessToken
from .serializers import CompagnieSerializer, ClientSerializer, UserSerializer, GroupSerializer

from .permissions import HasPermission
from .service import TokenService, ClientFileService, send_mail_information
from django.db import transaction


# from .import_excel.import_excel import get_excel
logger = logging.getLogger()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get_paginated_response(self, data):
        return Response(data)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated, HasPermission, ]
        return [permission() for permission in permission_classes]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_paginated_response(self, data):
        return Response(data)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated, HasPermission, ]
        return [permission() for permission in permission_classes]

class ManageFileViewSet(viewsets.ViewSet):
    model = None
    registry = None
    form_class = None

    # @transaction.atomic
    # @action(detail=False, methods=['post'], url_path='upload_select_file')
    # def upload_select_file(self, request, *args, **kwargs):
    #     try:
    #         excel_file = request.FILES['fileKey']
    #         data = get_excel(excel_file)
    #         return Response(data="data excel retrieve", status=status.HTTP_200_OK)
    #     except Exception as e:
    #         transaction.set_rollback(True)
    #         logger.error(str(e))
    #         return Response(data=str(e),
    #                         status=status.HTTP_400_BAD_REQUEST)

class MailViewset(viewsets.ViewSet):
    model = None
    registry = None
    form_class = None
    @transaction.atomic
    @action(detail=False, methods=['post'], url_path='send_mail')
    def send_mail(self, request, *args, **kwargs):
        try:
            send_mail_information()
            return Response(data="Mail correctement envoyé", status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            logger.error(str(e))
            return Response(data=str(e),
                            status=status.HTTP_400_BAD_REQUEST)
           
class CompagnieViewSet(viewsets.ModelViewSet):
    queryset = Compagnie.objects.all()
    serializer_class = CompagnieSerializer

    def list(self, request):
        compagnies = Compagnie.objects.all()
        serializer = CompagnieSerializer(compagnies, many=True)
        return Response(serializer.data)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):

        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save()
        TokenService.generate_access_token(client)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['GET'], url_path='download-script')
    def download_script(self, request, pk=None):
        client = self.get_object()
        token = str(AccessToken.objects.filter(client_acces_token=client).first())

        # Créer le fichier ZIP en mémoire à l'aide du service ClientFileService
        zip_content = ClientFileService.create_client_files(client.id, token)

        # Créer la réponse HTTP avec le fichier ZIP en pièce jointe
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="client_{client.id}.zip"'
        response.write(zip_content)

        return response
        
      