import html
import uuid
from gtts import gTTS
import pyttsx3
from memorization.utils import remove_tags_html
from word.models import ShortText
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "OK"

    def add_arguments(self, parser):
        parser.add_argument("--tag", nargs="+", type=str)

    def get_gtts(self, text_raw, audio_filename):
        tts = gTTS(text=text_raw, lang='en')
        tts.save(f"media/{audio_filename}")
    
    def get_tts_pyttsx3(self, text_raw, audio_filename):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'en-029' in voice.languages[0]:  # 'en' para inglês
                print(f"voice.languages: {voice.languages[0]}")
                engine.setProperty('voice', voice.id)
                engine.save_to_file(text_raw, f"media/{audio_filename}")
                engine.runAndWait()
                break
    
    def get_tts_elevenlabs(self, text_raw, audio_filename):
        from elevenlabs.client import ElevenLabs
        from elevenlabs import play, save, stream, Voice, VoiceSettings
        
        api_key = "sk_5c9a49a3124397539d7369b685f66020fecd3734727a1e44"
        client = ElevenLabs(api_key=api_key)
        audio = client.generate(
            text=text_raw,
            voice="Brian"
        )
        save(audio, f"media/{audio_filename}")

    def handle(self, *args, **options): 
        for elem in ShortText.objects.exclude(has_audio=True):
        # for elem in ShortText.objects.all():          
            text_raw = html.unescape(remove_tags_html(elem.text.strip()))            
            audio_filename = f"{str(uuid.uuid4())}.mp3"
            # self.get_gtts(text_raw, audio_filename)
            # self.get_tts_pyttsx3(text_raw, audio_filename)
            self.get_tts_elevenlabs(text_raw, audio_filename)
            
            elem.audio = audio_filename
            elem.has_audio = True
            elem.save()
