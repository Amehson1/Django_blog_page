from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.







class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields specific to the author


class Category(models.Model):
    name = models.CharField(max_length=100)


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag')


class Tag(models.Model):
    name = models.CharField(max_length=100)


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)