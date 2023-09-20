import uuid
from django.db import models


class TypePartSpeechChoices(models.TextChoices):
    PORTUGUESE = 'Portuguese'
    ENGLISH = 'English'


class Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    term = models.TextField()
    language = models.CharField(max_length=50, choices=TypePartSpeechChoices.choices, default=TypePartSpeechChoices.ENGLISH)
    tags = models.ManyToManyField('self', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('term',)]

    def __str__(self):
        return f'{self.term}'


class Terms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    tags = models.ManyToManyField(Tags, related_name='word_tags', null=True, blank=True)
    obs = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('text',)]

    def __str__(self):
        return f'{self.text} - {self.id}'
    

class Translation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    term = models.TextField()
    language = models.CharField(max_length=50, choices=TypePartSpeechChoices.choices, null=True, blank=True)
    reference = models.ForeignKey(Terms, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.term} - {self.id}'