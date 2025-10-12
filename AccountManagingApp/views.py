from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
import random


from django.contrib.auth import get_user_model
User = get_user_model()


def RegisterUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        profile_picture = request.FILES.get('profile_picture')


        if password != cpassword:
            messages.error(request, 'Passwords do not match')
            return redirect('RegisterUser')


        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('RegisterUser')


        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            profile_picture=profile_picture
        )
        user.save()
        messages.success(request, 'Account created successfully')
        return redirect('LoginUser')

    return render(request, 'AccountManagingApp/RegisterUser.html')

def LoginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username = username,password=password)

        if user is not None:
            login(request,user)
            return redirect('HomePage')
        else:
            return redirect('LoginUser')
    return render(request,'AccountManagingApp/LoginUser.html')

def LogoutUser(request):
    logout(request)
    return redirect('LoginUser')


def UpdateUser(request):
    if not request.user.is_authenticated:
        return redirect('LoginUser')

    user = request.user

    if request.method == "POST":
        new_username = request.POST.get('username')
        if new_username and new_username != user.username:
            if CustomUser.objects.filter(username=new_username).exists():
                messages.error(request, 'Username already taken.')
                return redirect('UpdateUser')
            user.username = new_username


        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)

        password = request.POST.get('password')
        newpass = request.POST.get('newpass')
        newpassconfirm = request.POST.get('newpassconfirm')

        if password and newpass and newpassconfirm:
            if not user.check_password(password):
                messages.error(request, 'Current password is incorrect.')
                return redirect('UpdateUser')

            if newpass != newpassconfirm:
                messages.error(request, 'New passwords do not match.')
                return redirect('UpdateUser')

            user.set_password(newpass)
            update_session_auth_hash(request, user)

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('MyAccount')
    return render(request, 'AccountManagingApp/UpdateUser.html', {"user": user})

def DeleteUser(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('LoginUser')
    return render(request, 'AccountManagingApp/DeleteUser.html')


def ForgotPassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "No user found with that username.")

        otp = random.randint(1000, 9999)

        request.session['reset_username'] = username
        request.session['reset_otp'] = str(otp)

        messages.info(request, f"Your OTP is: {otp}")
        return redirect('VerifyOtp')
    return render(request, 'AccountManagingApp/ForgotPassword.html')


def VerifyOtp(request):

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        session_otp = request.session.get('reset_otp')
        username = request.session.get('reset_username')


        if not session_otp or not username:
            messages.error(request, "Session expired. Try again.")
            return redirect('ForgotPassword')

        if entered_otp != session_otp:
            messages.error(request, "Invalid OTP.")
            return redirect('VerifyOtp')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('VerifyOtp')

        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()

        request.session.flush()
        messages.success(request, "Password reset successful! You can log in now.")
        return redirect('LoginUser')
    return render(request, 'AccountManagingApp/VerifyOtp.html')