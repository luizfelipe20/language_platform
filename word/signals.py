import os
import uuid
import openai
import random
from django.db import models
from .models import ShortText
from memorization.utils import remove_tags_html
from django.core.files.base import ContentFile
from django.dispatch import receiver


def shuffle_text(text):
    text = remove_tags_html(text)
    words_list = text.split(" ")
    random.shuffle(words_list)  # Embaralha a lista
    return " ".join(words_list)  # Junta os caracteres de volta


def generate_audio(instance):
    api_key = os.environ.get("GPT_API_KEY")
    client = openai.OpenAI(
        api_key=api_key
    )
        
    response = client.audio.speech.create(
        model="tts-1",  # Modelo TTS da OpenAI
        voice="alloy",  # Voz disponível: alloy, echo, fable, onyx, nova, shimmer
        input=instance.text
    )

    audio_bytes = response.content
    instance.audio.save(f"{str(uuid.uuid4())}.mp3", ContentFile(audio_bytes))
    print("Áudio gerado com sucesso: output.mp3")


@receiver(models.signals.post_save, sender=ShortText)
def post_save_short_texts(sender, instance, created, **kwargs):
    scrambled_text = shuffle_text(instance.text)
    ShortText.objects.filter(id=instance.id).update(scrambled_text=scrambled_text)
    # generate_audio(instance=instance)
