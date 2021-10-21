# Generated by Django 3.2.8 on 2021-10-21 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_scheduleitem_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduleitem',
            name='day',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='scheduleitem',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='scheduleitem',
            name='time_end',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='scheduleitem',
            name='time_start',
            field=models.TimeField(blank=True),
        ),
    ]
