# Generated by Django 4.2.6 on 2023-11-06 18:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0003_terms_language_alter_terms_text'),
        ('memorization', '0014_phrasemaker_translation_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phrasemaker',
            name='translation_options',
        ),
        migrations.CreateModel(
            name='TranslationGeneratorForSentence',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('request', models.TextField(blank=True, null=True)),
                ('answer', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sentences', models.ManyToManyField(blank=True, null=True, related_name='sentences_translation_generator', to='word.terms')),
            ],
        ),
    ]
