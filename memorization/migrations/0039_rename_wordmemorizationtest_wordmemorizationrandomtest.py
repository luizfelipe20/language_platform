# Generated by Django 4.2.1 on 2023-07-18 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0038_remove_challenge_terms_challengeterm'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WordMemorizationTest',
            new_name='WordMemorizationRandomTest',
        ),
    ]
