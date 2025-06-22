import random
from django.db import models
from .models import ShortText
from memorization.utils import remove_tags_html
from django.dispatch import receiver


def shuffle_text(text):
    text = remove_tags_html(text)
    words_list = text.split(" ")
    random.shuffle(words_list)  # Embaralha a lista
    return " ".join(words_list)  # Junta os caracteres de volta


@receiver(models.signals.post_save, sender=ShortText)
def post_save_short_texts(sender, instance, created, **kwargs):
    scrambled_text = shuffle_text(instance.text)
    ShortText.objects.filter(id=instance.id).update(scrambled_text=remove_tags_html(scrambled_text))