from django.db import models

# Create your models here.

class Hash(models.Model):
    text = models.TextField()
    hash = models.CharField(max_length=64) # limit only for sha256 so far
    algo = models.CharField(max_length=32, default='sha256') # hash method from pulldown

