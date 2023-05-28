from asyncio import sleep
import re
import json
import uuid
from django.db import models
from word.models import Tags, Terms, Translation, TypePartSpeechChoices
from word.utils import generate_audio, generate_translations, has_numbers
from .models import GPTIssues, Challenge, ImportTexts, PhraseGeneratorForTerms
from django.dispatch import receiver
from memorization.gpt_api import generates_response


@receiver(models.signals.post_save, sender=GPTIssues)
def gpt_issues(sender, instance, created, **kwargs):
    _object = GPTIssues.objects.filter(id=instance.id)

    response_gpt = generates_response(instance.issue, instance.profile)    
    _object.update(answer=response_gpt)
        
    for item in json.loads(response_gpt):
        if not Terms.objects.filter(text=item["phrase"]).exists(): 
            _object = Terms.objects.create(**{"text": item["phrase"], "gpt_identifier": str(instance.id)})
            translation = Translation.objects.create(**{"term": item["translation"], "language": TypePartSpeechChoices.ENGLISH})
            _object.translations.add(translation)


@receiver(models.signals.post_save, sender=Challenge)
def challenge(sender, instance, **kwargs):
    Challenge.objects.exclude(id=instance.id).update(is_active=False)


@receiver(models.signals.m2m_changed, sender=GPTIssues.tags.through)
def gpt_issues_tags(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for item in Terms.objects.filter(gpt_identifier=str(instance.id)):
            item.tags.set(instance.tags.all())


@receiver(models.signals.post_save, sender=ImportTexts)
def import_texts(sender, instance, **kwargs):
    text = re.split('[...?!!!.!]', str(instance.term))
    terms_list = []
    translation_list = []
    term_translation_through = {}

    _reference =  None

    for line in text:
        prhase = line

        if prhase.strip():
            term = Terms(**{"text": prhase, "reference": _reference, "pronunciation": generate_audio(prhase, uuid.uuid4().hex)})
            translation = Translation(**{"term": generate_translations(term.text), "language": TypePartSpeechChoices.ENGLISH})
            _reference = term

            term_translation_through[f"{term.id}"] = translation
                                                    
            terms_list.append(term)
            translation_list.append(translation)
    
    Terms.objects.bulk_create(terms_list)
    Translation.objects.bulk_create(translation_list)
    
    tags = instance.tags.all()

    for key in term_translation_through:
        term = Terms.objects.get(id=str(key))    
        term.tags.set(tags)
        term.translations.add(term_translation_through[str(key)])


@receiver(models.signals.post_save, sender=PhraseGeneratorForTerms)
def phrase_generator_for_terms(sender, instance, **kwargs):
    words = instance.terms.split(",")
    verb_tenses = ("present simple", "present continuous", "present perfect", "present perfect continuous", "past simple", "past continuous",
                   "past perfect", "past perfect continuous", "future simple", "future continuous", "future perfect", "future perfect continuous")
    base_text_list = []
    tags_list = []

    for item in words:
        tag = Tags.objects.create(**{"term": item, "language": TypePartSpeechChoices.ENGLISH})
        tags_list.append(tag)

        for tense in verb_tenses:
            base_text = f"""Return a list of {instance.amount} short sentences containing the word get, in the {tense} tense and exploring the different meanings that the word get can have. 
            The list must be in the format of a JSON list, each phrase generated must be assigned as a value to the prhase key inside each JSON element, 
            add one more translation key and add as value to it the translation of the phrase in Brazilian Portuguese. Be succinct and return only what was requested.""" 
            base_text_list.append(base_text)
        tag = Tags.objects.filter(term=tense).first()
        tags_list.append(tag)

    for text in base_text_list:
        response_gpt = generates_response(text, instance.profile)  
        sleep(10)  
        
        for item in json.loads(response_gpt):
            if not Terms.objects.filter(text=item["phrase"]).exists(): 
                _object = Terms.objects.create(**{"text": item["phrase"], "gpt_identifier": str(instance.id)})
                translation = Translation.objects.create(**{"term": item["translation"], "language": TypePartSpeechChoices.ENGLISH})
                _object.translations.add(translation)
                _object.tags.set(tags_list)