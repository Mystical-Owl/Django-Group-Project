from django.db import models

from django.contrib.auth.models import User

from investment_choices.models import InvestmentChoice

# Create your models here.

class UserInvestment (models.Model) :
    # user_id = models.IntegerField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    investment_choice = models.ForeignKey (InvestmentChoice, on_delete=models.DO_NOTHING)
    begin_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    investment_amount = models.FloatField()

    def __str__ (self) :
        return str(self.investment_amount)


