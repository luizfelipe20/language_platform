# Generated by Django 4.2.6 on 2023-11-06 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0015_remove_phrasemaker_translation_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='translationgeneratorforsentence',
            name='sentences',
        ),
        migrations.AddField(
            model_name='translationgeneratorforsentence',
            name='sentences',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='memorization.phrasemaker'),
        ),
    ]
