# Generated by Django 3.2.8 on 2021-11-03 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0006_auto_20211029_2000'),
        ('accounts', '0006_auto_20211020_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athlete',
            name='workouts_rsvped_for',
            field=models.ManyToManyField(blank=True, null=True, to='workouts.Workout'),
        ),
    ]
