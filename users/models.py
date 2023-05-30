from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

# OneToOneField means each argument(user) associated with one thing like Profile
# CASCADE means when we deleted the user the user profile also deleted but when we delete
# Profile the user wont be deleted. and it's one way


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')


# __str__ method help us to print the class with more details. in default it shows class.objects


    def __str__(self):
        return f'{self.user.username} Profile'


# create a save method than resize the large photo than user uploaded befor saving

    def save(self, *args, **kwargs):
        # with super class we can call a parent method like save to overwrite that
        super().save()
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
