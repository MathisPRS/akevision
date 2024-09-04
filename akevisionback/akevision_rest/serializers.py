from ipaddress import ip_address
from urllib.parse import urlparse
from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions
from .models import Compagnie, Client, GroupeWebsite, Website
from .service import TokenService, ClientFileService
from django.http import HttpResponseServerError
from akevision_rest import async_service

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True)
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'firstName', 'lastName', 'password', 'groups']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        groups_data = validated_data.pop('groups')
        for group_data in groups_data:
            user.groups.add(group_data)
        user.set_password(validated_data['password'])
        return user

class CompagnieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compagnie
        fields = ['id', 'name']

    def validate_name(self, value):
        if Compagnie.objects.filter(name=value).exists():
            raise serializers.ValidationError('La compagnie existe déjà')
        return value

class ClientSerializer(serializers.ModelSerializer):
    compagnie_id = serializers.PrimaryKeyRelatedField(queryset=Compagnie.objects.all(), source='compagnie')

    class Meta:
        model = Client
        fields = ['id', 'name', 'compagnie_id', 'os', 'ipv4']
   
    def validate_name(self, value):
        compagnie_id = self.initial_data.get('compagnie_id')
        if Client.objects.filter(name=value, compagnie_id=compagnie_id).exists():
            raise HttpResponseServerError('Un client du même nom existe déjà dans cette compagnie')
        return value
    
    def validate_compagnie_id(self, value):
        if not isinstance(value, int):
            value = value.id
        if not Compagnie.objects.filter(id=value).exists():
            raise HttpResponseServerError('La compagnie n\'existe pas')
        return value
    
    def validate_ipv4(self, value):
        try:
            ip_address(value)
        except ValueError:
            raise HttpResponseServerError('La valeur n\'est pas une adresse IPv4 valide')
        return value
    
    def create(self, validated_data):
        compagnie_id = validated_data['compagnie']
        compagnie = Compagnie.objects.get(id=compagnie_id)
        client = Client.objects.create(
            name=validated_data['name'],
            compagnie=compagnie,
            os=validated_data['os'],
            ipv4=validated_data['ipv4']
        )
        token = TokenService.generate_access_token(client)
        ClientFileService.create_client_files(client.id,)

        return client
    

class GroupeWebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupeWebsite
        fields = ['id', 'name']


class WebsiteSerializer(serializers.ModelSerializer):
    groupe_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Website
        fields = ['id', 'nameWebsite', 'url', 'alerte', 'groupe_name']

    def validate(self, data):
        groupe_name = data.get('groupe_name')
        nameWebsite = data.get('nameWebsite')
        url = data.get('url')

        # Check if URL is valid
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise serializers.ValidationError("Invalid URL")
        except ValueError:
            raise serializers.ValidationError("Invalid URL")

        # Check if groupe_name is provided
        if groupe_name:
            # Get or create groupe
            groupe, created = GroupeWebsite.objects.get_or_create(name=groupe_name)
            data['groupe_id'] = groupe.id

        # Check for duplicate website names within the same group
        if Website.objects.filter(nameWebsite=nameWebsite, groupe_id=data.get('groupe_id')).exists():
            raise serializers.ValidationError("Website with this name already exists in this group")

        return data

    def create(self, validated_data):
        groupe_id = validated_data.pop('groupe_id', None)
        validated_data.pop('groupe_name', None)  # Remove groupe_name from validated_data

        website = Website.objects.create(**validated_data)
        if groupe_id:
            website.groupe_id = groupe_id
            website.save()
            async_service.update_ssl_expiration()
        return website