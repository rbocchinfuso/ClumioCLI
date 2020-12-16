#!/home/cabox/miniconda3/envs/clumio/bin/python3
# conda activate clumio
# pip install -r requirements.txt

'''
Python CLI wrapper for the Clumio API

Usage:
  clumio-cli.py getvcs
  clumio-cli.py getvms
  clumio-cli.py backup <group>
  clumio-cli.py groups
  clumio-cli.py config
  clumio-cli.py (-h | --help)
  clumio-cli.py --version

Options:
  -h --help             Show this screen.
  --version             Show version.
  
Commands:
  getvcs                Query Clumio API to get vCenter(s) ID
  getvms                Query and build VM List via Clumio API.
  backup <group>        Initiate Clumio on-demand backup for VMs in group.
  groups                List group KEY : VALUE (group : vm list) pairs.
  config                List all config KEY : VALUE pairs.
'''

# Generic/Built-in
import requests
import json
import sys
import jsontable
import ast
import numpy
import pandas as pd
import configparser
from tabulate import tabulate
from jsonpath_ng import jsonpath, parse
from docopt import docopt
from rich import print as rprint
from rich.panel import Panel
from rich.progress import track
from rich.console import Console
from rich.table import Table
from colorama import Fore, Back, Style

# owned
__author__ = 'Rich Bocchinfuso'
__copyright__ = 'Copyright 2020, Clumio API Wrapper'
__credits__ = ['Rich Bocchinfuso']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Rich Bocchinfuso'
__email__ = 'rbocchinfuso@gmail.com'
__status__ = 'Dev'


def log(message):
    console = Console(width=220)
    style = "yellow"
    if DEBUG == "True":
        console.log(Panel(str(message), title="DEBUG OUTPUT", style=style))
              

def vm_table(data):
    # print json data as table
    paths = [
                {"$._embedded.items.name":"vm_name"},
                {"$._embedded.items.id":"id"},
                {"$._embedded.items.last_backup_timestamp":"last_backup_timestamp"},
                {"$._embedded.items.compliance_status":"compliance_status"},
                {"$._embedded.items.protection_status":"protection_status"},
#                 {"$._embedded.items.datacenter.name":"datacenter_name"},
#                 {"$._embedded.items.host.name":"host_name"},
#                 {"$._embedded.items.vm_folder.name":"vm_folder"}
            ]

    # create an instance of a converter
    converter = jsontable.converter()
    # set the paths you want to extract
    converter.set_paths(paths)
    # input a JSON to be interpreted
    table = (converter.convert_json(data))
    log(table)
    log(tabulate(table, headers="firstrow", tablefmt="grid"))
    return(table)


def vc_table(data):
    # json data as table
    paths = [
                {"$._embedded.items.id":"id"},
                {"$._embedded.items.type":"type"},
                {"$._embedded.items.ip_address":"ip_address"},
                {"$._embedded.items.endpoint":"endpoint"},
                {"$._embedded.items.status":"status"},
                {"$._embedded.items.backup_region":"backup_region"},
                {"$._embedded.items.cloud_connector_download_url":"cloud_connector_download_url"}
            ]

    # create an instance of a converter
    converter = jsontable.converter()
    # set the paths you want to extract
    converter.set_paths(paths)
    # input a JSON to be interpreted
    table = (converter.convert_json(data))
    log(table)
    print(tabulate(table, headers="firstrow", tablefmt="grid"))
    return(table)


def my_df(alldf,table,i):
      ## write json to file
#     with open('vms.json', 'w') as f:
#         print(s, file=f)    
    if i == 1:
        d = numpy.array(table)
        df = pd.DataFrame(d)
        new_header = df.iloc[0] #grab the first row for the header
        df = df[1:] #take the data less the header row
        df.columns = new_header #set the header row as the df header
        log(df)
        alldf = pd.concat([alldf,df])
        log(df.to_string(index=False))
    else:
        d = numpy.array(table)
        df = pd.DataFrame(d)
        new_header = df.iloc[0] #grab the first row for the header
        df = df[1:] #take the data less the header row
        df.columns = new_header #set the header row as the df header
        log(df)
        alldf = pd.concat([alldf,df])
        log(alldf.to_string(index=False))    
    return(alldf)
        

def get_pages(data):
    ## get page count
    total_pages_count = parse('$.total_pages_count')
    pages = (total_pages_count.find(data)[0].value)
    log(pages)   
    return(pages)

    
def my_request(base_url,api_path,headers,params):
    response = requests.request('GET', base_url + api_path, headers=headers, params = params)

    my_bytes_value = response.text.encode('utf8')
    log(my_bytes_value)

    ## Decode UTF-8 bytes to Unicode, and convert single quotes 
    ## to double quotes to make it valid JSON
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    log(my_json)
    log('- ' * 20)

    ## Load the JSON to a Python list & dump it back out as formatted JSON
    data = json.loads(my_json)
    s = json.dumps(data, indent=4)
    log(s)
    return(data)

