import os
import uuid
from django.db import models
from gtts import gTTS

class Translation(models.Model):
    class TypePartSpeechChoices(models.TextChoices):
        PORTUGUESE = 'Portuguese'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    term = models.CharField(max_length=500)
    language = models.CharField(max_length=50, choices=TypePartSpeechChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Word(models.Model):
    class TypePartSpeechChoices(models.TextChoices):
        VERB = 'Verb'
        ADJECTIVE = 'Adjective'
        PRONOUN = 'Pronoun'
        ADVERB = 'Adverb'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    writing = models.CharField(max_length=100)
    classification = models.CharField(max_length=50, choices=TypePartSpeechChoices.choices)
    pronunciation = models.FileField(upload_to="./audios", null=True, blank=True)
    fk_traslation = models.ForeignKey(Translation, related_name='translation', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        language = 'en'
        result = gTTS(text=self.writing, lang=language, slow=False)
        path = result.save(f"./word/audios/{self.writing}.mp3")
        self.pronunciation = f"./word/audios/{self.writing}.mp3"
        super(Word, self).save(*args, **kwargs)


class Phrase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    terms = models.CharField(max_length=500)
    pronunciation = models.FileField()
    fk_translation = models.ManyToManyField(Translation, related_name='phrase_translation', null=True, blank=True)
    fk_word = models.ManyToManyField(Word, related_name='phrase_word', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)