from itertools import chain
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Followers, LikePost, Post, Profile


# ---------------- SIGNUP ----------------
def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')

        if User.objects.filter(username=fnm).exists():
            return render(request, 'signup.html', {'invalid': 'User already exists'})

        my_user = User.objects.create_user(username=fnm, email=emailid, password=pwd)
        my_user.save()

        Profile.objects.create(user=my_user, id_user=my_user.id)

        login(request, my_user)
        return redirect('/')

    return render(request, 'signup.html')


# ---------------- LOGIN ----------------
def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')

        userr = authenticate(request, username=fnm, password=pwd)

        if userr is not None:
            login(request, userr)
            return redirect('/')

        return render(request, 'loginn.html', {'invalid': 'Invalid Credentials'})

    return render(request, 'loginn.html')


# ---------------- LOGOUT ----------------
@login_required(login_url='/loginn')
def logoutt(request):
    logout(request)
    return redirect('/loginn')


# ---------------- HOME FEED ----------------
@login_required(login_url='/loginn')
def home(request):
    following_users = Followers.objects.filter(
        follower=request.user.username
    ).values_list('user', flat=True)

    post = Post.objects.filter(
        Q(user=request.user.username) | Q(user__in=following_users)
    ).order_by('-created_at')

    profile = Profile.objects.filter(user=request.user).first()
    
    return render(request, 'main.html', {
        'post': post,
        'profile': profile,
    })


# ---------------- UPLOAD POST ----------------
@login_required(login_url='/loginn')
def upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')

        Post.objects.create(
            user=request.user,   # ✅ correct (ForeignKey)
            image=image,
            caption=caption
        )

        return redirect('/')   # redirect after upload

    return redirect('/')

# ---------------- LIKE / UNLIKE ----------------
@login_required(login_url='/loginn')
def likes(request, id):
    username = request.user.username
    post = get_object_or_404(Post, id=id)

    like_filter = LikePost.objects.filter(post_id=id, username=username).first()

    if like_filter is None:
        LikePost.objects.create(post_id=id, username=username)
        post.no_of_likes += 1
    else:
        like_filter.delete()
        post.no_of_likes -= 1

    post.save()

    return redirect('/')


# ---------------- EXPLORE ----------------
@login_required(login_url='/loginn')
def explore(request):
    post = Post.objects.all().order_by('-created_at')
    profile = get_object_or_404(Profile, user=request.user)

    return render(request, 'explore.html', {
        'post': post,
        'profile': profile
    })


# ---------------- PROFILE PAGE ----------------
@login_required(login_url='/loginn')
def profile(request, id_user):

    # 🔹 profile owner (viewed user)
    user_object = get_object_or_404(User, username=id_user)
    user_profile, created = Profile.objects.get_or_create(user=user_object)

    # 🔹 logged-in user profile
    my_profile = get_object_or_404(Profile, user=request.user)

    # 🔹 FIX: use User object, not username string
    user_posts = Post.objects.filter(user=user_object).order_by('-created_at')

    # 🔹 follower system (use User objects, NOT strings)
    follow_unfollow = 'Unfollow' if Followers.objects.filter(
        follower=request.user,
        user=user_object
    ).exists() else 'Follow'

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_posts.count(),
        'profile': my_profile,

        'follow_unfollow': follow_unfollow,

        # 🔹 FIXED follower counts
        'user_followers': Followers.objects.filter(user=user_object).count(),
        'user_following': Followers.objects.filter(follower=user_object).count(),
    }

    return render(request, 'profile.html', context)

    # UPDATE PROFILE
    if request.user.username == id_user:
        if request.method == 'POST':
            image = request.FILES.get('image', user_profile.profileimg)
            bio = request.POST.get('bio')
            location = request.POST.get('location')

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

            return redirect('/profile/' + id_user)

    return render(request, 'profile.html', context)


# ---------------- DELETE POST ----------------
@login_required(login_url='/loginn')
def delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('/profile/' + request.user.username)


# ---------------- SEARCH ----------------
@login_required(login_url='/loginn')
def search_results(request):
    query = request.GET.get('q', '')

    users = Profile.objects.filter(user__username__icontains=query)
    posts = Post.objects.filter(caption__icontains=query)

    return render(request, 'search_user.html', {
        'query': query,
        'users': users,
        'posts': posts,
    })


# ---------------- SINGLE POST VIEW ----------------
@login_required(login_url='/loginn')
def home_post(request, id):
    post = get_object_or_404(Post, id=id)
    profile = get_object_or_404(Profile, user=request.user)

    return render(request, 'main.html', {
        'post': post,
        'profile': profile
    })


# ---------------- FOLLOW / UNFOLLOW ----------------
@login_required(login_url='/loginn')
def follow(request):
    if request.method == 'POST':
        follower = request.POST.get('follower')
        user = request.POST.get('user')

        if Followers.objects.filter(follower=follower, user=user).exists():
            Followers.objects.filter(follower=follower, user=user).delete()
        else:
            Followers.objects.create(follower=follower, user=user)

        return redirect('/profile/' + user)

    return redirect('/')