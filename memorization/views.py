import html
import random
from django.shortcuts import render
from word.models import ShortText

def meu_formulario(request):
    if request.method == "POST":
        print(request.POST)
        words = request.POST.get("cards")
        instance_id = request.POST.get("instance_id")
        result = "".join(words)
        if ShortText.objects.filter(id=instance_id).exists():
            print("Instancia encontrada")
            if result in ShortText.objects.get(id=instance_id).text:
                print("Textos compatíveis")
                ShortText.objects.filter(id=instance_id).update(completed=True)
            else:
                print("Textos não compatíveis")

    instances = ShortText.objects.exclude(completed=True)
    num = random.randint(1, instances.count()-1)   
    elem = instances[num]
    scrambled_text = [html.unescape(item.strip()) for item in elem.scrambled_text.split(" ")]
    context = {
        'instance_id': elem.id,
        'audio': elem.audio,
        'scrambled_text': scrambled_text,
        'translate': elem.translate
    }
    return render(request, 'formulario.html', context)
