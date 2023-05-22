# Generated by Django 4.2.1 on 2023-05-21 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0014_remove_word_translation_word_translations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='phrase',
            old_name='fk_translation',
            new_name='translation',
        ),
        migrations.RenameField(
            model_name='phrase',
            old_name='fk_word',
            new_name='word',
        ),
        migrations.RemoveField(
            model_name='word',
            name='classification',
        ),
        migrations.DeleteModel(
            name='GrammaticalClasses',
        ),
    ]
