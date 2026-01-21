from django.db import models

from investment_choices.models import InvestmentChoice

# Create your models here.

class InvestmentData (models.Model) :

    investment_choice = models.ForeignKey (InvestmentChoice, on_delete=models.CASCADE, blank=True, null=True)
    investment_date = models.DateTimeField(blank=True, null=True)
    investment_price = models.FloatField(blank=True, null=True)

    def __str__ (self) :
        return str(self.investment_price)

    

