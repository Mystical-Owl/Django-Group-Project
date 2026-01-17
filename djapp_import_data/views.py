from django.shortcuts import render

from .utils import import_default_users, import_questionaire_answers

# Create your views here.

def func_import_default_data (request):

    import_default_users()

    import_questionaire_answers()

    return render(request, 'tpl_import_data/import_default_data.html')
