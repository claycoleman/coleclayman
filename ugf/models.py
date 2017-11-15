import re
import requests
import datetime
import json
import time

from django.conf import settings
from django.db import models

# hopefully things are passed in like this
ROUND_TYPES = (
    ("Seed", "seed"),
    ("Pre-Series A", "pre-series-a"),
    ("Series A", "a"),
    ("Series B", "b"),
    ("Series C", "c"),
    ("Series D", "d"),
    ("Exited (acquired)", "acquired"),
    ("Exited (IPO)", "ipo"),
    ("Series E", "e"),
    ("Series F", "f"),
    ("Series G", "g"),
    ("Series H", "h"),
    ("Series J", "j"),
    ("Series I", "i"),
    ("Series I", "i"),
)

class Company(models.Model):
    """Model definition for Company."""
    hubspot_id = models.IntegerField(null=True, blank=True, unique=True)

    name = models.CharField(max_length=255)
    domain = models.CharField(null=True, blank=True, max_length=255)
    retrieved_name = models.CharField(null=True, blank=True, max_length=255)

    zip_code = models.CharField(null=True, blank=True, max_length=255)
    state = models.CharField(null=True, blank=True, max_length=255)
    city = models.CharField(null=True, blank=True, max_length=255)
    country = models.CharField(null=True, blank=True, max_length=255)

    employee_count = models.IntegerField(null=True, blank=True)
    source = models.ForeignKey("Source", null=True, blank=True)

    # make a request to Mattermark to initially get this data
    mattermark_id = models.CharField(null=True, blank=True, max_length=50)
    
    # standardize how things are passed in: Series A -> a, Series b -> b, Exited (ipo) -> ipo, etc
    current_series = models.CharField(null=True, blank=True, max_length=255)
    last_funding_date = models.DateTimeField(null=True, blank=True)
    last_funding_amount = models.BigIntegerField(default=0.0)
    total_funding = models.BigIntegerField(default=0.0)

    date_created = models.DateTimeField(auto_now_add=True)

    valid_candidate = models.BooleanField(default=True)

    data_retrieved = models.BooleanField(default=False)
    data_pushed_to_hubspot = models.BooleanField(default=False)
    data_can_retrieved = models.BooleanField(default=True)
    date_data_retrieved = models.DateTimeField(null=True, blank=True)

    next_interaction_date = models.DateField(null=True, blank=True)
    should_alert_next_interaction = models.BooleanField(default=False)

    # should we get mattermark / growth score? Could be interesting way to measure these

    class Meta:
        """Meta definition for Company."""
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __unicode__(self):
        """Unicode representation of Company."""
        return self.name

    def get_last_funded_date(self):
        return self.last_funding_date


    def grab_hubspot_data(self):
        # make a request to the HubSpot db to get Company info
        resp = requests.get("https://api.hubapi.com/companies/v2/companies/%d?hapikey=%s&userId=%s" % (self.hubspot_id, settings.HUBSPOT_HAPI_KEY, settings.HUBSPOT_USER_ID) )
        print resp
        resp = resp.json()
        props = resp.get("properties", False)
        
        if not props:
            # we didn't get a valid company back which is weird because we JUST got a company from them
            return False
        
        # save it, then make mattermark request
        self.name = get_hubspot_value_for_property(props, 'name')
        self.domain = get_hubspot_value_for_property(props, 'domain')
        self.save()

        return True


    def grab_mattermark_data(self):
        search_url = "https://api.mattermark.com/companies/%s?key=%s" % (self.mattermark_id, settings.MATTERMARK_API_KEY)
        resp = requests.get(search_url)
        resp = resp.json()

        misses = 0

        self.domain = resp.get('website')
        self.zip_code = resp.get("zip")
        self.state = resp.get("state")
        self.city = resp.get("city")
        self.country = resp.get("country")

        employee_count = resp.get('employee_count')[0].get("score", "0") if resp.get('employee_count') else 0
        self.employee_count = int(employee_count) if employee_count else None
        
        self.total_funding = int(resp.get("total_funding")) if resp.get('total_funding') else None
        if not self.total_funding:
            misses += 1
        self.last_funding_amount = int(resp.get("last_funding_amount")) if resp.get('last_funding_amount') else None
        if not self.last_funding_amount:
            misses += 1
        
        last_funding_date = resp.get('last_funding_date', None)
        if last_funding_date:
            last_funding_date = datetime.datetime.strptime(last_funding_date, "%Y-%m-%d")
        
        self.last_funding_date = last_funding_date
        if not self.last_funding_date:
            misses += 1

        self.current_series = resp.get("stage")
        if not self.current_series:
            misses += 1

        self.data_retrieved = True
        self.date_data_retrieved = datetime.datetime.now()

        for index, funding_round in enumerate(resp.get("funding")):
            series = funding_round.get("series", "")
            amount = int( funding_round.get("amount") ) if funding_round.get("amount") else None
            funding_date = funding_round.get("funding_date", "")
            
            if not series or amount or funding_date:
                continue

            if funding_date:
                funding_date = datetime.datetime.strptime(funding_date, "%Y-%m-%d")

            new_funding_round = FundingRound.objects.create(amount=amount, series=series, funding_date=funding_date, company=self, funding_number=index)
            for investor in funding_round.get("investors").split(", "):
                new_investor, created = Investor.objects.get_or_create(name=investor)
                new_investor.companies.add(self)
                new_investor.funding_rounds.add(new_funding_round)
                new_investor.save()

            new_funding_round.save()
        
        self.valid_candidate = misses < 3 and not re.search('exited', self.current_series, re.IGNORECASE)
        self.save()

        self.update_funding_predictors()
        
        
    def update_funding_predictors(self):
        fundings = list(self.fundinground_set.order_by("funding_number"))
        for i in xrange(0, len(fundings) - 1):
            curr_funding = fundings[i]
            if not fundings[i+1].funding_date and curr_funding.funding_date:
                continue
            rp, created = RoundPredictor.objects.get_or_create(current_series=curr_funding.series)
            rp.add_new_data_point( (fundings[i+1].funding_date - curr_funding.funding_date).days )
        
    
    def update_hubspot_with_data(self):
        if not self.data_retrieved:
            return 

        data = {
            "properties": []
        }
        if self.last_funding_date:
            data.get('properties').append({
                'name': "last_funding_date",
                # timestamp in milliseconds
                'value': long(time.mktime(self.last_funding_date.date().timetuple())) * 1000,
            })

        if self.employee_count:
            data.get('properties').append({
                'name': "numberofemployees",
                'value': self.employee_count,
            })

        if self.last_funding_amount:
            data.get('properties').append({
                'name': "last_funding_amount",
                'value': self.last_funding_amount,
            })

        if self.current_series:
            data.get('properties').append({
                'name': "stage",
                'value': self.current_series,
            })
        
        # calculate date_for_next_interaction
        if self.current_series and self.last_funding_date:
            number_of_days_to_add = 365 # defaults to a year
            try: 
                predictor = RoundPredictor.objects.get(current_series=self.current_series)
                number_of_days_to_add = int(predictor.average_number_of_days)
            except Exception, e:
                pass

            td = datetime.timedelta(days=number_of_days_to_add)
           
            date_for_next_interaction = self.last_funding_date + td

            # TODO think of a way that will let UGF people simply update next date_for_next_interaction
            # that will signal to backend that we need to remind again after a date
            data.get('properties').append({
                'name': "date_for_next_interaction",
                # timestamp in milliseconds
                'value': long(time.mktime(date_for_next_interaction.date().timetuple())) * 1000,
            })
            self.should_alert_next_interaction = True
            self.next_interaction_date = date_for_next_interaction.date()

        headers = {
            "Content-Type": "application/json"
        }
        print data

        resp = requests.put("https://api.hubapi.com/companies/v2/companies/%d?hapikey=%s&userId=%s" % (self.hubspot_id, settings.HUBSPOT_HAPI_KEY, settings.HUBSPOT_USER_ID), data=json.dumps(data), headers=headers)
        print resp
        print resp.text
        self.data_pushed_to_hubspot = True
        self.save()



