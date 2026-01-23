from django.shortcuts import render
from django.shortcuts import redirect

from investment_choices.models import InvestmentChoice

from user_investments.models import UserInvestment

from user_investments.utils import make_aware_datetime
from user_investments.utils import make_aware_the_next_day
from user_investments.utils import make_aware_today
from user_investments.utils import make_aware_tomorrow

### import to use django messages framework
from django.contrib import messages

from datetime import date
from config.settings import DATE_STRING_FORMAT

# Create your views here.

def index (request) :
    '''
    '''
    
    if not request.user.is_authenticated:
        return redirect('/')

    user_investment_names = UserInvestment.objects.values_list(
        'user_investment_name', 
        flat=True
    ).distinct().order_by('user_investment_name')

    context = {
        'user_investment_names' : user_investment_names
    }
    return render(request, 'user_investments/index.html', context)
# end def index()

def show (request) :
    '''
    '''
    
    if not request.user.is_authenticated:
        return redirect('/')

    if request.method != "POST":
        return choices(request)
    
    user_investment_name = request.POST.get('user_investment_name')

    print(f"{user_investment_name = }")

    user_investments = UserInvestment.objects.filter(
        user_investment_name = user_investment_name
    )

    context = {
        'user_investments' : user_investments
    }

    return render(request, 'user_investments/show.html', context)
# end def index()

def choices (request) :
    '''
    '''

    if not request.user.is_authenticated:
        return redirect('/')

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
    
    if not request.user.is_authenticated:
        return redirect('/')

    if request.method != "POST":
        return choices(request)

    choose_date = request.POST.get('choose_date')

    if not choose_date:
        choose_date = date.today().strftime(DATE_STRING_FORMAT)

    total_amount = request.POST.get('total_amount')

    # no amount input
    if not total_amount:
        ## add alert message
        messages.error(request, 'Please input correct amount.')
    else:
        try:
            # if user input is not a number, goto exception
            total_amount = float(total_amount)
        except Exception as e:
            messages.error(request, 'Please input correct amount.')
            if request.user.username == 'admin':
                messages.error(request, 'e = ' + str(e))


    investment_choices = InvestmentChoice.objects.all()

    inv_names = []
    inv_values = []
    inv_name_val_dict = {}

    for investment_choice in investment_choices:
        inv_name = investment_choice.investment_name

        # default to 0% if not chosen from html
        inv_value = request.POST.get(inv_name, '0')

        # store values for context
        inv_names.append(inv_name)
        inv_values.append(inv_value)
        inv_name_val_dict[inv_name] = inv_value

        # inv_value is percentage
        investment_amount = float(total_amount) * float(inv_value) / 100

        db_choose_date = make_aware_datetime(choose_date)

        db_end_date = db_choose_date
        db_end_date_str = db_end_date.strftime(DATE_STRING_FORMAT)

        # check if user has previous investments
        updated_row_count = UserInvestment.objects.filter(
            user = request.user,
            investment_choice = investment_choice
        ).update(
            end_date = db_end_date,
            end_date_str = db_end_date_str
        )

        if updated_row_count == 0:
            db_start_date = db_choose_date
        else:
            db_start_date = make_aware_the_next_day(choose_date)

        db_start_date_str = db_start_date.strftime(DATE_STRING_FORMAT)

        user_investment_name = db_start_date.strftime(DATE_STRING_FORMAT)

        # save to database
        UserInvestment.objects.get_or_create(
            user                    = request.user,
            investment_choice       = investment_choice,
            user_investment_name    = user_investment_name,  # string
            begin_date              = db_start_date,
            investment_amount       = investment_amount,
            investment_total_amount = float(total_amount),
            begin_date_str          = db_start_date_str,
            end_date_str            = '',
        )

    # print (f"{inv_name_val_dict = }")

    messages.success(request, 'Investment choices saved successfully.')

    context = {
        'investment_choices' : investment_choices,
        'total_amount' : total_amount,
        'inv_names' : inv_names,
        'inv_values' : inv_values,
        'inv_name_val_dict' : inv_name_val_dict,
        'choose_date' : choose_date,
    }

    return render(request, 'user_investments/choices.html', context)
# end def save()
