from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'address', 'telephone', 'gender', 'occupation']  # Only the new fields
        # Optional: Customize widgets for better UI (since you have widget_tweaks installed)
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'gender': forms.Select(),
        }