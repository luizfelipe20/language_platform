# Generated by Django 4.2.6 on 2023-11-20 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0003_terms_language_alter_terms_text'),
        ('memorization', '0018_phrasemaker_name_phrasemaker_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='translationgeneratorforsentence',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='word.tags'),
        ),
    ]
