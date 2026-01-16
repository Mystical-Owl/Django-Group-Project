from django.shortcuts import render

# Create your views here.

def func_import_default_data (request):


    return render(request, 'questionaires/import.html')
