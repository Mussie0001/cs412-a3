# Generated by Django 5.1.3 on 2024-11-10 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('street_number', models.CharField(max_length=10)),
                ('street_name', models.CharField(max_length=100)),
                ('apartment_number', models.CharField(blank=True, max_length=10, null=True)),
                ('zip_code', models.CharField(max_length=10)),
                ('date_of_birth', models.DateField()),
                ('date_of_registration', models.DateField()),
                ('party_affiliation', models.CharField(max_length=2)),
                ('precinct_number', models.CharField(max_length=10)),
                ('v20state', models.BooleanField(default=False)),
                ('v21town', models.BooleanField(default=False)),
                ('v21primary', models.BooleanField(default=False)),
                ('v22general', models.BooleanField(default=False)),
                ('v23town', models.BooleanField(default=False)),
                ('voter_score', models.IntegerField(default=0)),
            ],
        ),
    ]
