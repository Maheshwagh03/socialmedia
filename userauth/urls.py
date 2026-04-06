from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from userauth import views



urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('loginn/', views.loginn, name='loginn'),
    path('logoutt/', views.logoutt, name='logoutt'),
    path('upload/', views.upload, name='upload'),
    path('search/', views.search_results, name='search_results'),
    path('like-post/<str:id>', views.likes, name='like-post'),
    # FIX: Changed from '#<str:id>' to 'post/<str:id>'
    path('post/<str:id>', views.home_post, name='home_post'), 
    path('explore', views.explore, name='explore'),
    path('profile/<str:id_user>', views.profile, name='profile'),
    path('delete/<str:id>', views.delete, name='delete'),
    path('follow', views.follow, name='follow'),
]