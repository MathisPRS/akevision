import random
import string
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework import serializers
from .models import Compagnie
from .models import Client

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
        fields = ['id', 'name','compagnie_id', 'os']
   
    def validate_name(self, value):
        print(value)
        if Client.objects.filter(name=value).exists():
            raise serializers.ValidationError('Un Client du meme nom existe déjà')
        return value
    
    def validate_compagnie_id(self, value):
        if not isinstance(value, int):
            value = value.id
        if not Compagnie.objects.filter(id=value).exists():
            raise serializers.ValidationError('La compagnie n\'existe pas')
        return value
    
    def validate_os(self, value):
        return value
    
    def create(self, validated_data):
        compagnie_id = validated_data['compagnie']
        compagnie = Compagnie.objects.get(id=compagnie_id)
        client = Client.objects.create(
            name=validated_data['name'],
            compagnie=compagnie,
            os=validated_data['os']
        )
        return client
    
    # def validate_security_key(self, value):
    #     print(value)
    #     return value