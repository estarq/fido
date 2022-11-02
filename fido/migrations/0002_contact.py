# Generated by Django 4.1 on 2022-11-01 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fido', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('message', models.TextField()),
            ],
        ),
    ]
