from django.urls import path
from .views import (
    RegisterUserView,
    LoginUserView,
    AuthMeView
)


urlpatterns = [
    path(r'auth/register', RegisterUserView.as_view()),
    path(r'auth/login', LoginUserView.as_view()),
    path(r'auth/me', AuthMeView.as_view()),
]