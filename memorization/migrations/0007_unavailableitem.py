# Generated by Django 4.2.7 on 2024-08-13 01:38

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('memorization', '0006_alter_options_option'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnavailableItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('word_memorization_random_test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='memorization.wordmemorizationrandomtest')),
            ],
        ),
    ]