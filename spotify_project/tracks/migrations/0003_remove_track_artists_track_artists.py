# Generated by Django 4.0.3 on 2022-03-29 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0001_initial'),
        ('tracks', '0002_track_artists'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='artists',
        ),
        migrations.AddField(
            model_name='track',
            name='artists',
            field=models.ManyToManyField(related_name='tracks', to='artists.artist'),
        ),
    ]