# Generated by Django 4.2.1 on 2023-09-25 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0002_remove_wordmemorizationrandomtest_lissen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='amount',
        ),
        migrations.AddField(
            model_name='challenge',
            name='correct_percentage_considered',
            field=models.PositiveIntegerField(default=80),
        ),
        migrations.AddField(
            model_name='challenge',
            name='number_of_correct_answers',
            field=models.PositiveIntegerField(default=10),
        ),
    ]
