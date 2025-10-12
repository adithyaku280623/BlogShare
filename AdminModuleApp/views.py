from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from BlogManagingApp.models import Post  # adjust if model is elsewhere

CustomUser = get_user_model()

# ---------------- USER MANAGEMENT ----------------
@staff_member_required
def AdminUserManagement(request):
    users = CustomUser.objects.all()
    return render(request, 'AdminModule/UserManagement.html', {'users': users})

@staff_member_required
def AdminDeleteUser(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.delete()
    messages.success(request, f'User {user.username} deleted successfully.')
    return redirect('AdminUserManagement')

@staff_member_required
def AdminBlockUser(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_active = False
    user.save()
    messages.warning(request, f'User {user.username} has been blocked.')
    return redirect('AdminUserManagement')

# ---------------- POST MANAGEMENT ----------------
@staff_member_required
def AdminPostManagement(request):
    posts = Post.objects.all()
    return render(request, 'AdminModule/PostManagement.html', {'posts': posts})

@staff_member_required
def AdminDeletePost(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    messages.success(request, f'Post "{post.title}" deleted successfully.')
    return redirect('AdminPostManagement')

@staff_member_required
def AdminBlockPost(request, post_id):
    post = Post.objects.get(id=post_id)
    post.is_active = False
    post.save()
    messages.warning(request, f'Post "{post.title}" has been blocked.')
    return redirect('AdminPostManagement')
