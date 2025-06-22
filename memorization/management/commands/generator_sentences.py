import re
import random
from django.core.management.base import BaseCommand
from memorization.gpt_api import sentence_generator
from memorization.models import MultipleChoiceMemorizationTestsOptions
from word.models import Tag, Term, Translation, TypePartSpeechChoices


class Command(BaseCommand):
    help = "OK"

    def handle(self, *args, **options): 
        with open('./memorization/management/commands/tokens.txt', 'r') as file:
            # Lê todas as linhas do arquivo e armazena em uma lista
            linhas = file.readlines()    
            _dict_options = {}

            for elem in linhas:
                token = elem.strip()
                _request_gpt = f"""Behave like an English teacher and create 5 sentences using the following sentence {token}. 
                Enumerate the sentences. Return exactly what was requested, without additional information.
                """
                _result_gpt = sentence_generator(_request_gpt)
                _dict_options[token] = self._sanitizing_responses(_result_gpt)
            
            _list_with_tags = self._formatter(_dict_options)
            _list_sentences = self._to_save(_list_with_tags)

            self._generate_correct_translations(_list_sentences)
            self._generate_incorrect_translations(_list_sentences)

    def _sanitizing_responses(self, _result_gpt):
        list_sentences = _result_gpt.split("\n")
        sentences_without_numbers = [re.sub(r'^\s*\d+[\.\-\)]\s*', '', item, flags=re.MULTILINE) for item in list_sentences]
        for elem in sentences_without_numbers:
            if 'Certainly' in elem or 'Sure' in elem:
                sentences_without_numbers.remove(elem)
        sentences_without_spaces = [item.strip().replace('\n', '') for item in sentences_without_numbers if len(item)]
        return sentences_without_spaces

    def _get_tag(self, elem):
        tag, _ = Tag.objects.get_or_create(term=elem)
        return tag

    def _formatter(self, _dict_options):
        _list_results = []

        for elem in _dict_options:
            tag = self._get_tag(elem)

            for sentence in _dict_options[elem]:    
                _list_results.append({
                    'tag': tag,
                    'sentence': sentence
                })

        return _list_results    

    def _to_save(self, _list):
        _results = []
        for elem in _list:
            try:
                sentence_obj, _ = Term.objects.get_or_create(**{
                    "text": elem.get("sentence"),
                    "language": TypePartSpeechChoices.ENGLISH, 
                })
                sentence_obj.tags.add(elem.get("tag"))
                _results.append({"obj": sentence_obj, "sentence": elem.get("sentence")})                
            except Exception as exc:
                print(f"exc__error: {exc}")
        
        return _results

    def _generate_correct_translations(self, _list):
        for elem in _list:
            _request_gpt = f"Give an example of a Brazilian Portuguese translation for the following sentence: {elem.get('sentence')}. Return exactly what was requested, without additional information."                
            _result_gpt = sentence_generator(_request_gpt)
            try:
                Translation.objects.get_or_create(**{
                    "term": _result_gpt,
                    "right_option": True,
                    "reference": elem.get('obj'),
                    "language": TypePartSpeechChoices.PORTUGUESE, 
                })
            except Exception as exc:
                print(f"_generates_translations_for_sentences__error: {exc}")

    def _generate_incorrect_translations(self, _list):
        for elem in _list:
            _request_gpt = f"Create 5 incorrect translations for the following sentence {elem.get('sentence')}, in Brazilian Portuguese, change the meaning of the sentences, but keep the grammatical structure, number the sentences. Return exactly what was requested, without additional information."                
            _result_gpt = sentence_generator(_request_gpt)
            _results = self._sanitizing_responses(_result_gpt)
            for item in _results:
                try:
                    Translation.objects.get_or_create(**{
                        "term": item,
                        "reference": elem.get('obj'),
                        "language": TypePartSpeechChoices.PORTUGUESE, 
                    })
                except Exception as exc:
                    print(f"_generates_translations_for_sentences__error: {exc}")