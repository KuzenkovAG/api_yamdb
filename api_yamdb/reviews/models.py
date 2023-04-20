from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()


class SlugGenreCategory(models.Model):
    """General Model for Genre and Categories."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Genre(SlugGenreCategory):
    """Model for genre of title."""


class Categories(SlugGenreCategory):
    """Model for category of title."""


class Title(models.Model):
    """Model Title, with indicating genre and category."""
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre, related_name='titles', through="TitleGenre"
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Model for relationship ManyToMany between Title and Genre."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    """A model for product reviews."""
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


class Comment(models.Model):
    """Model for comments to reviews."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.CharField(
        'Текст',
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
