
from questionaires.models import Questionaire
from questionaire_answers.models import QuestionaireAnswer

from questionaires.choices import questionaire_types


class QuestionairesAndQuestionaireAnswers () :
    def __init__ (self, questionaire, questionaire_answers) :
        self.questionaire = questionaire
        self.questionaire_answers = questionaire_answers
# end class QuestionairesAndQuestionaireAnswers()

def get_questionaires_and_questionaire_answers (questionaire_type):
    '''
    Returns python list of QuestionairesAndQuestionaireAnswers objects.
    '''
    questionaires_and_questionaire_answers = []

    questionaires = Questionaire.objects.filter(
        questionaire_type = questionaire_type
    ).order_by(
        'sort_order'
    )

    for questionaire in questionaires:
        questionaire_answers = QuestionaireAnswer.objects.filter(
            questionaire = questionaire
        ).order_by(
            'sort_order'
        )

        questionaires_and_questionaire_answers.append(
            QuestionairesAndQuestionaireAnswers(
                questionaire,
                questionaire_answers
            )
        )
    
    return questionaires_and_questionaire_answers
# end def get_questionaire_answers()

def update_all_questionaires_min_max_score ():
    '''
    Returns update record count.
    '''
    count = 0
    for questionaire_type in questionaire_types:
        count += update_questionaires_min_max_score(questionaire_type)
    return count
# end def update_all_questionaires_min_max_score()

def update_questionaires_min_max_score (questionaire_type):
    '''
    Returns update record count.
    '''
    count = 0

    total_min_score = 0
    total_max_score = 0

    questionaires = Questionaire.objects.filter(
        questionaire_type = questionaire_type
    )

    # go through all questions in questionaire_type
    for questionaire in questionaires:
        min_score = 10
        max_score = 0

        questionaire_answers = QuestionaireAnswer.objects.filter(
            questionaire = questionaire
        )

        # got through all answers in one questionaire
        for questionaire_answer in questionaire_answers:
            qa_score = questionaire_answer.answer_score * questionaire_answer.answer_weight

            if qa_score < min_score:
                min_score = qa_score
            
            if qa_score > max_score:
                max_score = qa_score
        
        questionaire.min_score = min_score
        questionaire.max_score = max_score
        questionaire.save()
        count += 1

        total_min_score += min_score
        total_max_score += max_score

    # also update all questionaires of the same type to store total min max score
    count += Questionaire.objects.filter(
        questionaire_type = questionaire_type
    ).update(
        total_min_score = total_min_score,
        total_max_score = total_max_score
    )

    return count
# end def get_questionaires_min_max_score()

def get_questionaires_total_min_max_score (questionaire_type):
    '''
    '''
    questionaires = Questionaire.objects.filter(
        questionaire_type = questionaire_type
    )[0]

    total_min_score = questionaires.total_min_score
    total_max_score = questionaires.total_max_score

    return (total_min_score, total_max_score)
# end def get_sum_questionaires_min_max_score()

def get_sum_questionaires_total_min_max_score ():
    '''
    '''
    total_min_score = 0
    total_max_score = 0

    for questionaire_type in questionaire_types:
        temp_total_min_score, temp_total_max_score = get_questionaires_total_min_max_score(questionaire_type)
        total_min_score += temp_total_min_score
        total_max_score += temp_total_max_score

    return (total_min_score, total_max_score)
# end def get_sum_questionaires_min_max_score()
