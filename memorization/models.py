import uuid
from django.db import models
from word.models import Tags
from ckeditor.fields import RichTextField


class Challenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tags = models.ManyToManyField(Tags, related_name='challenges_tags', null=True, blank=True)
    writing = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    number_of_correct_answers = models.PositiveIntegerField(default=10)
    correct_percentage_considered = models.PositiveIntegerField(default=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.tags.last()} - {self.created_at.strftime("%d/%m/%Y")}'
    

class WordMemorizationRandomTest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=100)
    term = RichTextField()
    answer = models.TextField(null=True, blank=True)
    hit_percentage = models.PositiveIntegerField(null=True, blank=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)