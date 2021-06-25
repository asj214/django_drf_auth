from django.urls import path
from .views import (
    RegisterUserView,
    LoginUserView,
    AuthMeView
)


urlpatterns = [
    path(r'customers/register', RegisterUserView.as_view()),
    path(r'customers/login', LoginUserView.as_view()),
    path(r'customers/me', AuthMeView.as_view()),
]