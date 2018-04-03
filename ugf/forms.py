from django import forms

class CRAForm(forms.Form):
    street_address = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': "Street address",  'title': "Please enter the company's street address", 'class': 'form-control'}))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': "City", 'title': "Please enter the company's city", 'class': 'form-control'}))
    state = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': "State", 'title': "Please enter the company's state", 'class': 'form-control'}))
    naics = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': "NAICS", 'title': "Please enter the company's NAICS code.", 'class': 'form-control'}))


class CompanyEntry(forms.Form):
    company_names = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': "e.g:\nCompany1\nCompany2\nCompany3", 'class': 'form-control'}))


class SignUpForm(forms.Form):
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': "Email (username)", 'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': "Password", 'class': 'form-control'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': "Password Again", 'class': 'form-control'}))
    secret_code = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': "What's the secret code?", 'class': 'form-control'}))


class UserLogin(forms.Form):  
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': "Email (username)", 'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': "Password", 'class': 'form-control'}))
    next_url = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': "hidden", 'class': 'hidden'}))


class AirtableDateForm(forms.Form):
    date_str = forms.CharField(required=True)


class HubspotCompanyCreation(forms.Form):
    objectId = forms.IntegerField(required=True)
    subscriptionType = forms.CharField(required=True)
    appId = forms.IntegerField(required=True)
    portalId = forms.IntegerField(required=True)

    occurredAt = forms.IntegerField(required=True)
    eventId = forms.IntegerField(required=True)
    subscriptionId = forms.IntegerField(required=False)
    attemptNumber = forms.IntegerField(required=True)
    changeSource = forms.CharField(required=False)
    changeFlag = forms.CharField(required=False)