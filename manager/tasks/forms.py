from django import forms  # type: ignore
from django.contrib.auth.forms import UserCreationForm  # type: ignore
from django.contrib.auth.models import User
from tasks.models import SubManager, Task, Reward, TaskType, PonctualTask


class SubManagerForm(forms.ModelForm):
    class Meta:
        model = SubManager
        exclude = ['active', 'user']


class TypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        exclude = ['sub_manager']


class TaskForm(forms.ModelForm):
    submanager_id = None

    class Meta:
        model = Task
        fields = ['name', 'coins_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'] = forms.ModelChoiceField(queryset=TaskType.objects.all(), required=False)
        self.fields['new_type'] = forms.CharField(max_length=255, required=False)

    def save(self, commit=True):
        if self.cleaned_data['new_type']:
            existing_type = TaskType.objects.filter(name=self.cleaned_data['new_type'],
                                                    sub_manager_id=self.submanager_id).first()
            if existing_type:
                self.instance.type = existing_type
            else:
                new_type = TaskType.objects.create(name=self.cleaned_data['new_type'],
                                                   sub_manager_id=self.submanager_id)
                self.instance.type = new_type
        else:
            self.instance.type = self.cleaned_data['type']
        return super().save(commit)


class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['name', 'coins_number']


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
