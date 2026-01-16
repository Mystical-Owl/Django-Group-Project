from django.contrib import admin

# Register your models here.

from .models import UserInvestment

class UserInvestmentAdmin (admin.ModelAdmin) :
    # list_display = ('user_id', 'user', 'investment_choice', 'begin_date', 'end_date', 'investment_amount')
    # list_display_links = ('user_id', )
    # list_editable = ('investment_choice', 'end_date', 'investment_amount')
    # search_fields = ('user_id', 'investment_choice', 'begin_date', 'end_date', 'investment_amount')
    # list_per_page = 25

    list_display = ('user', 'investment_choice', 'begin_date', 'end_date', 'investment_amount')
    list_display_links = ('user', )
    list_editable = ('investment_choice', 'end_date', 'investment_amount')
    search_fields = ('user', 'investment_choice', 'begin_date', 'end_date', 'investment_amount')
    list_per_page = 25


admin.site.register (UserInvestment, UserInvestmentAdmin)

