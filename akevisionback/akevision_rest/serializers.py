from django.contrib.auth.models import User, Group
from rest_framework import serializers

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

