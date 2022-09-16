from django.db import models


# Create your models here.
class Dog(models.Model):
    SEX = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(max_length=15)
    sex = models.CharField(max_length=1, choices=SEX)
    short_desc = models.CharField(max_length=100)
    desc = models.TextField()
    img = models.ImageField()
