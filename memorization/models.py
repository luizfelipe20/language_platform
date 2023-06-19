import uuid
from django.db import models
from word.models import Tags

class GPTIssues(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issue = models.TextField()
    profile = models.TextField(default="You are an English teacher and will help me with grammar questions.", null=True, blank=True)
    tags = models.ManyToManyField(Tags, related_name='gpt_issues_tags', null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Challenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tags = models.ManyToManyField(Tags, related_name='challenges_tags', null=True, blank=True)
    writing = models.BooleanField(default=False)
    audio = models.BooleanField(default=False)
    phrases_associated_with_term = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class WordMemorizationTest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=100)
    term = models.TextField(null=True, blank=True)
    audio = models.FileField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    hit_percentage = models.PositiveIntegerField(null=True, blank=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ImportTexts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    term = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tags, related_name='import_texts_tags', null=True, blank=True)
    link = models.URLField(max_length=400, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PhraseGeneratorForTerms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    terms = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tags, related_name='phrase_generator_for_terms', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ExtractTextFromPDF(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    link = models.URLField(max_length=400, null=True, blank=True)
    pdf = models.FileField(upload_to="./pdf", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
