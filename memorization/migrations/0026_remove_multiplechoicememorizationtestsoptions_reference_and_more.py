# Generated by Django 4.2.6 on 2023-11-26 02:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0025_wordmemorizationrandomtest_sentences_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multiplechoicememorizationtestsoptions',
            name='reference',
        ),
        migrations.DeleteModel(
            name='MultipleChoiceMemorizationTests',
        ),
        migrations.DeleteModel(
            name='MultipleChoiceMemorizationTestsOptions',
        ),
    ]
