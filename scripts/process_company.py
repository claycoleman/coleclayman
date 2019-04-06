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

from ugf.models import Company
from django.conf import settings

data_string = """aoData[sEcho]:1
aoData[iColumns]:56
aoData[sColumns]:
aoData[iDisplayStart]:0
aoData[iDisplayLength]:50
aoData[mDataProp_0]:check_box
aoData[mDataProp_1]:company_name
aoData[mDataProp_2]:domain
aoData[mDataProp_3]:description
aoData[mDataProp_4]:cached_growth_score
aoData[mDataProp_5]:mattermark_score
aoData[mDataProp_6]:momentum_score
aoData[mDataProp_7]:employees
aoData[mDataProp_8]:employees_month_ago
aoData[mDataProp_9]:employees_added_in_month
aoData[mDataProp_10]:employees_mom
aoData[mDataProp_11]:employees_6_months_ago
aoData[mDataProp_12]:employees_added_in_6_months
aoData[mDataProp_13]:employees_6_months_growth
aoData[mDataProp_14]:cached_uniques
aoData[mDataProp_15]:cached_uniques_week_ago
aoData[mDataProp_16]:uniques_wow
aoData[mDataProp_17]:cached_uniques_month_ago
aoData[mDataProp_18]:uniques_mom
aoData[mDataProp_19]:cached_mobile_downloads
aoData[mDataProp_20]:cached_mobile_downloads_week_ago
aoData[mDataProp_21]:mobile_downloads_wow
aoData[mDataProp_22]:cached_mobile_downloads_month_ago
aoData[mDataProp_23]:mobile_downloads_mom
aoData[mDataProp_24]:months_since_last_funding
aoData[mDataProp_25]:employees_added_since_last_funding
aoData[mDataProp_26]:new_person_months_since_last_funding
aoData[mDataProp_27]:new_funding_employee_growth
aoData[mDataProp_28]:est_founding_date
aoData[mDataProp_29]:stage
aoData[mDataProp_30]:investors
aoData[mDataProp_31]:total_funding
aoData[mDataProp_32]:last_funding_date
aoData[mDataProp_33]:last_funding_amount
aoData[mDataProp_34]:location
aoData[mDataProp_35]:city
aoData[mDataProp_36]:region
aoData[mDataProp_37]:state
aoData[mDataProp_38]:zip
aoData[mDataProp_39]:country
aoData[mDataProp_40]:continent
aoData[mDataProp_41]:revenue_range
aoData[mDataProp_42]:business_models
aoData[mDataProp_43]:industries
aoData[mDataProp_44]:interested
aoData[mDataProp_45]:alert_hash
aoData[mDataProp_46]:user_tags
aoData[mDataProp_47]:public_lists
aoData[mDataProp_48]:keywords
aoData[mDataProp_49]:has_mobile
aoData[mDataProp_50]:has_google_play
aoData[mDataProp_51]:has_itunes
aoData[mDataProp_52]:created_at
aoData[mDataProp_53]:department
aoData[mDataProp_54]:seniority
aoData[mDataProp_55]:jobtitle
aoData[sSearch]:
aoData[bRegex]:false
aoData[sSearch_0]:
aoData[bRegex_0]:false
aoData[bSearchable_0]:true
aoData[sSearch_1]:
aoData[bRegex_1]:false
aoData[bSearchable_1]:true
aoData[sSearch_2]:
aoData[bRegex_2]:false
aoData[bSearchable_2]:true
aoData[sSearch_3]:
aoData[bRegex_3]:false
aoData[bSearchable_3]:true
aoData[sSearch_4]:
aoData[bRegex_4]:false
aoData[bSearchable_4]:true
aoData[sSearch_5]:
aoData[bRegex_5]:false
aoData[bSearchable_5]:true
aoData[sSearch_6]:
aoData[bRegex_6]:false
aoData[bSearchable_6]:true
aoData[sSearch_7]:
aoData[bRegex_7]:false
aoData[bSearchable_7]:true
aoData[sSearch_8]:
aoData[bRegex_8]:false
aoData[bSearchable_8]:true
aoData[sSearch_9]:
aoData[bRegex_9]:false
aoData[bSearchable_9]:true
aoData[sSearch_10]:
aoData[bRegex_10]:false
aoData[bSearchable_10]:true
aoData[sSearch_11]:
aoData[bRegex_11]:false
aoData[bSearchable_11]:true
aoData[sSearch_12]:
aoData[bRegex_12]:false
aoData[bSearchable_12]:true
aoData[sSearch_13]:
aoData[bRegex_13]:false
aoData[bSearchable_13]:true
aoData[sSearch_14]:
aoData[bRegex_14]:false
aoData[bSearchable_14]:true
aoData[sSearch_15]:
aoData[bRegex_15]:false
aoData[bSearchable_15]:true
aoData[sSearch_16]:
aoData[bRegex_16]:false
aoData[bSearchable_16]:true
aoData[sSearch_17]:
aoData[bRegex_17]:false
aoData[bSearchable_17]:true
aoData[sSearch_18]:
aoData[bRegex_18]:false
aoData[bSearchable_18]:true
aoData[sSearch_19]:
aoData[bRegex_19]:false
aoData[bSearchable_19]:true
aoData[sSearch_20]:
aoData[bRegex_20]:false
aoData[bSearchable_20]:true
aoData[sSearch_21]:
aoData[bRegex_21]:false
aoData[bSearchable_21]:true
aoData[sSearch_22]:
aoData[bRegex_22]:false
aoData[bSearchable_22]:true
aoData[sSearch_23]:
aoData[bRegex_23]:false
aoData[bSearchable_23]:true
aoData[sSearch_24]:
aoData[bRegex_24]:false
aoData[bSearchable_24]:true
aoData[sSearch_25]:
aoData[bRegex_25]:false
aoData[bSearchable_25]:true
aoData[sSearch_26]:
aoData[bRegex_26]:false
aoData[bSearchable_26]:true
aoData[sSearch_27]:
aoData[bRegex_27]:false
aoData[bSearchable_27]:true
aoData[sSearch_28]:
aoData[bRegex_28]:false
aoData[bSearchable_28]:true
aoData[sSearch_29]:
aoData[bRegex_29]:false
aoData[bSearchable_29]:true
aoData[sSearch_30]:
aoData[bRegex_30]:false
aoData[bSearchable_30]:true
aoData[sSearch_31]:
aoData[bRegex_31]:false
aoData[bSearchable_31]:true
aoData[sSearch_32]:
aoData[bRegex_32]:false
aoData[bSearchable_32]:true
aoData[sSearch_33]:
aoData[bRegex_33]:false
aoData[bSearchable_33]:true
aoData[sSearch_34]:
aoData[bRegex_34]:false
aoData[bSearchable_34]:true
aoData[sSearch_35]:
aoData[bRegex_35]:false
aoData[bSearchable_35]:true
aoData[sSearch_36]:
aoData[bRegex_36]:false
aoData[bSearchable_36]:true
aoData[sSearch_37]:
aoData[bRegex_37]:false
aoData[bSearchable_37]:true
aoData[sSearch_38]:
aoData[bRegex_38]:false
aoData[bSearchable_38]:true
aoData[sSearch_39]:
aoData[bRegex_39]:false
aoData[bSearchable_39]:true
aoData[sSearch_40]:
aoData[bRegex_40]:false
aoData[bSearchable_40]:true
aoData[sSearch_41]:
aoData[bRegex_41]:false
aoData[bSearchable_41]:true
aoData[sSearch_42]:
aoData[bRegex_42]:false
aoData[bSearchable_42]:true
aoData[sSearch_43]:
aoData[bRegex_43]:false
aoData[bSearchable_43]:true
aoData[sSearch_44]:
aoData[bRegex_44]:false
aoData[bSearchable_44]:true
aoData[sSearch_45]:
aoData[bRegex_45]:false
aoData[bSearchable_45]:true
aoData[sSearch_46]:
aoData[bRegex_46]:false
aoData[bSearchable_46]:true
aoData[sSearch_47]:
aoData[bRegex_47]:false
aoData[bSearchable_47]:true
aoData[sSearch_48]:
aoData[bRegex_48]:false
aoData[bSearchable_48]:true
aoData[sSearch_49]:
aoData[bRegex_49]:false
aoData[bSearchable_49]:true
aoData[sSearch_50]:
aoData[bRegex_50]:false
aoData[bSearchable_50]:true
aoData[sSearch_51]:
aoData[bRegex_51]:false
aoData[bSearchable_51]:true
aoData[sSearch_52]:
aoData[bRegex_52]:false
aoData[bSearchable_52]:true
aoData[sSearch_53]:
aoData[bRegex_53]:false
aoData[bSearchable_53]:true
aoData[sSearch_54]:
aoData[bRegex_54]:false
aoData[bSearchable_54]:true
aoData[sSearch_55]:
aoData[bRegex_55]:false
aoData[bSearchable_55]:true
aoData[iSortCol_0]:4
aoData[sSortDir_0]:desc
aoData[iSortingCols]:1
aoData[bSortable_0]:true
aoData[bSortable_1]:true
aoData[bSortable_2]:true
aoData[bSortable_3]:true
aoData[bSortable_4]:true
aoData[bSortable_5]:true
aoData[bSortable_6]:true
aoData[bSortable_7]:true
aoData[bSortable_8]:true
aoData[bSortable_9]:true
aoData[bSortable_10]:true
aoData[bSortable_11]:true
aoData[bSortable_12]:true
aoData[bSortable_13]:true
aoData[bSortable_14]:true
aoData[bSortable_15]:true
aoData[bSortable_16]:true
aoData[bSortable_17]:true
aoData[bSortable_18]:true
aoData[bSortable_19]:true
aoData[bSortable_20]:true
aoData[bSortable_21]:true
aoData[bSortable_22]:true
aoData[bSortable_23]:true
aoData[bSortable_24]:true
aoData[bSortable_25]:true
aoData[bSortable_26]:true
aoData[bSortable_27]:true
aoData[bSortable_28]:true
aoData[bSortable_29]:true
aoData[bSortable_30]:true
aoData[bSortable_31]:true
aoData[bSortable_32]:true
aoData[bSortable_33]:true
aoData[bSortable_34]:true
aoData[bSortable_35]:true
aoData[bSortable_36]:true
aoData[bSortable_37]:true
aoData[bSortable_38]:true
aoData[bSortable_39]:true
aoData[bSortable_40]:true
aoData[bSortable_41]:true
aoData[bSortable_42]:true
aoData[bSortable_43]:true
aoData[bSortable_44]:true
aoData[bSortable_45]:true
aoData[bSortable_46]:true
aoData[bSortable_47]:true
aoData[bSortable_48]:true
aoData[bSortable_49]:true
aoData[bSortable_50]:true
aoData[bSortable_51]:true
aoData[bSortable_52]:true
aoData[bSortable_53]:true
aoData[bSortable_54]:true
aoData[bSortable_55]:true
aoData[sRangeSeparator]:~
aoData[sharing_key]:
treeQuery[boolean]:AND
treeQuery[members][0][field]:lookup
treeQuery[members][0][operator]:LIKE
treeQuery[members][0][value]:val1
es:false
customScoreWeights[web]:0
customScoreWeights[mobile_downloads]:1
customScoreWeights[twitter_mentions]:1
customScoreWeights[facebook_talking_count]:0
customScoreWeights[employees]:0"""


