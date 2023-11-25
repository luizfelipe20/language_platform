from gtts import gTTS
from deep_translator import GoogleTranslator


def generate_audio(writing, _id):
    language = 'en'
    result = gTTS(text=writing, lang=language, slow=False)
    result.save(f"./word/audios/{_id}.mp3")
    return f"./word/audios/{_id}.mp3"


def generate_translations(writing):
    translated = GoogleTranslator(source="auto", target="pt").translate(text=writing)
    return str(translated).lower()


def tag_normalization(term: str):
    return term.lower().replace(" ", "_").replace("/", "_")


def sentence_normalization(sentence: str):
    return sentence.strip().replace("<p>&nbsp;</p>","")