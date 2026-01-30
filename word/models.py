import os
import re
import json
import uuid
from datetime import timedelta
from django.db import transaction
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
    is_manual = models.BooleanField(default=False)
    text = RichTextField()
    translation = RichTextField(null=True, blank=True)
    phonetic_transcription_portuguese = RichTextField(null=True, blank=True)
    instruction_ia = RichTextField(null=True, blank=True)
    audio = models.FileField(upload_to='audios/', null=True, blank=True) 
    tags = models.ManyToManyField(Tag, related_name='short_texts_word_tags', null=True, blank=True)
    questions = models.TextField(null=True, blank=True)
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
    
    def replace_period(self, texto):
        texto = re.sub(r'(\d)\.(\d)', r'\1#\2', texto)
        texto = re.sub(r'([A-Za-z])\.([A-Za-z])', r'\1#\2',texto)
        return texto
    
    def text_formatter(self):
        _text = self.replace_period(self.text)
        phrases = _text.split('.')
        phrases = [f"{item.strip().replace('&nbsp;', '')}." for item in phrases]        
        phrases = [f"{' '.join(item.split())}" for item in phrases if len(item) > 3]         
        self.text = "\n\n".join(phrases).replace('#', '.').replace('&.39;', "'")
            
    def translator(self):
        _request_gpt = f"""
        Translate the following text into Brazilian Portuguese:{self.text}.
        Be concise and only provide the information requested.
        """
        self.translation = sentence_generator(_request_gpt)
    
    def tag_creation(self, name):
        Tag.objects.get_or_create(term=name)
    
    def question_generator(self, tag_name):
        elems = json.loads(self.questions)
        reference = ShortText.objects.get(id=self.id)
        tag = Tag.objects.get(term=tag_name)

        term_objs = []
        for obj in elems:
            term_objs.append(
                Term(
                    text=obj["question"],
                    reference=reference,
                    language=TypePartSpeechChoices.ENGLISH,
                )
            )

        with transaction.atomic():
            Term.objects.bulk_create(term_objs, ignore_conflicts=True)
            terms = Term.objects.filter(
                reference=reference,
                text__in=[obj["question"] for obj in elems],
            )

            term_map = {t.text: t for t in terms}
            for term in term_map.values():
                term.tags.add(tag)

            option_objs = []

            for obj in elems:
                sentence_obj = term_map[obj["question"]]

                for option in obj["options"]:
                    option_objs.append(
                        Option(
                            term=option,
                            right_option=option in obj["correct_answer"],
                            reference=sentence_obj,
                            language=TypePartSpeechChoices.PORTUGUESE,
                        )
                    )

            Option.objects.bulk_create(option_objs, batch_size=1000)

                            
    def save(self, *args, **kwargs):  
        tag_name = format_names_for_tags(self.title)
        self.text_formatter()
        if not len(self.tags.all()):
            self.tag_creation(tag_name)
                
        if not self.is_manual:      
            if not self.audio:
                self.audio_generator()
            if not self.translation:
                self.translator()    
        
        super().save(*args, **kwargs)
        
        if self.questions:
            if not Term.objects.filter(reference__id=self.id).exists():
                self.question_generator(tag_name)
                   

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