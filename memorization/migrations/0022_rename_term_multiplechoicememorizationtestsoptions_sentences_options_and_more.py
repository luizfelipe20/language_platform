# Generated by Django 4.2.6 on 2023-11-25 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0003_terms_language_alter_terms_text'),
        ('memorization', '0021_multiplechoicememorizationtestsoptions_term'),
    ]

    operations = [
        migrations.RenameField(
            model_name='multiplechoicememorizationtestsoptions',
            old_name='term',
            new_name='sentences_options',
        ),
        migrations.AddField(
            model_name='multiplechoicememorizationtests',
            name='answer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='multiplechoicememorizationtests',
            name='sentences_options',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='multiplechoicememorizationtestsoptions',
            name='reference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='word.terms'),
        ),
    ]