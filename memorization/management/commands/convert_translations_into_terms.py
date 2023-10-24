from django.core.management.base import BaseCommand
from word.models import Tags, Terms, Translation, TypePartSpeechChoices
from django.utils.html import format_html


class Command(BaseCommand):
    help = "OK"

    def add_arguments(self, parser):
        parser.add_argument("--tag", nargs="+", type=str)

    def handle(self, *args, **options): 
        for tag_name in options.get("tag"):            
            tag = Tags.objects.filter(term=tag_name).last()

            terms = Terms.objects.filter(tags__in=[tag]).order_by('created_at')

            for term in terms:
                print(term.translation_set.all())

                html = (f'<li>{elem.term}</li>' for elem in term.translation_set.all())

                obj, _ = Terms.objects.get_or_create(**{
                    "text": format_html(f"<ul>{''.join(html)}</ul>"),
                    "language": TypePartSpeechChoices.PORTUGUESE, 
                })
                obj.tags.add(tag)

                Translation.objects.get_or_create(**{
                    "term": term.text, 
                    "language": TypePartSpeechChoices.ENGLISH, 
                    "reference": obj}
                )

            if not terms:
                self.stdout.write(
                    self.style.WARNING('No changes were made !!!')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Successfully !!!')
                )