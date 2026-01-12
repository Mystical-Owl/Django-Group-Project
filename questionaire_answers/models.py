from django.db import models

from questionaires.models import Questionaires

# Create your models here.

class Questionaire_Answers (models.Model) :
    questionaire = models.ForeignKey (Questionaires, on_delete=models.DO_NOTHING)
    questionaire_answer = models.CharField (max_length=50)
    answer_score = models.IntegerField ()

    def __str__ (self) :
        return self.questionaire_answer


