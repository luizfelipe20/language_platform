# Generated by Django 4.2.1 on 2023-05-12 01:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('term', models.CharField(max_length=500)),
                ('language', models.CharField(choices=[('Portuguese', 'Portuguese')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('writing', models.CharField(max_length=100)),
                ('classification', models.CharField(choices=[('Verb', 'Verb'), ('Adjective', 'Adjective'), ('Pronoun', 'Pronoun'), ('Adverb', 'Adverb')], max_length=50)),
                ('pronunciation', models.FileField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fk_traslation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='word.translation')),
            ],
        ),
        migrations.CreateModel(
            name='Phrase',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('terms', models.CharField(max_length=500)),
                ('pronunciation', models.FileField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fk_translation', models.ManyToManyField(blank=True, null=True, related_name='phrase_translation', to='word.translation')),
                ('fk_word', models.ManyToManyField(blank=True, null=True, related_name='phrase_word', to='word.word')),
            ],
        ),
    ]
