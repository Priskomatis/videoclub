from atexit import register
from django.contrib import admin
from .models import Profile, User, Movie

# Register your models here.

#@admin.register(User)
#class UserAdmin(admin.ModelAdmin):
#    list_display = ["first_name", "last_name", "email",]

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "director", "price", "rating"]

admin.site.register(Profile)