from django.dispatch import receiver
from django.db import models
from word.models import Tags, Terms
from .utils import sentence_normalization, tag_normalization


@receiver(models.signals.post_save, sender=Terms)
def signals_sentence_normalization(sender, instance, **kwargs):    
    Terms.objects.filter(id=instance.id).update(text=sentence_normalization(instance.text))


@receiver(models.signals.post_save, sender=Tags)
def signals_tag_normalization(sender, instance, **kwargs):
    Tags.objects.filter(id=instance.id).update(term=tag_normalization(instance.term))