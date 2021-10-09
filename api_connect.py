import requests
import json
import pandas as pd
import time
company_house_numbers =pd.read_csv('chouse_num_sample.csv')

def company_number_request(companyNumber,api_key):
    url =rf"https://api.company-information.service.gov.uk/company/{companyNumber}/charges"

    response = requests.get(url, auth=(api_key,''))
    json_search_result = response.text
    search_result = json.JSONDecoder().decode(json_search_result)
    items = search_result.get('items')
    return items

def extract_info(charge_dict):
    create_date =  charge_dict.get('created_on')
    delivered_date =  charge_dict.get('delivered_on')
    satified_date =  charge_dict.get('satisfied_on')
    if satified_date is  None:
        status = 'Outstanding'
    else:
        status = 'Satisfied'
    persons_entitiled = charge_dict.get('persons_entitled')[0].get('name')
    desc = charge_dict.get('particulars').get('description')
    charge_code =  charge_dict.get('classification').get('description')
    list = [create_date,delivered_date,status,satified_date,persons_entitiled,desc,charge_code]
    return list

def loop_for_items(items):
    master_df = pd.DataFrame()
    for item in items:
        list_temp = pd.DataFrame(extract_info(item)).T
        master_df = pd.concat([list_temp,master_df])
    return master_df


###have a rate limiter
counter = 0
master_df = pd.DataFrame()
no_charge_detail_list = []
for companyNumber in company_house_numbers['chouse_num']:
    counter+=1
    items_company_house = company_number_request(str(companyNumber))
    if (items_company_house is None) :
        no_charge_detail_list.append(str(companyNumber))
        # print(fr'no charges found for : {companyNumber}')
    else:
        temp_df = loop_for_items(items_company_house)
        temp_df['cHouse_number'] = str(companyNumber)
        master_df = pd.concat([temp_df,master_df])

    if counter==500:
        print('500 request reach - going to sleep for 6mins')
        time.sleep(6*60)

cols = ['create_date','delivered_date','status','satisfied_date','person_entitled','desc','type_charge','chouse_number']
master_df.columns = cols