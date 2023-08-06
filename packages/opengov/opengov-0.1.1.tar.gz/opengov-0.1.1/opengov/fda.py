''' FDA Module '''
import requests
from .utils import *

fda_base_url = "https://api.fda.gov"
endpoint_field_list = ["drug", "animalandveterinary", "device", "food", "other"]
file_name_dict = dict()

# Populate file dictionary with names of JSON files
file_names = ['AdverseEvents', 'ProductLabeling', 'NDC', 'RecallReports', '501k', 'DeviceClassification', 'NSDE', 'Substance']
file_name_dict['AdverseEvents'] = 'event.json'
file_name_dict['ProductLabeling'] = 'label.json'
file_name_dict['NDC'] = 'ndc.json'
file_name_dict['RecallReports'] = 'enforcement.json'
file_name_dict['501k'] = '501k.json'
file_name_dict['DeviceClassification'] = 'classification.json'
file_name_dict['NSDE'] = 'nsde.json'
file_name_dict['Substance'] = 'substance.json'

# Get the raw FDA JSON
def raw_fda(endpoint_type: str, file_name: str, search: str = "", sort: str = "", count: str = "", limit: str = "", skip: str = ""):
    if endpoint_type not in endpoint_field_list:
        raise InputError('Please provide a valid endpoint name.')
    endpoint_type = "drug"
    file_name = file_name_dict['NDC']
    url = constructFDAEndpoint(fda_base_url, endpoint_type, file_name, search, sort, count, limit, skip)
    r = requests.get(url)
    return r.content

def raw_fda_help():
    print("raw_FDA VARIABLES: ")
    print("============")
    print("endpoint_type: str => " + str(endpoint_field_list))
    print("file_name: str => " + str(file_names))
    print("search: str => Default: Empty String")
    print("sort: str => Default: Empty String")
    print("count: str => Default: Empty String")
    print("limit: str => Default: Empty String")
    print("skip: str => Default: Empty String")

#def ndc_id_lookup(id: str):
