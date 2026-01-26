from datetime import datetime
from django.utils import timezone
from datetime import date
from datetime import timedelta
from config.settings import DATE_STRING_FORMAT

from investment_datas.models import InvestmentData


def make_aware_datetime (date_string) :
    '''
    Django expects all datetimes to have an associated timezone 
    when USE_TZ is active to maintain consistency and prevent 
    issues with time calculations.  Otherwise, there will be a
    DateTimeField naive datetime RuntimeWarning.
    '''

    # format used in this project
    format_string = DATE_STRING_FORMAT

    # Convert the string to a datetime object
    naive_datetime_object = datetime.strptime(date_string, format_string)

    # Make the datetime timezone-aware before assigning it
    aware_datetime = timezone.make_aware(naive_datetime_object)

    return aware_datetime
# end def make_aware_datetime()

def make_aware_today () :

    # Make the datetime timezone-aware before assigning it
    aware_datetime = timezone.make_aware(date.today())

    return aware_datetime
# end def make_aware_today()

def make_aware_tomorrow () :

    today = date.today()

    # Calculate tomorrow's date by adding one day
    tomorrow = today + timedelta(days=1)

    # Make the datetime timezone-aware before assigning it
    aware_datetime = timezone.make_aware(tomorrow)

    return aware_datetime
# end def make_aware_tomorrow()

def make_aware_the_next_day (date_string) :

    current_date = make_aware_datetime(date_string)

    # Calculate tomorrow's date by adding one day
    the_next_day = current_date + timedelta(days=1)

    return the_next_day
# end def make_aware_tomorrow()

def calc_end_inv_amount (user_investment, end_date=None):
    '''
    Returns amount at user_investment.end_date
    or param end_date
    or system current date
    '''

    begin_date = user_investment.begin_date

    begin_investment_data = InvestmentData.objects.filter(
        investment_choice   = user_investment.investment_choice,
        investment_date     = begin_date
    )[0]

    begin_inv_price = begin_investment_data.investment_price

    inv_end_date = user_investment.end_date

    if not inv_end_date:
        inv_end_date = end_date

    if not inv_end_date:
        inv_end_date = date.today()

    end_investment_datas = InvestmentData.objects.filter(
        investment_choice   = user_investment.investment_choice,
        investment_date     = inv_end_date
    )

    if end_investment_datas.count():
        end_investment_data = end_investment_datas[0]

        end_inv_price = end_investment_data.investment_price

        begin_inv_amount = user_investment.investment_amount

        end_inv_amount = begin_inv_amount * begin_inv_price / end_inv_price
    else:
        end_inv_amount = 0

    return end_inv_amount
# end def calc_end_amount()
