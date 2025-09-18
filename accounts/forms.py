from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email','phone','first_name','gender')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone','first_name', 'last_name', 'gender')
        readonly_fields = ('email',)

from django import forms
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'gender', 'dob', 'bio', 'profile_pic']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Custom phone validation logic (if needed)
        return phone

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        # Custom first name validation logic (if needed)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        # Custom last name validation logic (if needed)
        return last_name


