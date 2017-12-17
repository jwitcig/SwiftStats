from django import forms
from django.forms import Form

class RequestProcessingForm(Form):

    repo_url = forms.CharField(label='repo_url', required=True)
    username = forms.CharField(label='username', required=True)
    repo_name = forms.CharField(label='repo_name', required=True)

    class Meta:
        fields = ('repo_url', 'username', 'repo_name',)
