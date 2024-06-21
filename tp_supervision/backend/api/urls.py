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

    path('groups/<int:id>/<str:token>/', delete_group, name='delete-group'),
    path('groups/<int:id>/<str:token>/', update_group, name='update-group'),
    path('groups/<int:group_id>/permissions/<str:token>/', set_group_permissions, name='set-group-permissions'),
    path('groups/<int:group_id>/users/<str:token>/', set_users_in_group, name='set-users-in-group'),
    path('groups/<int:group_id>/users/<int:user_id>/<str:token>/', add_user_to_group, name='add-user-to-group'),
    path('groups/<str:token>/', create_group, name='create-group'),
    path('groups/<int:group_id>/<str:token>/', group_detail_view, name='group-detail'),
    path('users/<int:user_id>/groups/<int:group_id>/<str:token>/', remove_user_from_group, name='remove_user_from_group'),
    path('groups/<str:token>/', group_list_view, name='group-list'),
    path('users/<int:user_id>/permissions/<int:permission_id>/<str:token>/', disable_permission_for_user, name='disable_permission_for_user'),
    path('groups/<int:group_id>/permissions/<int:permission_id>/<str:token>/', disable_permission_in_group, name='disable_permission_in_group'),



    path('machines/<str:token>/', views.machine_list, name='machine-list'),
    path('machines/<int:pk>/<str:token>/', views.machine_detail, name='machine-detail'),
    # path('data/<str:token>/', views.data_list, name='data-list'),
    # path('data/<int:pk>/<str:token>/', views.data_detail, name='data-detail'),
    path('variabledata/<int:pk>/<str:token>/', views.variable_data_list, name='variabledata-list'),
    # path('variabledata/<int:pk>/', views.variable_data_detail, name='variabledata-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
