import uuid
from django.db import models
from word.models import Tags, Terms, TypePartSpeechChoices
from ckeditor.fields import RichTextField


class Challenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    tags = models.ManyToManyField(Tags, related_name='challenges_tags', null=True, blank=True)
    writing = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.created_at.strftime("%d/%m/%Y")} - {self.id}'
    

class HistoricChallenge(models.Model):
    number_of_correct_answers = models.PositiveIntegerField(default=10)
    correct_percentage_considered = models.PositiveIntegerField(default=80)
    random = models.BooleanField(default=False)
    language = models.CharField(max_length=50, choices=TypePartSpeechChoices.choices, default=TypePartSpeechChoices.ENGLISH)    
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class WordMemorizationRandomTest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=100)
    term = RichTextField(config_name='term_ckeditor')
    sentences_options = RichTextField(null=True, blank=True, config_name='sentences_options_ckeditor')
    answer = models.TextField(null=True, blank=True)
    hit_percentage = models.PositiveIntegerField(null=True, blank=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True, blank=True)
    historic_challenge = models.ForeignKey(HistoricChallenge, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PhraseMaker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    request = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tags, related_name='tags_phrase_maker', null=True, blank=True)
    sentences = models.ManyToManyField(Terms, related_name='sentences_phrase_maker', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.created_at.strftime("%d/%m/%Y")} - {self.id}'


class TranslationGeneratorForSentence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sentences = models.ForeignKey(PhraseMaker, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tags, null=True, blank=True)
    request = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MultipleChoiceMemorizationTestsOptions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.ForeignKey(Terms, on_delete=models.CASCADE, null=True, blank=True)
    sentences_options = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)