from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Investor


class UserRegistrationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not (username and email and password):
            return Response({'error': 'Por favor, forneça um username, email e password.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username já está em uso.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        investor = Investor(user=user, risk_profile='conservador')
        investor.save()

        return Response({'success': 'Usuário registrado com sucesso.'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not (username and password):
            return Response({'error': 'Por favor, forneça um username e password.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'success': 'Login realizado com sucesso.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'success': 'Logout realizado com sucesso.'}, status=status.HTTP_200_OK)

