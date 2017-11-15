#! /usr/bin/env python

import re, sys, os
import requests
import datetime

from random import shuffle

proj_path = os.path.join(os.path.dirname(__file__), '..')
# This is so Django knows where to find stuff.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
sys.path.append(proj_path)

import django
django.setup()

from django.core.mail import send_mail
from ugf.models import *
from django.conf import settings


url = "https://api.hubapi.com/companies/v2/companies/paged?hapikey=%s&userId=%s&properties=name&properties=date_for_next_interaction&properties=hubspot_owner_id&limit=250" % (settings.HUBSPOT_HAPI_KEY, settings.HUBSPOT_USER_ID)

def get_all_sourcing_team_members():
    url = "https://api.hubapi.com/owners/v2/owners?hapikey=%s&userId=%s" % (settings.HUBSPOT_HAPI_KEY, settings.HUBSPOT_USER_ID)
    resp = requests.get(url)
    owners_list = {}
    
    for owner in resp.json():
        if owner.get("lastName", "").endswith(" DST"):
        # test method for now
        # if owner.get("lastName", "").endswith("Coleman"):
            owners_list[owner.get('ownerId')] = owner
    
    return owners_list

resp = requests.get(url)

companies_to_assign = []

local_companies_lut = dict((company.hubspot_id, company) for company in Company.objects.exclude(hubspot_id=None))
hubspot_companies_lut = dict((company.get("companyId"), company) for company in resp.json().get("companies"))

# print local_companies_lut
# print hubspot_companies_lut

# get companies from hubspot
for company_id, company in hubspot_companies_lut.items():
    # print company

    # check if company has a different date than what we have on store for them
    # if it's different, update it!
    timestamp = get_hubspot_value_for_property(company.get("properties"), "date_for_next_interaction" )
    if not timestamp:
        continue

    next_interaction_date = datetime.datetime.fromtimestamp(long(timestamp) / 1000)
    print next_interaction_date
    
    if not local_companies_lut.get(company_id):
        continue # again, not really sure when this would happen

    if local_companies_lut[company_id].next_interaction_date != next_interaction_date.date():
        local_companies_lut[company_id].next_interaction_date = next_interaction_date.date()
        local_companies_lut[company_id].should_alert_next_interaction = True
        local_companies_lut[company_id].save()
        print "updated %s for should_alert_next_interaction" % local_companies_lut[company_id] 


    # TODO find out if they're needed to be updated
    # do_stuff = company.get("properties").get("date_for_next_interaction")
    # company is identified to be a good company to update

    # set hubspot_owner_id to owners

print "done with updating should_alert_next_interaction on companies"

owners_list = get_all_sourcing_team_members()
print "deal sourcing team", owners_list
owners_random_index_list = range(len(owners_list))
shuffle(owners_random_index_list)
current_owner_index = 0

owner_company_dict = {}

today = datetime.date.today()

# assign companies to owners
for company in Company.objects.filter(should_alert_next_interaction=True):
    # if we shouldn't reach out to them yet
    if company.next_interaction_date > today:
        continue
        
    company_id = company.hubspot_id
    hoid = get_hubspot_value_for_property( hubspot_companies_lut[company_id].get("properties"), "hubspot_owner_id")
    if hoid:
        hoid = int(hoid)
    print owners_list.keys()

    if (hoid == None or hoid not in owners_list.keys()):
        # assign the company to a random new owner from owners list 
        current_owner = owners_list.values()[owners_random_index_list[current_owner_index]]
        hoid = current_owner.get("ownerId")
        data = {
            "properties": []
        }
        data.get('properties').append({
            'name': "hubspot_owner_id",
            'value': hoid,
        })

        headers = {
            "Content-Type": "application/json"
        }
        print data

        resp = requests.put("https://api.hubapi.com/companies/v2/companies/%d?hapikey=%s&userId=%s" % (company_id, settings.HUBSPOT_HAPI_KEY, settings.HUBSPOT_USER_ID), data=json.dumps(data), headers=headers)

        print resp.text 

        current_owner_index = (current_owner_index + 1) % len(owners_random_index_list)
    
    company_to_contact_list = owner_company_dict.get(hoid, False)
    if not company_to_contact_list:
        owner_company_dict[hoid] = [company,]
    else:
        company_to_contact_list.append(company)

    company.should_alert_next_interaction = False
    company.save()


if len(owner_company_dict) == 0:
    sys.exit()

partner_message = """Hi Peter and Tom,

The following team members have just been assigned new companies or alerts on HubSpot:

"""

# send email to check out owners
for owner_id, owner in owners_list.items():
    curr_company_list = owner_company_dict.get(owner_id, False)
    if not curr_company_list:
        continue
    full_name = "%s %s" % (owner.get("firstName"), owner.get("lastName").replace(" DST", ""))
    company_list_string = ", ".join([ x.name for x in curr_company_list])
    message = """Hi there %s,

The following companies have just been assigned to you on HubSpot. Please log on, take a look the companies and their action items that need to be completed, and get them done!

%s

Thanks,

Peter""" % (owner.get("firstName") , company_list_string )

    print message
    partner_message += "%s\n\t%s\n\n" % (full_name, company_list_string)
    send_mail(
        "New Company Assignments",  # subject
        message, 
        "Peter Harris <noreply@ugrowthfund.com>", # from
        [owner.get("email"), ], # to
        fail_silently=False
    )

partner_message += """Thanks,

Clay Coleman"""

send_mail(
    "New Company Assignments for Students",  # subject
    partner_message, 
    "Clay Coleman <noreply@ugrowthfund.com>", # from
    ["coleclayman@gmail.com", "ccoleman@ugrowthfund.com"], # to
    fail_silently=False
)
