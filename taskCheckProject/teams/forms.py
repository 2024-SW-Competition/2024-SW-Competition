from django import forms
from .models import Team

class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'goal', 'duration']


class JoinTeamForm(forms.Form):
    code1 = forms.CharField(max_length=1, widget=forms.TextInput(attrs={'maxlength': '1'}))
    code2 = forms.CharField(max_length=1, widget=forms.TextInput(attrs={'maxlength': '1'}))
    code3 = forms.CharField(max_length=1, widget=forms.TextInput(attrs={'maxlength': '1'}))
    code4 = forms.CharField(max_length=1, widget=forms.TextInput(attrs={'maxlength': '1'}))

    def clean(self):
        cleaned_data = super().clean()
        code = ''.join([cleaned_data.get('code1', ''), cleaned_data.get('code2', ''), cleaned_data.get('code3', ''), cleaned_data.get('code4', '')])
        cleaned_data['invite_code'] = code

        return cleaned_data
