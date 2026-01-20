from django.contrib import admin

# Register your models here.

from .models import InvestmentChoice

class InvestmentChoiceAdmin (admin.ModelAdmin) :
    list_display = ('investment_name', 'investment_type', 'investment_description')
    list_display_links = ('investment_name', )
    list_editable = ('investment_type', 'investment_description')
    search_fields = ('investment_name', 'investment_type', 'investment_description')
    list_per_page = 25


admin.site.register (InvestmentChoice, InvestmentChoiceAdmin)

