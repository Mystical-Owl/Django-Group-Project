from django.shortcuts import render
from django.shortcuts import redirect

from .choices import questionaire_types

from questionaires.models import Questionaire
from questionaire_answers.models import QuestionaireAnswer

from .utils import get_questionaire_and_answers

# Create your views here.

def index (request) :
    if not request.user.is_authenticated:
        return redirect('/')

    context = {
        'questionaire_types' : questionaire_types,
    }
    return render(request, 'questionaires/index.html', context)
# end def index()

def questionaire (request, questionaire_type) :
    if not request.user.is_authenticated:
        return redirect('/')

    questionaire_and_answers = get_questionaire_and_answers(questionaire_type)

    context = {
        'questionaire_types'        : questionaire_types,
        'questionaire_and_answers'  : questionaire_and_answers,
    }
    return render(request, 'questionaires/questionaire.html', context)
# end def questionaire()

def save (request) :
    if not request.user.is_authenticated:
        return redirect('/')

    context = {
        'questionaire_types' : questionaire_types,
    }
    return render(request, 'questionaires/index.html', context)
# end def save()
