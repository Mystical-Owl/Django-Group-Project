from django.shortcuts import render
from django.shortcuts import redirect

from investment_choices.models import InvestmentChoice


# Create your views here.

def index (request) :
    '''
    '''
    context = {
        
    }
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
    if request.method != "POST":
        return redirect('user_investment:index')

    investment_choices = InvestmentChoice.objects.all()

    for investment_choice in investment_choices:
        inv_name = investment_choice.investment_name

        inv_value = request.POST.get(inv_name)

    context = {

    }
    return render(request, 'user_investments/save.html', context)
# end def save()
