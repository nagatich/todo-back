from django.urls import path

from .views import (
    LoginAPIView,
    LogoutAPIView,
    RegisterAPIView,
    ProfileAPIView,
)

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
]
