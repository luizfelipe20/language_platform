from django.db import models
from word.models import Term, Translation
from .models import Challenge, HistoricChallenge, Options, UnavailableItem, WordMemorizationRandomTest
from django.dispatch import receiver


@receiver(models.signals.post_save, sender=Challenge)
def post_save_challenge(sender, instance, created, **kwargs):
    Challenge.objects.exclude(id=instance.id).update(is_active=False)


@receiver(models.signals.post_save, sender=HistoricChallenge)
def post_save_historic_challenge(sender, instance, created, **kwargs):
    items = Term.objects.filter(
        tags__in=instance.challenge.tags.all(), 
        language=instance.language
    )
    UnavailableItem.objects.filter(reference__in=items).delete()
    print("PASSOU AQUI!!!!!!!!!!!!!")


@receiver(models.signals.post_save, sender=Options)
def post_save_options(sender, instance, created, **kwargs):
    if instance.selected:
        _reference = instance.word_memorization_random_test.reference
        translations = list(Translation.objects.filter(reference=_reference).values_list("term", flat=True))
        
        if instance.option in translations:
            WordMemorizationRandomTest.objects.filter(id=instance.word_memorization_random_test.id).update(is_true=True)
