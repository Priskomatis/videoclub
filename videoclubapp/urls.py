from django.urls import path
from django.urls import re_path

from .views import *
from . import views



urlpatterns= [
    path("", views.home, name="home"),                                  #If I only type /videoclubapp I will be redirected to the home page.
    #path('login', views.LoginInterfaceView.as_view()),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),   #If I type /videoclubapp/1, I will be redirected to the first movie.
    path('about', views.about, name="about" ),
    path('movielist', views.listOfMovies),
    path('search', views.search, name='search'),
    path('autorized', views.authorized, name='authorized'),             #Only authorized users can enter this admin interface.
    #path('signup', views.SignUpView.as_view(), name='signup'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login', views.LoginInterfaceView.as_view(), name='login'),
    path('logout', views.LogoutInterfaceView.as_view(), name='logout'),
    re_path('profile/', views.profile, name='profile'),
    path('<int:pk>/like', Addlike.as_view(), name='like'),
    path('<int:pk>/dislike', AddDislike.as_view(), name='dislike'),
]