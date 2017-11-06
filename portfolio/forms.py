from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'name', 'placeholder': "Enter name",  'title': "Please enter your name (at least 2 characters)", 'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'id': 'email', 'placeholder': "Enter email", 'title': "Please enter a valid email address", 'class': 'form-control'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'phone', 'class':"form-control required digits", 'type':"tel", 'size':"30", 'value':"", 'placeholder':"Enter phone", 'title':"Please enter a valid phone number (at least 10 characters)"}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'id': 'message', 'class': "form-control", 'cols': "3", 'rows': "5", 'placeholder': "Enter your message...", 'title': "Please enter your message (at least 10 characters)"}))

class CRAForm(forms.Form):
    street_address = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': "Street address",  'title': "Please enter the company's street address", 'class': 'form-control'}))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': "City", 'title': "Please enter the company's city", 'class': 'form-control'}))
    state = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': "State", 'title': "Please enter the company's state", 'class': 'form-control'}))
    naics = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': "NAICS", 'title': "Please enter the company's NAICS code.", 'class': 'form-control'}))


class ScriptureOpener(forms.Form):
    open_scriptures = forms.CharField(required=True, widget=forms.TextInput())

class ScripturePageSearch(forms.Form):
    book_of_scripture = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': "Street address",  'title': "Please enter the company's street address", 'class': 'form-control'}))
    page_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': "City", 'title': "Please enter the company's city", 'class': 'form-control'}))
    return_json = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': "City", 'title': "Please enter the company's city", 'class': 'form-control'}))


class BudgetItemCreateForm(forms.Form):
    value = forms.FloatField(required=True)
    category = forms.CharField(required=True)
    title = forms.CharField(required=True)
    month = forms.CharField(required=True)
    secret_code = forms.CharField(required=True)

class BudgetItemVerifyForm(forms.Form):
    month = forms.CharField(required=True)
    secret_code = forms.CharField(required=True)


