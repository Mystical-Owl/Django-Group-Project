from django.shortcuts import render
from django.shortcuts import redirect

from .choices import questionaire_types

from questionaires.models import Questionaire
from questionaire_answers.models import QuestionaireAnswer
from user_questionaire_answers.models import UserQuestionaireAnswer

from .utils import get_questionaire_and_answers

# Create your views here.

def index (request) :
    print('def index (request) :')
    if not request.user.is_authenticated:
        return redirect('/')

    context = {
        'questionaire_types' : questionaire_types,
    }
    return render(request, 'questionaires/index.html', context)
# end def index()

def questionaire (request, questionaire_type) :
    print('inside def questionaire (request, questionaire_type) ')
    if not request.user.is_authenticated:
        return redirect('/')

    questionaire_and_answers = get_questionaire_and_answers(questionaire_type)

    context = {
        'questionaire_types'        : questionaire_types,
        'questionaire_and_answers'  : questionaire_and_answers[:2],
    }
    return render(request, 'questionaires/questionaire.html', context)
# end def questionaire()

def save_uqa (request) :
    print('inside def save_uqa (request) ')

    if not request.user.is_authenticated:
        return redirect('/')

    if request.method != 'POST':
        return redirect('/')
    
    ## loop Questionaire for id
    ## check each id for answer
    ## save answer with user

    user = request.user

    print(f"{user.id = }")

    questionaires = Questionaire.objects.all()

    print('before for questionaire in questionaires:')

    for questionaire in questionaires:
        questionaire_answer_id = request.POST.get(str(questionaire.id))
        if questionaire_answer_id:
            questionaire_answer = QuestionaireAnswer.objects.filter(pk=questionaire_answer_id)[0]
            u, c = UserQuestionaireAnswer.objects.get_or_create(
                user=user,
                questionaire_answer=questionaire_answer
            )

            print(u, c)

    print('after for questionaire in questionaires:')

    context = {
        'questionaire_types' : questionaire_types,
    }
    return redirect('questionaires:index')
# end def save()
