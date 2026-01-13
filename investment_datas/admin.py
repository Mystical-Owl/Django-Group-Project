from django.contrib import admin

# Register your models here.

from .models import InvestmentData

class InvestmentDataAdmin (admin.ModelAdmin) :
    list_display = ('investment_choice', 'inv_date', 'inv_price')
    list_display_links = ('investment_choice', )
    list_editable = ('inv_date', 'inv_price')
    search_fields = ('investment_choice', 'inv_date', 'inv_price')
    list_per_page = 25


admin.site.register (InvestmentData, InvestmentDataAdmin)


