from django.contrib import admin

# Register your models here.

from .models import QuestionaireAnswer

class QuestionaireAnswerAdmin (admin.ModelAdmin) :
    list_display = ('questionaire', 'questionaire_answer', 'answer_score', 'answer_weight', 'sort_order')
    list_display_links = ('questionaire', )
    list_editable = ('questionaire_answer', 'answer_score', 'answer_weight', 'sort_order')
    search_fields = ('questionaire', 'questionaire_answer', 'answer_score')
    list_per_page = 25

admin.site.register (QuestionaireAnswer, QuestionaireAnswerAdmin)

