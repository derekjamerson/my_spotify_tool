# Generated by Django 4.0.4 on 2022-04-15 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='release_date',
            field=models.CharField(default='1111-11-11', max_length=10),
            preserve_default=False,
        ),
    ]