from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post,Comment


def CreatePost(request):

    if not request.user.is_authenticated:
        return redirect('LoginUser')

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")
        subject = request.POST.get("subject")

        Post.objects.create(
            user = request.user,
            title = title,
            content = content,
            image = image,
            subject = subject
        )
        return redirect('MyAccount')
    return render(request,'BlogManagingApp/CreatePost.html')


def HomePage(request):
    """
    Display posts and handle all comment actions: add, edit, delete
    """
    query = request.GET.get('q', '')
    posts = Post.objects.all().order_by('-created_at')
    if query:
        posts = posts.filter(title__icontains=query)

    # Handle comment actions
    if request.method == "POST":
        action = request.POST.get("action")
        comment_id = request.POST.get("comment_id")
        post_id = request.POST.get("post_id")
        text = request.POST.get("text", "").strip()

        # Add comment
        if action == "comment" and post_id and text:
            post = get_object_or_404(Post, id=post_id)
            Comment.objects.create(post=post, user=request.user, text=text)

        # Edit comment
        elif action == "edit_comment" and comment_id and text:
            comment = get_object_or_404(Comment, id=comment_id)
            if comment.user == request.user:
                comment.text = text
                comment.save()

        # Delete comment
        elif action == "delete_comment" and comment_id:
            comment = get_object_or_404(Comment, id=comment_id)
            if comment.user == request.user:
                comment.delete()

        return redirect(request.META.get('HTTP_REFERER', '/'))

    # Pagination: 1 post per page
    paginator = Paginator(posts, 1)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, "BlogManagingApp/HomePage.html", {
        "posts": posts,
        "query": query
    })

def MyAccount(request):

    if not request.user.is_authenticated:
        return redirect('LoginUser')

    posts = Post.objects.filter(user=request.user).order_by("-created_at")
    return render(request,'BlogManagingApp/MyAccount.html',{"posts":posts})


def PostDetail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "BlogManagingApp/PostDetail.html", {"post": post})



def DeletePost(request, post_id):
    if not request.user.is_authenticated:
        return redirect('LoginUser')

    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        return redirect('MyAccount')

    if request.method == "POST":
        post.delete()
        return redirect('MyAccount')

    return render(request, 'BlogManagingApp/DeletePost.html', {'post': post})

def EditPost(request,post_id):
    if not request.user.is_authenticated:
        return redirect("LoginUser")

    post = get_object_or_404(Post,id=post_id)
    if post.user != request.user:
        return redirect('MyAccount')
    if request.method == 'POST':
        title = request.POST.get('title')
        subject =request.POST.get('subject')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        post.title = title
        post.content = content
        post.subject = subject
        if image:
            post.image = image
        post.save()
        return redirect('PostDetail',post_id=post.id)
    return render(request,'BlogManagingApp/EditPost.html',{"post":post})

def AddComment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get("comment")
        if text:
            Comment.objects.create(post=post, user=request.user, text=text)
    return redirect("HomePage")

