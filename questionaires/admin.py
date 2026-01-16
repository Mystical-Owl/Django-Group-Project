from django.contrib import admin

# Register your models here.

from .models import Questionaire

class QuestionaireAdmin (admin.ModelAdmin) :
    list_display = ('questionaire_statement', 'questionaire_type')
    list_display_links = ('questionaire_statement', )
    list_editable = ('questionaire_type', )
    search_fields = ('questionaire_statement', 'questionaire_type')
    list_per_page = 25


admin.site.register (Questionaire, QuestionaireAdmin)

