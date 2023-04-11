# Generated by Django 3.2 on 2023-04-10 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('u', 'user'), ('m', 'moderator'), ('a', 'admin')], default='u', max_length=32),
        ),
    ]
