from django import forms
from django.forms import ModelForm
from Application.models import *

class SearchForm(ModelForm):
    class Meta:
        model = Search
        fields = '__all__'
        widgets = {
            'city' : forms.TextInput(attrs={'class': 'form-control'}),
            'genre' : forms.TextInput(attrs={'class': 'form-control'}),
        }

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        widgets = {}