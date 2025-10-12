from django.urls import path
from . import views

urlpatterns =[
    path('homepage/',views.HomePage,name="HomePage"),
    path('myaccount/',views.MyAccount,name='MyAccount'),
    path('createpost/',views.CreatePost,name='CreatePost'),
    path('post/delete/<int:post_id>/',views.DeletePost,name='DeletePost'),
    path('post/edit/<int:post_id>/',views.EditPost,name='EditPost'),
    path('post/<int:post_id>/', views.PostDetail, name='PostDetail'),
    path("add-comment/<int:post_id>/", views.AddComment, name="AddComment"),

]