# Generated by Django 4.0.3 on 2022-04-06 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0007_rename_duration_ms_track__duration_ms'),
    ]

    operations = [
        migrations.RenameField(
            model_name='track',
            old_name='_duration_ms',
            new_name='duration_ms',
        ),
    ]