def headers_func():
    headers = {
      'Accept': config['api']['accept_header'],
      'Content-Type':config['api']['content_type_header'],
      'Authorization': config['api']['bearer_token_header']
    }
    return(headers)


def start_backup(group):
    vcenter_id = config['vcenter']['id']
    base_url = config['api']['base_url']
    backup_api_path = '/backups/vmware/vms'
    url = (base_url + backup_api_path)
    headers = headers_func()
    df = pd.read_csv ('vms.csv')
    print(df)
    vm_list = ast.literal_eval(config.get("backup_groups", group))
    rprint(Panel('[green]START: Attempting to Start on-demand backup for group ' + group + ' via Clumio API', title="EXECUTION STATUS"))
    log(type(vm_list))
    log(vm_list)
    for vm in vm_list:
        print (Fore.CYAN + Style.BRIGHT + 'Starting backup on-demand backup for: ' + vm + Style.RESET_ALL)
        for index, row in df.iterrows():
            if (row['vm_name'] == vm):       
                vmName = (row['vm_name'])
                log ('VM Name: ' + vmName)
                ID = (row['id'])
                log ('VM ID: ' + ID)
                data = {'vcenter_id': vcenter_id, 'vm_id': ID}
                payload = json.dumps(data)
                response = requests.request('POST', url, headers=headers, data=payload)
                print(response.text)

                
def get_vcs():                
    vcenter_id = config['vcenter']['id']
    limit = config['api']['limit']
    base_url = config['api']['base_url']
    get_vc_api_path = '/datasources/vmware/vcenters'
    params = {'limit': limit}
    headers = headers_func()
    data = my_request(base_url,get_vc_api_path,headers,params)
    pages = get_pages(data)
    table = vc_table(data)
                

def get_vms():
    vcenter_id = config['vcenter']['id']
    limit = config['api']['limit']
    base_url = config['api']['base_url']
    get_vm_api_path = '/datasources/vmware/vcenters/' + vcenter_id + '/vms'

    # params = {'limit': '<limit>', 'start': '<start>', 'filter': '<filter>'}
    params = {'limit': limit}
    headers = headers_func()

    data = my_request(base_url,get_vm_api_path,headers,params)
    pages = get_pages(data)

    alldf = pd.DataFrame([])
    vm_table(data)
    rprint(Panel('[cyan]START: Fething and Building VM List via Clumio API', title="EXECUTION STATUS"))
    i = 1
    for i in track(range(1, int(pages))):
        print(Fore.CYAN + Style.BRIGHT + '...Fetching page ' + str(i) + ' from Clumio API...' + Style.RESET_ALL)
        get_vm_api_path = ('/datasources/vmware/vcenters/' + vcenter_id + '/vms?limit=' + limit + '&start=' + str(i))
        log(get_vm_api_path)
        data = my_request(base_url,get_vm_api_path,headers,params)
        table = vm_table(data)
        alldf = my_df (alldf,table,i)
    rprint(Panel('[green]DONE: Fething VM List via Clumio API', title="EXECUTION STATUS"))
    rprint(Panel('[cyan]START: Create DataFrame', title="EXECUTION STATUS"))
    print(alldf)
    rprint(Panel('[cyan]START: Writing DataFrame to vms.csv for future use', title="EXECUTION STATUS"))
    alldf.to_csv('vms.csv', index=False)
    rprint(Panel('[green]DONE: Writing DataFrame to vms.csv', title="EXECUTION STATUS"))


def list_config():
    table = Table(title="Configuration Key:Value Pairs")
    table.add_column("Key", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    for each_section in config.sections():
        for (each_key, each_val) in config.items(each_section):
            table.add_row(each_key, each_val)
    console = Console()
    console.print(table)

    
def list_groups():
    table = Table(title="Backup Groups Key:Value Pairs")
    table.add_column("Key", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    for (each_key, each_val) in config.items('backup_groups'):
        table.add_row(each_key, each_val)
    console = Console()
    console.print(table)
    
    
if __name__ == '__main__':
    # read and parse config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    DEBUG = config['local']['DEBUG']
    log(DEBUG)
    
    arguments = docopt(__doc__, version='Python CLI wrapper for the Clumio API - v0.1.0')
    if arguments['getvcs']:
        get_vcs()
    elif arguments['getvms']:
        get_vms()
    elif arguments['backup']:
        start_backup(arguments['<group>'])
    elif arguments['config']:
        list_config()
    elif arguments['groups']:
        list_groups()
    else:
        exit("{0} is not a command. \
          See 'clumio-cli.py --help'.".format(arguments['<command>']))

        
