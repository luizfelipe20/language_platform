# Generated by Django 4.2.6 on 2023-11-01 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0009_historicchallenge_challenge'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicchallenge',
            name='language',
            field=models.CharField(choices=[('Portuguese', 'Portuguese'), ('English', 'English')], default='English', max_length=50),
        ),
    ]
