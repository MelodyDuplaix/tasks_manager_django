from django import forms # type: ignore
from tasks.models import SubManager, Task, Reward, TaskType, PonctualTask
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.contrib.auth.models import User

class SubManagerForm(forms.ModelForm):
    class Meta:
        model = SubManager
        exclude = ['active', 'user']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'coins_number', 'type']

class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['name', 'coins_number']

class TypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        exclude = ['sub_manager']


class PonctualTaskForm(forms.ModelForm):
    class Meta:
        model = PonctualTask
        fields = ['name', 'coins_number']

class PasswordResetForm(forms.Form):
    email = forms.EmailField()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')