from questionaires.models import Questionaire
from user_questionaire_answers.models import UserQuestionaireAnswer

from questionaires.choices import questionaire_types

def is_user_finished_questionaire (user, questionaire_type) :
    '''
    Returns True if user has finished all questions in
    the given questionaire_type.
    '''
    questionaire_count = Questionaire.objects.filter(
        questionaire_type = questionaire_type
    ).count()

    user_questionaire_count = UserQuestionaireAnswer.objects.filter(
        user = user,
        questionaire__questionaire_type = questionaire_type
    ).count()

    if questionaire_count == user_questionaire_count :
        return True
    else:
        return False
# end def is_user_finished_questionaire ()

def is_user_finished_all_questionaires (user) :
    '''
    Returns True if user has finished all questionaires.
    '''
    user_finished_questionaire_count = 0

    for questionaire_type in questionaire_types.keys():
        user_finished_questionaire_count += is_user_finished_questionaire(user, questionaire_type)
    
    return user_finished_questionaire_count == len(questionaire_types)
# end def is_user_finished_questionaires ()
