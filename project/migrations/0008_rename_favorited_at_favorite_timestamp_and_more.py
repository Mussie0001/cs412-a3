# Generated by Django 5.1.3 on 2024-12-04 18:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_recipe_creator_favorite'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='favorited_at',
            new_name='timestamp',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='creator',
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('user', 'recipe')},
        ),
        migrations.DeleteModel(
            name='MealPlan',
        ),
    ]
