
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("post", views.post, name="post"),
    path("toggle_following/<str:profile_username>", views.toggle_following, name="toggle_following"),

    # API Routes
    path("toggle_like/<int:post_id>", views.toggle_like, name="toggle_like"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post")
]
