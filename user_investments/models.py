from django.db import models

from django.contrib.auth.models import User

from investment_choices.models import InvestmentChoice

# Create your models here.

class UserInvestment (models.Model) :
    user = models.ForeignKey (User, on_delete=models.CASCADE, blank=True, null=True)
    investment_choice = models.ForeignKey (InvestmentChoice, on_delete=models.CASCADE, blank=True, null=True)
    user_investment_name = models.CharField (max_length=50, blank=True, null=True)
    begin_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    investment_amount = models.FloatField(blank=True, null=True)
    investment_total_amount = models.FloatField(blank=True, null=True)

    def __str__ (self) :
        return str(self.investment_amount)


