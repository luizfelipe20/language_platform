import os
import html
import openai
from time import sleep
from word.models import ShortText
from memorization.utils import remove_tags_html
from django.core.management.base import BaseCommand

openai.api_key = os.environ.get("GPT_API_KEY")


class Command(BaseCommand):
    help = "OK"

    def add_arguments(self, parser):
        parser.add_argument("--tag", nargs="+", type=str)

    def handle(self, *args, **options): 
        for elem in ShortText.objects.exclude(has_translate=True):
            _text = remove_tags_html(html.unescape(elem.text))
            request = f"Traduza o texto a seguir para portugues do Brazil: {_text}"
            _translate = self.sentence_generator(request)
            elem.translate = _translate
            elem.has_translate = True
            elem.save()

    def query_api(self, messages):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=messages
        )
        return response.choices[0].message.content

    def sentence_generator(self, question):
        mensagens = [{"role": "user", "content": "you are an english teacher"}]
        mensagens.append({"role": "user", "content": question})
        try:
            answer = self.query_api(mensagens)
            return answer
        except Exception as exc:
            print(f"openai exception: {exc}")

            sleep(3)

            self.sentence_generator(question)