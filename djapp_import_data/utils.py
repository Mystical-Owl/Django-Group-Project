
### read csv files as python dictionary
from csv import DictReader

### import to use django auth framework
from django.contrib.auth.models import User

from numpy import vectorize

from config.settings import DEFAULT_DATA_ROOT

from questionaires.models import Questionaire
from questionaire_answers.models import QuestionaireAnswer

from investment_types.models import InvestmentType
from investment_choices.models import InvestmentChoice
from investment_datas.models import InvestmentData

from datetime import datetime
from django.utils import timezone

def clear_questionaire_answers ():
    '''
    Clear table questionaire_answers.
    Returns deleted record count.
    '''
    try:
        del_cnt, _ = QuestionaireAnswer.objects.all().delete()
        return del_cnt
    except Exception as e:
        print(e)
        return 0
# end def clear_questionaire_answers()

def clear_questionaires ():
    '''
    Clear table questionaires.
    Returns deleted record count.
    '''
    try:
        del_cnt, _ = Questionaire.objects.all().delete()
        return del_cnt
    except Exception as e:
        print(e)
        return 0
# end def clear_questionaires()

def import_questionaire_answers ():
    '''
    Import predefined questionaires and answers.
    '''
    # function to import questionaires and questionaire_answers
    ### predefined questionaires files:
    ###     IAAF_form_50_question.csv
    ###     LOT_50.csv
    ### test file:
    ###     sample_questionaires.csv


    ### set to True to output info in terminal
    DEBUG_FUNCTION = False

    def import_one_questionaire_answers (filename) :
        with open(
            DEFAULT_DATA_ROOT + '/' + filename,
            mode='r', 
            newline='', 
            encoding='utf-8'
        ) as csvfile:
            csv_reader = DictReader(csvfile)

            for row in csv_reader:
                # Each 'row' is a dictionary
                if DEBUG_FUNCTION:
                    print(row['question'])
                    print(row['questionaire_type'])
                    print(row['q_sort_order'])

                    print(row['answer'])
                    print(row['score'])
                    print(row['weight'])
                    print(row['ans_sort_order'])
                else:
                    q, created = Questionaire.objects.get_or_create(
                        questionaire_statement  = row['question'],
                        questionaire_type       = row['questionaire_type'],
                        sort_order              = int(row['q_sort_order'])
                    )

                    qa, created = QuestionaireAnswer.objects.get_or_create(
                        questionaire        = q,
                        questionaire_answer = row['answer'],
                        answer_score        = float(row['score']),
                        answer_weight       = float(row['weight']),
                        sort_order          = int(row['ans_sort_order'])
                    )
    # end def import_one_questionaire_answers()

    import_one_questionaire_answers('IAAF_form_50_question.csv')
    import_one_questionaire_answers('LOT_50.csv')
# end def import_questionaire_answers()

def import_default_users () :
    '''
    Creates default "regular" users for testing the website.
    '''

    @vectorize(cache=True)
    def create_one_user (username) :
        password    = '0';
        email       = '';
        first_name  = '';
        last_name   = '';

        ### cannot directly create user
        # # create user
        # user = User.objects.create_user(
        #     username    = username,
        #     password    = password,
        #     email       = email,
        #     first_name  = first_name,
        #     last_name   = last_name
        # )
        # user.save()
        ###
        ### use get_or_create()
        # get_or_create returns (object, created_boolean)
        user, created = User.objects.get_or_create(
            username = username,
            defaults = {
                'email'         : email,
                'first_name'    : first_name,
                'last_name'     : last_name,
                # Do not put password here directly, it won't be hashed
            }
        )

        if created:
            user.set_password(password)
            user.save()
    # end def create_one_user()

    usernames = [
        'andrew',
        'franco',
        'howard',
        'george',
    ]

    create_one_user(usernames)
# end def import_default_users()

def clear_investment_datas ():
    '''
    Clear table investment_datas.
    Returns deleted record count.
    '''
    try:
        del_cnt, _ = InvestmentData.objects.all().delete()
        return del_cnt
    except Exception as e:
        print(e)
        return 0
# end def clear_investment_datas()

def clear_investment_choices ():
    '''
    Clear table investment_choices.
    Returns deleted record count.
    '''
    try:
        del_cnt, _ = InvestmentChoice.objects.all().delete()
        return del_cnt
    except Exception as e:
        print(e)
        return 0
# end def clear_investment_choices()

def clear_investment_types ():
    '''
    Clear table investment_types.
    Returns deleted record count.
    '''
    try:
        del_cnt, _ = InvestmentType.objects.all().delete()
        return del_cnt
    except Exception as e:
        print(e)
        return 0
# end def clear_investment_types()

def import_investment_datas ():
    '''
    Import predefined questionaires and answers.
    '''
    # function to import investment_types, investment_choices and investment_datas
    ### predefined files:
    ###     funds_name_type_desc.csv
    ###     funds_daily_2015_to_2036.csv

    with open(
        DEFAULT_DATA_ROOT + '/' + 'funds_name_type_desc.csv',
        mode='r', 
        newline='', 
        encoding='utf-8'
    ) as csvfile:
        csv_reader = DictReader(csvfile)

        for row in csv_reader:
            i_type, _ = InvestmentType.objects.get_or_create(
                investment_type = row['type']
            )

            i_choice, _ = InvestmentChoice.objects.get_or_create(
                investment_name = row['name'],
                investment_type = i_type,
                investment_description = row['desc']
            )
        # end for
    # end with open()
    
    i_choice_A, _ = InvestmentChoice.objects.get_or_create(investment_name = 'Fund_A')
    i_choice_B, _ = InvestmentChoice.objects.get_or_create(investment_name = 'Fund_B')
    i_choice_C, _ = InvestmentChoice.objects.get_or_create(investment_name = 'Fund_C')
    i_choice_D, _ = InvestmentChoice.objects.get_or_create(investment_name = 'Fund_D')

    def create_one_investment_data (invesment_name, investment_choice, csv_row) :
        # Django expects all datetimes to have an associated timezone 
        # when USE_TZ is active to maintain consistency and prevent 
        # issues with time calculations.  Otherwise, there will be a
        # DateTimeField naive datetime RuntimeWarning.
        date_string = csv_row['Date']
        format_string = '%Y-%m-%d'
        # Convert the string to a datetime object
        naive_datetime_object = datetime.strptime(date_string, format_string)
        # Make the datetime timezone-aware before assigning it
        aware_datetime = timezone.make_aware(naive_datetime_object)
        i_data, created = InvestmentData.objects.get_or_create(
            investment_choice = investment_choice,
            investment_date = aware_datetime,
            investment_price = csv_row[invesment_name]
        )
        return i_data, created
    # end def create_one_investment_data()


    with open(
        DEFAULT_DATA_ROOT + '/' + 'funds_daily_2015_to_2036.csv',
        mode='r', 
        newline='', 
        encoding='utf-8'
    ) as csvfile:
        csv_reader = DictReader(csvfile)

        for row in csv_reader:
            create_one_investment_data('Fund_A', i_choice_A, row)
            create_one_investment_data('Fund_B', i_choice_B, row)
            create_one_investment_data('Fund_C', i_choice_C, row)
            create_one_investment_data('Fund_D', i_choice_D, row)
        # end for
    # end with open()
# end def import_investment_datas()
