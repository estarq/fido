from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=15)
    email = models.EmailField('email')
    message = models.TextField()


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
