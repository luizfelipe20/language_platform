import re
from word.models import Terms, Word
from memorization.utils import standardize_text
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "OK"

    def add_arguments(self, parser):
        parser.add_argument('--option', default=0, type=int)

    def handle(self, *args, **options): 
        options.get('option')

        _rules = {
            0: self._base,
            1: self._regex_based_removal,
            2: self._removal_malformed_sentences,
            3: self._remove_html_tags,
            4: self._remove_all_records_from_word_table
        }

        _rules[options.get('option')]()

    def _base(self):
        print('Deu bom!!!!!!')

    def _removal_malformed_sentences(self):
        ids = []
        instances = Terms.objects.order_by('-created_at')
        for elem in instances:
            raw_sentence = standardize_text(elem.text)
            print(raw_sentence)
            if "style" in raw_sentence or "_blank" in raw_sentence:
                ids.append(elem.id)

        print(ids)
        Terms.objects.filter(id__in=ids).delete()

    def _regex_based_removal(self):
        ids = []
        instances = Terms.objects.order_by('-created_at')
        for elem in instances:
            if bool(re.search(r'.*\?.*\?', elem.text)):
                ids.append(elem.id)

        print(ids)
        Terms.objects.filter(id__in=ids).delete()
    
    def _remove_html_tags(self):
        instances = Terms.objects.all().order_by('-created_at')[0:600]
        for elem in instances:
            try:
                raw_sentence = standardize_text(elem.text)
                print(raw_sentence)
                Terms.objects.filter(id=elem.id).update(text=raw_sentence)
            except Exception as exp:
                print(f'_remove_html_tags__error: {elem.id} -> {exp}')
    
    def _remove_all_records_from_word_table(self):
        Word.objects.all().delete()