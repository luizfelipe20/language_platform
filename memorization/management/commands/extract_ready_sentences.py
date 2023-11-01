from time import sleep
from django.core.management.base import BaseCommand
from word.models import Terms, Translation, Tags, TypePartSpeechChoices
from playwright.sync_api import sync_playwright

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'language_platform.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

class Command(BaseCommand):
    help = "OK"

    def handle(self, *args, **options): 
        for count in range(1, 91): 
            url = f'https://aulasdeinglesgratis.net/1800-frases-em-ingles-part-{count}/'
            try:
                with sync_playwright() as p:
                    browser = p.firefox.launch()
                    page = browser.new_page()
                    page.goto(url)
                    locator = page.locator("p")
                        
                    self.stdout.write(
                        self.style.HTTP_INFO(f'url: {url}')
                    )

                    self.set_setences(locator, count)
                    
                    page.close()
            except Exception as exc:
                self.stdout.write(
                    self.style.WARNING(f'playwright__erro: {exc}')
                )
                Terms.objects.last().delete()
                continue

    def set_setences(self, locator, count):
        for index, value in enumerate(locator.all_inner_texts()):
            try:
                if index < 20:
                    result = ''.join([elem.replace(".", "") for elem in value if not elem.isdigit()])
                    sentences = result.strip().splitlines()
                    self.stdout.write(
                        self.style.HTTP_INFO(f'sentences: {sentences}')
                    )
                    
                    obj, _ = Terms.objects.get_or_create(**{
                        "text": sentences[0],
                        "language": TypePartSpeechChoices.ENGLISH, 
                    })

                    tag, _ = Tags.objects.get_or_create(**{
                        "term": f"phrases_in_english_part_{count}"
                    })

                    obj.tags.add(tag)

                    Translation.objects.get_or_create(**{
                        "term": sentences[1], 
                        "language": TypePartSpeechChoices.PORTUGUESE, 
                        "reference": obj}
                    )
            except Exception as exc:
                self.stdout.write(
                    self.style.WARNING(f'set_setences__erro: {exc}')
                )
                Terms.objects.last().delete()
                continue
