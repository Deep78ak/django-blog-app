from django.urls import path

from .views import post_list, post_detail, register_user, login_user, logout_view, like_post, share_post, like_comment

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path("login/", login_user, name="login_user"),
    path("register/", register_user, name="register_user"),
    path('logout/', logout_view, name="logout"),
    path('like/<int:pk>/', like_post, name='like'),
    path('share/<int:pk>/', share_post, name="share"),
    path('comment/like/<int:id>/', like_comment, name="comment_like")
]