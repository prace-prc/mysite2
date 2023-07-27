from django import forms
from django.utils import timezone

from .models import Comment


class EmailPostForm(forms.Form):
    sender = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()


class CommentModelForm(forms.Form):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']