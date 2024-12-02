from django import forms
from tasks.models import SubManager, Task, Reward

class SubManagerForm(forms.ModelForm):
    class Meta:
        model = SubManager
        fields = '__all__'


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'coins_number', 'ponctuel', 'type']

class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['name', 'coins_number']