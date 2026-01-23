from datetime import datetime
from django.utils import timezone
from datetime import date
from datetime import timedelta
from config.settings import DATE_STRING_FORMAT

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

