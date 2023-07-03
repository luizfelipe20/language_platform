import re
import uuid
from django.db import models
from memorization.producer import push_queue, setup_broker
from word.crowlers.google_translate import get_sentences, get_tags, get_translations
from word.crowlers.word_reference import get_conjugation
from word.models import Tags, Terms, Translation, TypePartSpeechChoices
from word.utils import generate_audio, generate_translations
from .models import ExtractTextFromPDF, GPTIssues, Challenge, ImportTexts, PhraseGeneratorForTerms, VerbsConjugation, WordMemorizationTest
from django.dispatch import receiver
from memorization.gpt_api import generates_response
from unidecode import unidecode
from PyPDF2 import PdfReader


# @receiver(models.signals.pre_save, sender=WordMemorizationTest)
# def validating_word_memorization_test_duplication(sender, instance, **kwargs):
#     if WordMemorizationTest.objects.filter(term=instance.term).exists():
#         raise Exception("Word Memorization Test already registered!") 


@receiver(models.signals.post_save, sender=GPTIssues)
def gpt_issues(sender, instance, created, **kwargs):
    _object = GPTIssues.objects.filter(id=instance.id)

    response_gpt = generates_response(instance.issue, instance.profile)    
    _object.update(answer=response_gpt)
        
    # for item in json.loads(response_gpt):
    #     if not Terms.objects.filter(text=item["phrase"]).exists(): 
    #         _object = Terms.objects.create(**{"text": item["phrase"], "gpt_identifier": str(instance.id)})
    #         translation = Translation.objects.create(**{"term": item["translation"], "language": TypePartSpeechChoices.ENGLISH})
    #         _object.translations.add(translation)


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
    sentences = []
    text = str(instance.term).splitlines()
    text_remove_acronym_punctuation = [re.sub(r"(?<!\w)([A-Za-z])\.", r"\1", elem) for elem in text]
    text_separated_by_punctuation = [re.split('[.!\?]', str(elem)) for elem in text_remove_acronym_punctuation]
    for elems in text_separated_by_punctuation:
        [sentences.append(item) for item in elems if len(item)]
                
    terms_list = []
    translation_list = []
    term_translation_through = {}

    _reference =  None

    for sentence in sentences:

        if sentence:
            print(sentence)
            term = Terms(**{"text": sentence.strip(), "reference": _reference, "pronunciation": generate_audio(sentence.strip(), uuid.uuid4().hex)})
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
     

@receiver(models.signals.post_save, sender=ExtractTextFromPDF)
def extract_text_from_video(sender, instance, **kwargs):    
    reader = PdfReader(instance.pdf)
    
    print(len(reader.pages))
    
    for page in reader.pages[13:10]:
        text = page.extract_text()
        print(text)


@receiver(models.signals.post_save, sender=PhraseGeneratorForTerms)
def phrase_generator_for_terms(sender, instance, created, **kwargs):
    queue_name = "fila_1"
    exchange_name = "exchange_1"
    rabbitmq_instance = setup_broker(queue_name, exchange_name)

    terms = instance.terms.split(",")
    tags_translations = {
        "verbo": "verb",
        "substantivo": "substantive",
        "adjetivo": "adjective",
        "advérbio": "adverb",
        "conjunção": "conjunction",
        "pronome": "pronoun",
        "preposição": "preposition"
    }

    terms = [unidecode(elem.lower()) for elem in terms]

    for item in terms:        
        raw_tags = get_tags(item)
        tags = [tags_translations.get(tag) for tag in raw_tags]  
        
        _tags = [tag.term for tag in instance.tags.all()]

        tags += _tags 

        for tag in tags:
            if tag:
                push_queue(rabbitmq_instance, {"term": item, "tag": tag})


@receiver(models.signals.pre_save, sender=VerbsConjugation)
def verbs_conjugation(sender, instance, **kwargs):    
    queue_name = "fila_2"
    exchange_name = "exchange_2"
    rabbitmq_instance = setup_broker(queue_name, exchange_name)

    verbs = instance.verbs.split(",")

    print(instance.tags.all())

    for item in verbs:
        for tag in instance.tags.all():
            push_queue(rabbitmq_instance, {"term": item, "tag": tag.term})