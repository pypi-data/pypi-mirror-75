import requests
import json





class JSONObject:
  def __init__( self, dict ):
      vars(self).update( dict )
      
def qx_get(ip_addr,url_path):
    
    
    requests.packages.urllib3.disable_warnings()
    url ='http://'+ip_addr+':8080/api/v1/'+ url_path
    
       
    headers = {'content-type': 'application/json', 'cache-control': 'no-cache'}
    session = requests.Session()
    session.verify = False
     
    resp = session.get(url, headers=headers)
    
   
    if('200' in str(resp)):
      json_resp = json.loads(resp.text)
      return json_resp
    else:
      return resp

def qx_generator(ip_addr,url_path, pathlogic_pairs, pathlogic_type):
    
    requests.packages.urllib3.disable_warnings()
    url ='http://'+ip_addr+':8080/api/v1/generator/standards/'+ url_path
    
    json_body = { 'action':'start', 'pathological': { 'pairs': int(pathlogic_pairs), 'type': pathlogic_type } }  
    headers = {'content-type': 'application/json', 'cache-control': 'no-cache'}
    session = requests.Session()
    session.verify = False

    resp = session.put(url, data = json.dumps(json_body), headers=headers)
    return resp

def qx_generator_bbox(ip_addr, enabled):

    requests.packages.urllib3.disable_warnings()
    url ='http://'+ip_addr+':8080/api/v1/generator/bouncingBox'
    if( isinstance(enabled, bool)):
      
      json_body = {"enabled" : enabled}
      headers = {'content-type': 'application/json', 'cache-control': 'no-cache'}
      session = requests.Session()
      session.verify = False
      resp = session.put(url, data = json.dumps(json_body), headers=headers)      
      return resp
    else:
      return 'variable must be boolean'
    
def qx_generator_audio(ip_addr, audio_json):
    if(isinstance(audio_json, dict)):
      requests.packages.urllib3.disable_warnings()
      url ='http://'+ip_addr+':8080/api/v1/generator/audio'
      if 'links' in audio_json:
        del audio_json['links']
      if 'message' in audio_json:
        del audio_json['message']
      if 'status' in audio_json:
        del audio_json['status']
      if 'mode' in audio_json:
        audio_json['mode'] = 'Off'
      headers = {'content-type': 'application/json', 'cache-control': 'no-cache'}
      session = requests.Session()
      session.verify = False
      resp = session.put(url, data = json.dumps(audio_json), headers=headers)
      return resp
    else:
       return 'varaible must be dict'

def qx_cursors(ip_addr, ap_line, ap_pixel):
    if(isinstance(ap_line, int) and isinstance(ap_pixel, int)):
        requests.packages.urllib3.disable_warnings()
        url ='http://'+ip_addr+':8080/api/v1/analyser/cursors/activePictureCursor'
        json_body = {'activePictureLine':ap_line, 'activePicturePixel': ap_pixel}
        headers = {'content-type': 'application/json', 'cache-control': 'no-cache'}
        session = requests.Session()
        session.verify = False
        resp = session.put(url, data = json.dumps(json_body), headers=headers)
        return resp
    else:
       return 'varaibles must be int'

def qx_screenshots(ip_addr):
    requests.packages.urllib3.disable_warnings()
    url ='http://'+ip_addr+':8080/api/v1/screenshots/images'
    headers = {'content-type': 'application/json', 'cache-control': 'no-cache'}
    session = requests.Session()
    json_body = {}
    session.verify = False
    resp = session.post(url, data = json.dumps(json_body), headers=headers)
    return resp

def qx_presets(ip_addr, preset_name, action):
    requests.packages.urllib3.disable_warnings()
    url_name = preset_name.replace(' ', '%2520')
    url ='http://'+ip_addr+':8080/api/v1/presets/userPresets/' + url_name
    headers = {'content-type': 'application/json', 'cache-control': 'no-cache'}
    session = requests.Session()
    json_body = { 'action': action, 'newPresetName':preset_name }
    session.verify = False
    resp = session.put(url, data = json.dumps(json_body), headers=headers)
    return resp



      

       
       
       
       
    
