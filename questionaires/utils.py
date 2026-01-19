
from questionaires.models import Questionaire
from questionaire_answers.models import QuestionaireAnswer

class QuestionaireAndAnswers () :
    def __init__ (self, questionaire, questionaire_answers) :
        self.questionaire = questionaire
        self.questionaire_answers = questionaire_answers
# end class QuestionaireAndAnswers()

def get_questionaire_and_answers (questionaire_type):
    '''
    Returns python list of QuestionaireAndAnswers objects.
    '''
    questionaire_and_answers = []

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

        questionaire_and_answers.append(
            QuestionaireAndAnswers(
                questionaire,
                questionaire_answers
            )
        )
    
    return questionaire_and_answers
# end def get_questionaire_answers()
