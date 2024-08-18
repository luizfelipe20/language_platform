import re
import random
from django.core.management.base import BaseCommand
from memorization.gpt_api import sentence_generator
from memorization.models import MultipleChoiceMemorizationTestsOptions
from word.models import Tags, Terms, Word, Translation, TypePartSpeechChoices


class Command(BaseCommand):
    help = "OK"

    def handle(self, *args, **options): 
        with open('./memorization/management/commands/tokens.txt', 'r') as file:
            # Lê todas as linhas do arquivo e armazena em uma lista
            linhas = file.readlines()    
            _dict_phrasal_verbs = {}

            for _phrasal_verb in linhas[:5]:
                phrasal_verb = _phrasal_verb.strip()
                request = """
                    Act as an English grammar teacher, return a list in csv format without header with 5 example sentences for the word TERM. 
                    Be succinct and only return what was requested. 
                    """.replace("TERM", phrasal_verb)
                _dict_phrasal_verbs[f'{phrasal_verb}'] = self._sanitizing_responses(request)
            
            _list = self._formatter(_dict_phrasal_verbs)
            _list = self._to_save(_list)
            self._get_translations(_list)
            self._populate_options(_list)

    def _get_definition(self, elem):
        request = f"""
            Acted as an English teacher and returned the definition of the phrasal verb: {elem}. Please answer in Brazilian Portuguese 
        """
        _result = sentence_generator(request)
        obj, _ = Word.objects.get_or_create(
            **{
                "name": elem, 
                "definition": _result, 
                "part_of_speech": "phrasal verb"
            }
        )
        return obj

    def _get_tag(self, elem):
        tag, _ = Tags.objects.get_or_create(term=elem)
        return tag
    
    def _get_translations(self, _list):
        for elem in _list:
            request = f"""Act as an English teacher and return 5 Brazilian Portuguese translation options for the phrase {elem.get('sentence')}. 
                Be brief and only return what was requested."""                
            standardized_sentence = self._sanitizing_responses(request)          

            for item in standardized_sentence:
                try:
                    Translation.objects.get_or_create(**{
                        "term": item,
                        "reference": elem.get('obj'),
                        "language": TypePartSpeechChoices.PORTUGUESE, 
                    })
                except Exception as exc:
                    print(f"_generates_translations_for_sentences__error: {exc}")

    def _formatter(self, _dict_phrasal_verbs):
        _list_results = []

        for elem in _dict_phrasal_verbs:
            self._get_definition(elem)
            tag = self._get_tag(elem)

            for sentence in _dict_phrasal_verbs[elem]:    
                _list_results.append({
                    'tag': tag,
                    'sentence': sentence
                })

        return _list_results    

    def _sanitizing_responses(self, request):
        _result = sentence_generator(request)
        standard = r'\d+\. '
        replacement = ''
        standardized_sentence = str(re.sub(standard, replacement, _result)).splitlines()
        _sentences = [item for item in standardized_sentence if len(item)]
        return _sentences[1:]

    def _to_save(self, _list):
        _results = []
        for elem in _list:
            try:
                sentence_obj, _ = Terms.objects.get_or_create(**{
                    "text": elem.get("sentence"),
                    "language": TypePartSpeechChoices.ENGLISH, 
                })
                sentence_obj.tags.add(elem.get("tag"))
                _results.append({"obj": sentence_obj, "sentence": elem.get("sentence")})                
            except Exception as exc:
                print(f"exc__error: {exc}")
        
        return _results
    
    def _populate_options(self, _list):
        for elem in _list:
            _translations = list(Translation.objects.filter(reference=elem.get('obj')).values_list("term", flat=True))
            _request = f"""
                Atuei como um professor de portugues e gere 10 frases aleatorias seguindo a estrutura gramatical da frase {_translations[0]}, 
                mas alterando o sentido original
            """
            _options = self._sanitizing_responses(_request)
            _options += _translations[0:2]
            res = random.sample(_options, len(_options))
            _options = ",".join(res)

            try:
                MultipleChoiceMemorizationTestsOptions.objects.get_or_create(**{
                    "sentences_options": _options,
                    "reference": elem.get('obj'),
                })
            except Exception as exc:
                print(f"_populate_translation_options__error: {exc}")