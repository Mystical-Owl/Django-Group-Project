from django.contrib import admin

# Register your models here.

from .models import InvestmentType

class InvestmentTypeAdmin (admin.ModelAdmin) :
    list_display = ('investment_type', )
    list_display_links = ('investment_type', )
    list_editable = ( )
    search_fields = ('investment_type', )
    list_per_page = 25


admin.site.register (InvestmentType, InvestmentTypeAdmin)

