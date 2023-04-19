import csv

from django.core.management.base import BaseCommand

from reviews import models


class Command(BaseCommand):
    help = "Import CSV data."

    def handle(self, *args, **options):
        files = [
            (models.Genre, 'static/data/genre.csv'),
            (models.Categories, 'static/data/category.csv'),
            (models.Title, 'static/data/titles.csv'),
            (models.TitleGenre, 'static/data/genre_title.csv'),
            (models.User, 'static/data/users.csv'),
            (models.Review, 'static/data/review.csv'),
            (models.Comment, 'static/data/comments.csv'),
        ]

        for model, file in files:
            object_model = model.objects.all()
            object_model.delete()
            rows_csv = []
            with open(file, encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    row_csv = model(**row)
                    rows_csv.append(row_csv)

            model.objects.bulk_create(rows_csv)
            print(model.objects.all())
