from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'name', 'placeholder': "Enter name",  'title': "Please enter your name (at least 2 characters)", 'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'id': 'email', 'placeholder': "Enter email", 'title': "Please enter a valid email address", 'class': 'form-control'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'phone', 'class':"form-control required digits", 'type':"tel", 'size':"30", 'value':"", 'placeholder':"Enter phone", 'title':"Please enter a valid phone number (at least 10 characters)"}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'id': 'message', 'class': "form-control", 'cols': "3", 'rows': "5", 'placeholder': "Enter your message...", 'title': "Please enter your message (at least 10 characters)"}))