from django.shortcuts import render

from investment_choices.models import InvestmentChoice


# Create your views here.

def index (request) :
    '''
    '''
    return render(request, 'user_investments/index.html', context)
# end def index()

def choices (request) :
    '''
    '''
    investment_choices = InvestmentChoice.objects.all()

    context = {
        'investment_choices' : investment_choices,
    }

    return render(request, 'user_investments/choices.html', context)
# end def choices()

def save (request) :
    '''
    '''
    return render(request, 'user_investments/index.html', context)
# end def save()
