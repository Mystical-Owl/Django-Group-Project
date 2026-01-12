from django.db import models

from .choices import questionaire_types

# Create your models here.

class Questionaire (models.Model) :
    questionaire_statement = models.CharField (max_length=1000)
    questionaire_type = models.CharField (max_length=20, choices=questionaire_types.items())

    def __str__ (self) :
        return self.question_stmt
    