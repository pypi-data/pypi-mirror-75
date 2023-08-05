import requests
import json
from requests_ntlm import HttpNtlmAuth


class login:

  def __init__(self, ip_addr):
      self.ip = ip_addr
      
      requests.packages.urllib3.disable_warnings()
    
      url = 'https://'+self.ip+':9089/api/auth'
      login = {'username': 'admin', 'password':'password'}
      payload = json.dumps(login)
    
      self.headers = {'content-type': 'application/json', 'cache-control': 'no-cache'}
      self.session = requests.Session()
      self.session.verify = False
      self.session.auth = HttpNtlmAuth('admin','password')
      auth = self.session.post(url,data = payload,headers =self.headers)
      # add if statement for proper auth response
      self.headers['Authorization'] = auth.text
      

class JSONObject:
  def __init__( self, dict ):
      vars(self).update( dict )


def SNP_reboot(ip_addr):
    snp = login(ip_addr)
    headers = snp.headers
    session = snp.session
    url = 'https://'+ip_addr+':9089/api/console/reboot'
    resp = session.post(url, headers = headers)
    resp_list = json.loads(resp.text)
    return resp_list

def SNP_confreset(ip_addr):
    snp = login(ip_addr)
    headers = snp.headers
    session = snp.session
    url = 'https://'+ip_addr+':9089/api/console/confreset'
    resp = session.post(url, headers = headers)
    resp_list = json.loads(resp.text)
    return resp_list

def SNP_factoryreset(ip_addr):
  
    snp = login(ip_addr)
    headers = snp.headers
    session = snp.session
    url = 'https://'+ip_addr+':9089/api/console/factreset'
    resp = session.post(url, headers = headers)
    resp_list = json.loads(resp.text)
    return resp_list
  
  
def SNP_get(ip_addr, url_string):
    snp = login(ip_addr)
    headers = snp.headers
    session = snp.session
    url ='https://'+ip_addr+':9089/api/'+url_string
    resp = session.get(url, headers = headers)
    return resp
  
def SNP_status(ip_addr):
    snp = login(ip_addr)
    headers = snp.headers
    session = snp.session
    url = 'https://'+ip_addr+':9089/api/console/status'
    resp = session.get(url, headers = headers)
    resp_list = json.loads(resp.text)
    return resp_list

def SNP_alarms_get(ip_addr):
    snp = login(ip_addr)
    headers = snp.headers
    session = snp.session
    url ='https://'+ip_addr+':9089/api/elements/'+ ip_addr + '/alarms'
    resp = session.get(url, headers=headers)
    resp_list = json.loads(resp.text)
    return resp_list

def SNP_ssh(ip_addr):
    snp = login(ip_addr)
    headers = snp.headers
    session = snp.session
    url ='https://'+ip_addr+':9089/api/console/togglessh'
    resp = session.post(url, headers=headers)
    resp_list = json.loads(resp.text)
    return resp_list

def SNP_license_get(ip_addr):
    snp = login(ip_addr)
    headers = snp.headers
    session = snp.session
    url ='https://'+ip_addr+':9089/api/elements/127.0.0.1/licenses'
    resp = session.get(url, headers=headers)
    resp_list = json.loads(resp.text)
    return resp_list

def SNP_license_set(ip_addr, license_key):
    
    license_data  = {'license_key': license_key}
    
    license_payload = json.dumps(license_data)
    snp = login(ip_addr)
    headers = snp.headers
    session = snp.session
    url ='https://'+ip_addr+':9089/api/elements/127.0.0.1/licenses'
    resp = session.post(url,data = license_payload, headers = headers)
    return resp
    
def SNP_preset(ip_addr, list_load_import_create, preset='preset_name.prst', reboot = True, preset_file=""):
    snp = login(ip_addr)
    headers = snp.headers
    session = snp.session

    if(list_load_import_create=='list'):
      url ='https://'+ip_addr+':9089/api/presets'
      resp = session.get(url, headers=headers)
      resp_list = json.loads(resp.text)
      return resp_list
    
    if(list_load_import_create=='load'):
      json_data = {'fme_ip_address': '127.0.0.1', 'preset_file': preset, 'reboot_after': reboot}
      url ='https://'+ip_addr+':9089/api/presets/loadpreset'
      resp = session.post(url, data = json.dumps(json_data), headers=headers)

      return resp

    if(list_load_import_create=='import'):
      url ='https://'+ip_addr+':9089/api/presets/'+preset
      resp = session.put(url, data = preset_file, headers=headers)
      return resp

    if(list_load_import_create=='create'):
      url = 'https://'+ip_addr+':9089/api/presets/'+preset
      json_data = {'fme_ip_address': '127.0.0.1', 'name': preset, 'element_type': 'Selenio Network Processor', 'interface_version': ''}
      resp = session.post(url, data = json.dumps(json_data), headers=headers)

      return resp


      
        
      
      
def SNP_parameter_get(ip_addr, config_status, object_id,parameter_class):
    
    
    snp = login(ip_addr)
    headers = snp.headers
    session = snp.session
    
    url ='https://'+ip_addr+':9089/api/elements/'+ip_addr+'/'+config_status+'/'
    resp = session.get(url+object_id, headers=headers)


    # add if statement for proper response from SNP
    nested1 = json.loads(resp.text)
    
    if(config_status=='config'):
        
        nested2 = json.loads(nested1.get('config'))
    else:
        nested2 = nested1
    #nested3 = json.loads(json.dumps(test2.get('System_Control')),object_hook = JSONObject)
    
    nested3 = nested2.get(parameter_class)
    
    return nested3

def SNP_parameter_set(ip_addr, object_id, parameter_class, parameter_dict):

    snp = login(ip_addr)
    headers = snp.headers
    session = snp.session

    url ='https://'+ip_addr+':9089/api/elements/'+ip_addr+'/config/'
     #get first
    resp = session.get(url+object_id, headers=headers)
    
    # add if statement for proper response from SNP
    nested1 = json.loads(resp.text)

    nested2 = json.loads(nested1.get('config'))
    
    nested2[parameter_class]=parameter_dict
    nested1['config'] = json.dumps(nested2)
    
    resp = session.put(url+object_id, data = json.dumps(nested1), headers=headers)

    return resp

  
