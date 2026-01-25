import re
import uuid
from typing import List
from django.core.management.base import BaseCommand


def split_text_into_paragraphs(text, max_chars=2000):
    paragraphs = []
    current_paragraph = ""

    for word in text.split():
        # Verifica se adicionar a palavra ultrapassa o limite
        if len(current_paragraph) + len(word) + 1 <= max_chars:
            current_paragraph += (" " + word) if current_paragraph else word
        else:
            paragraphs.append(current_paragraph)
            current_paragraph = word

    if current_paragraph:
        paragraphs.append(current_paragraph)

    return paragraphs


def write_to_file(content: str, filename: str) -> None:
    """Write formatted text to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
 

class Command(BaseCommand):
    help = "OK"
        
    def handle(self, *args, **options): 
        with open('./memorization/management/commands/short_text.txt', 'r') as file:
            raw_text = file.read()
            paragraphs = split_text_into_paragraphs(raw_text)
            token = str(uuid.uuid4())
            with open(f"text_{token}.txt", "w", encoding="utf-8") as f:
                for p in paragraphs:
                    f.write(p + "\n\n")



