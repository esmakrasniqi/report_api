from django import forms
from .models import Task

class taskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=("name",'description')
        labels = {
            'name':"Name",
            'description':"Description"
        }