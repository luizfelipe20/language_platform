# Generated by Django 4.2.1 on 2023-05-28 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0018_phrasegeneratorforterms'),
    ]

    operations = [
        migrations.AddField(
            model_name='phrasegeneratorforterms',
            name='amount',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]