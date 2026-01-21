from django.db import models

# Create your models here.

class InvestmentType (models.Model) :
    investment_type = models.CharField (max_length=50, blank=True, null=True)

    def __str__ (self) :
        return self.investment_type

