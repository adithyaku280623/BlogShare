from django.urls import path
from . import views

urlpatterns = [
    path('admin/users/', views.AdminUserManagement, name='AdminUserManagement'),
    path('admin/posts/', views.AdminPostManagement, name='AdminPostManagement'),
    path('admin/delete-user/<int:user_id>/', views.AdminDeleteUser, name='AdminDeleteUser'),
    path('admin/delete-post/<int:post_id>/', views.AdminDeletePost, name='AdminDeletePost'),
    path('admin/block-user/<int:user_id>/', views.AdminBlockUser, name='AdminBlockUser'),
    path('admin/block-post/<int:post_id>/', views.AdminBlockPost, name='AdminBlockPost'),
]