# set cookie each time
header_string = """Accept:*/*
Accept-Encoding:gzip, deflate, br
Accept-Language:en-US,en;q=0.8
Connection:keep-alive
Content-Length:9318
Content-Type:application/x-www-form-urlencoded; charset=UTF-8
Cookie: gsScrollPos-505=; _hjIncludedInSample=1; _okdetect=%7B%22token%22%3A%2215073056288780%22%2C%22proto%22%3A%22https%3A%22%2C%22host%22%3A%22mattermark.com%22%7D; session=ssst2rqq80qi6fmreiomhpblq1; last_seen=1507305661960; _ok=2129-165-10-5506; contextly=%7B%22id%22%3A%22GC8Kh6KxJfrCOYBI1HkgDq4na%22%7D; messagesUtk=72322e7ee70d9dacb5f7789374145a4e; _okbk=cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1508593182165%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C; olfsk=olfsk6599495194673957; wcsid=HJcnOzIfOHFl8Byn6o5pG0V08K0JEBt0; hblid=MUJUgvzqAZ3WR3qb6o5pG0V08K0JE36r; _oklv=1508596150168%2CHJcnOzIfOHFl8Byn6o5pG0V08K0JEBt0; ln=3f3ae26f1435d1c29e8e6c9360273aad82b0e255%7ELSsibWMvmiMcIEWomudO060gu%2B1REB0EOcZodAqW%2FYk%3D; api_authentication_token=0e9b1506f2371e8b6d88bd6e5007405cbec4907b%7E068e59fe00b6e3b2276ca0c64ab89424332c2609772daaab384a1bc319e0ddcd; optimizelyEndUserId=oeu1507305626694r0.8958100235562194; _ga=GA1.2.1093259035.1507305627; _gid=GA1.2.814967103.1509996690; ajs_group_id=null; ajs_user_id=%221019%22; ajs_anonymous_id=%22d2f77d39-70bb-46ac-b665-8d94421c858b%22; _pendo_meta.325571ac-f7f5-4d10-5263-e5a560f9c317=1258628793; _pendo_visitorId.325571ac-f7f5-4d10-5263-e5a560f9c317=1019; __hstc=268945070.72322e7ee70d9dacb5f7789374145a4e.1507305662658.1508595055923.1509996690190.12; __hssrc=1; __hssc=268945070.3.1509996690190; hubspotutk=72322e7ee70d9dacb5f7789374145a4e; _hp2_ses_props.1103682097=%7B%22r%22%3A%22https%3A%2F%2Fmattermark.com%2Fapp%2F%22%2C%22ts%22%3A1509996735699%2C%22d%22%3A%22mattermark.com%22%2C%22h%22%3A%22%2Fapp%2Fdata%22%7D; _hp2_id.1103682097=%7B%22userId%22%3Anull%2C%22pageviewId%22%3A%228478967855716460%22%2C%22sessionId%22%3A%228756403095270133%22%2C%22identity%22%3A%221019%22%2C%22trackerVersion%22%3A%223.0%22%7D
Host:mattermark.com
Origin:https://mattermark.com
Referer:https://mattermark.com/app/data?operator[0]=lookup%09LIKE%09val1&sortBy=cached_growth_score&sortDirection=desc&score_mobile_downloads=1&score_twitter_mentions=1
User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36
X-Requested-With:XMLHttpRequest"""


