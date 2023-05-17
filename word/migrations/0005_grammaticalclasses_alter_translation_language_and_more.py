# Generated by Django 4.2.1 on 2023-05-16 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0004_alter_word_pronunciation'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrammaticalClasses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('language', models.CharField(choices=[('Portuguese', 'Portuguese'), ('English', 'English')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='translation',
            name='language',
            field=models.CharField(choices=[('Portuguese', 'Portuguese'), ('English', 'English')], max_length=50),
        ),
        migrations.RemoveField(
            model_name='word',
            name='classification',
        ),
        migrations.AddField(
            model_name='word',
            name='classification',
            field=models.ManyToManyField(blank=True, null=True, related_name='word_grammatical_classes', to='word.grammaticalclasses'),
        ),
    ]
