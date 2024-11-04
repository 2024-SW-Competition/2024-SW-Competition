from django import forms
from .models import Team
from story.models import Comment

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
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # 문자열이 아닌, 실제 모델 클래스를 사용
        fields = ['text']
