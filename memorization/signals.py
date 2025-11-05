from django.db import models
from .models import Challenge
from django.dispatch import receiver


@receiver(models.signals.post_save, sender=Challenge)
def post_save_challenge(sender, instance, created, **kwargs):
    Challenge.objects.exclude(id=instance.id).update(is_active=False)
