# Generated by Django 4.2.6 on 2023-11-25 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0020_multiplechoicememorizationtests_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiplechoicememorizationtestsoptions',
            name='term',
            field=models.TextField(blank=True, null=True),
        ),
    ]
