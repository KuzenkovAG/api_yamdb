from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Title(models.Model):
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

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Review(models.Model):
    '''A model for product reviews'''
    text = models.TextField(
        verbose_name='Tекст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Aвтор'
    )
    score = models.PositiveIntegerField(
        verbose_name='Oценка',
        validators=[
            MinValueValidator(
                1,
                message='Нельзя поставить оценку ниже 1'
            ),
            MaxValueValidator(
                10,
                message='Нельзя поставить оценку выше 10'
            ),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        null=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return self.text
