from django.db import models

from accounts.models import User


class Contact(models.Model):
    name = models.CharField(max_length=15)
    email = models.EmailField()
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

    STATES = (
        ('Alabama', 'Alabama'), ('Alaska', 'Alaska'), ('Arizona', 'Arizona'), ('Arkansas', 'Arkansas'),
        ('California', 'California'), ('Colorado', 'Colorado'), ('Connecticut', 'Connecticut'),
        ('Delaware', 'Delaware'), ('Florida', 'Florida'), ('Georgia', 'Georgia'), ('Hawaii', 'Hawaii'),
        ('Idaho', 'Idaho'), ('Illinois', 'Illinois'), ('Indiana', 'Indiana'), ('Iowa', 'Iowa'),
        ('Kansas', 'Kansas'), ('Kentucky', 'Kentucky'), ('Louisiana', 'Louisiana'), ('Maine', 'Maine'),
        ('Maryland', 'Maryland'), ('Massachusetts', 'Massachusetts'), ('Michigan', 'Michigan'),
        ('Minnesota', 'Minnesota'), ('Mississippi', 'Mississippi'), ('Missouri', 'Missouri'),
        ('Montana', 'Montana'), ('Nebraska', 'Nebraska'), ('Nevada', 'Nevada'), ('New Hampshire', 'New Hampshire'),
        ('New Jersey', 'New Jersey'), ('New Mexico', 'New Mexico'), ('New York', 'New York'),
        ('North Carolina', 'North Carolina'), ('North Dakota', 'North Dakota'), ('Ohio', 'Ohio'),
        ('Oklahoma', 'Oklahoma'), ('Oregon', 'Oregon'), ('Pennsylvania', 'Pennsylvania'),
        ('Rhode Island', 'Rhode Island'), ('South Carolina', 'South Carolina'), ('South Dakota', 'South Dakota'),
        ('Tennessee', 'Tennessee'), ('Texas', 'Texas'), ('Utah', 'Utah'), ('Vermont', 'Vermont'),
        ('Virginia', 'Virginia'), ('Washington', 'Washington'), ('West Virginia', 'West Virginia'),
        ('Wisconsin', 'Wisconsin'), ('Wyoming', 'Wyoming')
    )
    state = models.CharField(max_length=14, choices=STATES, default=STATES[0][0])
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    shelter = models.OneToOneField(Shelter, on_delete=models.CASCADE)
