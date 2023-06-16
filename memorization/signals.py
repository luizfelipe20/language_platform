import re
import json
import uuid
from django.db import models
from word.models import Tags, Terms, Translation, TypePartSpeechChoices
from word.utils import generate_audio, generate_translations
from .models import ExtractTextFromPDF, GPTIssues, Challenge, ImportTexts, PhraseGeneratorForTerms, WordMemorizationTest
from django.dispatch import receiver
from memorization.gpt_api import generates_response


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


@receiver(models.signals.post_save, sender=PhraseGeneratorForTerms)
def phrase_generator_for_terms(sender, instance, created, **kwargs):
    terms = instance.terms.split(",")
    text = instance.base_text.replace("WORDS", instance.terms)
    
    for term in terms:
        if not Tags.objects.filter(term=term).exists():
            Tags.objects.create(**{"term": term, "language": TypePartSpeechChoices.ENGLISH})
    
    response_gpt = generates_response(text, instance.profile)
    response_gpt_json = "".join(re.findall(r'[\[{},:\s"\w\]]', response_gpt))      
    PhraseGeneratorForTerms.objects.filter(id=instance.id).update(answer=response_gpt_json)
    
    try:
        start = response_gpt_json.index("[")
        size = len(response_gpt_json)+1
        data_json = response_gpt_json[start:size]
        payload = json.loads(data_json)
    except Exception as exp:
        raise Exception(f"Unsupported payload! {exp}") 
     
    for item in payload:
        for tag in instance.tags.all():
            for sentence in item.get(tag.term, []):                    
                if not Terms.objects.filter(text=sentence).exists(): 
                    _object = Terms.objects.create(**{"text": sentence, "gpt_identifier": str(instance.id)})
                    _tag_word = Tags.objects.filter(term=item["term"]).last()
                    _object.tags.add(_tag_word)

    _objects = Terms.objects.filter(gpt_identifier=instance.id)    
    for _object in _objects:
        _object.tags.set(instance.tags.all())
 

@receiver(models.signals.post_save, sender=ExtractTextFromPDF)
def extract_text_from_video(sender, instance, **kwargs):    
    # https://www.geeksforgeeks.org/extract-text-from-pdf-file-using-python/
    from PyPDF2 import PdfReader
    
    reader = PdfReader(instance.pdf)
    
    print(len(reader.pages))
    
    for page in reader.pages[13:10]:
        text = page.extract_text()
        print(text)