from django import forms
from tasks.models import SubManager, Objectif, Task, Reward

class SubManagerForm(forms.ModelForm):
   class Meta:
     model = SubManager
     fields = '__all__'

class ObjectifForm(forms.ModelForm):
    class Meta:
        model = Objectif
        fields = ['coins_number']
        labels = {
            'coins_number': 'Nombre de pièces',
        }
        widgets = {
            'coins_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 1000,
            }),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'coins_number', 'ponctuel', 'type']

class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['name', 'coins_number']