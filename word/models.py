import os
import uuid
from django.db import models
from django.dispatch import receiver
from .utils import generate_audio, generate_translations

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


class GrammaticalClasses(models.Model):
    type = models.CharField(max_length=100)
    language = models.CharField(max_length=50, choices=TypePartSpeechChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    writing = models.CharField(max_length=100)
    classification = models.ManyToManyField(GrammaticalClasses, related_name='word_grammatical_classes', null=True, blank=True)
    tags = models.ManyToManyField(Tags, related_name='word_tags', null=True, blank=True)
    pronunciation = models.FileField(upload_to="./audios", null=True, blank=True)
    translations = models.ManyToManyField(Translation, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

@receiver(models.signals.post_save, sender=Word)
def generate_audio_post_save(sender, instance, **kwargs):
    _object = Word.objects.filter(id=instance.id)
    
    _object.update(pronunciation=generate_audio(instance.writing, instance.id))
    
    translated = generate_translations(instance.writing)
    _object.first().translations.add(Translation.objects.create(**{"term": translated}))


class Phrase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    terms = models.TextField()
    pronunciation = models.FileField(upload_to="./audios", null=True, blank=True)
    fk_translation = models.ManyToManyField(Translation, related_name='phrase_translation', null=True, blank=True)
    fk_word = models.ManyToManyField(Word, related_name='phrase_word', blank=True, null=True)
    tags = models.ManyToManyField(Tags, related_name='phrase_tags', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        language = 'en'
        result = gTTS(text=self.writing, lang=language, slow=False)
        path = result.save(f"./word/audios/{self.created_at}.mp3")
        self.pronunciation = f"./word/audios/{self.created_at}.mp3"
        super(Word, self).save(*args, **kwargs)