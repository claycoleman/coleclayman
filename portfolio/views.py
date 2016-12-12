import requests

from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from .models import *
from .forms import *

# Create your views here.


def home(request):
    context = {}
    context['home'] = True
    projects = Project.objects.all()
    for project in projects:
        project.create_slug()
        print project
    context['projects'] = projects
    categories = Category.objects.all()
    for category in categories:
        category.create_slug()
    context['categories'] = categories
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        context['form'] = form
        print "hello"
        if form.is_valid():
            print 'yikes'
            send_mail("coleclayman portfolios: %s" % form.cleaned_data['name'], form.cleaned_data['message'] + "\n" + form.cleaned_data['phone'], form.cleaned_data['email'], [settings.EMAIL_HOST_USER], fail_silently=False)
            return render(request, 'thanks.html')
    else:
        form = ContactForm()
        context['form'] = form


    return render_to_response('home.html', context, context_instance=RequestContext(request))


def video_call(request, pk, slug=None):
    context = {}

    video_call = VideoCall.objects.get(pk=pk)

    context['video_call'] = video_call
    context['create'] = True if slug == "parent" else False

    return render(request, 'video_call.html', context)


@csrf_exempt
def video_call_ajax(request):
    if request.POST:
        username = request.POST.get('atypical', False)
        password = request.POST.get('more_atypical', False)

        if not username and password:
            return HttpResponse("bad call")

        # auth_user = authenticate(username=username, password=password)

        # if auth_user is None:
        if username != 'atypical' and password != 'more_atypical'
            return HttpResponse("bad credentials")

        val = request.POST.get('val', '').strip()
        number = request.POST.get('number', '').strip()
        pk = request.POST.get('pk', '').strip()

        try:
            video_call = VideoCall.objects.get(pk=pk)
        except Exception as e:
            return HttpResponse('bad pk')

        if not val or not number:
            return HttpResponse('incomplete call')

        if number == '1':
            video_call.p1_key = val
            video_call.p2_key = ""
            video_call.save()

        if number == '2':
            video_call.p2_key = val
            video_call.save()

        return HttpResponse('success')

    if request.GET:
        username = request.GET.get('atypical', False)
        password = request.GET.get('more_atypical', False)

        if not username and password:
            return HttpResponse("bad call")

        auth_user = authenticate(username=username, password=password)

        if auth_user is None:
            return HttpResponse("bad credentials")

        number = request.GET.get('number', '').strip()
        pk = request.GET.get('pk', '').strip()

        try:
            video_call = VideoCall.objects.get(pk=pk)
        except Exception as e:
            return HttpResponse('bad pk')

        if not number:
            return HttpResponse('incomplete call')

        if number == '1':
            return HttpResponse('%s' % video_call.p1_key)

        if number == '2':
            return HttpResponse('%s' % video_call.p2_key)

        return HttpResponse('bad number call')

    return HttpResponse("bad method")

def ugf(request):
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


    return render_to_response('ugf.html', context, context_instance=RequestContext(request))


class ProjectDetailView(DetailView):
    model = Project
    template_name = "project_detail.html"
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['projects'] = Project.objects.all()[:4]

        return context


def check_cra_address(address):
    return_dict = {}

    payload = {
        'Host': 'geomap.ffiec.gov',
        'Connection': 'keep-alive',
        'Content-Length': 82,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://geomap.ffiec.gov',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'Referer': 'https://geomap.ffiec.gov/FFIECGeocMap/GeocodeMap1.aspx',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cookie': 'BIGipServergeomap.ffiec.gov.app~geomap.ffiec.gov_pool=2638334084.20480.0000; _ga=GA1.2.130982089.1469575894; _gat=1',
    }

    
    geocode_url = 'https://geomap.ffiec.gov/FFIECGeocMap/GeocodeMap1.aspx/GetGeocodeData'
    geocode_data = '{sSingleLine: "%s", iCensusYear: "2016"}' % (address)

    geo_resp = requests.post(geocode_url, data=geocode_data, headers=payload)


    try:
        geo_json = geo_resp.json().get('d', False)
    except Exception, e:
        return_dict['success'] = False
        return_dict['message'] = "bad request; no json() - " + geo_resp.text

        return return_dict

    if not geo_json:
        return_dict['success'] = False
        return_dict['message'] = "bad request; has json but no d"
        
        return return_dict


    if geo_json.get('iCensusYear') < 10:
        return_dict['success'] = False
        return_dict['message'] = 'fail, here is the message: ' + geo_json.get('sMsg')
        
        return return_dict

    address_string = "%s<br>%s<br>%s<br>%s" % ( geo_json.get('sAddress'), 
                                                      geo_json.get('sCityName'),
                                                      geo_json.get('sCountyName'),
                                                      geo_json.get('sStateName') )


    url = 'https://geomap.ffiec.gov/FFIECGeocMap/GeocodeMap1.aspx/GetCensusDataNoMSA'

    state_code = geo_json.get('sStateCode')
    county_code = geo_json.get('sCountyCode')
    tract_code = geo_json.get('sTractCode')

    data = '{sStateCode: "%s", sCountyCode: "%s", sTractCode: "%s", iCensusYear: "2016"}' % (state_code, county_code, tract_code)
    response = requests.post(url, data=data, headers=payload)

    json = response.json()
    # print json.get('d')
    income_json = json.get('d', {'sIncome_Indicator': 'Failed request.'})
    income_level = income_json.get('sIncome_Indicator', 'Failed request.')

    if "Failed request." in income_level:
        return_dict['success'] = False
        return_dict['message'] = "Bad json of second url"
        
        return return_dict

    est_income = float( income_json.get('sEst_Income') )
    tract_income = float( income_json.get('sHUD_est_MSA_MFI') )

    lowest_income = min(est_income, tract_income)
    min_income = lowest_income * 0.8


    print 'Income Level for above address is:', income_level
    print "CRA Qualified:", "Yes!" if income_level == "Low" or income_level == "Moderate" else "No..."

    cra_qualified = income_level == "Low" or income_level == "Moderate"
    
    return_dict['cra_qualified'] = cra_qualified
    return_dict['address'] = address_string
    return_dict['min_income'] = int(min_income)
    return_dict['income_level'] = income_level
    return_dict['success'] = True

    return return_dict


def check_naics_code(naics_code):
    print naics_code
    response = requests.get('https://www.federalregister.gov/articles/2016/01/26/2016-00924/small-business-size-standards-for-manufacturing')

    text = response.text

    match = '<td class="">%s</td>' % naics_code

    if match in text:
        text = text.partition(match)[2].partition('</td>')[2]
        num_employees = text.partition('<td>')[2].partition('</td>')[0]
        # print "match in text"
        # print "num_employees", num_employees
        return {'success': True, 'num_employees': num_employees }
    else:
        # print "no match in text"
        return {'success': False, }

