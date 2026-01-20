from django.db import models

from investment_types.models import InvestmentType

# Create your models here.

class InvestmentChoice (models.Model) :
    investment_name = models.CharField (max_length=50)
    investment_type = models.ForeignKey (InvestmentType, on_delete=models.DO_NOTHING)
    investment_description = models.CharField (max_length=500, blank=True, null=True)

    def __str__ (self) :
        return self.fund_name


