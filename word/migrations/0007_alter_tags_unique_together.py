# Generated by Django 4.2.7 on 2023-12-14 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0006_alter_tags_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tags',
            unique_together={('term',)},
        ),
    ]
