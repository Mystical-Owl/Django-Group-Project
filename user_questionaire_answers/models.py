from django.db import models

from questionaire_answers.models import QuestionaireAnswer

# Create your models here.

class UserQuestionaireAnswer (models.Model) :
    user_id = models.IntegerField(blank=True, null=True)
    questionaire_answer = models.ForeignKey (QuestionaireAnswer, on_delete=models.DO_NOTHING)

    def __str__ (self) :
        return str(user_id)

        