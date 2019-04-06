import requests
from datetime import date

def check_cra_address(address):
    return_dict = {}
    current_year = date.today().year - 1

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
    geocode_data = '{sSingleLine: "%s", iCensusYear: "%s"}' % (address, current_year)

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

    data = '{sStateCode: "%s", sCountyCode: "%s", sTractCode: "%s", iCensusYear: "%s"}' % (state_code, county_code, tract_code, current_year)
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
