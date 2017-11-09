#! /usr/bin/env python

import re, sys, os
import json
import requests
import hashlib
import datetime
import calendar
import time
import random
import unicodedata
import urllib

from bs4 import BeautifulSoup
import unidecode

proj_path = os.path.join(os.path.dirname(__file__), '..')
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
sys.path.append(proj_path)

import django
django.setup()

from ugf.models import *
from django.conf import settings

def grab_mattermark_data(company):
    search_url = "https://api.mattermark.com/companies/%s?key=%s" % (company.mattermark_id, settings.MATTERMARK_API_KEY)
    resp = requests.get(search_url)
    resp = resp.json()

    misses = 0

    company.domain = resp.get('website')
    company.zip_code = resp.get("zip")
    company.state = resp.get("state")
    company.city = resp.get("city")
    company.country = resp.get("country")

    employee_count = resp.get('employee_count')[0].get("score", "0") if resp.get('employee_count') else 0
    company.employee_count = int(employee_count) if employee_count else None
    
    company.total_funding = int(resp.get("total_funding")) if resp.get('total_funding') else None
    if not company.total_funding:
        misses += 1
    company.last_funding_amount = int(resp.get("last_funding_amount")) if resp.get('last_funding_amount') else None
    if not company.last_funding_amount:
        misses += 1
    
    last_funding_date = resp.get('last_funding_date', None)
    if last_funding_date:
        last_funding_date = datetime.datetime.strptime(last_funding_date, "%Y-%m-%d")
    
    company.last_funding_date = last_funding_date
    if not company.last_funding_date:
        misses += 1

    company.current_series = resp.get("stage")
    if not company.current_series:
        misses += 1

    company.data_retrieved = True
    company.date_data_retrieved = datetime.datetime.now()

    for funding_round in resp.get("funding"):
        amount = int( funding_round.get("amount") ) if funding_round.get("amount") else None
        series = funding_round.get("series", "")
        funding_date = funding_round.get("funding_date", "")

        if funding_date:
            funding_date = datetime.datetime.strptime(funding_date, "%Y-%m-%d")

        new_funding_round = FundingRound.objects.create(amount=amount, series=series, funding_date=funding_date, company=company)
        for investor in funding_round.get("investors").split(", "):
            new_investor, created = Investor.objects.get_or_create(name=investor)
            new_investor.companies.add(company)
            new_investor.funding_rounds.add(new_funding_round)
            new_investor.save()

        new_funding_round.save()
    
    company.valid_candidate = misses < 3 and not re.search('exited', company.current_series, re.IGNORECASE)
    company.save()

        

if not sys.argv[1]:
    print "usage: ./process_company_via_api.py <ugf-company-id>"
    sys.exit()

ugf_company_id = sys.argv[1]

company = Company.objects.get(id=ugf_company_id)
print company

if not company.mattermark_id:
    search_url = "https://api.mattermark.com/search?key=%s&term=%s&object_types=company" % (settings.MATTERMARK_API_KEY, company.name)
    resp = requests.get(search_url)
    # perform search for company
    for company_response in resp.json():
        if company_response.get("object_name") == company.name:
            company.mattermark_id = company_response.get("object_id")
            company.data_can_retrieved = True
            break

    if not company.mattermark_id:
        company.mattermark_id = settings.MATTERMARK_FAIL
        company.data_can_retrieved = False
    
    # save the company to db
    company.save()

    pass    

# get mattermark data for company_id
if company.mattermark_id != settings.MATTERMARK_FAIL:
    grab_mattermark_data(company)

sys.exit()
