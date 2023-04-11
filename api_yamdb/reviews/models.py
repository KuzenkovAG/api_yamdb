from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.text


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=256)
    year = models.DateTimeField('Год выпуска', auto_now_add=True)
    description = models.TextField()
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        related_name='genre', blank=True, null=True
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='category', blank=True, null=True
    )

    def __str__(self):
        return self.name
