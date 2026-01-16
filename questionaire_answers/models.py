from django.db import models

from questionaires.models import Questionaire

# Create your models here.

class QuestionaireAnswer (models.Model) :
    questionaire = models.ForeignKey (Questionaire, on_delete=models.DO_NOTHING)
    questionaire_answer = models.CharField (max_length=50)
    answer_score = models.FloatField (blank=True, null=True)
    answer_weight = models.FloatField (blank=True, null=True)
    sort_order = models.IntegerField (blank=True, null=True)

    def __str__ (self) :
        return self.questionaire_answer


