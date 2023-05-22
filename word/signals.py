from django.dispatch import receiver
from django.db import models
from word.models import Phrase, Translation, Word
from .utils import generate_audio, generate_translations
# from django.db.models.signals import m2m_changed


@receiver(models.signals.post_save, sender=Word)
def generate_audio_for_words(sender, instance, **kwargs):
    _object = Word.objects.filter(id=instance.id)
    _object.update(pronunciation=generate_audio(instance.writing, instance.id))
    

@receiver(models.signals.post_save, sender=Word)
def generate_translation_for_words(sender, instance, **kwargs):
    _object = Word.objects.get(id=instance.id)
    translation = Translation.objects.create(**{"term": generate_translations(instance.writing)})
    _object.translations.add(translation)
    _object.save()

# @receiver(m2m_changed, sender=Word.translations.through)
# def update_m2m(sender, instance, action, reverse, *args,**kwargs):
#     # print(f"sender: {dir(sender)}")
#     # print(f"instance: {dir(instance)}")
   
#     print(f"instance: {instance.pk}")

#     # print(f"kwargs: {kwargs}")
#     # print(f"model: {kwargs.get('model')}")
#     # print(kwargs.get('pk_set'), action)

#     if action in ('pre_add'):
#         if list(kwargs.get('pk_set')):
#             pk_set = list(kwargs.get('pk_set'))[0]
#             instance.translations.add(kwargs.get('model').objects.get(id=pk_set))
#             instance.save()

    # if action in ('post_add', 'post_remove', 'post_clear'):
    #     instance.translations.add(f'post_comment_count_{instance.pk}', instance.comments.count())

# m2m_changed.connect(update_m2m,sender=Word.translations.through)


@receiver(models.signals.post_save, sender=Phrase)
def generate_audio_for_phrases(sender, instance, **kwargs):
    _object = Phrase.objects.filter(id=instance.id)
    _object.update(pronunciation=generate_audio(instance.terms, instance.id))


@receiver(models.signals.post_save, sender=Phrase)
def generate_translation_for_phrases(sender, instance, **kwargs):
    _object = Phrase.objects.get(id=instance.id)
    translation = Translation.objects.create(**{"term": generate_translations(instance.writing)})
    _object.translations.add(translation)
    _object.save()