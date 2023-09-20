import random
from django.db import models
from word.models import Terms
from .models import Challenge
from django.dispatch import receiver


@receiver(models.signals.post_save, sender=Challenge)
def challenge(sender, instance, created, **kwargs):
    Challenge.objects.exclude(id=instance.id).update(is_active=False)


# @receiver(models.signals.m2m_changed, sender=Challenge.tags.through)
# def challenge_m2m(sender, instance, action, pk_set, **kwargs):
#     if action == 'post_add':
#         terms_ids = list(Terms.objects.filter(tags__in=instance.tags.all()).values_list("id", flat=True).distinct("id"))

#         references_ids = []
#         if instance.phrases_associated_with_term:
#             references_ids = list(Terms.objects.filter(reference__in=terms_ids).values_list("id", flat=True).distinct("id"))

#         terms_ids += references_ids

#         list_terms = list(Terms.objects.filter(id__in=terms_ids).values_list("id", flat=True).distinct("id"))

#         random_itens = random.sample(list_terms, instance.amount)

#         terms = Terms.objects.filter(id__in=random_itens)