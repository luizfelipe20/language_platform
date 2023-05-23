from django.dispatch import receiver
from django.db import models

from memorization.gpt_api import generates_response
from .models import GPTIssues, Challenge


@receiver(models.signals.post_save, sender=GPTIssues)
def gpt_issues(sender, instance, **kwargs):
    _object = GPTIssues.objects.filter(id=instance.id)
    _object.update(answer=generates_response(instance.question))


@receiver(models.signals.post_save, sender=Challenge)
def challenge(sender, instance, **kwargs):
    Challenge.objects.exclude(id=instance.id).update(is_active=False)