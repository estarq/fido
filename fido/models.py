from django.db import models

from accounts.models import User
from common.constants import US_STATES


class Contact(models.Model):
    name = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()


class Shelter(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=15)
    description = models.TextField()
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    website = models.URLField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE)


class ShelterAddress(models.Model):
    class Meta:
        verbose_name_plural = 'Shelter addresses'

    def __str__(self):
        return f'{self.street}, {self.city}, {self.state} {self.zip_code}'

    state = models.CharField(max_length=14, choices=US_STATES, default=US_STATES[0][0])
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    shelter = models.OneToOneField(Shelter, on_delete=models.CASCADE)


class Pet(models.Model):
    SEXES = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    name = models.CharField(max_length=15)
    sex = models.CharField(max_length=6, choices=SEXES, default=SEXES[0][0])
    description = models.TextField()
    photo = models.ImageField()
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        ordering = ['-pk']

    def __str__(self):
        return self.name


class Cat(Pet):
    AGE_RANGES = (
        ('Kitten', 'Kitten'),
        ('Young', 'Young'),
        ('Adult', 'Adult'),
        ('Senior', 'Senior')
    )
    BREEDS = (
        ('Abyssinian', 'Abyssinian'),
        ('Bengal', 'Bengal'),
        ('Birman', 'Birman'),
        ('Devon Rex', 'Devon Rex'),
        ('Egyptian Mau', 'Egyptian Mau'),
        ('Foldex', 'Foldex'),
        ('Himalayan', 'Himalayan'),
        ('Maine Coon', 'Maine Coon'),
        ('Persian', 'Persian'),
        ('Ragdoll', 'Ragdoll'),
        ('Scottish Fold', 'Scottish Fold'),
        ('Siamese', 'Siamese'),
        ('Sphynx', 'Sphynx'),
    )

    age = models.CharField(max_length=6, choices=AGE_RANGES, default=AGE_RANGES[0][0])
    breed = models.CharField(max_length=13, choices=BREEDS, default=BREEDS[0][0])


class Dog(Pet):
    AGE_RANGES = (
        ('Puppy', 'Puppy'),
        ('Young', 'Young'),
        ('Adult', 'Adult'),
        ('Senior', 'Senior')
    )
    BREEDS = (
        ('Basset Hound', 'Basset Hound'),
        ('Beagle', 'Beagle'),
        ('Border Collie', 'Border Collie'),
        ('Boston Terrier', 'Boston Terrier'),
        ('Boxer', 'Boxer'),
        ('Cockapoo', 'Cockapoo'),
        ('Cocker Spaniel', 'Cocker Spaniel'),
        ('French Bulldog', 'French Bulldog'),
        ('Golden Retriever', 'Golden Retriever'),
        ('Greyhound', 'Greyhound'),
        ('Irish Setter', 'Irish Setter'),
        ('Labrador Retriever', 'Labrador Retriever'),
        ('Poodle', 'Poodle'),
    )

    age = models.CharField(max_length=6, choices=AGE_RANGES, default=AGE_RANGES[0][0])
    breed = models.CharField(max_length=18, choices=BREEDS, default=BREEDS[0][0])
