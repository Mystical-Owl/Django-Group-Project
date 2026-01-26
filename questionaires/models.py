from django.db import models

from .choices import questionaire_types

# Create your models here.

class Questionaire (models.Model) :
    questionaire_statement = models.CharField (max_length=1000)
    questionaire_type = models.CharField (max_length=50, choices=questionaire_types.items())
    sort_order = models.IntegerField (blank=True, null=True)
    min_score = models.FloatField (blank=True, null=True)
    max_score = models.FloatField (blank=True, null=True)
    total_min_score = models.FloatField (blank=True, null=True)
    total_max_score = models.FloatField (blank=True, null=True)

    def __str__ (self) :
        return self.questionaire_statement
    