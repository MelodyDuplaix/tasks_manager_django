from django import forms # type: ignore
from tasks.models import SubManager, Task, Reward, TaskType, PonctualTask

class SubManagerForm(forms.ModelForm):
    class Meta:
        model = SubManager
        fields = '__all__'

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