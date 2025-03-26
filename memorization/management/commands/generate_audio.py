import html
import uuid
from gtts import gTTS
from TTS.api import TTS
from memorization.utils import remove_tags_html
from word.models import ShortText
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "OK"

    def add_arguments(self, parser):
        parser.add_argument("--tag", nargs="+", type=str)

    def get_gtts(self, text_raw):
        tts = gTTS(text=text_raw, lang='en')
        audio_filename = f"{str(uuid.uuid4())}.mp3"
        tts.save(f"media/{audio_filename}")
    
    def get_tts():
        tts = TTS(model_name="tts_models/pt-br/fast_speech2", gpu=False)
        texto = "Olá, esse é um exemplo de áudio gerado a partir de texto usando o Coqui TTS."
        tts.tts_to_file(text=texto, file_path="audio.wav")

    def handle(self, *args, **options): 
        
        for elem in ShortText.objects.exclude(has_audio=True):          
            text_raw = html.unescape(remove_tags_html(elem.text.strip()))
            print(f"text_raw: {text_raw}") 
            tts = gTTS(text=text_raw, lang='en')
            audio_filename = f"{str(uuid.uuid4())}.mp3"
            tts.save(f"media/{audio_filename}")
            elem.audio = audio_filename
            elem.has_audio = True
            elem.save()
