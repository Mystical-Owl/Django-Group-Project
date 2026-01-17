import csv

### import to use django auth framework
from django.contrib.auth.models import User

from numpy import vectorize

from config.settings import DEFAULT_DATA_ROOT

from questionaires.models import Questionaire
from questionaire_answers.models import QuestionaireAnswer


# function to import questionaires and questionaire_answers
def import_questionaire_answers ():
    '''
    Import predefined questionaires and answers.
    '''
    
    ### set to True to output info in terminal
    DEBUG_FUNCTION = False

    with open(
        DEFAULT_DATA_ROOT + '/sample_questionaires.csv',
        mode='r', 
        newline='', 
        encoding='utf-8'
    ) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        "question",
        "questionaire_type",
        "sort_order",
        "answer",
        "score",
        "weight",
        "ans_sort_order"

        for row in csv_reader:
            # Each 'row' is a dictionary
            if DEBUG_FUNCTION:
                print(row['question'])
                print(row['questionaire_type'])
                print(row['sort_order'])

                print(row['answer'])
                print(row['score'])
                print(row['weight'])
                print(row['ans_sort_order'])
            else:
                q, created = Questionaire.objects.get_or_create(
                    questionaire_statement  = row['question'],
                    questionaire_type       = row['questionaire_type'],
                    sort_order              = int(row['sort_order'])
                )

                qa, created = QuestionaireAnswer.objects.get_or_create(
                    questionaire        = q,
                    questionaire_answer = row['answer'],
                    answer_score        = float(row['score']),
                    answer_weight       = float(row['weight']),
                    sort_order          = int(row['ans_sort_order'])
                )   
                
    ### end def import_questionaire_answers()

def import_default_users () :
    '''
    Creates default "regular" users for testing the website.
    '''
    usernames = [
        'andrew',
        'franco',
        'howard',
        'george',
    ]
    create_one_user(usernames)

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
        username=username,
        defaults={
            'email'         : email,
            'first_name'    : first_name,
            'last_name'     : last_name,
            # Do not put password here directly, it won't be hashed
        }
    )

    if created:
        user.set_password(password)
        user.save()
