from datetime import date

from django import forms

from .models import Player, Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'city', 'category']


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'number', 'position', 'birth_date', 'team']
        widgets = {
            'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def clean_birth_date(self):
        value = self.cleaned_data['birth_date']
        if value > date.today():
            raise forms.ValidationError('La fecha de nacimiento no puede ser futura.')
        return value
