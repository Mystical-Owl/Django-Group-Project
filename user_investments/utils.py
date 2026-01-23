

from datetime import datetime
from django.utils import timezone

def make_aware_datetime (date_string) :
    '''
    Django expects all datetimes to have an associated timezone 
    when USE_TZ is active to maintain consistency and prevent 
    issues with time calculations.  Otherwise, there will be a
    DateTimeField naive datetime RuntimeWarning.
    '''
    format_string = '%Y-%m-%d'
    # Convert the string to a datetime object
    naive_datetime_object = datetime.strptime(date_string, format_string)
    # Make the datetime timezone-aware before assigning it
    aware_datetime = timezone.make_aware(naive_datetime_object)

    return aware_datetime
# end def make_aware_datetime()
