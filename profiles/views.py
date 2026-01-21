'''
Function-based views. They require login (@login_required).
profile_view: Shows the profile or prompts to create if missing.
profile_create: Creates a new profile (only if none exists, but you can add a check).
profile_update: Edits existing profile.
profile_delete: Deletes the profile (with confirmation).
'''

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm

@login_required
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'profiles/profile.html', {'profile': profile})
    except Profile.DoesNotExist:
        messages.info(request, "You haven't created a profile yet.")
        return redirect('profile_create')

@login_required
def profile_create(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Link to current user
            profile.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('profile_view')
    else:
        form = ProfileForm()
    return render(request, 'profiles/profile_form.html', {'form': form, 'action': 'Create'})

@login_required
def profile_update(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/profile_form.html', {'form': form, 'action': 'Update'})

@login_required
def profile_delete(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        profile.delete()
        messages.success(request, 'Profile deleted successfully!')
        return redirect('profile_create')  # Redirects to create prompt
    return render(request, 'profiles/profile_confirm_delete.html', {'profile': profile})
