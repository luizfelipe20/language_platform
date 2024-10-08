# Generated by Django 4.2.7 on 2024-08-10 20:27

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('term', models.TextField()),
                ('language', models.CharField(choices=[('Portuguese', 'Portuguese'), ('English', 'English')], default='English', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tags', models.ManyToManyField(blank=True, null=True, to='word.tags')),
            ],
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', ckeditor.fields.RichTextField()),
                ('obs', models.TextField(blank=True, null=True)),
                ('language', models.CharField(choices=[('Portuguese', 'Portuguese'), ('English', 'English')], default='English', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tags', models.ManyToManyField(blank=True, null=True, related_name='word_tags', to='word.tags')),
            ],
            options={
                'unique_together': {('text',)},
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('definition', models.TextField(blank=True, null=True)),
                ('part_of_speech', models.CharField(blank=True, max_length=100, null=True)),
                ('language', models.CharField(choices=[('Portuguese', 'Portuguese'), ('English', 'English')], default='English', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WordTerm',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('term', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='word.terms')),
                ('word', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='word.word')),
            ],
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('term', models.TextField()),
                ('language', models.CharField(blank=True, choices=[('Portuguese', 'Portuguese'), ('English', 'English')], max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='word.terms')),
            ],
            options={
                'unique_together': {('term', 'reference', 'language')},
            },
        ),
    ]
