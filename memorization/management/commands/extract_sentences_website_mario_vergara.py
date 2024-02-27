import os
import django
from langdetect import detect
from django.core.management.base import BaseCommand
from word.models import Terms, Translation, Tags, TypePartSpeechChoices
from playwright.sync_api import sync_playwright
from word.utils import tag_normalization
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'language_platform.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

class Command(BaseCommand):
    help = "OK"

    def handle(self, *args, **options): 
        url = f'https://www.mairovergara.com/phrasal-verbs/'
        with sync_playwright() as p:
            browser = p.firefox.launch()
            page = browser.new_page()
            page.goto(url)
            link_locators = page.locator('.td-pb-padding-side').get_by_role('link').all()
            
            for elem in link_locators:
                try:
                    link = elem.get_attribute("href")

                    if Tags.objects.filter(term__contains=tag_normalization(link)).exists():
                        self.stdout.write(
                            self.style.HTTP_INFO(f'href: {link}')
                        )
                    else:
                        if 'phrasal-verb' in link:
                            
                            self.stdout.write(
                                self.style.WARNING(f'href: {link}')
                            )
                            
                            page = browser.new_page()
                            page.goto(link)
                            sentences = page.locator('p')
                            
                            for elem in sentences.all_inner_texts():
                                if len(elem) > 15:
                                    phrase = elem.split('\n')[0].replace("’", "'") 
                                    if self.is_english(phrase) in ['en', 'cy']:
                                        self.set_setences(link, phrase)
                            
                            page.close()

                except Exception as exc:
                    self.stdout.write(
                        self.style.WARNING(f'playwright__erro: {exc}')
                    )

            page.close()

    def is_english(self, sentence):
        return detect(sentence)

    def set_setences(self, link, sentence):
        
        try:            
            obj, _ = Terms.objects.get_or_create(**{
                "text": sentence,
                "language": TypePartSpeechChoices.ENGLISH, 
            })

            if not Tags.objects.filter(term=tag_normalization(link)).exists():
                Tags.objects.create(**{
                    "term": f"{link}"
                })

            tag = Tags.objects.get(term=tag_normalization(link))
            obj.tags.add(tag)

        except Exception as exc:
            self.stdout.write(
                self.style.WARNING(f'set_setences__erro: {exc}')
            )