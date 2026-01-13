from django.contrib import admin

# Register your models here.

from .models import InvestmentChoice

class InvestmentChoiceAdmin (admin.ModelAdmin) :
    list_display = ('fund_name', 'fund_type', 'fund_description')
    list_display_links = ('fund_name', )
    list_editable = ('fund_type', 'fund_description')
    search_fields = ('fund_name', 'fund_type', 'fund_description')
    list_per_page = 25


admin.site.register (InvestmentChoice, InvestmentChoiceAdmin)

