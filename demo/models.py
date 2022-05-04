from django.db import models

# Create your models here.


class ImageHolder(models.Model):
    img = models.ImageField()