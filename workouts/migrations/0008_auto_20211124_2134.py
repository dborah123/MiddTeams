# Generated by Django 3.2.8 on 2021-11-25 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_athlete_workouts_rsvped_for'),
        ('workouts', '0007_excuserequest_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excuserequest',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.athlete'),
        ),
        migrations.AlterField(
            model_name='excuserequest',
            name='reason',
            field=models.CharField(choices=[('#1', 'Sick'), ('#2', 'Injured'), ('#4', 'Other')], max_length=200),
        ),
        migrations.AlterField(
            model_name='excuserequest',
            name='workout',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workouts.workout'),
        ),
    ]
