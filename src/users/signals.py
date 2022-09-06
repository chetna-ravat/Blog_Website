# this is a signal that gets fired after an object is saved
# in our case we want to get a post_save signal when a user is created. thus we need to import User model as well
from django.db.models.signals import post_save

# in this case User would be our sender
from django.contrib.auth.models import User

# A receiver is also going to be a functions that gets this signal and performs the task
from django.dispatch import receiver

# 
from .models import Profile

@receiver(post_save, sender= User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender= User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

    