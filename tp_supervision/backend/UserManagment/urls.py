
from  django.urls import path

from .views import *

urlpatterns = [
    path("api/register", user_registration_view, name="register"),
    path("api/login", user_login_view, name="login"),

]
