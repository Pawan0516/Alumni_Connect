from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('is_suspended','org_admin')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'org_admin', 'is_suspended', 'is_verified')
        readonly_fields = ('email',)
