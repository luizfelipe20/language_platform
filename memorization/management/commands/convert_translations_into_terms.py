from django.core.management.base import BaseCommand
from word.models import Tags, Terms, Translation, TypePartSpeechChoices


class Command(BaseCommand):
    help = "OK"

    def add_arguments(self, parser):
        parser.add_argument("--tag", nargs="+", type=str)

    def handle(self, *args, **options): 
        for tag_name in options.get("tag"):
            translations = []
            
            tag = Tags.objects.filter(term=tag_name).last()

            translations = Translation.objects.filter(reference__tags__in=[tag]).order_by('created_at')

            _dict_translation  = {}

            for translation in translations:
                _dict_translation[str(translation.id)] = {
                    "reference": translation.reference, 
                    "translation_term": translation.term, 
                    "tag": tag
                }

            for item in _dict_translation:

                obj, _ = Terms.objects.get_or_create(**{"text": _dict_translation[item]["translation_term"]})
                obj.tags.add(_dict_translation[item]["tag"])

                Translation.objects.get_or_create(**{
                    "term": _dict_translation[item]["reference"].text, 
                    "language": TypePartSpeechChoices.ENGLISH, 
                    "reference": obj}
                )

            if not translations:
                self.stdout.write(
                    self.style.WARNING('No changes were made !!!')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Successfully !!!')
                )