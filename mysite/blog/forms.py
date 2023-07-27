from django import forms

class EmailPostForm(forms.Form):
    sender = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()