# Generated by Django 4.2.1 on 2023-07-03 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0030_alter_terms_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='terms',
            unique_together={('text',)},
        ),
    ]
