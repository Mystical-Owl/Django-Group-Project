from django.db import models

# Create your models here.

class InvestmentType (models.Model) :
    investment_type = models.CharField (max_length=50, blank=True, null=True)
    investment_score_range_start = models.FloatField (blank=True, null=True)
    investment_score_range_end = models.FloatField (blank=True, null=True)

    def __str__ (self) :
        return self.investment_type

