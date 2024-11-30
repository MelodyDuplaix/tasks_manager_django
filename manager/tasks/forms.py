from django import forms
from tasks.models import SubManager

class SubManagerForm(forms.ModelForm):
   class Meta:
     model = SubManager
     fields = '__all__'