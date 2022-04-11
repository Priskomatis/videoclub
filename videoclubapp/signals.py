from telnetlib import theNULL
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

from .models import *

# Without singals, we woudl have to access the admin interface and manually create a profile each time a user was created.
# Sender: A model that notifies the receiver when an event occurs
# Receiver: The receiver is usally a function that works on the data once it is notified of some action that has taken place
# for instance when a user instance is just about to be saved inside the database.
# The connection between the sender and the receivers is done through signal dispatchers
# using signals we can create a profile instance right when a new user instance is created inside the database.
#
#
#

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):    # Create prof is the receiver function which is run every time a user is created.
    if created:                                             # User is the sender which is responsible for making the notification
                                                            #post_save is the signal that is sent at the end of the save method.
        Profile.objects.create(user=instance)
                                                            #After the User model's save method has finished executing, it sends a signa (post_save) to the receiver function (create_profile)
                                                            #then this function will receive the signal to create and save a profile instance for that user.

@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()