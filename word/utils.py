from gtts import gTTS
from deep_translator import GoogleTranslator


def generate_audio(writing, _id):
    language = 'en'
    result = gTTS(text=writing, lang=language, slow=False)
    result.save(f"./word/audios/{_id}.mp3")
    return f"./word/audios/{_id}.mp3"


def generate_translations(writing):
    translated = GoogleTranslator(source="auto", target="pt").translate(text=writing)
    return translated