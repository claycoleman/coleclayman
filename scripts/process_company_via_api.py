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
    company.grab_mattermark_data()
    company.update_hubspot_with_data()

sys.exit()
