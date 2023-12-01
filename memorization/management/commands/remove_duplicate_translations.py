from django.core.management.base import BaseCommand
from word.models import Translation


class Command(BaseCommand):
    help = "OK"


    def handle(self, *args, **options): 
        for elem in Translation.objects.all().order_by('created_at'):
            duplicate_translations = Translation.objects.filter(term=elem.term, reference=elem.reference).exclude(id=elem.id)

            if duplicate_translations:
                Translation.objects.filter(id__in=duplicate_translations.values_list("id", flat=True)).delete()

                self.stdout.write(
                    self.style.SUCCESS(f'duplicate_translations: {duplicate_translations}')
                )