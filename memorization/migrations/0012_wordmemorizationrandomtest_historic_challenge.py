# Generated by Django 4.2.6 on 2023-11-03 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0011_remove_challenge_correct_percentage_considered_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordmemorizationrandomtest',
            name='historic_challenge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='memorization.historicchallenge'),
        ),
    ]
