from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from django.conf import settings
from .group_views import *
from .views import *


urlpatterns = [
    path('users/registera/', register_admin, name='register_admin'),
    path('users/register/<str:token>/', register_user, name='register_user'),
    path('users/<int:user_id>/permissions/<str:token>/', set_user_permissions, name='set_user_permissions'),
    path('users/<str:token>/', user_list_view, name='user_list'),
    path('users/<int:id>/<str:token>/', update_user, name='update_user'),
    path('users/user_delete/<str:token>/', views.delete_user, name='user_info'),
    path('users/change_password/<str:token>/', views.change_password, name='user_info'),
    path('users/login', login_user, name='login_user'),
    path('users/logout/', logout_user, name='logout_user'),
    path('users/<int:user_id>/<str:token>/', user_detail_view, name='user_detail'),
    path('users/<int:user_id>/permissions/<int:permission_id>/<str:token>/', add_permission_to_user, name='add_permission_to_user'),

  



    path('machines/<str:token>/', views.machine_list, name='machine-list'),
    path('machines/<int:pk>/<str:token>/', views.machine_detail, name='machine-detail'),
    # path('data/<str:token>/', views.data_list, name='data-list'),
    # path('data/<int:pk>/<str:token>/', views.data_detail, name='data-detail'),
    path('variabledata/<int:pk>/<str:token>/', views.variable_data_list, name='variabledata-list'),
    # path('variabledata/<int:pk>/', views.variable_data_detail, name='variabledata-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
