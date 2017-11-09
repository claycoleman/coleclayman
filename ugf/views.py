import re, sys, os
import requests
import datetime
import subprocess

from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .helpers import *
from .models import *
from .forms import *

@login_required(login_url="/ugf/login/")
def cra_checker(request):
    context = {}
    form = CRAForm(request.POST or None)

    context['form'] = form
    if request.method == "POST":
        if form.is_valid():
            context['separate'] = request.POST.get('together', False) == 'separate'
            naics_code = form.cleaned_data.get('naics', False)
            if naics_code:
                naics_results = check_naics_code(naics_code)
                if naics_results['success']:
                    context['max_employees'] = naics_results['num_employees']
                else:
                    print "fail on naics..."


            street_address = form.cleaned_data['street_address']
            if form.cleaned_data.get('city', False):
                street_address += " " + form.cleaned_data['city']
            if form.cleaned_data.get('state', False):
                street_address += " " + form.cleaned_data['state']
            
            results = check_cra_address(street_address)
            context['success'] = results['success']
            if results['success']:
                # successful address!
                context['cra_qualified'] = results['cra_qualified']
                context['address'] = results['address']
                context['min_income'] = results['min_income']
                context['income_level'] = results['income_level'].lower()
                if results['cra_qualified']:
                    # CRA qualified
                    context['results'] = "This address is CRA qualified!"
                else:
                    context['results'] = "This address is NOT CRA qualified."

            else:
                context['results'] = "Uh oh, there was an error with that address."
                print results['message']
        else:
            print "invalid"

    return render(request, 'cra_checker.html', context)


@login_required(login_url="/ugf/login/")
def ugf_home(request):
    return render(request, "ugf_home.html")


@login_required(login_url="/ugf/login/")
def deal_sourcing(request):
    context = {}
    
    return render(request, 'deal_sourcing.html', context)


@login_required(login_url="/ugf/login/")
def company_table(request):
    context = {}
    
    companies = Company.objects.filter(data_retrieved=True, valid_candidate=True)
    six_months = set( companies.filter(last_funding_date__gte=datetime.datetime.now() - datetime.timedelta(days=6*30)) )
    twelve_months = set( companies.filter(last_funding_date__gte=datetime.datetime.now() - datetime.timedelta(days=12*30)) )
    eighteen_months = set( companies.filter(last_funding_date__gte=datetime.datetime.now() - datetime.timedelta(days=18*30)) )
    thirty_months = set( companies.filter(last_funding_date__gte=datetime.datetime.now() - datetime.timedelta(days=30*30)) )

    # print six_months
    # print twelve_months
    # print eighteen_months
    # print thirty_months

    group_a = eighteen_months - twelve_months
    context['group_a'] = group_a
    
    group_b = thirty_months - eighteen_months
    context['group_b'] = group_b
    group_c = twelve_months - six_months
    context['group_c'] = group_c

    context['remainder'] = set(companies) - group_c - group_b - group_a

    return render(request, 'company_table.html', context)


@login_required(login_url="/ugf/login/")
def company_detail(request, pk):
    context = {}
    
    return render(request, 'company_detail.html', context)


@login_required(login_url="/ugf/login/")
def company_entry(request):
    context = {}
    
    form = CompanyEntry(request.POST or None)

    companies_added = []
    companies_found = []

    if request.method == "POST":
        if form.is_valid():
            company_names = form.cleaned_data.get("company_names").strip()
            companies = company_names.split("\n")

            for company_name in companies:
                if not company_name:
                    continue
                # probably want to slugify?
                company_name_clean = company_name.strip()

                new_company, created = Company.objects.get_or_create(name=company_name_clean)
                if created:
                    companies_added.append(new_company)
                else:
                    companies_found.append(new_company)

            context['companies_added'] = companies_added
            context['companies_found'] = companies_found
            form = CompanyEntry()
        else:
            pass
            # form is NOT valid

    context['form'] = form
    context['companies_waiting'] = Company.objects.filter(data_retrieved=False)

    return render(request, 'company_entry.html', context)


form_titles = {
    'email': "Email",
    'password': "Password",
    'password2': "Password again",
    'secret_code': "Secret code",
}


