import os
import uuid
import openai
from word.models import ShortText
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "OK"

    def add_arguments(self, parser):
        parser.add_argument("--tag", nargs="+", type=str)

    def handle(self, *args, **options): 

        # Substitua pela sua chave da API OpenAI
        api_key = os.environ.get("GPT_API_KEY")

        # Criar o cliente OpenAI
        client = openai.OpenAI(
            api_key=api_key
        )

        
        for elem in ShortText.objects.exclude(audio=None):
            response = client.audio.speech.create(
                model="tts-1",  # Modelo TTS da OpenAI
                voice="alloy",  # Voz disponível: alloy, echo, fable, onyx, nova, shimmer
                input=elem.text
            )

            audio_bytes = response.content
            elem.audio.save(f"{str(uuid.uuid4())}.mp3", ContentFile(audio_bytes))

            print("Áudio gerado com sucesso: output.mp3")
