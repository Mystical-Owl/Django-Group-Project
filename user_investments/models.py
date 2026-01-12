from django.db import models

# Create your models here.

class UserInvestment (models.Model) :

    user_id = models.IntegerField(blank=True, null=True)
    