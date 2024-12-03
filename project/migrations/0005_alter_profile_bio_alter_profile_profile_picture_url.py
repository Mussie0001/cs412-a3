# Generated by Django 5.1.3 on 2024-12-03 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_remove_profile_city_remove_profile_profile_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]