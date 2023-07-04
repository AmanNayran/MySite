from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('list/', UserLoginView.as_view(), name='list'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
