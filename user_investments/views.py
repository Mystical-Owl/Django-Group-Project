from django.shortcuts import render
from django.shortcuts import redirect

from investment_choices.models import InvestmentChoice

### import to use django messages framework
from django.contrib import messages

from datetime import date

# Create your views here.

def index (request) :
    '''
    '''
    return choices(request)

    # context = {
        
    # }
    # return render(request, 'user_investments/index.html', context)
# end def index()

def choices (request) :
    '''
    '''
    investment_choices = InvestmentChoice.objects.all()

    choose_date = date.today().strftime("%Y-%m-%d")

    context = {
        'investment_choices' : investment_choices,
        'choose_date' : choose_date,
    }

    return render(request, 'user_investments/choices.html', context)
# end def choices()

def save (request) :
    '''
    '''
    if request.method != "POST":
        return choices(request)

    choose_date = request.POST.get('choose_date')

    if not choose_date:
        choose_date = date.today().strftime("%Y-%m-%d")

    amount = request.POST.get('amount')

    # no amount input
    if not amount:
        ## add alert message
        messages.error(request, 'Please input correct amount.')
    else:
        try:
            # if user input is not a number, goto exception
            amount = float(amount)
        except Exception as e:
            messages.error(request, 'Please input correct amount.')

    investment_choices = InvestmentChoice.objects.all()

    inv_names = []
    inv_values = []
    inv_name_val_dict = {}

    for investment_choice in investment_choices:
        inv_name = investment_choice.investment_name
        inv_value = request.POST.get(inv_name)

        inv_names.append(inv_name)
        inv_values.append(inv_value)
        inv_name_val_dict[inv_name] = inv_value


    print (f"{inv_name_val_dict = }")

    context = {
        'investment_choices' : investment_choices,
        'amount' : amount,
        'inv_names' : inv_names,
        'inv_values' : inv_values,
        'inv_name_val_dict' : inv_name_val_dict,
        'choose_date' : choose_date,
    }

    return render(request, 'user_investments/choices.html', context)
# end def save()
