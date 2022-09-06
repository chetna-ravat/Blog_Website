from django.contrib import admin
from.models import Profile


# Register your models here.

# TODO why are we setting up profile via an admin route

admin.site.register(Profile)

