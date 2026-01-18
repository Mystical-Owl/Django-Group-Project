from django.shortcuts import render
from django.shortcuts import redirect

from .utils import import_default_users
from .utils import import_questionaire_answers
from .utils import clear_questionaire_answers
from .utils import clear_questionaires

### import to use django messages framework
from django.contrib import messages

# Create your views here.

def func_import_index (request) :
    if request.user.is_authenticated and request.user.username == 'admin':
        return render(request, 'tpl_import_data/import_index.html')
    else:
        return redirect('/')

def func_import_default_questionaire_data (request):

    if request.user.is_authenticated and request.user.username == 'admin':
        if request.method == 'POST':
            import_default_users()
            import_questionaire_answers()
            ## add alert message
            messages.success(request, 'Default data imported successfully.')

    return redirect('app_import_data:djep_import_index')
# end def func_import_default_questionaire_data()

def func_delete_default_questionaire_data (request):

    if request.user.is_authenticated and request.user.username == 'admin':
        if request.method == 'POST':
            # first delete answers
            del_cnt = clear_questionaire_answers()
            if del_cnt > 0:
                ## add alert message
                messages.success(request, 'Default answers deleted successfully.')
            else:
                messages.info(request, 'No data deleted.')

            # then delete questions
            del_cnt = clear_questionaires()
            if del_cnt > 0:
                ## add alert message
                messages.success(request, 'Default questions deleted successfully.')
            else:
                messages.info(request, 'No data deleted.')
        else:
            messages.info(request, 'No data deleted.')

    return redirect('app_import_data:djep_import_index')
# end def func_delete_default_questionaire_data()
