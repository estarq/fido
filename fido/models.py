from django.db import models

from accounts.models import User
from common.constants import CAT_AGE_RANGES, CAT_BREEDS, DOG_AGE_RANGES, DOG_BREEDS, SEXES, US_STATES


class Message(models.Model):
    name = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()


class Shelter(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField()
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    website = models.URLField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ShelterAddress(models.Model):
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=14, choices=US_STATES, default=US_STATES[0][0])
    zip_code = models.CharField(max_length=10)
    shelter = models.OneToOneField(Shelter, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Shelter addresses'

    def __str__(self):
        return f'{self.street}, {self.city}, {self.state} {self.zip_code}'


class Pet(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField()
    photo = models.ImageField()
    sex = models.CharField(max_length=6, choices=SEXES, default=SEXES[0][0])
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Cat(Pet):
    age = models.CharField(max_length=6, choices=CAT_AGE_RANGES, default=CAT_AGE_RANGES[0][0])
    breed = models.CharField(max_length=13, choices=CAT_BREEDS, default=CAT_BREEDS[0][0])


class Dog(Pet):
    age = models.CharField(max_length=6, choices=DOG_AGE_RANGES, default=DOG_AGE_RANGES[0][0])
    breed = models.CharField(max_length=18, choices=DOG_BREEDS, default=DOG_BREEDS[0][0])
