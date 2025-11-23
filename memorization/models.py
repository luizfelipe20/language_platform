import uuid
from django.db import models
from word.models import Tag, Term, TypePartSpeechChoices


class Challenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='challenges_tags', null=True, blank=True)
    hearing = models.BooleanField(default=False)
    writing = models.BooleanField(default=False)
    translation = models.BooleanField(default=False)
    phonetic_transcription = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    number_of_correct_answers = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.created_at.strftime("%d/%m/%Y")} - {self.id}'
    

class HistoryAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.ForeignKey(Term, on_delete=models.CASCADE, null=True, blank=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True, blank=True)
    got_it_right = models.BooleanField(default=False)
    language = models.CharField(max_length=50, choices=TypePartSpeechChoices.choices, default=TypePartSpeechChoices.ENGLISH)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'


class ChallengesCompleted(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.ForeignKey(Term, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True, blank=True)
    language = models.CharField(max_length=50, choices=TypePartSpeechChoices.choices, default=TypePartSpeechChoices.ENGLISH)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'