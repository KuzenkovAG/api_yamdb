import csv

from django.core.management.base import BaseCommand, CommandError

from reviews import models


class Command(BaseCommand):
    help = "Import CSV data."

    def handle(self, *args, **options):
        files = [
            (models.Genre, 'genre.csv'),
            (models.Categories, 'category.csv'),
            (models.Title, 'titles.csv'),
            (models.User, 'users.csv'),
            (models.Review, 'review.csv'),
            (models.Comment, 'comments.csv'),
        ]

        for model, file in files:

            with open(file) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        object_model = model.objects.create(**row)
                    except model.DoesNotExist:
                        raise CommandError('Model does not exist.')

                    object_model.opened = False
                    object_model.save()
