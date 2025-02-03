import os
import openai
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "OK"

    def add_arguments(self, parser):
        parser.add_argument("--tag", nargs="+", type=str)

    def handle(self, *args, **options): 

        # Configure sua chave da OpenAI
        openai.api_key = os.environ.get("GPT_API_KEY")

        # Texto a ser convertido em áudio
        texto = "Olá, este é um exemplo de áudio gerado com a API da OpenAI."

        # Geração de áudio
        response = openai.audio.speech.create(
            model="tts-1",  # Modelo de conversão de texto para fala
            voice="alloy",  # Voz disponível: alloy, echo, fable, onyx, nova, shimmer
            input=texto
        )

        # Salvando o áudio em um arquivo
        with open("output.mp3", "wb") as f:
            f.write(response.content)

        print("Áudio gerado com sucesso: output.mp3")

