import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def paginate_posts(request, posts):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')

    return paginator.get_page(page_number)


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    page_obj = paginate_posts(request, posts)

    return render(request, "network/index.html", {
        "posts": page_obj,
        "feed": True
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, username):
    profiled_user = User.objects.get(username=username)
    posts = Post.objects.filter(creator=profiled_user).order_by("-timestamp")
    page_obj = paginate_posts(request, posts)

    return render(request, "network/profile.html", {
        "profile": User.objects.get(username=username),
        "posts": page_obj,
        "feed": True
    })


@login_required
def following(request):
    posts = Post.objects.filter(creator__in=request.user.following.all()).order_by("-timestamp")
    page_obj = paginate_posts(request, posts)

    return render(request, "network/following.html", {
        "posts": page_obj,
        "feed": True
    })


@login_required
def post(request):
    if request.method == "POST":
        content = request.POST["content"]
        new_post = Post(content=content, creator=request.user)
        new_post.save()
    
    return HttpResponseRedirect(reverse("index"))


@login_required
def toggle_following(request, profile_username):
    profile_user = User.objects.get(username=profile_username)

    # Unfollow if user is following
    if request.user in profile_user.followers.all():
        request.user.following.remove(profile_user)

    # Folllow if user not following
    else:
        request.user.following.add(profile_user)

    return HttpResponseRedirect(reverse("profile", args=(profile_username,)))


@csrf_exempt
@login_required
def toggle_like(request, post_id):
    
    # Toggle liking of post if request is PUT
    if request.method =="PUT":
        
        # Query for requested post
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)

        # Toggle whether post is liked or not
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        post.save()
        return HttpResponse(status=204)

    # Request must be via PUT
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)


@csrf_exempt
@login_required
def edit_post(request, post_id):
    
    # Edit post if request is PUT
    if request.method =="PUT":
        
        # Query for requested post
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)

        # Update post content
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

    # Request must be via PUT
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)



    

