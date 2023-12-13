from django.core.management.base import BaseCommand
from memorization.gpt_api import sentence_generator
from memorization.utils import remove_number_from_text, standardize_text
from word.models import Tags, Terms, Translation, TypePartSpeechChoices


class Command(BaseCommand):
    help = "OK"

    def add_arguments(self, parser):
        parser.add_argument("--tag", nargs="+", type=str)

    def handle(self, *args, **options): 
        for tag_name in options.get("tag"):            
            tag = Tags.objects.filter(term=tag_name).last()

            sentences_filtered_by_tags = Terms.objects.filter(tags__in=[tag], language=TypePartSpeechChoices.ENGLISH).order_by('-created_at')
            for obj_sentence in sentences_filtered_by_tags:
                if not Translation.objects.filter(reference=obj_sentence).exists():
                    self._generates_translations_for_sentences(obj_sentence)

    def _generates_translations_for_sentences(self, obj_sentence):
        request = "Return at least five translations into Brazilian Portuguese of the phrase 'SENTENCE'. Be brief and only return what was requested.".replace("SENTENCE", standardize_text(obj_sentence.text))                

        result = sentence_generator(request)

        for item in str(result).splitlines():
            try:
                obj, _ = Translation.objects.get_or_create(**{
                    "term": remove_number_from_text(item),
                    "reference": obj_sentence,
                    "language": TypePartSpeechChoices.PORTUGUESE, 
                })
                self.stdout.write(
                    self.style.SUCCESS(f"new_translations: {obj} !!!!")
                )
            except Exception as exc:
                print(f"_generates_translations_for_sentences__error: {exc}")