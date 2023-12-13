import random
from django.core.management.base import BaseCommand
from memorization.gpt_api import sentence_generator
from memorization.models import MultipleChoiceMemorizationTestsOptions
from memorization.utils import remove_number_from_text
from word.models import Tags, Terms, Translation
from django.utils.html import format_html


class Command(BaseCommand):
    help = "OK"

    def add_arguments(self, parser):
        parser.add_argument("--tag", nargs="+", type=str)

    def handle(self, *args, **options): 
        for tag_name in options.get("tag"):            
            tags = Tags.objects.filter(term__contains=tag_name)

            print(f"tags: {tags}")

            terms = Terms.objects.filter(tags__in=tags).order_by('-created_at')

            for term in terms:
                self._populate_translation_options(term)

    def _populate_translation_options(self, reference):
        _sentences_options = MultipleChoiceMemorizationTestsOptions.objects.filter(reference=reference)
        if _sentences_options.count():
            self.stdout.write(
                self.style.SUCCESS(f"_sentences_options: {_sentences_options.last().sentences_options} \n")
            )
            return
        
        sentences = Translation.objects.filter(reference=reference).values_list("term", flat=True)
        request = "Retorne 15 frases com a mesma estrutura gramatical da frase 'SENTENCE' mas com significados diferentes da frase. Seja sucinto e retorne apenas o foi solicitado.".replace("SENTENCE", sentences[0])
        result = sentence_generator(request)
        gpt_senteces = str(result).splitlines()

        list_translations = list(sentences)[:2] + [remove_number_from_text(item) for item in gpt_senteces]
        random.shuffle(list_translations)

        itens = [f"<li>{item}</li>" for item in list_translations]        
        list_html =format_html(f"<ul>{''.join(itens)}</ul>")

        try:
            if not MultipleChoiceMemorizationTestsOptions.objects.filter(reference=reference).exists():
                obj, _ = MultipleChoiceMemorizationTestsOptions.objects.get_or_create(**{
                    "sentences_options": list_html,
                    "reference": reference,
                })

                self.stdout.write(
                    self.style.SUCCESS(f"new_sentences_options: {obj} !!!!")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"already_updated: {reference} !!!!")
                )

        except Exception as exc:
            print(f"_populate_translation_options__error: {exc}")