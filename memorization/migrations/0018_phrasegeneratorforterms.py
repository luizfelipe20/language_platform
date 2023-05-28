# Generated by Django 4.2.1 on 2023-05-28 21:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0023_terms_gpt_identifier'),
        ('memorization', '0017_importtexts_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhraseGeneratorForTerms',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('terms', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tags', models.ManyToManyField(blank=True, null=True, related_name='phrase_generator_tags', to='word.tags')),
            ],
        ),
    ]