import re
import random
from django.core.management.base import BaseCommand
from memorization.gpt_api import sentence_generator
from memorization.models import MultipleChoiceMemorizationTestsOptions
from word.models import Tags, Terms, Word, Translation, TypePartSpeechChoices


class Command(BaseCommand):
    help = "OK"

    def handle(self, *args, **options): 
        with open('./memorization/management/commands/phrasal_verbs.txt', 'r') as file:
            # Lê todas as linhas do arquivo e armazena em uma lista
            linhas = file.readlines()    
            _dict_phrasal_verbs = {}

            for _phrasal_verb in linhas[:5]:
                phrasal_verb = _phrasal_verb.strip()
                request = f"""
                    Act as an English grammar teacher, return a list in csv format without header with 6 example sentences 
                    exploring the different meanings of the phrasal verb {phrasal_verb}. Be succinct and only return what was requested. 
                    """
                _dict_phrasal_verbs[f'{phrasal_verb}'] = self._sanitizing_responses(request)
            
            _list = self._formatter(_dict_phrasal_verbs)
            _list = self._to_save(_list)
            self._get_translations(_list)
            self._populate_options(_list)

    def _get_definition(self, elem):
        request = f"""
            Act like an English teacher and return the most common definitions for the phrasal verb {elem}. Please answer in Brazilian Portuguese 
        """
        _result = sentence_generator(request)
        if not Word.objects.filter(**{
                "name": elem, 
                "part_of_speech": "phrasal verb"
            }).exists():
            obj = Word.objects.create(
                **{
                    "name": elem, 
                    "definition": _result, 
                    "part_of_speech": "phrasal verb"
                }
            )
            return obj
        obj = Word.objects.filter(name=elem).last()
        return obj

    def _get_tag(self, elem):
        if not Tags.objects.filter(term=elem).exists():
            tag = Tags.objects.create(
                **{"term": elem}
            )
            return tag

        tag = Tags.objects.filter(term=elem).last()
        return tag
    
    def _get_translations(self, _list):
        for elem in _list:
            request = f"""Act as an English teacher and return 5 Brazilian Portuguese translation options for the phrase {elem.get('sentence')}. 
                Be brief and only return what was requested."""                
            standardized_sentence = self._sanitizing_responses(request)          

            for item in standardized_sentence:
                try:
                    if not Translation.objects.filter(**{
                        "term": item,
                        "reference": elem.get('obj'),
                    }).exists():
                        Translation.objects.create(**{
                            "term": item,
                            "reference": elem.get('obj'),
                            "language": TypePartSpeechChoices.PORTUGUESE, 
                        })
                except Exception as exc:
                    print(f"_generates_translations_for_sentences__error: {exc}")

    def _formatter(self, _dict_phrasal_verbs):
        _list_results = []

        for elem in _dict_phrasal_verbs:
            definition = self._get_definition(elem)
            tag = self._get_tag(elem)

            for sentence in _dict_phrasal_verbs[elem]:
                url = f"http://localhost:8000/admin/word/word/{definition.id}/change/"
                sentence_html = f"<a href='{url}' target='_blank'><span>{sentence}</span></a>"
                
                _list_results.append({
                    'tag': tag,
                    'sentence': sentence,
                    'sentence_html': sentence_html, 
                })

        return _list_results    

    def _sanitizing_responses(self, request):
        _result = sentence_generator(request)
        standard = r'\d+\. '
        replacement = ''
        standardized_sentence = str(re.sub(standard, replacement, _result)).splitlines()
        _sentences = [item for item in standardized_sentence if len(item)]
        _list = _sentences[1:] 

        if len(_list) == 0:
            print(f"Não veio nada {_list}")
            return self._sanitizing_responses(request)

        return _list

    def _to_save(self, _list):
        _results = []
        for elem in _list:
            try:
                if not Terms.objects.filter(**{
                    "text": elem.get("sentence_html"),
                    "language": TypePartSpeechChoices.ENGLISH, 
                }).exists():
                    sentence_obj = Terms.objects.create(**{
                        "text": elem.get("sentence_html"),
                        "language": TypePartSpeechChoices.ENGLISH, 
                    })
                    sentence_obj.tags.add(elem.get("tag"))
                else:
                    sentence_obj = Terms.objects.filter(**{
                        "text": elem.get("sentence_html"),
                        "language": TypePartSpeechChoices.ENGLISH, 
                    })

                _results.append({"obj": sentence_obj, "sentence": elem.get("sentence")})                
            except Exception as exc:
                print(f"exc__error: {exc}")
        
        return _results
    
    def _populate_options(self, _list):
        for elem in _list:
            _translations = list(Translation.objects.filter(reference=elem.get('obj')).values_list("term", flat=True))

            if len(_translations) == 0:
                Terms.objects.get(id=elem.get('obj').id).delete()
                continue

            _request = f"""
                Se comporte como um professor de português e retorne 10 frases aleatorias seguindo a mesma estrutura gramatical da frase {_translations[0]}, 
                porém alterando o sentido original.
            """

            _options = self._sanitizing_responses(_request)
            _options = _options + _translations[0:2]
            res = random.sample(_options, len(_options))
            _options = ",".join(res)

            try:
                MultipleChoiceMemorizationTestsOptions.objects.get_or_create(**{
                    "sentences_options": _options,
                    "reference": elem.get('obj'),
                })
            except Exception as exc:
                print(f"_populate_translation_options__error: {exc}")