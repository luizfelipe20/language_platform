# Generated by Django 4.2.5 on 2023-09-29 18:46

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0002_remove_terms_gpt_identifier_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='terms',
            name='language',
            field=models.CharField(choices=[('Portuguese', 'Portuguese'), ('English', 'English')], default='English', max_length=50),
        ),
        migrations.AlterField(
            model_name='terms',
            name='text',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
