from django.urls import path
from .views import PasswordView

urlpatterns = [
    path('password/<str:service_name>/', PasswordView.as_view()),
    path('password/', PasswordView.as_view()),
]
