import uuid
from django.db import models
from word.models import Word
"""
fk_phrases
fk_words
fk_translations
written_answer
audio_answer
hit_percentage
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
"""


class WritingWordMemorizationTest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.ForeignKey(Word, related_name='word_memorization_word', on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    hit_percentage = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AudioWordMemorizationTest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.ForeignKey(Word, related_name='audio_memorization_word', on_delete=models.SET_NULL, null=True, blank=True)
    audio = models.FileField(null=True, blank=True)
    answer = models.TextField()
    hit_percentage = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)