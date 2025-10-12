from django.urls import path
from . import views

urlpatterns =[
    path('login/',views.LoginUser,name='LoginUser'),
    path('register/',views.RegisterUser,name='RegisterUser'),
    path('logout/',views.LogoutUser,name='LogoutUser'),
    path('updateuser/',views.UpdateUser,name='UpdateUser'),
    path('deleteuser/',views.DeleteUser,name='DeleteUser'),
    path('forgotpassword/', views.ForgotPassword, name='ForgotPassword'),
    path('verify_otp/', views.VerifyOtp, name='VerifyOtp'),
]