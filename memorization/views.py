import html
import random
from memorization.models import Challenge
from word.models import ShortText, Term, Translation, HistoryAttempt
from django.shortcuts import render
from django.db.models import Count, Q
from memorization.utils import remove_tags_html


def meu_formulario(request):
    if request.method == "POST":
        print(request.POST)
        words = request.POST.get("cards")
        instance_id = request.POST.get("instance_id")
        result = "".join(words)
        if ShortText.objects.filter(id=instance_id).exists():
            instance_text = remove_tags_html(html.unescape(ShortText.objects.get(id=instance_id).text)) 

            if result in instance_text:
                context = {
                    'translate': ShortText.objects.get(id=instance_id).translate,
                }
                ShortText.objects.filter(id=instance_id).update(completed=True)
                return render(request, 'success_form.html', context)
            else:
                context = {
                    'success': instance_text,
                    'error': result
                }
                return render(request, 'error_form.html', context)

    instances = ShortText.objects.exclude(completed=True)
    num = random.randint(0, instances.count()-1)   
    elem = instances[num]
    scrambled_text = [html.unescape(item.strip()) for item in elem.scrambled_text.split(" ")]
    context = {
        'instance_id': elem.id,
        'audio': elem.audio,
        'scrambled_text': scrambled_text,
        'translate': elem.translate
    }
    return render(request, 'form.html', context)


def vocabulary_test(request):
    if request.method == 'POST': 
        instance_id = request.POST.get("instance_id")
        instance = Term.objects.get(id=instance_id)            
        answer_option_form = request.POST.get('answer_option')
        answer_option = instance.translation_set.filter(right_option=True).last()
        got_it_right = str(answer_option.id) == answer_option_form

        HistoryAttempt.objects.create(**{
            "reference": instance,
            "got_it_right": got_it_right
        })

        message = 'Wrong answer!!!'
        color = 'text-red'
        if got_it_right:
            message = 'Correct answer!!!'
            color = 'text-green'

        context = {
            'color': color,
            'message': message
        }
        return render(request, 'result_form.html', context)
    else:
        _qtd_correct_answers = Challenge.objects.filter(is_active=True).last().number_of_correct_answers
        
        instances = Term.objects.annotate(
            num_historyattempt=Count('historyattempt'), filter=Q(historyattempt__got_it_right=True)
            ).filter( 
            num_historyattempt__gte=_qtd_correct_answers
        )

        instances = Term.objects.exclude(id__in=instances)
        num = random.randint(0, instances.count()-1)   
        elem = instances[num]
        translations = list(elem.translation_set.all().values('id', 'term').order_by('?'))
        context = {
            'instance_id': elem.id,
            'sentence': elem.text,
            'options': translations
        }
    return render(request, 'template_proof.html', context)
