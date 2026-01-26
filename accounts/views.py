from django.shortcuts import render

### import for redirect
from django.shortcuts import redirect

### import to use django messages framework
from django.contrib import messages

### import to use django auth framework
from django.contrib.auth.models import User

### auth from both paths works
# from django.contrib import auth
from django.contrib.auth.models import auth

# from djapp_contacts.models import Contact

# Create your views here.

## new import for self defined functions
# from django.http import HttpResponse

## using template:

def func_login (request):
    if request.method == 'POST':
        # process form data here
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('app_accounts:djep_dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('app_accounts:djep_login')
    else:
        return render(request, 'tpl_accounts/login.html')

def func_logout (request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out.')
        return redirect('app_accounts:djep_login')
        # return redirect('app_pages:djep_index')
    else:
        return render(request, 'tpl_accounts/login.html')

### check fields in register all at the same time
def func_register (request):
    if request.method == 'POST':
        # process form data here
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        b_invalid_form_data_flag = False
    
        if User.objects.filter(username=username).exists():
            b_invalid_form_data_flag = True
            messages.error(request, 'Username already taken')

        if User.objects.filter(email=email).exists():
            b_invalid_form_data_flag = True
            messages.error(request, 'Email already registered')

        if password != password2:
            b_invalid_form_data_flag = True
            messages.error(request, 'Passwords do not match')

        if b_invalid_form_data_flag:
            form_values = {
                'first_name' : first_name,
                'last_name' : last_name,
                'username' : username,
                'email' : email,
            }
            context = {
                'form_values' : form_values,
            }
            return render(request, 'tpl_accounts/register.html', context)
        else:
            # valid form data
            # create user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return render(request, 'tpl_accounts/login.html')
    else:  
        # not form post action
        ### default registration page display
        return render(request, 'tpl_accounts/register.html')

### check fields in register one at a time
# def func_register (request):
#     if request.method == 'POST':
#         # process form data here
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')
#         #
#         if password == password2:
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, 'Username already taken')
#                 return render(request, 'tpl_accounts/register.html')
#             else:
#                 if User.objects.filter(email=email).exists():
#                     messages.error(request, 'Email already registered')
#                     return render(request, 'tpl_accounts/register.html')
#                 else:
#                     # create user
#                     user = User.objects.create_user(
#                         username=username,
#                         password=password,
#                         email=email,
#                         first_name=first_name,
#                         last_name=last_name
#                     )
#                     user.save()
#                     messages.success(request, 'Registration successful. You can now log in.')
#                     return render(request, 'tpl_accounts/login.html')
#         else:
#             messages.error(request, 'Passwords do not match')
#             return redirect('app_accounts:djep_register')
#         #
#     else:
#         ### default registration page display
#         return render(request, 'tpl_accounts/register.html')


def func_dashboard (request):
    # contacts = Contact.objects.all().order_by('-contact_date')
    # user_contacts = Contact.objects.all(
    # ).order_by(
    #     '-contact_date'
    # ).filter(
    #     user_id=request.user.id,
    #     user_id__isnull=False
    # )

    context = {
        # 'contacts' : user_contacts,
    }

    return render(request, 'tpl_accounts/dashboard.html', context=context)
