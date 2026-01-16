from django.db import models

from investment_choices.models import InvestmentChoice

# Create your models here.

class InvestmentData (models.Model) :

    investment_choice = models.ForeignKey (InvestmentChoice, on_delete=models.DO_NOTHING)
    inv_date = models.DateTimeField()
    inv_price = models.FloatField()

    def __str__ (self) :
        return str(self.inv_price)

    

