import os
import re
import json
import uuid
from datetime import timedelta
from django.contrib.auth.models import User
from openai import OpenAI
from django.db import models
from ckeditor.fields import RichTextField
from django.core.files.base import ContentFile

from memorization.gpt_api import sentence_generator


def format_names_for_tags(title):
    title = title.lower()
    title = re.sub(r"\s+", "_", title)
    return title

class TypePartSpeechChoices(models.TextChoices):
    PORTUGUESE = 'Portuguese'
    ENGLISH = 'English'


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    term = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=50, choices=TypePartSpeechChoices.choices, default=TypePartSpeechChoices.ENGLISH)
    tags = models.ManyToManyField('self', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     unique_together = [('term',)]

    def __str__(self):
        return f'{self.term}'


class ShortText(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=True, blank=True)
    text = RichTextField()
    translation = RichTextField(null=True, blank=True)
    phonetic_transcription_portuguese = RichTextField(null=True, blank=True)
    instruction_ia = RichTextField(null=True, blank=True)
    audio = models.FileField(upload_to='audios/', null=True, blank=True) 
    tags = models.ManyToManyField(Tag, related_name='short_texts_word_tags', null=True, blank=True)
    language = models.CharField(max_length=50, choices=TypePartSpeechChoices.choices, default=TypePartSpeechChoices.ENGLISH)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'
    
    def audio_generator(self):
        client = OpenAI(api_key=os.environ.get("GPT_API_KEY"))
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            response_format="mp3",
            input=self.text
        )        
        file_name = f"audio_{self.pk or 'temp'}.mp3"
        audio_data = ContentFile(response.content, name=file_name)
        self.audio.save(file_name, audio_data, save=True)
        
    def translator(self):
        _request_gpt = f"""
        Translate the following text into Brazilian Portuguese:{self.text}.
        Be concise and only provide the information requested.
        """
        self.translation = sentence_generator(_request_gpt)
    
    def tag_creation(self):
        Tag.objects.get_or_create(term=format_names_for_tags(self.title))
                
    def save(self, *args, **kwargs):        
        if not self.audio:
            self.audio_generator()
        if not self.translation:
            self.translator()
        if not len(self.tags.all()):
            self.tag_creation()        
        super().save(*args, **kwargs)
                   

class Term(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.ForeignKey(ShortText, on_delete=models.CASCADE, null=True, blank=True)
    text = RichTextField()
    tags = models.ManyToManyField(Tag, related_name='word_tags', null=True, blank=True)
    obs = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=50, choices=TypePartSpeechChoices.choices, default=TypePartSpeechChoices.ENGLISH)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('text',)]

    def __str__(self):
        return f'{self.id}'
    

class Option(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    term = models.TextField()
    right_option = models.BooleanField(default=False)
    language = models.CharField(max_length=50, choices=TypePartSpeechChoices.choices, null=True, blank=True)
    reference = models.ForeignKey(Term, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('term', 'reference', 'language')]

    def __str__(self):
        return f'{self.term} - {self.id}'


class TotalStudyTimeLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login_time = models.DateTimeField(null=True, blank=True)
    session_id = models.CharField(max_length=70, null=True, blank=True) 
    status = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)