from django import forms

class CommentForm(forms.Form):
    author = forms.CharField(required=True)
    body = forms.CharField(required=True)


class UploadFileForm(forms.Form):
    file = forms.FileField(required=True)
