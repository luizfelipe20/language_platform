import re
import json
from django.core.management.base import BaseCommand
from memorization.gpt_api import sentence_generator
from word.models import Tag, Term, Option, ShortText, TypePartSpeechChoices


class Command(BaseCommand):
    help = "OK"

    def handle(self, *args, **options): 
        with open('./memorization/management/commands/short_text.txt', 'r') as file:
            short_text = file.read()
            _request_gpt = f"""
            {short_text}
            Based on the text above, generate twenty multiple-choice questions where only one option is correct, 
            and return the result in JSON format, The JSON file must contain the keys: "question", "options", "correct_answer".
            """
            
            tag_obj, _ = Tag.objects.get_or_create(term="short_text_2")
            
            short_text_obj, _ = ShortText.objects.get_or_create(text=short_text)
            short_text_obj.tags.add(tag_obj)
            
            _result_gpt = sentence_generator(_request_gpt)
            json_str = re.search(r'\{.*\}', _result_gpt, re.DOTALL).group()
            elems = json.loads(json_str)['questions']
            for obj_chat_gpt in elems:
                sentence_obj, _ = Term.objects.get_or_create(**{
                    "text": obj_chat_gpt['question'],
                    "reference": short_text_obj,
                    "language": TypePartSpeechChoices.ENGLISH, 
                })
                sentence_obj.tags.add(tag_obj)
                for option in obj_chat_gpt['options']:
                    Option.objects.get_or_create(**{
                        "term": option,
                        "right_option": option in obj_chat_gpt['correct_answer'],
                        "reference": sentence_obj,
                        "language": TypePartSpeechChoices.PORTUGUESE, 
                    })