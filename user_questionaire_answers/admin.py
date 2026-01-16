from django.contrib import admin

# Register your models here.

from .models import UserQuestionaireAnswer

class UserQuestionaireAnswerAdmin (admin.ModelAdmin) :
    # list_display = ('user_id', 'user', 'questionaire_answer')
    # list_display_links = ('user_id', )
    # list_editable = ('questionaire_answer', )
    # search_fields = ('user_id', 'questionaire_answer')
    # list_per_page = 25

    list_display = ('user', 'questionaire_answer')
    list_display_links = ('user', )
    list_editable = ('questionaire_answer', )
    search_fields = ('user', 'questionaire_answer')
    list_per_page = 25


admin.site.register (UserQuestionaireAnswer, UserQuestionaireAnswerAdmin)

