from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings


# Create your views here.

def post_list(request):
    post_list_details = Post.objects.annotate(comment_count=Count('comment'))
    paginator = Paginator(post_list_details, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'post_list.html', {'posts': posts})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)[::-1]
    post.total_comments = len(comments)
    if request.method == 'POST':
        name = request.user.username
        email = request.user.email
        text = request.POST.get('text')

        if name and email and text:
            Comment.objects.create(post=post, name=name, email=email, text=text)
            return redirect('post_detail', pk=pk)

    return render(request, 'post_detail.html', {'post': post, 'comments': comments})


def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.set_password(password1)
                user.save()
                login(request, user)
                return redirect('/')
            if user:
                pass

    return render(request, 'register.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
    return render(request, 'login.html')


@login_required
def like_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        post.likes += 1
        post.save()
        # Redirect to the same post detail page to avoid form resubmission
        return redirect(f'/post/{pk}')


@login_required
def like_comment(request, id):
    print(request.method)
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=id)
        comment.likes += 1
        comment.save()
        print("dfjgbhdflukghdulfgysuil")
        # Redirect to the same post detail page to avoid form resubmission
        # return redirect('post_detail', pk=pk)
        return redirect('post_detail', pk=comment.post.pk)


@login_required
def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def share_post(request, pk):
    try:
        url = request.environ['HTTP_HOST'] + f"/post/{pk}"
        subject = 'Your Link to the Website'
        message = request.POST.get('message')
        message += f'URL: http://{url}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = request.POST.get("recipient").replace(",", "").split(" ")
        send_mail(subject, message, from_email, recipient_list)
        messages.success(request, 'email sent.')
        return redirect('post_detail', pk=pk)
    except:
        messages.error(request, f'Email not sent.')
        return redirect('post_detail', pk=pk)
