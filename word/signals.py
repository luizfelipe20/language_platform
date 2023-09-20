from django.dispatch import receiver
from django.db import models
from word.models import Tags
from .utils import text_normalization


@receiver(models.signals.pre_save, sender=Tags)
def validating_tag_duplication(sender, instance, **kwargs):
    if Tags.objects.filter(term=instance.term).exists():
        raise Exception("Tag already registered!") 


@receiver(models.signals.post_save, sender=Tags)
def normalization_tag(sender, instance, **kwargs):
    Tags.objects.filter(id=instance.id).update(term=text_normalization(instance.term))