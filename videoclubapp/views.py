from email import message
from msilib.schema import ListView
from multiprocessing import context
from re import L, template
import re
from turtle import title
from typing import List
from xmlrpc.client import FastParser
from django import http
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseRedirect, Http404

import videoclubapp
from .models import User, Movie
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from .forms import RegisterForm, UpdateProfileForm, UpdateUserForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


# Create your views here.

#Login
#class LoginInterfaceView(LoginView):
#    template_name = 'login.html'




#Register

#class SignUpView(CreateView):
#    form_class = UserCreationForm
#    template_name = 'register.html'
#    success_url = 'about'

#    def get(self, request, *args, **kwargs):
#        if self.request.user.is_authenticated:
#            return redirect('videoclubapp/')
#        return super().get(request, *args, **kwargs)


#@login_required
#def profile(request):
#    return render(request, 'profile.html')




#LIKE/DISLIKE

class Addlike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):

        post = Movie.objects.get(pk=pk) #We grab the movie we want to see the likes/dislikes

        is_dislike = False                      #We will check if the user has ALREADY disliked the movie before moving forward.
                                                #If they have, then when they user will like the movie, we will remove them from the dislike list.
                                                #We basically check for both cases at

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False                         #Since the user hasn't like the post already.

        for like in post.likes.all():           #First we loop through the likes to see if the user has already liked the post, if they haven't then we add them
            if like == request.user:
                is_like = True
                break

        if not is_like:                         #we add the user to the list.
            post.likes.add(request.user)

        if is_like:                             #If the user double likes the post, that undos the like, so we remove the user from the list of users that has liked this post.
            post.likes.remove(request.user)     #request.user to check who the user is.

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Movie.objects.get(pk=pk)

        is_like = False                         #We will check if the user has ALREADY liked the movie.

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False                      #Same as with the AddLike class.

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:                      #We add or remove the user from/in the list based on if they have disliked the movie.
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)





#PASSWORD CHANGE

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Your password was changed successfully"
    success_url = reverse_lazy('home')


#Profile View

@login_required
def profile(request):
    if request.method == 'POST':                    #We import the required forms and create instances of those forms depending on wether the request is get or post
        user_form = UpdateUserForm(request.POST, instance=request.user)                                 
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
                                                    #If the form is submited (request is post) we pass in the post data to the forms, for the profile there is also a file.image data
                                                    #coming in the request, which is placed in the request.FILE so we need to pass that to.
                                                    #The form fields get populated with the current information of the logged in user.

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated!')
            return redirect('home')
    else:
        user_form = UpdateUserForm(instance=request.user)           
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})

#Login
class LoginInterfaceView(LoginView):
    template_name = 'login.html'

#Logout
class LogoutInterfaceView(LogoutView):
   template_name = 'logout.html'

#Register
class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):                        #Creates a new instance of an empty form
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):                       #Creates a new instance of the form with the post data and checks if its valid (form.is_valid), then process
                                                                    # the cleaned form data and save the user to our database with their info.
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')                    #Just a message to let the user know that their account was successfully generated.
            messages.success(request, f'Account created for {username}')

            return redirect('login')                                         #Directs the user to the home page of our website after their signed in.
        return render(request, self.template_name, {'form': form})



@login_required(login_url='/admin') #We will be redirected here if we try to enter a forbidden page without authentication.
def authorized(request):
    return render(request, 'authorized.html',{})



def home(request):      #We want the home view to display a list of all the movies
    movies = Movie.objects.all()
    return render(request, "home.html", {
        'movies' : movies,
    })

def movie_detail(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        raise Http404('Movie not found')
    return render(request, 'movie_detail.html', {
        'movie': movie,
    })

def about(request):
    return render(request, 'about.html')

def listOfMovies(request):
    all_Movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': all_Movies})


def search(request):
    if request.method=="POST":                  #Its a post method since the user sends data.
        query = request.POST.get('name', None)
        if query:
            results = Movie.objects.filter(title__contains=query) or Movie.objects.filter(genre__contains=query)    #The user can search a movie by name or by its genre.
            return render(request, 'search_movies.html', {"results":results})

    return render(request, 'search_movies.html')



#Search
