from django.shortcuts import render
from django.shortcuts import redirect

from .choices import questionaire_types

from questionaires.models import Questionaire
from questionaire_answers.models import QuestionaireAnswer
from user_questionaire_answers.models import UserQuestionaireAnswer

from .utils import get_questionaires_and_questionaire_answers

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

    questionaires_and_questionaire_answers = get_questionaires_and_questionaire_answers(questionaire_type)

    context = {
        'questionaire_types'        : questionaire_types,
        'questionaires_and_questionaire_answers'  : questionaires_and_questionaire_answers,
    }

    return render(request, 'questionaires/questionaire.html', context)
# end def questionaire()

def save_uqa (request) :
    '''
    '''
    DEBUG_FUNCTION = False

    if DEBUG_FUNCTION:
        print('inside def save_uqa (request) ')

    if not request.user.is_authenticated:
        return redirect('/')

    if request.method != 'POST':
        return redirect('/')
    
    ## loop Questionaire for id
    ## check each id for answer
    ## save answer with user

    user = request.user

    if DEBUG_FUNCTION:
        print(f"{user.id = }")

    questionaires = Questionaire.objects.all()

    if DEBUG_FUNCTION:
        print('before for questionaire in questionaires:')

    for questionaire in questionaires:
        questionaire_answer_id = request.POST.get(str(questionaire.id))

        if questionaire_answer_id:
            # first delete other answers
            UserQuestionaireAnswer.objects.filter(
                user                = user,
                questionaire        = questionaire
            ).delete()

            UserQuestionaireAnswer.objects.filter(
                user                    = user,
                questionaire__isnull    = True
            ).delete()

            # save current answer
            questionaire_answer = QuestionaireAnswer.objects.filter(pk=questionaire_answer_id)[0]

            u, c = UserQuestionaireAnswer.objects.get_or_create(
                user                = user,
                questionaire        = questionaire,
                questionaire_answer = questionaire_answer
            )
            
            if DEBUG_FUNCTION:
                print(u.pk, u, c)

    if DEBUG_FUNCTION:
        print('after for questionaire in questionaires:')

    context = {
        'questionaire_types' : questionaire_types,
    }

    return redirect('questionaires:index')
# end def save()
