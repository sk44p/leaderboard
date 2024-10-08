from django import forms
from .models import Player

class NewGameForm(forms.Form):
    red_team = forms.ModelMultipleChoiceField(queryset=Player.objects.all(), widget=forms.CheckboxSelectMultiple, label="Red Team")
    yellow_team = forms.ModelMultipleChoiceField(queryset=Player.objects.all(), widget=forms.CheckboxSelectMultiple, label="Yellow Team")

    def clean(self):
        cleaned_data = super().clean()
        red_team = cleaned_data.get('red_team')
        yellow_team = cleaned_data.get('yellow_team')

        if not red_team or not yellow_team:
            raise forms.ValidationError("You must select players for both teams.")

        # Optionally, add checks to ensure teams do not overlap
        overlapping_players = set(red_team) & set(yellow_team)
        if overlapping_players:
            raise forms.ValidationError("The same player cannot be on both teams.")

        return cleaned_data

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'avatar']  # Add fields you want to include in the form