def next_button(class_val):
    return class_val and "btn" in class_val and "float_right" in class_val and "btn_small" in class_val and "btn_outline" not in class_val


def get_domain_from_url(url_string):
    matches = re.findall(r"[\.|/]([a-z0-9]+\.[^/^.]+)/", url_string)
    return matches[0] if matches else None


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii


def extract_text_from_tag(tag):
    matches = re.findall(r">([^<]+)", tag)
    if matches:
        return matches[0]
    else:
        return None


def find_company_data_by_name(company_name="Polly"):
    # return cos.get(company_name, None)
    url = "https://mattermark.com/app/data/get/"
    url_company_name = urllib.quote_plus(company_name)

    data_list = data_string.replace("val1", url_company_name).replace("lookup", "keywords").split("\n")
    data_dict = dict( [ (data_pair.partition(":")[0], data_pair.partition(":")[2] ) for data_pair in data_list ] )

    header_list = header_string.replace("val1", url_company_name).replace("lookup", "keywords").split("\n")
    header_dict = dict( [ (header_pair.partition(":")[0], header_pair.partition(":")[2] ) for header_pair in header_list ] )
    
    tries = 3
    while tries > 0:
        try:
            resp = requests.post(url, data=data_dict, headers=header_dict)
            print resp
            if "40" in str(resp):
                print resp.text
            the_json = resp.json()
            the_results = the_json.get("aaData", [])

            for result in the_results:
                if company_name.lower() in result.get("company_name", "").lower():
                    return result
            break
        except Exception, e:
            requests.get("https://mattermark.com/app/data", headers=header_dict)
            tries -= 1
            print "sleeping\r"
            time.sleep(random.randint(2,5))
            print "sleeping... done"
            
    return None


