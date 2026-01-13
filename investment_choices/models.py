from django.db import models

from investment_types.models import InvestmentType

# Create your models here.

class InvestmentChoice (models.Model) :
    fund_name = models.CharField (max_length=50)
    fund_type = models.ForeignKey (InvestmentType, on_delete=models.DO_NOTHING)

    def __str__ (self) :
        return self.fund_name


