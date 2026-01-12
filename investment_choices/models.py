from django.db import models

# Create your models here.

class InvestmentChoice (models.Model) :
    fund_name = models.CharField (max_length=50)
    # fund_type = 