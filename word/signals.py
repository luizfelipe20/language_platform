from django.dispatch import receiver
from django.db import models
from word.models import Tags, Translation, Terms, TypePartSpeechChoices
from .utils import generate_audio, generate_translations


@receiver(models.signals.pre_save, sender=Tags)
def validating_tag_duplication(sender, instance, **kwargs):
    if Tags.objects.filter(term=instance.term).exists():
        raise Exception("Tag already registered!") 


@receiver(models.signals.post_save, sender=Terms)
def generate_audio_for_words(sender, instance, created, **kwargs):
    if created:
        if not Terms.objects.get(id=instance.id).pronunciation:
            _object = Terms.objects.filter(id=instance.id)
            _object.update(pronunciation=generate_audio(instance.text, instance.id))
    

@receiver(models.signals.post_save, sender=Terms)
def generate_translation_for_words(sender, instance, created, **kwargs):
    if created:        
        _object = Terms.objects.get(id=instance.id)
        translation = Translation.objects.create(**{"term": generate_translations(instance.text), "language": TypePartSpeechChoices.ENGLISH})
        _object.translations.add(translation)