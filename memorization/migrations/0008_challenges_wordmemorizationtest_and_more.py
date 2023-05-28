# Generated by Django 4.2.1 on 2023-05-23 01:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0016_alter_word_translations'),
        ('memorization', '0007_alter_gptissues_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenges',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('writing', models.BooleanField(default=False)),
                ('audio', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('amount', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tags', models.ManyToManyField(blank=True, null=True, related_name='challenges_tags', to='word.tags')),
            ],
        ),
        migrations.CreateModel(
            name='WordMemorizationTest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reference', models.CharField(max_length=100)),
                ('term', models.TextField(blank=True, null=True)),
                ('audio', models.FileField(blank=True, null=True, upload_to='')),
                ('answer', models.TextField(blank=True, null=True)),
                ('hit_percentage', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='writingwordmemorizationtest',
            name='word',
        ),
        migrations.DeleteModel(
            name='AudioWordMemorizationTest',
        ),
        migrations.DeleteModel(
            name='WritingWordMemorizationTest',
        ),
    ]