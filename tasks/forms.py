from django.forms import ModelForm
from .models import Tarea
from django import forms

class TaskForm(ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'importante']
        widgest = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe el titulo'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe la descripción'}),
            'importante': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }