from distutils.command.upload import upload
from email.policy import default
from random import choices
from statistics import mode
from django.contrib.auth.models import User

from tkinter import CASCADE
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator #To set a minimum and a maximum number a rating of a movie can have.
from PIL import Image

# Create your models here.


class Movie(models.Model):
    GENRE_CHOICES = [('ACTION', 'ACTION'), ('DRAMA', 'DRAMA'),('MYSTERY', 'MYSTERY')]

    title = models.CharField(max_length=50, default="")
    director = models.CharField(max_length=50, blank=True, default="")
    price = models.DecimalField(max_digits=3, decimal_places=2, blank=True, default=1)
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)])
    description = models.TextField(max_length=500, blank=True, default="")

    genre = models.CharField(max_length=7, choices=GENRE_CHOICES, default="")

    image = models.ImageField(upload_to='img', default="" )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default="avatar.jpg", upload_to='profile_images')        #upload_to is our Media folder/profile_images that saves all the avatar images.
                                                                                    #When the user updates their profile image, the image they uploaded will be stored in this folder.
    bio = models.TextField()

    def __str__(self):
        return self.user.username       #We display the user's username in the admin interface

    #RESIZE IMAGE
    def save(self, *args, **kwargs):
        super().save()

        #The following commands are to convert the image to a jpg so it can be saved with no problems.
        img = Image.open(self.avatar.path)
        img = img.convert('RGB')            #Image.convert is from the PIL library which returns a copy of the image after the conversion
        img.save('audacious.jpg')