class Source(models.Model):
    """Model definition for Source."""

    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Source."""

        verbose_name = 'Source'
        verbose_name_plural = 'Sources'

    def __unicode__(self):
        """Unicode representation of Source."""
        return self.name


class FundingRound(models.Model):
    company = models.ForeignKey("Company")
    series = models.CharField(max_length=255)
    funding_date = models.DateTimeField(null=True, blank=True)
    amount = models.BigIntegerField(null=True, blank=True)
    funding_number = models.IntegerField(default=0)

    def __unicode__(self):
        """Unicode representation of Source."""
        return "Series %s for %s" % (self.series, self.company)


class Investor(models.Model):
    name = models.CharField(max_length=255)
    companies = models.ManyToManyField("Company")
    funding_rounds = models.ManyToManyField("FundingRound")

    def __unicode__(self):
        """Unicode representation of Source."""
        return self.name


class RoundPredictor(models.Model):
    current_series = models.CharField(null=True, blank=True, max_length=255)
    data_list = models.TextField(null=True, blank=True)
    average_number_of_days = models.FloatField(default=0)
    number_of_data_points = models.IntegerField(default=0)

    def __unicode__(self):
        """Unicode representation of Source."""
        return "series %s waits %.2f on average" % (self.current_series, self.average_number_of_days)

    def add_new_data_point(self, number_of_days):
        if self.number_of_data_points > 0:
            self.data_list += ";%d" % number_of_days
            full_weight = self.full_weight
            full_weight += number_of_days
            self.number_of_data_points += 1
            self.average_number_of_days = full_weight / self.number_of_data_points
        else:
            self.data_list = "%d" % number_of_days
            self.number_of_data_points = 1
            self.average_number_of_days = number_of_days

        self.save()

    @property
    def full_weight(self):
        return self.average_number_of_days * self.number_of_data_points


def get_hubspot_value_for_property(props, property_name):
    return props.get(property_name, {}).get('value', None)
