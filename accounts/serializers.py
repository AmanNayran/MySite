from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Investor

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class InvestorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Investor
        fields = ['user', 'perfil_de_risco']
