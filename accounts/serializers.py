from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Investor

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

class InvestorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Investor
        fields = ['user', 'perfil_de_risco']
