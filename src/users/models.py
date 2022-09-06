from django.db import models
from django.contrib.auth.models import User

# we are image funstion from pillow library because we want to resize our image file
from PIL import Image 


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to='profile_pics')
    
    # dunder str method is use to print the object value and not the reference
    def __str__(self):
        return f'{self.user.username} Profile'

# we want to override the save method which django provides by default and define our own save method
# the super method would run the save function of our parent class
    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

