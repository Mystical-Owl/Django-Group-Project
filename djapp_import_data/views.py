from django.shortcuts import render
from django.shortcuts import redirect

from .utils import import_default_users
from .utils import import_questionaire_answers
from .utils import clear_questionaire_answers
from .utils import clear_questionaires
from .utils import import_investment_datas
from .utils import clear_investment_datas
from .utils import clear_investment_choices
from .utils import clear_investment_types

### import to use django messages framework
from django.contrib import messages

# Create your views here.

def func_import_index (request) :
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.username == 'admin':
        return redirect('/')

    return render(request, 'tpl_import_data/import_index.html')
# end def func_import_index()

def func_import_default_questionaire_data (request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.username == 'admin':
        return redirect('/')

    if request.method == 'POST':
        import_default_users()
        import_questionaire_answers()
        ## add alert message
        messages.success(request, 'Default questionaire data imported successfully.')

    return redirect('app_import_data:djep_import_index')
# end def func_import_default_questionaire_data()

def func_delete_default_questionaire_data (request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.username == 'admin':
        return redirect('/')

    if request.method == 'POST':
        # first delete answers
        del_cnt = clear_questionaire_answers()
        if del_cnt > 0:
            ## add alert message
            messages.success(request, 'Default questionaire answers deleted successfully.')
        else:
            messages.info(request, 'No data deleted.')

        # then delete questions
        del_cnt = clear_questionaires()
        if del_cnt > 0:
            ## add alert message
            messages.success(request, 'Default questionaire questions deleted successfully.')
        else:
            messages.info(request, 'No data deleted.')
    else:
        messages.info(request, 'No data deleted.')

    return redirect('app_import_data:djep_import_index')
# end def func_delete_default_questionaire_data()

def func_import_default_investment_datas (request):
    ### 30688
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.username == 'admin':
        return redirect('/')

    if request.method == 'POST':
        import_investment_datas()
        ## add alert message
        messages.success(request, 'Default investment data imported successfully.')

    return redirect('app_import_data:djep_import_index')
# end def func_import_default_investment_datas()

def func_delete_default_investment_datas (request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.username == 'admin':
        return redirect('/')

    if request.method == 'POST':
        # first delete datas
        del_cnt = clear_investment_datas()
        if del_cnt > 0:
            ## add alert message
            messages.success(request, 'Default investment datas deleted successfully.')
        else:
            messages.info(request, 'No data deleted.')

        # then delete choices
        del_cnt = clear_investment_choices()
        if del_cnt > 0:
            ## add alert message
            messages.success(request, 'Default investment choices deleted successfully.')
        else:
            messages.info(request, 'No data deleted.')

        # then delete types
        del_cnt = clear_investment_types()
        if del_cnt > 0:
            ## add alert message
            messages.success(request, 'Default investment types deleted successfully.')
        else:
            messages.info(request, 'No data deleted.')
    else:
        messages.info(request, 'No data deleted.')

    return redirect('app_import_data:djep_import_index')
# end def func_delete_default_questionaire_data()

