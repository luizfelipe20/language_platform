import uuid
from django.db import models


class TypePartSpeechChoices(models.TextChoices):
    PORTUGUESE = 'Portuguese'
    ENGLISH = 'English'


class Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    term = models.CharField(max_length=100)
    language = models.CharField(max_length=50, choices=TypePartSpeechChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Translation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    term = models.CharField(max_length=500)
    language = models.CharField(max_length=50, choices=TypePartSpeechChoices.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.term} - {self.id}'


class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    writing = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tags, related_name='word_tags', null=True, blank=True)
    pronunciation = models.FileField(upload_to="./audios", null=True, blank=True)
    translations = models.ManyToManyField(Translation, related_name='word_translations', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
   
class Phrase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    terms = models.TextField()
    pronunciation = models.FileField(upload_to="./audios", null=True, blank=True)
    translation = models.ManyToManyField(Translation, related_name='phrase_translation', null=True, blank=True)
    word = models.ManyToManyField(Word, related_name='phrase_word', blank=True, null=True)
    tags = models.ManyToManyField(Tags, related_name='phrase_tags', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)