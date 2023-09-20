import uuid
from django.db import models
from word.models import Tags


class Challenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tags = models.ManyToManyField(Tags, related_name='challenges_tags', null=True, blank=True)
    writing = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class WordMemorizationRandomTest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=100)
    term = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    hit_percentage = models.PositiveIntegerField(null=True, blank=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)