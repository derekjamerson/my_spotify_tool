# Generated by Django 4.0.3 on 2022-03-28 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('spotify_id', models.CharField(max_length=22, primary_key=True, serialize=False)),
            ],
        ),
    ]
