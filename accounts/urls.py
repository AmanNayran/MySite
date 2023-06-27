from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('list/', UserListView.as_view(), name='list'),
]