def grab_matter_mark_data():
    new_companies = Company.objects.filter(data_retrieved=False)

    old_companies_to_update = Company.objects.filter(date_data_retrieved__gt=datetime.datetime.now() - datetime.timedelta(days=settings.NUMBER_OF_MONTHS * 30))

    # columns_data = {
    #                 "stage": "total_funding",
    #                 "total_funding": "total_funding",
    #                 "last_funding_date": "last_funding_date",
    #                 "last_funding_amount": "last_funding_amount",
    #                 "company_name": 31,
    #                 "domain": 32,
    #             }

    for new_company in new_companies:
        company_dict = find_company_data_by_name(new_company.name)

        if company_dict:
            print "got valid company for %s!" % new_company.name
        else:
            print "no valid company for %s...\n-----" % new_company.name
            continue

        misses = 0
        current_series = extract_text_from_tag( company_dict.get("stage") )
        print "current_series", current_series

        if current_series:
            new_company.current_series = current_series
        else:
            misses += 1
        
        total_funding = extract_text_from_tag( company_dict.get("total_funding") )
        print "total_funding", total_funding
        total_funding = re.sub(r'[^\d.MB]', '', total_funding)

        if total_funding.endswith("M"):
            total_funding = int(float(total_funding[:-1]) * 1000000)
        elif total_funding.endswith("B"):
            total_funding = int(float(total_funding[:-1]) * 1000000000)

        print "processed total_funding", total_funding
        if total_funding:
            new_company.total_funding = total_funding
        else:
            misses += 1
        

        last_funding_date = company_dict.get("last_funding_date")
        print "last_funding_date", last_funding_date
        if last_funding_date:
            new_company.last_funding_date = datetime.datetime.strptime(last_funding_date, "%Y-%m-%d")
        else:
            misses += 1
        
        

        last_funding_amount = company_dict.get("last_funding_amount")
        print "last_funding_amount", last_funding_amount

        last_funding_amount = re.sub(r'[^\d.MB]', '', last_funding_amount)
        if last_funding_amount.endswith("M"):
            last_funding_amount = int(last_funding_amount[:-1]) * 1000000
        elif last_funding_amount.endswith("B"):
            last_funding_amount = int(last_funding_amount[:-1]) * 1000000000
        print "processed last_funding_amount", last_funding_amount

        if last_funding_amount:
            new_company.last_funding_amount = last_funding_amount
        else:
            misses += 1

        retrieved_name = extract_text_from_tag( company_dict.get("company_name") )
        print "retrieved_name", retrieved_name
        new_company.retrieved_name = retrieved_name

        if last_funding_amount:
            new_company.last_funding_amount = last_funding_amount
        else:
            misses += 1


        # for key, col in columns_data.items():
        #     data = company_dict.get(key)
        #     if key in ["stage", "total_funding", "company_name", "domain"]:
        #         data = extract_text_from_tag(data)
        #     print key, data
            
        
        new_company.data_retrieved = True
        new_company.valid_candidate = misses < 3 and not re.search('exited', new_company.current_series, re.IGNORECASE)
        new_company.date_data_retrieved = datetime.datetime.now()
        new_company.save()
        
        print "-----"
        print "sleeping\r"
        time.sleep(random.randint(2,5))
        print "sleeping... done"
        


grab_matter_mark_data()
sys.exit()
