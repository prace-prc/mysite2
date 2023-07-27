from django import forms
from django.utils import timezone

from .models import Comment


class EmailPostForm(forms.Form):
    sender = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

    def __init__(self, *args, **kwargs):
        super(CommentModelForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['email'].required = False
        self.fields['body'].required = False
