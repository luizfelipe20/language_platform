import html
import random
from memorization.models import Challenge
from word.models import ShortText, Term, Translation, HistoryAttempt
from django.shortcuts import render
from django.db.models import Count, Q
from memorization.utils import remove_tags_html


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
        challenge = Challenge.objects.filter(is_active=True).last()
                
        successful_attempts = Term.objects.annotate(
            num_historyattempt=Count('historyattempt'), filter=Q(historyattempt__got_it_right=True)
            ).filter( 
            num_historyattempt__gte=challenge.number_of_correct_answers
        )

        options = Term.objects.filter(tags__in=challenge.tags.all()).exclude(id__in=successful_attempts)
        if not options.count():
            context = {
                'color': 'text-green',
                'message': 'Test completed successfully.!!!!'
            }
            return render(request, 'result_form.html', context)
        
        num = random.randint(0, options.count()-1)   
        elem = options[num]
        translations = list(elem.translation_set.all().values('id', 'term').order_by('?'))
        context = {
            'instance_id': elem.id,
            'sentence': elem.text,
            'options': translations
        }
    return render(request, 'template_proof.html', context)