def signup_view(request):
    context = {}
    form = SignUpForm()
    context['form'] = form
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        context['form'] = form
        if form.is_valid():
            print form.cleaned_data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            secret_code = form.cleaned_data['secret_code']

            if secret_code != settings.SIGN_UP_SECRET_CODE:
                context['valid'] = 'Invalid secret code. Sorry.'
            else:
                if password == password2:
                    try:
                        new_user = User.objects.create_user(username=email, email=email, password=password)
                        context['valid'] = 'Thank you for signing up!'
                        auth_user = authenticate(username=email, password=password)
                        login(request, auth_user)
                        return redirect('ugf_home')
                    except IntegrityError, e:
                        context['valid'] = 'A user with that email already exists.'
                else:
                    context['valid'] = 'Your passwords didn\'t match!'
        else:
            valid_str = ""
            for error_field in form.errors:
                valid_str = "<p>%s is required.</p>" % (form_titles.get(error_field)) + valid_str
            context['valid'] = valid_str

    print context.get('valid', "")
    return render(request, 'signup_view.html', context)


def login_view(request):
    context = {}
    form = UserLogin()
    context['form'] = form 
   
    if request.method == 'POST':
        form = UserLogin(request.POST)
        context['form'] = form

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            next_url = form.cleaned_data.get('next_url')
            auth_user = authenticate(username=email, password=password)
            if auth_user is not None:
                if auth_user.is_active:
                    login(request, auth_user)
                    context['valid'] = 'Login Successful'
                    if next_url:
                        return HttpResponseRedirect(next_url)
                    return redirect('ugf_home')
                else:
                    context['valid'] = 'Invalid User'
            else:
                context['valid'] = 'Login Failed! Try again'
        else:
            valid_str = ""
            for error_field in form.errors:
                valid_str = "<p>%s is required.</p>" % (form_titles.get(error_field)) + valid_str
            context['valid'] = valid_str
    else:
        form = UserLogin({'next_url': request.GET.get("next", "")})
        context['form'] = form

    return render(request, 'login_view.html', context)


def logout_view(request):
    logout(request)
    return redirect('login_view')


def get_hubspot_value_for_property(props, property_name):
    return props.get(property_name, {}).get('value', None)

@csrf_exempt
def hubspot(request):
    if not request.method == "POST":
        return HttpResponseBadRequest()

    form = HubspotCompanyCreation(request.POST)
    if not form.is_valid():
        return JsonResponse({'result': 'failure', 'errno': 1}, safe=False) 
        

    new_hb_id = form.cleaned_data.get("objectId")
    app_id = form.cleaned_data.get("appId")
    portal_id = form.cleaned_data.get("portalId")
    
    subscription_type = form.cleaned_data.get("subscriptionType")

    if subscription_type == "company.creation":
        if app_id != settings.HUBSPOT_APP_ID or portal_id != settings.HUBSPOT_PORTAL_ID:
            return JsonResponse({'result': 'failure', 'errno': 2}, safe=False) 

        print "new objectID", new_hb_id
        # create new Company with hubspotid
        new_company, created = Company.objects.get_or_create(hubspot_id=new_hb_id)
        
        # make a request to the HubSpot db to get Company info
        resp = requests.get("https://api.hubapi.com/companies/v2/companies/%d?hapikey=%s&userId=%s" % (new_hb_id, settings.HUBSPOT_HAPI_KEY, settings.HUBSPOT_USER_ID) )
        print resp
        resp = resp.json()
        props = resp.get("properties", False)
        
        if not props:
            # we didn't get a valid company back which is weird because we JUST got a company from them
            return JsonResponse({'result': 'failure', 'errno': 3}, safe=False) 
        
        # save it, then make mattermark request
        new_company.name = get_hubspot_value_for_property(props, 'name')
        new_company.domain = get_hubspot_value_for_property(props, 'domain')
        new_company.save()

        # live version
        subprocess.Popen( (["/sites/virtualenvs/coleclayman/bin/python", "../scripts/process_company_via_api.py", "%s" % new_company.id]) )
        # local version
        # subprocess.Popen( (["/Users/claycoleman/Dev/virtualenvs/coleclayman/bin/python", settings.PROJECT_ROOT + "/../scripts/process_company_via_api.py", "%s" % new_company.id]) )
        
        return JsonResponse({'result': 'success'}, safe=False)

    return JsonResponse({'result': 'failure', 'errno': 4}, safe=False) 