# Generated by Django 5.1.3 on 2024-12-04 18:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_recipes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorited_at', models.DateTimeField(auto_now_add=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to='project.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]