from django.shortcuts import render
from django.shortcuts import redirect

from investment_types.models import InvestmentType
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

from user_questionaire_answers.utils import is_user_finished_all_questionaires

from user_questionaire_answers.utils import user_questionaire_score

from questionaires.utils import get_sum_questionaires_total_min_max_score

from math import floor as math_floor

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
        'user_investment_names' : user_investment_names,
        'is_user_finished_all_questionaires' : is_user_finished_all_questionaires(request.user),
    }
    return render(request, 'user_investments/index.html', context)
# end def index()

def show (request) :
    '''
    '''
    DEBUG_FUNCTION = False
    
    if not request.user.is_authenticated:
        return redirect('/')

    if request.method != "POST":
        return choices(request)
    
    user_investment_name = request.POST.get('user_investment_name')

    if DEBUG_FUNCTION:
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
    List all choices.
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
    Save and go back to choices with saved values.
    '''
    DEBUG_FUNCTION = True
    
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
                messages.error(request, 'Exception == ' + str(e))


    investment_choices = InvestmentChoice.objects.all()

    # inv_names = []
    # inv_values = []
    inv_name_val_dict = {}

    for investment_choice in investment_choices:
        inv_name = investment_choice.investment_name

        # default to 0% if not chosen from html
        inv_value = request.POST.get(inv_name, '0')

        # store values for context
        # inv_names.append(inv_name)
        # inv_values.append(inv_value)
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

    if DEBUG_FUNCTION:
        print (f"user_investments.views.save() {inv_name_val_dict = }")

    messages.success(request, 'Investment choices saved successfully.')

    context = {
        'investment_choices'    : investment_choices,
        'total_amount'          : total_amount,
        # 'inv_names'             : inv_names,
        # 'inv_values'            : inv_values,
        'inv_name_val_dict'     : inv_name_val_dict,
        'choose_date'           : choose_date,
    }

    return render(request, 'user_investments/choices.html', context)
# end def save()

def ai_investment_choices (request) :
    '''
    User must complete questionnaires before coming here.
    '''
    DEBUG_FUNCTION = True
    
    if not request.user.is_authenticated:
        return redirect('/')

    if request.method != "POST":
        return choices(request)

    choose_date = request.POST.get('choose_date')

    if not choose_date:
        choose_date = date.today().strftime(DATE_STRING_FORMAT)

    total_amount = request.POST.get('total_amount')

    if not total_amount:
        total_amount = ''

    # ai limit investment choices

    user_questionaires_score = user_questionaire_score(request.user)

    ## need to normalize to total min/max score

    total_min_score, total_max_score = get_sum_questionaires_total_min_max_score()

    def normalize_score (user_score, min_score, max_score, map_min_score, map_max_score):
        n = (user_score - min_score) / (max_score - min_score)
        n_map = n * (map_max_score - map_min_score) + map_min_score
        return n_map

    normalized_user_questionaires_score = normalize_score(
        user_questionaires_score, 
        total_min_score,
        total_max_score,
        0,
        10,
    )

    investment_types = InvestmentType.objects.filter(
        investment_score_range_start__lte = normalized_user_questionaires_score,
        investment_score_range_end__gte = normalized_user_questionaires_score
    )

    investment_choices = InvestmentChoice.objects.filter(
        investment_type__in = investment_types
    )

    if DEBUG_FUNCTION:
        print(f"{user_questionaires_score = }")
        print(f"{total_max_score = }")
        print(f"{total_max_score = }")
        print(f"{normalized_user_questionaires_score = }")
        print(f"{investment_types.count() = }")
        print(f"{investment_choices.count() = }")

    def floor_to_tens (n):
        return int(math_floor(n / 10) * 10)

    # inv_names = []
    # inv_values = []
    inv_name_val_dict = {}

    # set to same inv_value
    # use average
    if investment_choices.count() != 0:
        inv_value = floor_to_tens(100 / investment_choices.count())
    else:
        inv_value = 0

    ### need to store string value into dictioinary for template html to use
    inv_value = str(inv_value)

    for investment_choice in investment_choices:
        inv_name = investment_choice.investment_name

        # store values for context
        # inv_names.append(inv_name)
        # inv_values.append(inv_value)
        inv_name_val_dict[inv_name] = inv_value

    if DEBUG_FUNCTION:
        print (f"user_investments.views.ai_investment_choices() {inv_name_val_dict = }")

    context = {
        'investment_choices'    : investment_choices,
        'total_amount'          : total_amount,
        # 'inv_names'             : inv_names,
        # 'inv_values'            : inv_values,
        'inv_name_val_dict'     : inv_name_val_dict,
        'choose_date'           : choose_date,
    }

    return render(request, 'user_investments/choices.html', context)
# end def ai_investment_choices()
