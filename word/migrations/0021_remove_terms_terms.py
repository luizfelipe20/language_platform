# Generated by Django 4.2.1 on 2023-05-23 02:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0020_alter_tags_term'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='terms',
            name='terms',
        ),
    ]