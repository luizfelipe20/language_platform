# Generated by Django 4.2.1 on 2023-05-23 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0008_challenges_wordmemorizationtest_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordmemorizationtest',
            name='counter',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
